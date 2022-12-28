import re
from typing import List

from ..constants import *
from ..logging import get_logger

class Word(object):
    def __init__(self, word, pos_tag=''):
        self.word = word
        self.words = [word]
        # pos_tag is remnant from old classic_reagent_tagger. Only here while
        # new reagent tagging system is being proven to work.
        self.pos = pos_tag

    def __str__(self):
        if hasattr(self, 'word'):
            return self.word
        else:
            return ' '.join([str(word) for word in self.words])

    def update(self):
        self.__init__(self.words)

# was, were, are, is, should be
class AuxiliaryVerbWord(Word):
    def __init__(self, words):
        self.words = words

class NumberWord(Word):
    def __init__(self, word):
        self.words = [word]
        self.quantity = float(word.word.lstrip('~'))

class UnitWord(Word):
    def __init__(self, word):
        self.words = [word]
        self.unit = str(word)
        self.unit_code = WORD_UNIT_DICT[self.unit]

class VolumeUnitWord(UnitWord):
    def __init__(self, word):
        super().__init__(word)

class MassUnitWord(UnitWord):
    def __init__(self, word):
        super().__init__(word)

class TempUnitWord(UnitWord):
    def __init__(self, word):
        super().__init__(word)

class StirSpeedUnitWord(UnitWord):
    def __init__(self, word):
        super().__init__(word)

class LengthUnitWord(UnitWord):
    def __init__(self, word):
        super().__init__(word)

class TimeUnitWord(UnitWord):
    def __init__(self, word):
        super().__init__(word)

class MolPercentUnitWord(UnitWord):
    def __init__(self, words):
        self.words = words
        self.unit = ' '.join([str(word) for word in words])
        self.unit_code = WORD_UNIT_DICT[self.unit]

class MolUnitWord(UnitWord):
    def __init__(self, word):
        super().__init__(word)

class ConcUnitWord(UnitWord):
    def __init__(self, word):
        super().__init__(word)

class PercentUnitWord(UnitWord):
    def __init__(self, word):
        super().__init__(word)

class EquivalentsUnitWord(UnitWord):
    def __init__(self, word):
        super().__init__(word)

class PressureUnitWord(UnitWord):
    def __init__(self, word):
        super().__init__(word)

class RatioWord(Word):
    def __init__(self, words):
        self.words = words
        self.nominator, self.denominator = words[0].word.split(':')

class RangeWord(Word):
    def __init__(self, words):
        self.words = words
        phrase = ' '.join([str(word) for word in words])
        self.unit = ''

        if ' to ' in phrase:
            numbers = [word for word in words if type(word) == NumberWord]
            if not numbers:
                numbers = [word for word in words if isinstance(
                    word, QuantityWord)]
                if numbers:
                    self.unit = numbers[0].unit
            if len(numbers) > 0:
                self.min = numbers[0].quantity
            if len(numbers) > 1:
                self.max = numbers[1].quantity
            else:
                self.max = self.min
            self.val = (self.min + self.max) / 2

        else:
            match = re.match(range_float_regex_pattern, str(words[0]))
            self.min, self.max, self.val = None, None, None
            if match:
                self.min = float(match[1])
                self.max = float(match[3])
                self.val = (self.min + self.max) / 2

    def __str__(self):
        return f'{self.val} {self.unit}'

class SupplierWord(Word):
    def __init__(self, words):
        self.words = words

