from typing import List, Tuple
from ...constants import WORD_UNIT_DICT, float_regex_pattern

#: Replace HTML character codes with actual characters, and remove HTML
#: elements.
HTML_REPLACEMENTS: List[Tuple[str, str]] = [
    ('&#xB0; ', '°'),  # Degrees symbol
    ('&#x03B4;', 'γ'),  # Gamma symbol
    # Encoding bug makes this character instead of non breaking space.
    ('Â', ''),
    ('&nbsp;', ' '),  # Convert non breaking space to normal space.
    (r'(<.*?>)', ''),  # Delete HTML elements i.e. <b>
]

#: Replacements to fix missing spaces in synthesis texts.
# Mistakes common in Reaxys.
MISSING_SPACE_REPLACEMENTS: List[Tuple[str, str]] = [
    # Fix this.Sentence starts without space.
    (r'([A-Za-z])\.([A-Za-z])', r'\1. \2'),
    (r'(r\. t\.)', 'r.t.'),  # Fix error introduced by pattern above.
    (r'(°C)([a-zA-Z])', r'\1 \2'),  # Fix 30 °Ctext has no space.
    ('  ', ' '),  # Convert accidental double space to single space.
]

# Hyphen quantity replacement, i.e. '250-mL' -> '250 mL'
units_regex = r'('
for item in WORD_UNIT_DICT:
    units_regex += item + r'|'
units_regex = units_regex[:-1] + ')'
HYPHEN_QUANTITY_REPLACEMENT: Tuple[str, str] = (
    float_regex_pattern + '-' + units_regex,
    r'\1 \2')

