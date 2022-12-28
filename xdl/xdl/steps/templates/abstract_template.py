from ..base_steps import AbstractStep
from ...errors import (
    XDLStepTemplateNameError,
    XDLStepTemplateMissingPropError,
    XDLStepTemplatePropTypeError,
    XDLStepTemplateMissingDefaultPropError,
    XDLStepTemplateInvalidDefaultPropError,
    XDLStepTemplateMissingPropLimitError,
    XDLStepTemplateInvalidPropLimitError,
)

class AbstractStepTemplate(AbstractStep):
    """Base class to create step templates such as AbstractAddStep. Purpose of
    this class is to allow MANDATORY_PROP_TYPES to be defined for all generic
    step classes, e.g. Add, Filter etc. Then platform specific implemenations
    of these steps can inherit this class and have this class will validate that
    they support the mandatory properties. This should ensure interoperability
    between platforms, if scripts are written according to the standard defined
    by the mandatory properties of the step templates. Extra properties will be
    allowed as before, but will have no guarantee of interoperability between
    platforms.

    Raises:
        XDLStepTemplateMissingPropError: Implementation is missing mandatory
            prop.
        XDLStepTemplatePropTypeError: Implementation has mandatory prop, but
            prop type is wrong.
    """

    # Mandatory class attributes to fill in when creating templates
    MANDATORY_NAME = ''
    MANDATORY_PROP_TYPES = {}
    MANDATORY_PROP_LIMITS = {}
    MANDATORY_DEFAULT_PROPS = {}

    def __init__(self, param_dict):
        """Validate that step implements all mandatory properties correctly and
        call super __init__.
        """
        self.validate()
        super().__init__(param_dict)

    def validate(self):
        """Validate step class conforms to standard in step template class."""
        self.validate_name()
        self.validate_prop_types()
        self.validate_default_props()
        self.validate_prop_limits()

    def validate_name(self):
        """Check step name is correct.

        Raises:
            XDLStepTemplateNameError
        """
        if self.name != self.MANDATORY_NAME:
            raise XDLStepTemplateNameError(self.MANDATORY_NAME, self.name)

    def validate_prop_types(self):
        """Validate that all mandatory props are present in prop types, and that
        have the correct prop types.

        Raises:
            XDLStepTemplateMissingPropError
            XDLStepTemplatePropTypeError
        """
        for prop, prop_type in self.MANDATORY_PROP_TYPES.items():

            # Check prop in PROP_TYPES
            if prop not in self.PROP_TYPES:
                raise XDLStepTemplateMissingPropError(
                    self.MANDATORY_NAME, prop, prop_type)

            # Check prop type is correct type
            elif prop_type != self.PROP_TYPES[prop]:
                raise XDLStepTemplatePropTypeError(
                    self.MANDATORY_NAME, prop, prop_type, self.PROP_TYPES[prop])

    def validate_default_props(self):
        """Validate that all mandatory default props are present and correct.

        Raises:
            XDLStepTemplateMissingDefaultPropError
            XDLStepTemplateInvalidDefaultPropError
        """
        for prop, default_value in self.MANDATORY_DEFAULT_PROPS.items():

            # Check prop in DEFAULT_PROPS
            if prop not in self.DEFAULT_PROPS:
                raise XDLStepTemplateMissingDefaultPropError(
                    self.MANDATORY_NAME, prop, default_value)

            # Check default prop is correct. A mandatory default prop value of
            # None means that the implemented value can be anything.
            elif (default_value is not None
                    and self.DEFAULT_PROPS[prop] != default_value):
                raise XDLStepTemplateInvalidDefaultPropError(
                    self.MANDATORY_NAME,
                    prop,
                    default_value,
                    self.DEFAULT_PROPS[prop]
                )

    def validate_prop_limits(self):
        """Validate that all mandatory prop limits are implemented and have the
        correct values.
        """
        for prop, prop_limit in self.MANDATORY_PROP_LIMITS.items():

            # Check prop in PROP_LIMITS
            if prop not in self.PROP_LIMITS:
                raise XDLStepTemplateMissingPropLimitError(
                    self.MANDATORY_NAME, prop, prop_limit)

            # Check prop limit is correct.
            elif self.PROP_LIMITS[prop] != prop_limit:
                raise XDLStepTemplateInvalidPropLimitError(
                    self.MANDATORY_NAME,
                    prop,
                    prop_limit,
                    self.PROP_LIMITS[prop]
                )