class QuantityWord(Word):
    def __init__(self, words):
        self.words = words

        try:
            number_pos = 0
            assert isinstance(words[-1], UnitWord)
            while (number_pos < len(words) - 1
                   and not type(words[number_pos]) in [NumberWord, RangeWord]):
                # 'about 1 mL'
                number_pos += 1
            assert isinstance(words[number_pos], (NumberWord, RangeWord))
        except AssertionError:
            logger = get_logger()
            logger.warning('Error: Failed to instantiate QuantityWord\nProblem words: {0}'.format(
                ' '.join([str(word) for word in words])))
            return

        self.unit = words[-1].unit
        self.unit_code = words[-1].unit_code

        for word in words:
            if type(word) == NumberWord:
                self.quantity = word.quantity
                break

            elif type(word) == RangeWord:
                self.quantity = (word.max + word.min) / 2
                break

    def __str__(self):
        words_to_use = []
        at_num = False
        for word in self.words:
            if re.match(r'[~-]?[0-9]', str(word)):
                at_num = True
                words_to_use.append(word)
            elif at_num:
                words_to_use.append(word)
        s = ' '.join([str(word).lstrip('~').lstrip(' ')
                      for word in words_to_use])
        return s

class MolPercentWord(QuantityWord):
    def __init__(self, words):
        super().__init__(words)

class StirSpeedWord(QuantityWord):
    def __init__(self, words):
        super().__init__(words)

class pHWord(QuantityWord):
    def __init__(self, words):
        self.words = words
        self.unit = None
        self.unit_code = None
        self.quantity = words[1]
        self.ph = str(words[1])

class MultiplierWord(Word):
    def __init__(self, words):
        self.words = words
        phrase = ' '.join([str(word) for word in words])
        # 'four times 60 mL'
        if phrase.lower() in LITERAL_MULTIPLIER_DICT:
            self.multiplier = LITERAL_MULTIPLIER_DICT[phrase.lower()]

        elif len(words) > 1:
            # '4 x 60 mL'
            for word in words:
                if type(word) == NumberWord:
                    try:
                        self.multiplier = int(str(word))
                    except ValueError:
                        self.multiplier = float(str(word))

        # '4x 60 mL'
        else:
            multiplier_match = re.match(
                multiplier_regex_pattern, words[0].word)[1]
            try:
                self.multiplier = int(multiplier_match)
            except ValueError:
                try:
                    self.multiplier = float(multiplier_match)
                except ValueError as e:
                    raise(e)

class VolumeWord(QuantityWord):
    def __init__(self, words):
        super().__init__(words)

    @property
    def ml(self):
        if self.unit_code == VOLUME_ML:
            return self.quantity
        elif self.unit_code == VOLUME_L:
            return self.quantity * 1000
        elif self.unit_code == VOLUME_CL:
            return self.quantity * 10
        elif self.unit_code == VOLUME_DL:
            return self.quantity * 100
        elif self.unit_code == VOLUME_UL:
            return self.quantity / 1000

class RepeatedVolumeWord(VolumeWord):
    def __init__(self, words):
        for word in words:
            if type(word) == VolumeWord:
                super().__init__(word.words)
                self.volume = word

            elif type(word) == MultiplierWord:
                self.multiplier = word.multiplier

        self.words = words

class MassWord(QuantityWord):
    def __init__(self, words):
        super().__init__(words)

class TempWord(QuantityWord):
    def __init__(self, words):
        super().__init__(words)

class TimeWord(QuantityWord):
    def __init__(self, words):
        super().__init__(words)

class LengthWord(QuantityWord):
    def __init__(self, words):
        super().__init__(words)

class ConcWord(QuantityWord):
    def __init__(self, words):
        self.words = words
        # [NumberWord, ConcUnitWord]
        if len(words) == 2:
            if type(words[0]) == NumberWord and type(words[1]) == ConcUnitWord:
                super().__init__(words)

            # [PercentWord, 'aq'] e.g. '57 % aq'
            elif type(words[0]) == PercentWord and str(words[1]) == 'aq':
                self.quantity = words[0].quantity
                self.unit = r'% aq'
                self.unit_code = PERCENT

        # [Word] e.g. '3M'
        else:
            self.quantity = re.match(conc_regex_pattern, str(words[0]))[1]
            self.unit = 'M'
            self.unit_code = MOL_PER_L

class MolWord(QuantityWord):
    def __init__(self, words):
        super().__init__(words)