LITERAL_NUMBER_REPLACEMENTS = [
    (r'(^| )(a couple of)[ ]', r'\g<1>2 '),
    (r'(^| )(several)[ ]', r'\g<1>7 '),
    (r'(^| )(zero)[ ]', r'\g<1>0 '),
    (r'(^| )([o|O])ne[ ]', r'\g<1>1 '),
    (r'(^| )([t|T])wo[ ]', r'\g<1>2 '),
    (r'(^| )([t|T])hree[ ]', r'\g<1>3 '),
    (r'(^| )([f|F])our[ ]', r'\g<1>4 '),
    (r'(^| )([f|F])ive[ ]', r'\g<1>5 '),
    (r'(^| )([s|S])ix[ ]', r'\g<1>6 '),
    (r'(^| )([s|S])even[ ]', r'\g<1>7 '),
    (r'(^| )([e|E])ight[ ]', r'\g<1>8 '),
    (r'(^| )([n|N])ine[ ]', r'\g<1>9 '),
    (r'(^| )([t|T])en[ ]', r'\g<1>10 '),
    (r'(^| )([e|E])leven[ ]', r'\g<1>11 '),
    (r'(^| )([t|T])welve[ ]', r'\g<1>12 '),
    (r'(^| )([t|T])hirteen[ ]', r'\g<1>13 '),
    (r'(^| )([f|F])ourteen[ ]', r'\g<1>14 '),
    (r'(^| )([f|F])ifteen[ ]', r'\g<1>15 '),
    (r'(^| )([s|S])ixteen[ ]', r'\g<1>16 '),
    (r'(^| )([s|S])eventeen[ ]', r'\g<1>17 '),
    (r'(^| )([e|E])ighteen[ ]', r'\g<1>18 '),
    (r'(^| )([n|N])ineteen[ ]', r'\g<1>19 '),
    (r'(^| )([t|T])wenty[ ]', r'\g<1>20 '),
    (r'(^| )([t|T])wenty(-| )([o|O])ne[ ]', r'\g<1>21 '),
    (r'(^| )([t|T])wenty(-| )([t|T])wo[ ]', r'\g<1>22 '),
    (r'(^| )([t|T])wenty(-| )([t|T])hree[ ]', r'\g<1>23 '),
    (r'(^| )([t|T])wenty(-| )([f|F])our[ ]', r'\g<1>24 '),
    (r'(^| )([t|T])wenty(-| )([f|F])ive[ ]', r'\g<1>25 '),
    (r'(^| )([t|T])wenty(-| )([s|S])ix[ ]', r'\g<1>26 '),
    (r'(^| )([t|T])wenty(-| )([s|S])even[ ]', r'\g<1>27 '),
    (r'(^| )([t|T])wenty(-| )([e|E])ight[ ]', r'\g<1>28 '),
    (r'(^| )([t|T])wenty(-| )([n|N])ine[ ]', r'\g<1>29 '),
    (r'(^| )([t|T])hirty[ ]', r'\g<1>30  '),
    (r'(^| )([t|T])hirty(-| )([o|O])ne[ ]', r'\g<1>31 '),
    (r'(^| )([t|T])hirty(-| )([t|T])wo[ ]', r'\g<1>32 '),
    (r'(^| )([t|T])hirty(-| )([t|T])hree[ ]', r'\g<1>33 '),
    (r'(^| )([t|T])hirty(-| )([f|F])our[ ]', r'\g<1>34 '),
    (r'(^| )([t|T])hirty(-| )([f|F])ive[ ]', r'\g<1>35 '),
    (r'(^| )([t|T])hirty(-| )([s|S])ix[ ]', r'\g<1>36 '),
    (r'(^| )([t|T])hirty(-| )([s|S])even[ ]', r'\g<1>37 '),
    (r'(^| )([t|T])hirty(-| )([e|E])ight[ ]', r'\g<1>38 '),
    (r'(^| )([t|T])hirty(-| )([n|N])ine[ ]', r'\g<1>39 '),
    (r'(^| )([f|F])orty[ ]', r'\g<1>40  '),
    (r'(^| )([f|F])orty(-| )([o|O])ne[ ]', r'\g<1>41 '),
    (r'(^| )([f|F])orty(-| )([t|T])wo[ ]', r'\g<1>42 '),
    (r'(^| )([f|F])orty(-| )([t|T])hree[ ]', r'\g<1>43 '),
    (r'(^| )([f|F])orty(-| )([f|F])our[ ]', r'\g<1>44 '),
    (r'(^| )([f|F])orty(-| )([f|F])ive[ ]', r'\g<1>45 '),
    (r'(^| )([f|F])orty(-| )([s|S])ix[ ]', r'\g<1>46 '),
    (r'(^| )([f|F])orty(-| )([s|S])even[ ]', r'\g<1>47 '),
    (r'(^| )([f|F])orty(-| )([e|E])ight[ ]', r'\g<1>48 '),
    (r'(^| )([f|F])orty(-| )([n|N])ine[ ]', r'\g<1>49 '),
    (r'(^| )([f|F])ifty[ ]', r'\g<1>50  '),
    (r'(^| )([f|F])ifty(-| )([o|O])ne[ ]', r'\g<1>51 '),
    (r'(^| )([f|F])ifty(-| )([t|T])wo[ ]', r'\g<1>52 '),
    (r'(^| )([f|F])ifty(-| )([t|T])hree[ ]', r'\g<1>53 '),
    (r'(^| )([f|F])ifty(-| )([f|F])our[ ]', r'\g<1>54 '),
    (r'(^| )([f|F])ifty(-| )([f|F])ive[ ]', r'\g<1>55 '),
    (r'(^| )([f|F])ifty(-| )([s|S])ix[ ]', r'\g<1>56 '),
    (r'(^| )([f|F])ifty(-| )([s|S])even[ ]', r'\g<1>57 '),
    (r'(^| )([f|F])ifty(-| )([e|E])ight[ ]', r'\g<1>58 '),
    (r'(^| )([f|F])ifty(-| )([n|N])ine[ ]', r'\g<1>59 '),
    (r'(^| )([s|S])ixty[ ]', r'\g<1>60  '),
    (r'(^| )([s|S])ixty(-| )([o|O])ne[ ]', r'\g<1>61 '),
    (r'(^| )([s|S])ixty(-| )([t|T])wo[ ]', r'\g<1>62 '),
    (r'(^| )([s|S])ixty(-| )([t|T])hree[ ]', r'\g<1>63 '),
    (r'(^| )([s|S])ixty(-| )([f|F])our[ ]', r'\g<1>64 '),
    (r'(^| )([s|S])ixty(-| )([f|F])ive[ ]', r'\g<1>65 '),
    (r'(^| )([s|S])ixty(-| )([s|S])ix[ ]', r'\g<1>66 '),
    (r'(^| )([s|S])ixty(-| )([s|S])even[ ]', r'\g<1>67 '),
    (r'(^| )([s|S])ixty(-| )([e|E])ight[ ]', r'\g<1>68 '),
    (r'(^| )([s|S])ixty(-| )([n|N])ine[ ]', r'\g<1>69 '),
    (r'(^| )([s|S])eventy[ ]', r'\g<1>70  '),
    (r'(^| )([s|S])eventy(-| )([o|O])ne[ ]', r'\g<1>71 '),
    (r'(^| )([s|S])eventy(-| )([t|T])wo[ ]', r'\g<1>72 '),
    (r'(^| )([s|S])eventy(-| )([t|T])hree[ ]', r'\g<1>73 '),
    (r'(^| )([s|S])eventy(-| )([f|F])our[ ]', r'\g<1>74 '),
    (r'(^| )([s|S])eventy(-| )([f|F])ive[ ]', r'\g<1>75 '),
    (r'(^| )([s|S])eventy(-| )([s|S])ix[ ]', r'\g<1>76 '),
    (r'(^| )([s|S])eventy(-| )([s|S])even[ ]', r'\g<1>77 '),
    (r'(^| )([s|S])eventy(-| )([e|E])ight[ ]', r'\g<1>78 '),
    (r'(^| )([s|S])eventy(-| )([n|N])ine[ ]', r'\g<1>79 '),
    (r'(^| )([e|E])ighty[ ]', r'\g<1>80  '),
    (r'(^| )([e|E])ighty(-| )([o|O])ne[ ]', r'\g<1>81 '),
    (r'(^| )([e|E])ighty(-| )([t|T])wo[ ]', r'\g<1>82 '),
    (r'(^| )([e|E])ighty(-| )([t|T])hree[ ]', r'\g<1>83 '),
    (r'(^| )([e|E])ighty(-| )([f|F])our[ ]', r'\g<1>84 '),
    (r'(^| )([e|E])ighty(-| )([f|F])ive[ ]', r'\g<1>85 '),
    (r'(^| )([e|E])ighty(-| )([s|S])ix[ ]', r'\g<1>86 '),
    (r'(^| )([e|E])ighty(-| )([s|S])even[ ]', r'\g<1>87 '),
    (r'(^| )([e|E])ighty(-| )([e|E])ight[ ]', r'\g<1>88 '),
    (r'(^| )([e|E])ighty(-| )([n|N])ine[ ]', r'\g<1>89 '),
    (r'(^| )([n|N])inety[ ]', r'\g<1>90  '),
    (r'(^| )([n|N])inety(-| )([o|O])ne[ ]', r'\g<1>91 '),
    (r'(^| )([n|N])inety(-| )([t|T])wo[ ]', r'\g<1>92 '),
    (r'(^| )([n|N])inety(-| )([t|T])hree[ ]', r'\g<1>93 '),
    (r'(^| )([n|N])inety(-| )([f|F])our[ ]', r'\g<1>94 '),
    (r'(^| )([n|N])inety(-| )([f|F])ive[ ]', r'\g<1>95 '),
    (r'(^| )([n|N])inety(-| )([s|S])ix[ ]', r'\g<1>96 '),
    (r'(^| )([n|N])inety(-| )([s|S])even[ ]', r'\g<1>97 '),
    (r'(^| )([n|N])inety(-| )([e|E])ight[ ]', r'\g<1>98 '),
    (r'(^| )([n|N])inety(-| )([n|N])ine[ ]', r'\g<1>99 '),
    (r'(^| )([o|O])ne(-| )([h|H])undred[ ]', r'\g<1>100 '),
]

