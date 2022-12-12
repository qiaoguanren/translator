from typing import List, Tuple
from ..steps import Step
from ..reagents import Reagent
from ..hardware import Component
from ..xdl import XDL
from ..utils.xdl_base import XDLBase

class ReactionBlueprint(XDLBase):

    def __init__(self, props):
        super().__init__(props)

    def build_prep(self) -> Tuple[List[Step], List[Reagent]]:
        """Abstract method, but not mandatory, can just return empty lists.
        Build prep stage of procedure. Add reagents.

        Returns:
            Tuple[List[Step], List[Reagent]]: (steps, reagents) tuple.
        """
        return [], []

    def build_reaction(self) -> Tuple[List[Step], List[Reagent]]:
        """Abstract method, but not mandatory, can just return empty lists.
        Build reaction stage of procedure. Heat reaction mixture.

        Returns:
            Tuple[List[Step], List[Reagent]]: (steps, reagents) tuple.
        """
        return [], []

    def build_workup(self) -> Tuple[List[Step], List[Reagent]]:
        """Abstract method, but not mandatory, can just return empty lists.
        Build workup stage of procedure. Isolate product. Separations etc.

        Returns:
            Tuple[List[Step], List[Reagent]]: (steps, reagents) tuple.
        """
        return [], []

    def build_purification(self) -> Tuple[List[Step], List[Reagent]]:
        """Abstract method, but not mandatory, can just return empty lists.
        Build purification stage of procedure. E.g. Run column, distill...

        Returns:
            Tuple[List[Step], List[Reagent]]: (steps, reagents) tuple.
        """
        return [], []

    def build(self, save: str = None) -> XDL:
        """Build XDL object and save to file if save path given.

        Arguments:
            save (str): File path to save .xdl file to.

        Returns:
            XDL: XDL object of built procedure.
        """
        prep_steps, prep_reagents = self.build_prep()
        reaction_steps, reaction_reagents = self.build_reaction()
        workup_steps, workup_reagents = self.build_workup()
        purification_steps, purification_reagents = self.build_purification()
        steps = prep_steps + reaction_steps + workup_steps + purification_steps
        reagents = (
            prep_reagents
            + reaction_reagents
            + workup_reagents
            + purification_reagents
        )
        x = XDL(steps=steps, reagents=reagents, hardware=[
            Component(id="reactor", component_type="reactor"),
            Component(id="rotavap", component_type="rotavap")
        ])

        if save:
            x.save(save)

        return x
