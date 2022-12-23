from typing import Any, Dict, Optional, Union

from .utils.sanitisation import amount_str_to_units, amount_to_float


class Context:
    """Container for objects required by steps."""

    def __init__(self, parent_context=None, **kwargs: Dict[str, Any]) -> None:
        self._context_params = {}
        self.update(parent_context=parent_context, **kwargs)

    def resolve(self, item: str) -> Union[Any, None]:
        """
        Returns a Reagent, Component or Parameter object that has an 'id'
        matching the initial input 'item' string. If no match found, returns
        None

        Args:
            item (str): id of item to resolve.

        Returns:
            Object: Reagent, Component or Parameter object which has an 'id'
            matching the initial input 'item' string.
        """
        all_items = {}
        all_items.update({r.id: r for r in self.reagents} or {})
        all_items.update({h.id: h for h in self.hardware.components} or {})
        all_items.update({p.id: p for p in self.parameters} or {})
        if self.parent_context:
            return all_items.get(item, self.parent_context.resolve(item))
        else:
            return all_items.get(item, None)

    def update(self, **kwargs: Dict[str, Any]) -> None:
        for arg in kwargs:
            self._context_params[arg] = kwargs[arg]

    def __deepcopy__(self, memo):
        return Context(**self._context_params)

    def __setattr__(self, name: str, value: Any) -> None:
        if name == "_context_params":
            return object.__setattr__(self, name, value)
        else:
            self.update({name: value})

    def __getattr__(self, attr: str) -> Any:
        # try to resolve from context params dict
        if attr in self._context_params:
            return self._context_params[attr]

        else:
            # stop iterating if this context is the root context
            # this will return nothing during hasattr if not attribute
            if self.parent_context is None:
                return self._context_params.get(attr)

            # otherwise look in the parent context recursively
            else:
                return getattr(self.parent_context, attr)

    @property
    def root_context(self):
        """Returns the context at the root of the Context tree by recursively
        searching for parent context until there is no parent context.

        Returns:
            Context: Context object at the root of context tree.
        """
        if not self._context_params["parent_context"]:
            return self
        else:
            return self._context_params["parent_context"].root_context

    @property
    def _reference_reagent(self):
        """Reagent object used for equivalence reference.

        Returns:
            Reagent: Reagent object.
        """
        return self.resolve(self.equiv_reference)

    @property
    def _equiv_moles(self) -> float:
        """Work out number of moles in 1 equivalent. This is calculated using
        the ```equiv_amount``` specified in the ```prepare_for_execution```
        method in the XDL object.

        Returns:
            float: number of moles in 1 equivalent.
        """
        try:
            #  sanitise equiv_amount into arbitrary units
            equiv_amount = amount_to_float(self.equiv_amount)
        except AttributeError:
            return None

        #  retrieve standard units for equivalent
        equiv_units = amount_str_to_units(self.equiv_amount)

        #  equivalent amount expressed directly as moles, so return unchanged
        if equiv_units == "mol":
            return equiv_amount

        #  equivalent amount expressed as mL, so work out number of moles in
        #  1 equivalent
        elif equiv_units == "mL":
            concentration = self._reference_reagent.concentration

            if concentration is not None:
                return (concentration / 1000) * equiv_amount

            density = self._reference_reagent.density
            molecular_weight = self._reference_reagent.molecular_weight

            if density and molecular_weight:
                mass = equiv_amount * density
                return mass / molecular_weight

        #  equivalebt amount expressed in mass units, so work out number of
        #  moles in 1 equivalent
        elif equiv_units == "g":

            #  attempt to use reference reagent's molecular weight to work out
            #  N moles for 1 equivalent
            molecular_weight = self._reference_reagent.molecular_weight
            if molecular_weight is not None:
                return equiv_amount / molecular_weight

            #  molecular weight for reference reagent has not been provided,
            #  so attempt to use density and concentration instead
            density = self._reference_reagent.density
            concentration = self._reference_reagent.concentration

            if density is not None and concentration is not None:

                #  get volume of 1 equivalent of reference reagent => convert
                #  to n_moles of reference reagent
                #  mL =  g / g mL-1
                volume = equiv_amount / density

                #  mol  =  mol mL-1 / mL
                n_moles = (concentration / 1000) * volume
                return n_moles

        #  this should never return None if equiv_amount, equiv_reference have
        #  been specified in ```prepare_for_execution```
        return None

    @property
    def _base_scale(self) -> float:
        """Make sure base scale given in blueprint procedure is of correct
        correct units i.e. mol / eq, and if so, return base scale without units.

        Returns:
            float: base scale in mol / eq to scale blueprint procedure by.
        """
        try:
            return amount_to_float(self.base_scale)
        except AttributeError:
            return None

    def amount_to_mass(
        self,
        amount: float = None,
        amount_units: str = None,
        reagent_mw: float = None,
        final_amount: float = None,
    ) -> Optional[float]:
        """
        Convert amount to final mass.

        Returns:
            float: final mass to use (in g).
        """
        # if amount units specified in 'unit / eq', scale final_amount using
        # base_scale as a reference
        if self._base_scale and self._equiv_moles:
            equiv_scale = self._equiv_moles / self._base_scale

            if "/" in amount:
                final_amount = final_amount * equiv_scale

        if amount is not None:

            #  moles to mass
            if amount_units == "mol":

                if reagent_mw:
                    return reagent_mw * final_amount

            #  mass to mass
            elif amount_units == "g":
                return final_amount

            #  equivalents to mass
            elif amount_units == "equivalents":
                #  get equivalent amount - convert
                return self.equivalents_to_mass(
                    final_amount=final_amount,
                    amount_units=amount_units,
                    reagent_mw=reagent_mw,
                )

        return None

    def equivalents_to_mass(
        self,
        final_amount: float = None,
        amount_units: str = None,
        reagent_mw: float = None,
    ) -> Optional[float]:
        """Convert number of equivalents to final mass. This is calculated
        using the ```equiv_amount``` and ```equiv_reference``` parameters
        specified on call of the XDL object's ```prepare_for_execution```
        method.

        Returns:
            float: final mass to use in Add step (in mL).
        """
        if hasattr(self, "_context_params"):
            if hasattr(self, "_equiv_moles"):
                if self._equiv_moles and final_amount:
                    return self.moles_to_mass(
                        n_mols=final_amount * self._equiv_moles,
                        final_amount=final_amount,
                        amount_units=amount_units,
                        reagent_mw=reagent_mw,
                    )

        return None

    def moles_to_mass(
        self,
        amount_units: str = None,
        final_amount: float = None,
        reagent_mw: float = None,
        n_mols: float = None,
    ) -> Optional[float]:
        """Convert moles to final mass.

        Args:
            n_mols (float, optional): number of moles of target reagent. If
                None, self.final_amount is used. Defaults to None.

        Returns:
            float: final mass to use (in g).
        """

        #  get n_moles from 'amount'
        if n_mols is None:
            if amount_units == "mol":
                n_mols = final_amount
            else:
                return None

        mass = reagent_mw * n_mols
        return mass

    def calculate_volume(
        self,
        volume: float = None,
        mass: float = None,
        amount: float = None,
        amount_units: str = None,
        final_amount: float = None,
        reagent_concentration: float = None,
        reagent_molecular_weight: float = None,
        reagent_density: float = None,
        reagent_solid: bool = None,
    ) -> Optional[float]:
        """
        Calculate final volume from mass and / or amount.
        """
        # if amount units specified in 'unit / eq', scale final_amount using
        # base_scale as a reference
        if self._base_scale and self._equiv_moles:
            equiv_scale = self._equiv_moles / self._base_scale
            if "/" in amount:
                final_amount = final_amount * equiv_scale

        if volume is None:
            if mass is not None:
                volume = self.mass_to_volume(mass=mass, reagent_density=reagent_density)
            elif amount is not None:
                volume = self.amount_to_volume(
                    amount=amount,
                    amount_units=amount_units,
                    reagent_solid=reagent_solid,
                    final_amount=final_amount,
                    reagent_density=reagent_density,
                    reagent_concentration=reagent_concentration,
                    reagent_molecular_weight=reagent_molecular_weight,
                )

        return volume

    def mass_to_volume(
        self,
        mass: Optional[float] = None,
        reagent_density: Optional[float] = None,
        reagent_concentration: Optional[float] = None,
        reagent_molecular_weight: Optional[float] = None,
    ) -> Optional[float]:
        """
        Convert mass to final volume.

        Args:
            mass (float, optional): mass in g. Defaults to None. If None,
                self.mass is used.

        Returns:
            float: final volume to use (in mL).
        """
        if not mass:
            return None
        if reagent_density:
            return mass / reagent_density
        if reagent_concentration and reagent_molecular_weight:

            n_moles = mass / reagent_molecular_weight
            return (n_moles / reagent_concentration) * 1000
        return None

    def amount_to_volume(
        self,
        amount: float = None,
        amount_units: str = None,
        reagent_solid: bool = None,
        reagent_density: float = None,
        reagent_concentration: float = None,
        reagent_molecular_weight: float = None,
        final_amount: float = None,
    ) -> Optional[float]:
        """
        Convert amount to final volume. Amount can be in units convertible to
        'mol' (moles), 'g' (mass), 'mL' (mass) or 'equivalents' (equivalents of
        reference reagent).

        Returns:
            float: final volume to use in Add step (in mL).
        """

        if amount and not reagent_solid:

            if amount_units == "mL":
                return final_amount

            #  moles to volume
            elif amount_units == "mol":
                return self.moles_to_volume(
                    n_mols=final_amount,
                    final_amount=final_amount,
                    amount_units=amount_units,
                    reagent_density=reagent_density,
                    reagent_concentration=reagent_concentration,
                    reagent_molecular_weight=reagent_molecular_weight,
                )

            #  mass to volume
            elif amount_units == "g":
                return self.mass_to_volume(
                    mass=final_amount,
                    reagent_density=reagent_density,
                    reagent_concentration=reagent_concentration,
                    reagent_molecular_weight=reagent_molecular_weight,
                )

            #  equivalents to volume
            elif amount_units == "equivalents":

                #  get equivalent amount - convert
                return self.equivalents_to_volume(
                    final_amount=final_amount,
                    amount_units=amount_units,
                    reagent_density=reagent_density,
                    reagent_concentration=reagent_concentration,
                    reagent_molecular_weight=reagent_molecular_weight,
                )
        return None

    def moles_to_volume(
        self,
        n_mols: float = None,
        amount_units: str = None,
        final_amount: float = None,
        reagent_density: float = None,
        reagent_concentration: float = None,
        reagent_molecular_weight: float = None,
    ) -> Optional[float]:
        """Convert moles to final volume.

        Args:
            n_mols (float, optional): number of moles of target reagent. If
                None, self.final_amount is used. Defaults to None.

        Returns:
            float: final volume to use (in mL).
        """
        #  get n_moles from 'amount'
        if n_mols is None:
            if amount_units == "mol":
                n_mols = final_amount
            else:
                return None

        #  if available, get concentration of reagent to add (in mol / L)
        if reagent_concentration:
            return n_mols / (reagent_concentration / 1000)

        mass = reagent_molecular_weight * n_mols
        if reagent_density:
            return mass / reagent_density
        return None

    def equivalents_to_volume(
        self,
        final_amount: float = None,
        amount_units: str = None,
        reagent_density: float = None,
        reagent_concentration: float = None,
        reagent_molecular_weight: float = None,
    ) -> Optional[float]:
        """Convert number of equivalents to final volume. This is calculated
        using the ```equiv_amount``` and ```equiv_reference``` parameters
        specified on call of the XDL object's ```prepare_for_execution```
        method.

        Returns:
            float: final volume to use in Add step (in mL).
        """
        #  get number of moles in 1 equivalent
        n_moles = self._equiv_moles

        if final_amount and n_moles:
            return self.moles_to_volume(
                n_mols=final_amount * n_moles,
                amount_units=amount_units,
                final_amount=final_amount,
                reagent_density=reagent_density,
                reagent_concentration=reagent_concentration,
                reagent_molecular_weight=reagent_molecular_weight,
            )
        return None