ORGSYN_UNITS_REGEX_END = r'\.([, )])([^A-Z])'

#: Replacements to standardise temperature phrases.
TEMP_REPLACEMENTS: List[Tuple[str, str]] = [
    ('º', '°'),
    ('⁰', '°'),
    (r'° C', '°C'),  # change '° C' to '°C'
    (r'°C\. ([a-z])', r'°C \1'),  # change '°C.' to '°C'.
    (r'°([^C])', r'°C\1'),  # OrgSyn doesn't write C after °
    (r' ([0-9])C', r' \1 °C'),  # '0C' to '0 °C'
    (r'([0-9])°C', r'\1 °C'),  # Add space after number i.e. '30°C' -> '30 °C'.
    (r'at 0 ([a-z])', r'at 0 °C \1'),
    (r'to r\.t\. ([A-Z])', r'to rt. \1'),
    (r'to r\.t\. ([a-z])', r'to rt \1'),

    # Assume explicit temp will be given, sorts 'pre-cooled (0 °C) anhydrous
    # ether (4 × 50 mL)' where 'pre-cooled' messes up reagent tagging.
    (r'pre-cooled', ''),
]

#: Replacements to standardise time units
TIME_REPLACEMENTS: List[Tuple[str, str]] = [
    # Full stop interpreted incorrectly as end of sentence.
    (float_regex_pattern + r' s\. ([a-z])', r'\1  seconds \2'),
    (float_regex_pattern + r' sec\. ([a-z])', r'\1  seconds \2'),
    (float_regex_pattern + r' secs\. ([a-z])', r'\1  seconds \2'),

    (float_regex_pattern + r' m\. ([a-z])', r'\1  minutes \2'),
    (float_regex_pattern + r' min\. ([a-z])', r'\1  minutes \2'),
    (float_regex_pattern + r' mins\. ([a-z])', r'\1  minutes \2'),

    (float_regex_pattern + r' h\. ([a-z])', r'\1 hours \2'),
    (float_regex_pattern + r' hr\. ([a-z])', r'\1 hours \2'),
    (float_regex_pattern + r' hrs\. ([a-z])', r'\1 hours \2'),

    # With short units full stop becomes part of word e.g. 'h.' is interpreted
    # as word. Don't know for sure secs, mins and hrs cause same problem but
    # best to be safe.
    (float_regex_pattern + r' s\. ([A-Z])', r'\1  seconds. \2'),
    (float_regex_pattern + r' sec\. ([A-Z])', r'\1  seconds. \2'),
    (float_regex_pattern + r' secs\. ([A-Z])', r'\1  seconds. \2'),

    (float_regex_pattern + r' m\. ([A-Z])', r'\1  minutes. \2'),
    (float_regex_pattern + r' min\. ([A-Z])', r'\1  minutes. \2'),
    (float_regex_pattern + r' mins\. ([A-Z])', r'\1  minutes. \2'),

    (float_regex_pattern + r' h\. ([A-Z])', r'\1 hours. \2'),
    (float_regex_pattern + r' hr\. ([A-Z])', r'\1 hours. \2'),
    (float_regex_pattern + r' hrs\. ([A-Z])', r'\1 hours. \2'),

    ('one-half hour', '30 mins'),  # Seen in Org. Synth.
]

