from .words import (
    Word,
    QuantityWord,
    TimeWord,
    TempWord,
    PressureWord,
    QuantityGroupWord,
    ReagentWord,
    ReagentGroupWord,
    SolutionWord,
    MixtureWord,
    NumberWord,
    MultiplierWord,
    VesselComponentWord,
    AbstractReagentWord,
    StirSpeedWord,
    MassWord,
)
from ..constants import (
    DEFAULT_SLOW_STIR_SPEED,
    DEFAULT_FAST_STIR_SPEED,
    REFLUX_PLACEHOLDER_TEMP,
    FAST_STIRRING_WORDS,
    DEFAULT_OVERNIGHT_TIME,
    DEFAULT_BELOW_TEMP_REDUCTION
)

class Modifier(Word):
    def __init__(self, words):
        self.words = words

class TemperatureModifier(Modifier):
    def __init__(self, words):
        self.words = words
        self.temp = None
        phrase = ' '.join([str(word) for word in words])
        if ('room temperature' in phrase
            or 'ambient temperature' in phrase
            or ' rt' in phrase
                or ' r.t' in phrase):
            self.temp = 25

        elif 'reflux' in phrase:
            # Code temp for step to have reflux temperature guessed during
            # conversion to XDL
            self.temp = REFLUX_PLACEHOLDER_TEMP

        elif 'dry ice' in phrase:
            self.temp = -78

        # Catch 'ice bath' and 'ice-salt bath'
        elif 'ice' in phrase and 'bath' in phrase:
            self.temp = 0

        elif 'water bath' in phrase:
            self.temp = 100

        elif 'oil bath' in phrase:
            self.temp = 150

        elif 'free flame' in phrase:
            self.temp = 150

        for word in self.words:
            if type(word) == TempWord:
                self.temp = word.quantity

            elif type(word) == QuantityGroupWord:
                for quantity in word.words:
                    if type(quantity) == TempWord:
                        self.temp = quantity.quantity

        if 'below' in phrase:
            self.temp -= DEFAULT_BELOW_TEMP_REDUCTION

class TimeModifier(Modifier):
    def __init__(self, words):
        self.words = words
        self.time = None
        phrase = ' '.join([str(word) for word in words])
        if 'overnight' in phrase:
            self.time = Word(f'{DEFAULT_OVERNIGHT_TIME/ 3600} hrs')
        elif 'several hours' in phrase:
            self.time = Word('7 hrs')
        # Until reaction completed...
        elif 'until reaction' in phrase:
            self.time = 0
        else:
            for word in self.words:
                if type(word) == TimeWord:
                    self.time = word
                elif type(word) == QuantityGroupWord:
                    for quantity in word.quantities:
                        if type(quantity) == TimeWord:
                            self.time = quantity

class PressureModifier(Modifier):
    def __init__(self, words):
        self.words = words
        self.pressure = None
        for word in self.words:
            if type(word) == PressureWord:
                self.pressure = word
            elif type(word) == QuantityGroupWord:
                self.pressure = word.quantities[0]

class VesselModifier(Modifier):
    def __init__(self, words):
        self.words = words
        self.components = [word for word in words
                           if type(word) == VesselComponentWord]

class AtmosphereModifier(Modifier):
    def __init__(self, words):
        self.words = words

class DetailsModifier(Modifier):
    def __init__(self, words):
        self.words = words

class ReagentModifier(Modifier):
    def __init__(self, words):
        self.words = words
        self.reagents = []
        self.n_portions = 1
        # Get all ReagentWords in a list.
        for word in words:
            if type(word) == ReagentGroupWord:
                for reagent in word:
                    self.reagents.append(reagent)

            elif isinstance(word, AbstractReagentWord):
                if self.n_portions == 1:
                    if hasattr(word, 'repeats') and word.repeats != 1:
                        self.n_portions = word.repeats

                self.reagents.append(word)

            # '3 80 mL portions of ether...'
            elif type(word) == NumberWord:
                self.n_portions = int(word.quantity)

        # i.e. 'to', 'with', etc
        self.preposition = ' '.join([str(word) for word in words[:-1]]).lower()

class TechniqueModifier(Modifier):
    def __init__(self, words):
        self.words = words

class MethodModifier(Modifier):
    def __init__(self, words):
        self.words = words

class StirringModifier(Modifier):
    def __init__(self, words):
        self.words = words
        self.stir_speed = 'default'
        for word in words:
            if 'slow' in str(word):
                self.stir_speed = DEFAULT_SLOW_STIR_SPEED
            for fast_stirring_word in FAST_STIRRING_WORDS:
                if fast_stirring_word in str(word):
                    self.stir_speed = DEFAULT_FAST_STIR_SPEED

            if type(word) == StirSpeedWord:
                self.stir_speed = word.quantity

            elif type(word) == QuantityGroupWord:
                for subword in word.words:
                    if type(subword) == StirSpeedWord:
                        self.stir_speed = subword.quantity

class AdditionModifier(Modifier):
    def __init__(self, words):
        self.words = words
        self.mass_at_interval = None
        self.n_portions = None
        for i, word in enumerate(words):
            if type(word) == MassWord:
                if i + 2 < len(words):
                    if str(words[i + 1]) == 'every' and type(words[i + 2]) == TimeWord:
                        self.mass_at_interval = {
                            'mass': str(word),
                            'interval': str(words[i + 2])
                        }

            elif str(word) == 'portions':
                if i - 1 >= 0 and type(words[i - 1]) == NumberWord:
                    self.n_portions = words[i - 1].quantity

class RepeatModifier(Modifier):
    def __init__(self, words):
        self.words = words
        if type(words[0]) == MultiplierWord:
            self.repeats = words[0].multiplier
