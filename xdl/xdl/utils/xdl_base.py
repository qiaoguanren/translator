from typing import Dict, Any, List, Union
from .sanitisation import (
    DEFAULT_PROP_LIMITS, convert_val_to_std_units, parse_bool)
from .logging import get_logger
from ..errors import (
    XDLMissingDefaultPropError,
    XDLMissingPropTypeError,
    XDLFailedPropLimitError,
    XDLTypeConversionError,
)
from ..utils.prop_limits import PropLimit
from ..constants import VESSEL_PROP_TYPE, REAGENT_PROP_TYPE

class XDLBase(object):
    """Base object for Step, Component and Reagent objects. The functionality
    this class provides is all based around the properties dict. This class has
    a variables self.properties. This is initialized with whatever is passed to
    the constructor of the subclass, according to the prop specification of
    the subclass (PROP_TYPES, DEFAULT_PROPS) etc.

    This is where XDLBase subclasses become funky. After initialization,
    everything in the properties dict, so everything that was passed to the
    constructor == everything in PROP_TYPES, can be accessed as a class
    attribute, due to the __getattr__ and __setattr__ overrides here.

    So taking a step as an example:

    `step.volume` is exactly the same value as `step.properties[volume]`

    In the case of getting one of these variables, you could use either of those
    syntaxes and get exactly the same result. This is not the case however when
    setting the values of properties.

    `step.volume = 15` is not the same as `step.properties[volume] = 15`

    The override of __setattr__ means that when any value in the properties dict
    is set, as well as updating the properties dict, the update method is
    called. This sanitizes values and adds defaults as necessary.

    Editing the properties dict directly should be avoided as it means prop
    sanitization and validation is skipped. If this is necessary, for example
    you wish to update a lot of properties and then update for performance
    reasons, then you can update the properties dict directly, but you must call
    update afterwards.

    This system is quite weird when you're not used to it. It seems like
    witchcraft accessing member variables that don't seem to be initialized
    anywhere. But once you're used to it, it speeds up development massively as
    you can very quickly access / change properties with minimal typing.

    Attributes:
        name (str): Returns the class name
        properties (Dict[str, Any]): Dict of properties related to the XDL
            element. Generally should never be used directly, and items
            contained within the properties dict should be accessed/set as
            if they are attributes, as described above.
        PROP_TYPES (Dict[str, type]): PROP_TYPES gives the type of every prop
            Explicitly handled types:
                str       Remains unchanged
                int       Parsed as int
                float     Either parsed as float, or units removed from string
                          such as '2 mL' and remainer of string parsed as float
                          and converted to standard units based on units in
                          string
                bool      Parsed as bool
                List[str] Parsed as space separated list of strings
                'vessel'  Vessel declared in Hardware section of XDL
                'reagent' Reagent declared in Reagents section of XDL

            Any other type will just remain unchanged during sanitization.
        DEFAULT_PROPS (Dict[str, Any]): Dictionary of values to pass in for
            properties when their value is given as 'default'.
        INTERNAL_PROPS (List[str]): List of properties that should never be
            passed in as args, and are instead calculated automatically from the
            graph during on_prepare_for_execution.
        PROP_LIMITS  (Dict[str, PropLimit]): Defines detailed validation
            criteria for all props in the form of PropLimit objects. If no prop
            limit is given for a prop, then a default prop limit will be used
            based on the prop type.
        ALWAYS_WRITE (List[str]): List of properties that should always be
            written, even if they are the same as default values. For example,
            you may have default 20 mL volume for WashSolid. This does not mean
            that you don't want to write it, otherwise the XDL is unclear over
            how much solvent is used when reading it.

    Methods:
        update: Reloads properties dict. Should be called after the properties
            dict is updated directly.
    """

    # Prop specification variables

    # List of properties that should always be written, even if they are the
    # same as default values. For example, you may have default 20 mL volume for
    # WashSolid. This does not mean that you don't want to write it, otherwise
    # the XDL is unclear over how much solvent is used when reading it.
    ALWAYS_WRITE: List[str] = []

    # Dictionary of values to pass in for properties when their value is given
    # as 'default'.
    DEFAULT_PROPS: Dict[str, Any] = {}

    # List of properties that should never be passed in as args, and are instead
    # calculated automatically from the graph during on_prepare_for_execution.
    INTERNAL_PROPS: List[str] = []

    # PROP_TYPES gives the type of every prop
    #
    # Explicitly handled types:
    #   str       Remains unchanged
    #   int       Parsed as int
    #   float     Either parsed as float, or units removed from string such as
    #             '2 mL' and remainer of string parsed as float and converted to
    #             standard units based on units in string
    #   bool      Parsed as bool
    #   List[str] Parsed as space separated list of strings
    #   'vessel'  Vessel declared in Hardware section of XDL
    #   'reagent' Reagent declared in Reagents section of XDL
    #
    # Any other type will just remain unchanged during sanitization.
    PROP_TYPES: Dict[str, Union[type, str]] = {}

    # Defines detailed validation criteria for all props in the form of
    # PropLimit objects. If no prop limit is given for a prop, then a default
    # prop limit will be used based on the prop type.
    PROP_LIMITS: Dict[str, PropLimit] = {}

    # properties dict. Holds all current values of the properties of the step,
    # as described by the prop specification variables above.
    properties: Dict[str, Any] = {}

    def __init__(self, param_dict: Dict[str, Any]) -> None:
        """Initialize properties dict and loggger."""
        # Remove stuff like self that isn't a property as param dict comes from
        # `locals()`
        properties = {
            k: v for k, v in param_dict.items() if k in self.PROP_TYPES
        }

        # Initialize properties dict
        self.properties = {}

        # Load properties into self.properties
        self._load_properties(properties)

        # Initialize logger
        self.logger = get_logger()

    ##################
    # Public Methods #
    ##################

    @property
    def name(self) -> str:
        """Get class name."""
        return type(self).__name__

    def update(self) -> None:
        """This should be called explicitly if the properties dict is edited
        directly. Means that whenever new props are supplied they are sanitized
        and defaults added.
        """
        self._load_properties(self.properties)

    #####################
    # Prop Sanitization #
    #####################

    def _load_properties(self, properties: Dict[str, Any]) -> None:
        """Load dict of properties into self.properties.
        Add default values from DEFAULT_PROPS where 'default' is given as value.
        Sanitize properties according to PROP_LIMITS.

        Arguments:
            properties (Dict[str, Any]): dict of property names and values.
        """
        # Add new properties to self.properties
        for prop in self.PROP_TYPES:
            if prop in properties:
                self.properties[prop] = self._load_property(
                    prop, properties[prop])

    def _load_property(self, prop: str, value: Any) -> Any:
        """If value is default, return default value. Otherwise return
        sanitized value.

        Args:
            prop (str): Prop corresponding to value.
            value (Any): Value to load.

        Returns:
            Any: Default value if value is 'default', otherwise sanitized
                value.
        """
        if value == 'default':
            return self._get_default(prop)
        return self._clean_property(prop, value)

    def _get_default(self, prop: str) -> Any:
        """Get default value for given prop.

        Args:
            prop (str): Prop to get default value for.

        Returns:
            Any: Default value for prop.

        Raises:
            XDLMissingDefaultPropError: If no default value is found for prop in
                self.DEFAULT_PROPS
        """
        # Default value found in DEFAULT_PROPS, update properties
        if prop in self.DEFAULT_PROPS:
            return self._clean_property(prop, self.DEFAULT_PROPS[prop])

        # Default value not found in DEFAULT_PROPS, raise error
        else:
            raise XDLMissingDefaultPropError(self.name, prop)

    def _clean_property(self, prop: str, value: Any) -> Any:
        """Clean individual property. Convert value to correct type and convert
        to standard units if necessary. Also validate against prop limit.

        Args:
            prop (str): Prop corresponding to value.
            value (Any): Value to be cleaned.

        Returns:
            Any: Value cleaned according to self.PROP_TYPES.

        Raises:
            XDLFailedPropLimitError: If prop limit validation fails.
            XDLTypeConversionError: If unable to convert to type specified in
                self.PROP_TYPES
        """

        # Return children unchanged.
        if prop == 'children':
            return value

        # If string, remove any double spaces and strip
        if type(value) == str:
            while '  ' in value:
                value = value.replace('  ', ' ')
            value = value.strip()

        # Return 'None' as NoneType.
        if value in ['None', None]:
            return None

        # Validate using prop limit
        self._test_prop_limit(prop, value)

        # Convert value to correct type, and convert to standard units if
        # necessary.
        prop_type = self._get_prop_type(prop)

        # str prop type, reagent and vessel prop types are also str in terms
        # of value sanitization
        if prop_type in [str, REAGENT_PROP_TYPE, VESSEL_PROP_TYPE]:
            # Convert None values to empty string
            if value in [[], {}]:
                return ''
            return str(value)

        # float prop type, convert str to standard units. If value is not a str
        # try to cast to float, if TypeError or ValueError is raised, raise
        # XDLTypeConversionError.
        elif prop_type == float:
            if type(value) == str:
                return convert_val_to_std_units(value)
            else:
                try:
                    return float(value)
                except (TypeError, ValueError):
                    raise XDLTypeConversionError(
                        self.name, prop, prop_type, value)

        # bool prop type
        elif prop_type == bool:
            if type(value) == str:
                return parse_bool(value)
            elif type(value) == bool:
                return value
            else:
                raise XDLTypeConversionError(self.name, prop, prop_type, value)

        # Used by 3 option stir property in WashSolid (True, 'solvent' or False)
        elif prop_type == Union[bool, str]:
            bool_value = parse_bool(value)
            # bool value found, return bool
            if bool_value is not None:
                return bool_value
            # bool val not found just return str value
            else:
                return str(value)

        # int prop type, try and cast to int, if TypeError or ValueError raised,
        # raise XDLTypeConversionError
        elif prop_type == int:
            try:
                return int(value)
            except (TypeError, ValueError):
                raise XDLTypeConversionError(self.name, prop, prop_type, value)

        # List[str] prop type, parse space separated list or return
        # list unchanged
        elif prop_type == List[str]:
            # Parse space separated list
            if type(value) == str:
                split_list = value.split()
                # Convert 'None' string to NoneType
                for i in range(len(split_list)):
                    if split_list[i].lower() == 'none':
                        split_list[i] = None
                return split_list

            # Value if already list, return unchanged
            elif type(value) == list:
                return value

        # Union[str, int] prop type, used for ports
        elif prop_type == Union[str, int]:
            if type(value) == str:
                # Try and cast to int
                try:
                    return int(value)
                # If not possible just return str value.
                except (TypeError, ValueError):
                    return str(value)
            elif type(value) == int:
                return value
            else:
                return str(value)

        # If prop type not matched by any of these conditions, just return
        # unchanged.
        return value

    def _get_prop_type(self, prop: str) -> Union[str, type]:
        """Get prop type, raise error if prop type can't be found.

        Returns:
            Union[str, type]: Prop type of given prop.

        Raises:
            XDLMissingPropTypeError: If prop type not found for prop in
                self.PROP_TYPES
        """
        try:
            return self.PROP_TYPES[prop]
        except KeyError:
            raise XDLMissingPropTypeError(self.name, prop)

    def _get_prop_limit(self, prop: str) -> PropLimit:
        """Get prop limit.  If prop limit not found in PROP_LIMITS, look for
        default prop limit based on type. If this can't be found return None
        and don't do any prop limit validation.

        Returns:
            PropLimit: Prop limit of given prop.
        """
        # Try to get prop limit from self.PROP_LIMITS
        try:
            return self.PROP_LIMITS[prop]

        except KeyError:
            # Look for default prop limit to use based on type
            prop_type = self.PROP_TYPES[prop]
            if prop_type in DEFAULT_PROP_LIMITS:
                return DEFAULT_PROP_LIMITS[prop_type]

            # If no default prop limit can be found, allow None prop limit that
            # does no validation, since some types can't really be validated.
            else:
                return None

    def _test_prop_limit(self, prop: str, value: Any) -> None:
        """Test given property value against prop limit.

        Args:
            prop (str): Property value corresponds to.
            value (str): Value to test against relevant prop limit.

        Raises:
            XDLFailedPropLimitError: If given value is deemed invalid by prop
                limit.
        """
        # None value, don't test
        if value is None or value == '':
            return

        # Get prop limit
        prop_limit = self._get_prop_limit(prop)

        # No prop limit found, don't test
        if prop_limit is None:
            return

        # Convert value to string if it isn't already a string
        value = str(value)

        # Test value against prop limit, and raise error if it fails the test
        try:
            assert prop_limit.validate(value)
        except AssertionError:
            # Value did not pass prop limit validation.
            raise XDLFailedPropLimitError(self.name, prop, value, prop_limit)

    #################
    # Magic Methods #
    #################

    def __setattr__(self, name: str, value: Any) -> None:
        """
        If name is in self.properties do self.properties[name] = value and call
        self.update. The purpose of this is that so whenever a property is
        changed, it is sanitized and default values are added.

        If attr is not in self.properties just set attribute as normal.
        """
        # attr in self.properties, add to properties dict and update
        if name in self.properties:
            self.properties[name] = self._load_property(name, value)

        # attr not in self.properties, update as normal
        else:
            object.__setattr__(self, name, value)

    def __getattr__(self, name: str) -> None:
        """
        If name is in self.properties return self.properties[name].
        Otherwise return attribute as normal.
        """
        # attr in self.properties, return value from self.properties
        if name in self.properties:
            return self.properties[name]

        # attr not in self.properties, return as normal
        else:
            return object.__getattribute__(self, name)