#: Replacements to standardise mass units.
MASS_REPLACEMENTS: List[Tuple[str, str]] = [
    (r' grams ', ' g '),
    # OrgSyn write units this way
    (r' g' + ORGSYN_UNITS_REGEX_END, r' g\1\2'),
    (r' mg' + ORGSYN_UNITS_REGEX_END, r' mg\1\2'),
    (r' ug' + ORGSYN_UNITS_REGEX_END, r' ug\1\2'),
    (r' μg' + ORGSYN_UNITS_REGEX_END, r' μg\1\2'),
    (r' kg' + ORGSYN_UNITS_REGEX_END, r' kg\1\2'),
]

#: Replacements to standardise volume units.
VOLUME_REPLACEMENTS: List[Tuple[str, str]] = [
    (r'millilit((er)|(re))s', 'mL'),
    (r' cc' + ORGSYN_UNITS_REGEX_END, r' cc\1\2'),
    (r' ml' + ORGSYN_UNITS_REGEX_END, r' ml\1\2'),
    (r' mL' + ORGSYN_UNITS_REGEX_END, r' mL\1\2'),
    (r' l' + ORGSYN_UNITS_REGEX_END, r' l\1\2'),
    (r' L' + ORGSYN_UNITS_REGEX_END, r' L\1\2'),
]

#: Support units without space before them e.g. '1ml' instead of '1 ml'.
UNIT_PATTERNS: List[Tuple[str, str]] = []
units = '|'.join(list([item for item in WORD_UNIT_DICT if item != 'M']))
UNIT_PATTERNS = [
    (
        r'( |^|\()' + float_regex_pattern + r'(' + units + r')( |$|\.|\,|\))',
        r'\1\2 \3\4'
    ),
]

