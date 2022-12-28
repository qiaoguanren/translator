from ..errors import XDLError

class XDLReadError(XDLError):
    pass


class XDLInvalidStepTypeError(XDLReadError):
    def __init__(self, step_name):
        self.step_name = step_name

    def __str__(self):
        return f'"{self.step_name}" is not a valid step type.'

class XDLInvalidPropError(XDLReadError):
    def __init__(self, step_name, prop):
        self.step_name = step_name
        self.prop = prop

    def __str__(self):
        return f'"{self.prop}" is an invalid prop for {self.step_name}.'

########
# JSON #
########

class XDLInvalidJSONError(XDLReadError):
    pass

class XDLJSONMissingHardwareError(XDLInvalidJSONError):
    def __str__(self):
        return 'XDL JSON is missing "hardware" section.'

class XDLJSONMissingReagentsError(XDLInvalidJSONError):
    def __str__(self):
        return 'XDL JSON is missing "reagents" section.'

class XDLJSONMissingStepsError(XDLInvalidJSONError):
    def __str__(self):
        return 'XDL JSON is missing "steps" section.'

class XDLJSONHardwareNotArrayError(XDLInvalidJSONError):
    def __str__(self):
        return 'Hardware section should be an array.'

class XDLJSONReagentsNotArrayError(XDLInvalidJSONError):
    def __str__(self):
        return 'Reagents section should be an array.'

class XDLJSONStepsNotArrayError(XDLInvalidJSONError):
    def __str__(self):
        return 'Steps section should be an array.'

class XDLJSONInvalidSectionError(XDLInvalidJSONError):
    def __init__(self, section_name):
        self.section_name = section_name

    def __str__(self):
        return f'{self.section_name} is an invalid section for XDL JSON.\
 Valid section keys: "steps", "reagents", "hardware".'

class XDLJSONMissingStepNameError(XDLInvalidJSONError):
    def __str__(self):
        return 'Step missing "name" parameter in XDL JSON.'

class XDLJSONMissingPropertiesError(XDLInvalidJSONError):
    def __str__(self):
        return 'XDL element must have "properties" object in XDL JSON.'