class PercentWord(QuantityWord):
    def __init__(self, words):
        super().__init__(words)

class BPWord(Word):
    def __init__(self, words):
        self.words = words

class MPWord(Word):
    def __init__(self, words):
        self.words = words

class YieldWord(Word):
    def __init__(self, words):
        self.words = words
        self.percentage_yield = None
        for word in words:
            if type(word) == PercentWord:
                self.percentage_yield = word.quantity

class EquivalentsWord(QuantityWord):
    def __init__(self, words):
        super().__init__(words)

class PressureWord(QuantityWord):
    def __init__(self, words):
        super().__init__(words)

class PercentInSolventWord(QuantityWord):
    def __init__(self, words):
        # super().__init__(words)
        self.words = words
        self.unit = None
        self.unit_code = None
        self.reagent = [word for word in words if type(word) == ReagentNameWord]
        self.volume = [word for word in words if type(word) == VolumeWord]
        self.mass = [word for word in words if type(word) == MassWord]
        if self.reagent:
            self.reagent = self.reagent[0]
        if self.volume:
            self.volume = self.volume[0]
        if self.mass:
            self.mass = self.mass[0]

class QuantityGroupWord(Word):
    def __init__(self, words):
        self.words = words
        self.quantities = []
        for word in words:
            if isinstance(word, QuantityWord):
                self.quantities.append(word)

    def contains_volume(self):
        return any(type(quantity) == VolumeWord for quantity in self.quantities)

    def contains_mass(self):
        return any([type(quantity) == MassWord for quantity in self.quantities])

    def contains_amount(self):
        return (any([type(quantity) in [MassWord, VolumeWord, EquivalentsWord]
                     for quantity in self.quantities]))

    def __iter__(self):
        return iter(self.quantities)

class AbstractReagentWord(Word):
    """Base class for all reagent related words so that one class can be used
    for matching Reagents/Solutions/ReagentGroups etc.
    """

    def __init__(self, words):
        self.words = words
        self.cold, self.icecold, self.hot, self.warm, self.minimum_volume = (
            False, False, False, False, False
        )
        self.temp = None

class ReagentNameFragmentWord(Word):
    def __init__(self, words):
        self.words = words

class ReagentNameWord(Word):
    def __init__(self, words):
        self.words = words
        self.cold, self.icecold, self.hot, self.warm, self.minimum_volume = (
            False, False, False, False, False)
        start_pt = 0
        for i, word in enumerate(words):
            if str(word) in COLD_WORDS:
                self.cold = True
                start_pt = i + 1

            elif str(word) in ICECOLD_WORDS:
                self.icecold = True
                start_pt = i + 1

            elif str(word) in HOT_WORDS:
                self.hot = True
                start_pt = i + 1

            elif str(word) in WARM_WORDS:
                self.warm = True
                start_pt = i + 1

            elif str(word) in MINIMUM_VOLUME_WORDS:
                self.minimum_volume = True
                start_pt = i + 1

            elif str(word) in MISC_REAGENT_NAME_START_WORDS:
                start_pt = i + 1

        if start_pt < len(words):
            self.reagent_name = format_reagent_name(words[start_pt:])
        else:
            self.reagent_name = ' '.join([str(word) for word in words])