#: Misc replacements to standardise text.
MISC_REPLACEMENTS: List[Tuple[str, str]] = [
    (r'conc\.', 'concentrated'),
    (r'[ ]aq(\.)?[ ]', r' aqueous '),
    HYPHEN_QUANTITY_REPLACEMENT,
    # If you have '...for 3 h. The mixture was then...' the 'h.' becomes a word,
    # rather than the full stop being interpreted as the end of a sentence.
    # To fix this replace 'h' with 'hours'.
    (float_regex_pattern + r' h\. ', r'\1 hours. '),
    (r'equiv\.', 'equiv'),  # Full stops mess stuff up during tokenizing.
    (r'(^| |\()ca\.( |[0-9])', r'\1\2'),  # '(ca. 3 mL)' -> '(3 mL)'

    (float_regex_pattern + r'[x×X]' + float_regex_pattern, r'\1 x \2'),

    # Specific to OrgSyn
    (' per cent ', ' % '),

    # Journal references. Could tag in future instead of removing
    (r' \(Org. Syn. Coll. Vol. [I]+, [0-9]{4}, [0-9]{1,3}\)', ''),


    # Notes not currently recorded so remove from text, could tag in future
    # instead of removing.
    (r' \(Note [0-9]+\) and \(Note [0-9]+\)', '  '),
    (r'\(Notes [0-9]+, [0-9]+\)', ''),
    (r' \(Note [0-9]+\)', ' '),
    (r'\(Note [0-9]+ and Note [0-9]+\)', ''),

    # Figures not currently recorded so remove from text, could tag in future
    # instead of removing.
    (r' \(Figure [0-9]+[a-zA-Z]?\) and \(Figure [0-9]+[a-zA-Z]?\)', '  '),
    (r'\(Figures [0-9]+[a-zA-Z]?, [0-9]+[a-zA-Z]?\)', ''),
    (r' \(Figure [0-9]+[a-zA-Z]?\)', ' '),
    (r'\(Figure [0-9]+[a-zA-Z]? and Figure [0-9]+[a-zA-Z]?\)', ''),

    # '−70' can't be converted to float so replace '−' with '-'.
    (r' −([0-9]+)', r' -\1'),

    # Needed to make this sentence work as 'then' can't be a modifier continue
    # word, but second modifier group must still be recognised.
    # '''
    # The volatiles are removed by rotatory evaporation (300 mmHg, 30 °C bath
    # temperature) and then, under a higher vacuum (1 mmHg) for 24 h to afford
    # gold(I) chloride complex 3 (0.879 g, quantitative yield) as a white solid
    # (Note 4) (Figure 2).'''
    # '''
    (r' and then, ', 'and, '),
    (r' and then ', ' and '),
    (r' as well as ', ' and '),

    (r'([\( ])mm Hg([ ,\)])', r'\1mmHg\2'),

    (r'--', '-'),
    (r'approx. ', '~'),
    (r' at <', ' below '),
]

#: Simplify vessel phrases as vessels can be determined independently based on
# procedure. They don't need to come from the text.
VESSEL_REPLACEMENTS: List[Tuple[str, str]] = [
    # convert stuff like '500 mL round-bottomed flask' to 'flask'.
    (r'([0-9]+)?[-| ]m[l|L] [a-zA-Z\-]+([ |-][a-zA-Z]+)? flask', ' flask'),

]

#: Replacements to standardise inert atmosphere phrases.
INERT_ATMOSPHERE_REPLACEMENTS: List[Tuple[str, str]] = [
    (
        r'(([n|N]itrogen)|([A|a]rgon)|([I|i]nert)) atmosphere',
        'inert atmosphere'
    ),
    (r'(([n|N]itrogen)|([A|a]rgon)) protection', 'inert atmosphere'),
    (r'nitrogen- purged', 'nitrogen-purged'),
]

#: Replacements to standardise action phrases.
ACTION_REPLACEMENTS: List[Tuple[str, str]] = [
    (r'Purification was by', r'The product was purified by'),
    ('by reflux', 'by heating at reflux'),
    (r' stirs ', r' is stirred '),
]

#: Replacements to standardise text and make NLP tasks downstream easier.
TACTICAL_REPLACEMENTS: List[Tuple[str, str]] = []

# Order is arbitrary
for item in [
    LITERAL_NUMBER_REPLACEMENTS,
    MISC_REPLACEMENTS,
    UNIT_PATTERNS,
    TEMP_REPLACEMENTS,
    MASS_REPLACEMENTS,
    VOLUME_REPLACEMENTS,
    TIME_REPLACEMENTS,
    VESSEL_REPLACEMENTS,
    INERT_ATMOSPHERE_REPLACEMENTS,
    ACTION_REPLACEMENTS,
]:

    TACTICAL_REPLACEMENTS.extend(item)
