#  std
import weakref
from typing import Any, Dict, List, Optional, Type

from networkx import MultiDiGraph

from .context import Context
from .errors import XDLAttrDuplicateID
from .hardware import Hardware
from .parameters import Parameter
from .reagents import Reagent
from .steps.core import AbstractStep, Step
from .utils.steps import steps_from_step_templates, steps_into_sections


class Blueprint(AbstractStep):
    """Ordered template of steps that can be reused multiple times throughout a
    synthesis. Blueprint object contains general reagents, hardware and
    experimental conditions that are later mapped to specific values when
    the blueprint is declared.

    kwargs should contain details of 'abstract' to 'real' hardware and reagent
    mappings (e.g. abstract_reagent=real_reagent). As well as any other
    information such as parameter values the equivalence_reference and the
    equivalence_amount.

    Args:
        reagent_templates (List[Reagent]): List of blueprint Reagents defined in
            blueprint. May be 'default' reagents or abstract reagents that will
            be mapped to a 'real' reagent during Blueprint step use.
        hardware_templates (Hardware): Hardware defined in blueprint.
        internal_parameters (List[Parameters]): List of Parameter's defined in
            blueprint.
        step_templates (List[Step]): Uninstantiated Step objects.

        reagents (List[Reagent]): List of Reagents to be used in Blueprint
            Procedure. Reagent id's will represent 'real' reagents from graph.
        hardware (Hardware): Hardware to be used in Blueprint Procedure.
            Component id's will represent 'real' components from graph.
        parameters (List[Parameters]): List of Parameter's with final parameter
            values (values given during Blueprint declaration overwrite those
            defined in the internal_parameters).
        children (List[Step]): List of instantiated Steps representing
            the procedure.
        step_sections (Dict[str, List[Step]]): child steps split up into
            corresponding synthesis sections e.g. 'Prep', 'Purification' etc.

        context (Context): context of parent object that spawned the blueprint.
        equiv_reference (str, optional): reagent to act as a reference
                when calculating equivalents.
        equiv_amount (str, optional): amount of reference reagent equal to
            one equivalent (including units) e.g "2.0 g".
            Valid units include mol, g, mL.
        base_scale (Optional[str], optional): Reference equivalence scale in
            in which the blueprint procedure was developed and amounts
            calculated from. Units should be specified in
            amount (mol, g etc.) / equivalent (e.g. '0.5 mmol / eq').
            Defaults to None.

    """

    def __init__(
        self,
        context: Context,
        equiv_reference: str = None,
        equiv_amount: str = None,
        **kwargs,
    ) -> None:
        # set defaults from DEFAULT_PROPS and any other kwargs (e.g. 'id')
        super().__init__({**self.DEFAULT_PROPS, **kwargs})

        validate_blueprint_ids(self)

        # extract default reagents first
        reagent_dict = {r.id: r for r in self.reagent_templates if r.name}

        for r in self.reagent_templates:
            # If name not mapped, look up under the same name
            if r.id in kwargs:
                candidate = kwargs.get(r.id, r.id)
                resolved_reagent = context.resolve(candidate)
                if resolved_reagent:
                    reagent_dict[r.id] = resolved_reagent
            else:
                if r.id not in reagent_dict:
                    self.logger.warning(
                        "Reagent %s declared but no defaults specified or"
                        " explicitly mapped.",
                        r.id,
                    )
        self.reagents = list(reagent_dict.values())

        # overwrite default parameter values if supplied in BP declaration
        params_dict = {p.id: p for p in self.internal_parameters}
        for k, v in kwargs.items():
            if k in params_dict:
                params_dict[k].value = v
        self.parameters = list(params_dict.values())

        hardware_dict = {}
        for h in self.hardware_templates:
            candidate = kwargs[h.id]
            resolved_component = context.resolve(candidate)
            if resolved_component:
                hardware_dict[h.id] = resolved_component
        self.hardware = Hardware(list(hardware_dict.values()))

        self.context = Context(
            parent_context=context,
            reagents=self.reagents,
            parameters=self.internal_parameters,
            hardware=self.hardware,
            xdl=weakref.ref(self),
        )

        if equiv_reference is not None and equiv_amount is not None:
            if equiv_reference in kwargs:
                equiv_reference = kwargs[equiv_reference]

            self.context.update(
                equiv_reference=equiv_reference,
                equiv_amount=equiv_amount,
            )

        if self.base_scale:
            self.context.update(base_scale=self.base_scale)

        final_steps = {}
        for section, steps in self.step_templates.items():
            final_steps[section] = steps_from_step_templates(
                self,
                steps,
                bindings=kwargs,
            )
        self.children, self.sections = steps_into_sections(final_steps)

    def on_prepare_for_execution(self, graph: MultiDiGraph) -> None:
        """Prepares the current step for execution.

        Args:
            graph (MultiDiGraph): Graph to use for preparing steps for execution
        """
        super().on_prepare_for_execution(graph)

    def get_steps(self) -> List[Step]:
        return self.children

    def locks(self, platform_controller: Any) -> List:
        """Returns locks that are nodes that are used while the blueprint step is
        executing. Locks should be specific to the Blueprint only and not any
        Blueprint substeps.

        Args:
            platform_controller (Any): Platform controller to use for
                calculating which nodes in graph are used by step.

        Returns:
            List: List of step locks.
        """
        return []


