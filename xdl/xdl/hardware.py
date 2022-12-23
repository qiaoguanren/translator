from typing import Generator, List, Union

from .utils.xdl_base import XDLBase

# These lists are here so that generic names like 'rotavap' can be used
# in XDL, and specific names like 'IKARV10' can be used in the graph
# and the XDLExecutor will still know that it can map a component with
# type 'rotavap' to a component with type 'IKARV10'.
REACTOR_TYPES: List[str] = ["reactor", "ChemputerReactor"]
FILTER_TYPES: List[str] = ["filter", "ChemputerFilter"]
SEPARATOR_TYPES: List[str] = ["separator", "ChemputerSeparator"]
ROTAVAP_TYPES: List[str] = ["rotavap", "RV10Rotovap", "R300Rotovap"]
FLASK_TYPES: List[str] = ["flask", "ChemputerFlask"]
WASTE_TYPES: List[str] = ["waste", "ChemputerWaste"]
CARTRIDGE_TYPES: List[str] = ["cartridge", "ChemputerCartridge"]


class Component(XDLBase):
    """This will be retired in future versions. Class for representing vessel in
    which reaction mixture resides.

    Args:
        id (str): ID for the component.
        component_type (str): Type of the component i.e. 'ChemputerFlask'
        chemical (str): Optional. Chemical component contains.
    """

    PROP_TYPES = {
        "id": str,
        "component_type": str,
        "chemical": str,
    }

    DEFAULT_PROPS = {
        "chemical": None,
    }

    def __init__(
        self,
        id: str,  # noqa: A002
        component_type: str,
        chemical: str = "default",
        **kwargs,
    ) -> None:
        super().__init__(locals())


class Hardware:
    """This will be retired in future versions.
    Object describing entire setup. The purpose is easily accessible lists
    of reactors, flasks, filters, wastes etc.

    Args:
        components (List[Component]): List of Component objects.
    """

    def __init__(self, components: List[Component]) -> None:

        self.components = components
        self.component_ids = [item.id for item in self.components]
        self.reactors = []
        self.flasks = []
        self.wastes = []
        self.filters = []
        self.separators = []
        self.rotavaps = []
        self.cartridges = []

        for component in self.components:
            if component.component_type in REACTOR_TYPES:
                self.reactors.append(component)

            elif component.component_type in SEPARATOR_TYPES:
                self.separators.append(component)

            elif component.component_type in FILTER_TYPES:
                self.filters.append(component)

            elif component.component_type in FLASK_TYPES:
                self.flasks.append(component)

            elif component.component_type in WASTE_TYPES:
                self.wastes.append(component)

            elif component.component_type in ROTAVAP_TYPES:
                self.rotavaps.append(component)

            elif component.component_type in CARTRIDGE_TYPES:
                self.cartridges.append(component)
        self.waste_xids = [waste.id for waste in self.wastes]

    def __getitem__(self, item: str) -> Union[Component, None]:
        """Get components like this: graph_hardware['filter']."""
        for component in self.components:
            if component.id == item:
                return component
        return None

    def __iter__(self) -> Generator[Component, None, None]:
        yield from self.components

    def __len__(self) -> int:
        return len(list(self.components))