class ReagentWord(AbstractReagentWord):
    def __init__(self, words):
        super().__init__(words)
        self.quantities = []
        self.repeats = 1
        self.name = 'unknown_reagent'
        percent_str = ''
        for word in words:
            if type(word) == QuantityGroupWord:
                for _, quantity in enumerate(word):
                    self.quantities.append(quantity)

                    # stuff like 10% in ethanol should be included in reagent name
                    if type(quantity) in [PercentWord, PercentInSolventWord]:
                        percent_str = str(quantity)

                    elif type(quantity) == TempWord:
                        self.temp = quantity

                    elif type(quantity) == RepeatedVolumeWord:
                        self.repeats = quantity.multiplier

            elif isinstance(word, QuantityWord):
                self.quantities.append(word)

            elif type(word) == ReagentNameWord:
                self.name = word.reagent_name
                self.cold, self.icecold, self.warm, self.hot = (
                    word.cold, word.icecold, word.warm, word.hot,)
                self.minimum_volume = word.minimum_volume

            elif type(word) == MultiplierWord:
                self.repeats = word.multiplier

        # If reagent is just '1' e.g. reference to product from previous step.
        if self.name == 'unknown_reagent':
            for word in words:
                if type(word) == NumberWord:
                    self.name = f'compound {str(word)}'

        if percent_str:
            self.name += f' ({percent_str})'

    @property
    def volume(self):
        for quantity in self.quantities:
            if quantity.unit_code in VOLUME_UNIT_CODES:
                return quantity
        return 0

    @property
    def mass(self):
        for quantity in self.quantities:
            if quantity.unit_code in MASS_UNIT_CODES:
                return quantity
        return 0

class ReagentPlaceholderWord(AbstractReagentWord):
    def __init__(self, words):
        super().__init__(words)
        self.volume = 0
        self.name = ' '.join([str(word) for word in words])
        for word in words:
            if type(word) == VolumeWord:
                self.volume = str(word)
        if str(self).startswith('the rest of'):
            self.volume = 'all'

class ReagentGroupWord(AbstractReagentWord):
    def __init__(self, words):
        self.words = words
        self.reagents = [
            word
            for word in self.words
            if isinstance(word, AbstractReagentWord)
        ]
        self.name = ' and '.join([reagent.name for reagent in self.reagents])

    def __iter__(self):
        return iter(self.reagents)

class SolutionWord(AbstractReagentWord):
    def __init__(self, words):
        super().__init__(words)
        self.solvent = None
        self.solutes = []
        self.repeats = 1
        phrase = ' '.join(
            [str(word) for word in words]).lower()

        # 'An aqueous solution of methyl iodide (5 g).'
        if 'aqueous solution' in phrase:
            self.solvent = ReagentWord([ReagentNameWord([Word('water', 'NN')])])
            self.solutes = [word for word in words if type(word) == ReagentWord]
            if len(self.solutes) == 1:
                for word in self.solutes[0].words:
                    if type(word) == QuantityGroupWord:
                        for subword in word.words:
                            self.process_percent_in_solvent_word(subword)

        # 'A solution of methyl iodide (5 g) in ethanol.'
        elif re.match(r'a ([a-z0-9A-Z ]+ )?solution of', phrase):

            if type(words[-1]) == ReagentGroupWord:
                self.solvent = words[-1].reagents[-1]
                self.solutes = words[-1].reagents[:-1]

            else:
                i = 0
                while i < len(words) and str(words[i]) != 'solution':
                    i += 1
                offset = i - 1
                # e.g. 'a hot solution of'
                self.solutes = [words[3 + offset]]
                if len(words) >= 6 + offset:
                    self.solvent = words[5 + offset]
                else:
                    for word in self.solutes[0].words:
                        if type(word) == QuantityGroupWord:
                            for subword in word.words:
                                self.process_percent_in_solvent_word(subword)

        elif ' in ' in phrase:
            self.solutes = [words[0]]
            self.solvent = words[-1]
            for subword in self.solvent.words:
                if type(subword) == QuantityGroupWord:
                    for quantity_word in subword.words:
                        self.process_repeated_volume_word(quantity_word)

        elif ' of ' in phrase:
            solvent_found = False
            for word in words:
                if isinstance(word, AbstractReagentWord):
                    if not solvent_found:
                        self.solvent = word
                        solvent_found = True
                    else:
                        self.solutes = [word]

        self.name = ' '.join([reagent.name for reagent in self.solutes])
        if self.solvent:
            self.name += f' {self.solvent.name} solution'

        if self.solutes and hasattr(self.solutes[0], 'repeats') and self.repeats == 1:
            self.repeats = self.solutes[0].repeats

        self.volume = self.get_volume()

    def process_percent_in_solvent_word(self, word):
        if (type(word) == PercentInSolventWord
            and word.volume != None
                and word.reagent != None):
            if not self.solvent:
                self.solvent = ReagentWord(
                    [word.volume, Word('of'), word.reagent])
            else:
                self.solvent.quantities.append(word.volume)

            if word.mass:
                self.solutes[0].quantities.append(word.mass)

    def process_repeated_volume_word(self, word):
        if type(word) == RepeatedVolumeWord:
            if not self.solvent.volume:
                self.solvent.quantities.append(self.solvent.volume)

            self.repeats = word.multiplier

    def get_volume(self):
        # Get total solution volume
        volume = 0
        if self.solvent and self.solvent.volume:
            volume += self.solvent.volume.ml

        for solute in self.solutes:

            if type(solute) == ReagentGroupWord:
                for subsolute in solute.reagents:
                    if subsolute.volume:
                        volume += subsolute.volume.ml

            elif solute.volume:
                volume += solute.volume.ml

        return volume