def infer_props(items: List[any]) -> Dict[str, str]:
    """Creates a PROP_TYPE-like dictionary with all items id's.
    Values of returned dict are always str.

    Args:
        items (List[any]): List of objects with an id attribute.

    Returns:
        Dict[str:str]: PROP_TYPE like dictionary of format: {item 'id': str}
            for item in items.
    """
    return {item.id: str for item in items}


def create_blueprint(
    id: str,  # noqa: A002
    props: Dict[str, Any],
    steps: List[Step],
    hardware: Hardware,
    reagents: List[Reagent],
    parameters: List[Parameter],
    base_scale: Optional[str] = None,
    **kwargs,
) -> Type[Blueprint]:
    """Creates XDL Blueprint object.

    Args:
        id (str): desired id fo created Blueprint.
        props (Dict[str, Any]): properties of blueprint, e.g 'id'.
        steps (List[Step]): Uninstantiated Step objects.
        hardware (Hardware): Hardware object containing all Components for
            blueprints.
        reagents (List[Reagent]): List of Reagent objects.
        parameters (List[Parameter]): List of Parameter objects.
        base_scale (Optional[str], optional): Reference equivalence scale in
            in which the blueprint procedure was developed and amounts
            calculated from. Units should be specified in
            amount (mol, g etc.) / equivalent (e.g. '0.5 mmol / eq').
            Defaults to None.

    Returns:
        Type[Blueprint]: Instantiated Blueprint.
    """
    prop_types = infer_props(hardware + reagents + parameters)
    default_props = {
        **{p.id: p.value for p in parameters if p.value is not None},
        **{r.id: r.name for r in reagents if r.name is not None},
    }

    cls_dict = {
        "id": id,
        "name": id,
        "PROP_TYPES": prop_types,
        "DEFAULT_PROPS": default_props,
        "step_templates": steps,
        "props": props,
        "hardware_templates": hardware,
        "reagent_templates": reagents,
        "internal_parameters": parameters,
        "base_scale": base_scale,
        **kwargs,
    }

    return type(id, (Blueprint,), cls_dict)


def validate_blueprint_ids(bp: Blueprint) -> None:
    """Checks that there is no duplication of component, reagent or
    parameter id's within blueprints.

     Args:
        bp (Blueprint): Blueprint object to validate.

    Raises:
        XDLAttrDuplicateID: raised if two or more components, reagents or
            parameters share the same name / id.
        XDLMissingStepError: raised if one or more blueprint step cannot be
            looked up in platform's step library.
    """

    # ensure no parameters in blueprint have duplicate parameter ids
    for parameter in bp.internal_parameters:
        matches = [p for p in bp.internal_parameters if p.id == parameter.id]

        if len(matches) > 1:
            raise XDLAttrDuplicateID(id=parameter[0], target_class="Parameter")

    # ensure no reagents in blueprint have duplicate reagents ids
    for reagent in bp.reagent_templates:
        matches = [r for r in bp.reagent_templates if r.id == reagent.id]
        if len(matches) > 1:
            raise XDLAttrDuplicateID(id=reagent[0], target_class="Reagent")

    reagent_ids = [reagent.id for reagent in bp.reagent_templates]
    vessel_ids = [vessel.id for vessel in bp.hardware_templates]
    parameter_ids = (
        [param.id for param in bp.internal_parameters] if bp.internal_parameters else []
    )

    # make sure no IDs are duplicated across different sections
    all_ids = [*reagent_ids, *vessel_ids, *parameter_ids]
    if sorted(set(all_ids)) != sorted(all_ids):
        duplicates = {i for i in all_ids if all_ids.count(i) > 1}
        raise XDLAttrDuplicateID(
            id=str(duplicates),
            target_class="Blueprint Reagents, Hardware and Parameter",
        )
