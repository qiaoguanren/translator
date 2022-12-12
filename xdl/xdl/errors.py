import sys

###############
# Base Errors #
###############

class XDLError(Exception):
    pass

class XDLGraphError(XDLError):
    pass

class XDLCompilationError(XDLError):
    pass

class XDLExecutionError(XDLError):
    pass

class XDLValueError(XDLError):
    pass

#######################
# File I/O and Syntax #
#######################

class XDLInvalidFileTypeError(XDLError):
    def __init__(self, file_ext):
        self.file_ext = file_ext

    def __str__(self):
        return f'{self.file_ext} is an invalid XDL file type. Valid file\
 file types: .xdl, .xdlexe, .json'

class XDLInvalidSaveFormatError(XDLError):
    def  __init__(self, file_format):
        self.file_format = file_format

    def  __str__(self):
        return f'"{self.file_format}" is an invalid file format for saving\
 XDL. Valid file formats: "xml", "json".'

class XDLVesselNotDeclaredError(XDLError):
    def __init__(self, vessel):
        self.vessel = vessel

    def __str__(self):
        return f'"{self.vessel}" used as vessel in procedure but not declared\
 in <Hardware> section of XDL'

class XDLReagentNotDeclaredError(XDLError):
    def __init__(self, reagent):
        self.reagent = reagent

    def __str__(self):
        return f'"{self.reagent}" used as reagent in procedure but not declared\
 in <Reagents> section of XDL'

class XDLFileNotFoundError(XDLError):
    def __init__(self, file_name):
        self.file_name = file_name

    def __str__(self):
        return f'{self.file_name} does not exist.'

class XDLInvalidInputError(XDLError):
    def __init__(self, input_str):
        self.input_str = input_str

    def __str__(self):
        return f'Cannot instantiate XDL from this. Invalid syntax.\
     \n\n{self.input_str}'

class XDLInvalidArgsError(XDLError):
    def __str__(self):
        return 'Unable to initialise XDL object, invalid argument combination\
 given. Either xdl arg must be given with the name of a valid XDL\
 file or XDL string, or steps, reagents and hardware arguments must\
 all be given with lists of instantiated objects.'

#########
# Graph #
#########

class XDLGraphInvalidFileTypeError(XDLGraphError):
    def __init__(self, graph_file):
        self.graph_file = graph_file

    def __str__(self):
        return f'Graph file "{self.graph_file}" has any invalid file type.\
 Valid file types: .json, .graphml'

class XDLGraphFileNotFoundError(XDLGraphError):
    def __init__(self, graph_file):
        self.graph_file = graph_file

    def __str__(self):
        return f'Graph file "{self.graph_file}" does not exist.'

class XDLGraphTypeError(XDLGraphError):
    def __init__(self, graph_file):
        self.graph_file = graph_file

    def __str__(self):
        return f'{type(self.graph_file)} is not a valid type to load a graph\
 Accepted objects: Paths to .json or .graphml graph files. Contents of .json\
 graph as dict. Networkx MultiDiGraph.'

###############
# Compilation #
###############

class XDLDoubleCompilationError(XDLCompilationError):
    def __str__(self):
        return 'Cannot compile same XDL object twice.'

#############
# Execution #
#############

class XDLInvalidPlatformControllerError(XDLExecutionError):
    def __init__(self, platform_controller):
        self.platform_controller = platform_controller

    def __str__(self):
        return f'Invalid platform controller supplied. Type:\
 {type(self.platform_controller)} Value: {self.platform_controller}'

class XDLExecutionBeforeCompilationError(XDLExecutionError):
    def __str__(self):
        return 'Trying to execute procedure that has not been compiled. First\
 call xdl_obj.prepare_for_execution(graph).'

class XDLDurationBeforeCompilationError(XDLExecutionError):
    def __str__(self):
        return 'Trying to calculate duration for procedure that has not been\
 compiled. First call xdl_obj.prepare_for_execution(graph).'

class XDLReagentVolumesBeforeCompilationError(XDLExecutionError):
    def __str__(self):
        return 'Trying to calculate reagent volumes for procedure that has not\
 been compiled. First call xdl_obj.prepare_for_execution(graph).'

class XDLExecutionOnDifferentGraphError(XDLExecutionError):
    def __str__(self):
        return 'Trying to execute XDL on different graph than the one it was\
 compiled with.'

########
# Misc #
########

class XDLStepIndexError(XDLError):
    def __init__(self, step_index, len_steps):
        self.step_index = step_index
        self.len_steps = len_steps

    def __str__(self):
        return f'{self.step_index} is out of bounds for step list with length\
 {self.len_steps}'

class XDLInvalidPlatformError(XDLError):
    def __init__(self, platform):
        self.platform = platform

    def __str__(self):
        return f'{self.platform} is an invalid platform. Platform must\
 be "chemputer" or a subclass of AbstractPlatform.'

class XDLLanguageUnavailableError(XDLError):
    def __init__(self, language, available_languages=None):
        self.language = language
        self.available_languages = available_languages

    def __str__(self):
        s = f'Language {self.language} not supported.'
        if self.available_languages is not None:
            s += f'Available languages: {", ".join(self.available_languages)}'
        return s

##################
# Step Templates #
##################

class XDLStepTemplateError(XDLError):
    pass