class MixtureWord(AbstractReagentWord):
    def __init__(self, words):
        super().__init__(words)
        self.name = ' '.join([str(word) for word in words])
        self.quantities = [
            word for word in words if isinstance(word, QuantityWord)]
        self.volume = self.get_volume()

    def get_volume(self):
        volume = 0
        for word in self.words:
            if type(word) == VolumeWord:
                return str(word)

            elif type(word) in [ReagentWord, SolutionWord]:
                return str(word.volume)

            elif type(word) == ReagentGroupWord:
                for reagent in word:
                    if hasattr(reagent, 'volume'):
                        return str(reagent.volume)
        return volume


class VesselWord(Word):
    def __init__(self, words):
        self.words = words

    def process_modifiers(self, modifiers):
        self.modifiers = modifiers

class VesselComponentWord(Word):
    def __init__(self, words):
        self.words = words

class VesselComponentGroupWord(Word):
    def __init__(self, words):
        self.words = words

class BathWord(Word):
    def __init__(self, words):
        self.words = words

class TechniqueWord(Word):
    def __init__(self, words):
        self.words = words

    def process_modifiers(self, words):
        self.modifiers = []

class ColorWord(Word):
    def __init__(self, words):
        self.words = words

class DetailsWord(Word):
    def __init__(self, words):
        self.words = words

#############
### UTILS ###
#############


REAGENT_NAME_REPLACEMENTS = [
    (' ,', ','),
    (', ', ','),
    ('( ', '('),
    (' (', '('),
    (') ', ')'),
    (' )', ')'),
]

def format_reagent_name(words: List[Word]) -> str:
    """Given list of words, combine them into reagent name. Basically just
    fixes places where words are joined by spaces but shouldn't be.

    Args:
        words (List[Word]): List of Word objects to join into reagent name.

    Returns:
        str: Reagent name created from words.
    """
    reagent_name = None
    # 'Dry' -> 'dry'
    first_word = str(words[0])
    if len(first_word) > 2:
        # Don't change 'N,N'  -> 'n,N' or 'H2' -> 'h2'
        if first_word[1:].lower() == first_word[1:]:
            first_word = first_word[0].lower() + first_word[1:]
            reagent_name = ' '.join(
                [first_word] + [str(word) for word in words[1:]])

    if not reagent_name:
        reagent_name = ' '.join([str(word) for word in words])

    for replacement in REAGENT_NAME_REPLACEMENTS:
        reagent_name = reagent_name.replace(replacement[0], replacement[1])
    while '  ' in reagent_name:
        reagent_name = reagent_name.replace('  ', ' ')
    return reagent_name

class YieldPhraseWord(Word):
    def __init__(self, words):
        self.words = words