class XDLStepTemplateMissingPropError(XDLStepTemplateError):
    def __init__(self, name, prop, prop_type):
        self.name = name
        self.prop = prop
        self.prop_type = prop_type

    def __str__(self):
        return f'"{self.name}" step template requires an "{self.prop}"\
 ({self.prop_type}) property, but this has not been found in PROP_TYPES.'

class XDLStepTemplatePropTypeError(XDLStepTemplateError):

    def __init__(self, name, prop, prop_type, invalid_prop_type):
        self.name = name
        self.prop = prop
        self.prop_type = prop_type
        self.invalid_prop_type = invalid_prop_type

    def __str__(self):
        return f'"{self.name}" step template requires that "{self.prop}" has\
 prop type {str(self.prop_type)}. Prop type found is\
 {str(self.invalid_prop_type)}.'

class XDLStepTemplateMissingDefaultPropError(XDLStepTemplateError):
    def __init__(self, name, prop, default_prop):
        self.name = name
        self.prop = prop
        self.default_prop = default_prop

    def __str__(self):
        return f'"{self.name}" step template requires that "{self.prop}"\
 has a default value of {self.default_prop}, but this has not been found in\
 DEFAULT_PROPS.'

class XDLStepTemplateInvalidDefaultPropError(XDLStepTemplateError):

    def __init__(self, name, prop, default_prop, invalid_default_prop):
        self.name = name
        self.prop = prop
        self.default_prop = default_prop
        self.invalid_default_prop = invalid_default_prop

    def __str__(self):
        return f'"{self.name}" step template requires that "{self.prop}" has\
 has a default value of {str(self.default_prop)}. Default value found is\
 {str(self.invalid_default_prop)}.'

class XDLStepTemplateMissingPropLimitError(XDLStepTemplateError):
    def __init__(self, name, prop, prop_limit):
        self.name = name
        self.prop = prop
        self.prop_limit = prop_limit

    def __str__(self):
        return f'"{self.name}" step template requires that "{self.prop}"\
 has prop_limit {self.prop_limit}, but this has not been found in\
 PROP_LIMITS.'

class XDLStepTemplateInvalidPropLimitError(XDLStepTemplateError):

    def __init__(self, name, prop, prop_limit, invalid_prop_limit):
        self.name = name
        self.prop = prop
        self.prop_limit = prop_limit
        self.invalid_prop_limit = invalid_prop_limit

    def __str__(self):
        return f'"{self.name}" step template requires that "{self.prop}" has\
 has a prop limit {str(self.prop_limit)}. Prop limit found is\
 {str(self.invalid_prop_limit)}.'

class XDLStepTemplateNameError(XDLStepTemplateError):

    def __init__(self, mandatory_name, name):
        self.mandatory_name = mandatory_name
        self.name = name

    def __str__(self):
        return f'{self.mandatory_name} step must have class name\
 {self.mandatory_name}. Name found: {self.name}.'

##############
# Prop Types #
##############

class XDLUndeclaredDefaultPropError(XDLError):
    def __init__(self, step_name, prop):
        self.step_name = step_name
        self.prop = prop

    def __str__(self):
        return f'{self.step_name} step class has {self.prop} in DEFAULT_PROPS\
 but not in PROP_TYPES.'

class XDLUndeclaredPropLimitError(XDLError):
    def __init__(self, step_name, prop):
        self.step_name = step_name
        self.prop = prop

    def __str__(self):
        return f'{self.step_name} step class has {self.prop} in PROP_LIMITS\
 but not in PROP_TYPES.'

class XDLUndeclaredInternalPropError(XDLError):
    def __init__(self, step_name, prop):
        self.step_name = step_name
        self.prop = prop

    def __str__(self):
        return f'{self.step_name} step class has {self.prop} in INTERNAL_PROPS\
 but not in PROP_TYPES.'

class XDLUndeclaredAlwaysWriteError(XDLError):
    def __init__(self, step_name, prop):
        self.step_name = step_name
        self.prop = prop

    def __str__(self):
        return f'{self.step_name} step class has {self.prop} in ALWAYS_WRITE\
 but not in PROP_TYPES.'

class XDLMissingDefaultPropError(XDLError):
    def __init__(self, xdl_element_name, prop):
        self.xdl_element_name = xdl_element_name
        self.prop = prop

    def __str__(self):
        return f'"default" given as value for {self.prop} property, but no\
 default value found in {self.xdl_element_name} DEFAULT_PROPS.'

class XDLMissingPropTypeError(XDLError):
    def __init__(self, xdl_element_name, prop):
        self.xdl_element_name = xdl_element_name
        self.prop = prop

    def __str__(self):
        return f'Missing prop type for {self.prop} in {self.xdl_element_name}\
 class.'

class XDLFailedPropLimitError(XDLValueError):
    def __init__(self, xdl_element_name, prop, value, prop_limit):
        self.xdl_element_name = xdl_element_name
        self.prop = prop
        self.value = value
        self.prop_limit = prop_limit

    def __str__(self):
        return f'{self.xdl_element_name}: Value "{self.value}" does not match\
 "{self.prop}" prop limit. {self.prop_limit.hint}'

class XDLTypeConversionError(XDLValueError):
    def __init__(self, xdl_element_name, prop, prop_type, value):
        self.xdl_element_name = xdl_element_name
        self.prop = prop
        self.value = value
        self.prop_type = prop_type

    def __str__(self):
        return f'{self.xdl_element_name}: Unable to convert {self.prop} value\
 {self.value} to {self.prop_type}.'
