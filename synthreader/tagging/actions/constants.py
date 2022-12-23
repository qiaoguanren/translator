import copy
from ...words import (
    DryWord,
    FilterWord,
    AddWord,
    StirWord,
    RemoveWord,
    IsolateWord,
    WashWord,
    HeatWord,
    ExtractWord,
    DiluteWord,
    AuxiliaryVerbWord,
    ActionWord,
    WaitWord,
    DistillWord,
    NeutralizeWord,
    EvaporateWord,
    EvacuateWord,
    RequireWord,
    CoolWord,
    PurifyWord,
    MixWord,
    PressWord,
    RefluxWord,
    CombineWord,
    AffordWord,
    SonicateWord,
    DissolveWord,
    RecrystallizeWord,
    ContinueWord,
    AchieveWord,
    CollectWord,
    SubjectedWord,
    PlaceWord,
    ProvideWord,
)
from ...utils import Optional, AnyOf

PAST_ACTION_PATTERNS = [
    (['dried', 'under', 'vacuum'], DryWord),
    (['pressed', 'as', 'dry', 'as', 'possible'], DryWord),
    (['air-dried'], DryWord),
    (['air', 'dried'], DryWord),
    (['pressed', 'dry'], DryWord),
    (['dried'], DryWord),
    (['left', 'to', 'dry'], DryWord),
    (['flame-dried'], DryWord),

    (['washed'], WashWord),

    (['filtered'], FilterWord),
    (['gravity', 'filtered'], FilterWord),
    (['filtered', 'off'], FilterWord),
    (['vacuum-filtered'], FilterWord),
    (['vacuum', 'filtered'], FilterWord),
    (['eluted'], FilterWord),
    (['flushed'], FilterWord),

    (['removed'], RemoveWord),

    (['isolated'], IsolateWord),

    (['mechanically', 'stirred'], StirWord),
    (['stirred'], StirWord),
    (['swirled'], StirWord),
    (['allowed', 'to', 'stir'], StirWord),

    (['added'], AddWord),
    (['treated'], AddWord),
    (['suspended'], AddWord),
    (['loaded'], AddWord),
    (['charged'], AddWord),
    (['repeatedly', 'rinsed'], AddWord),
    (['rinsed'], AddWord),
    (['poured'], AddWord),
    (['transferred'], AddWord),
    (['quenched'], AddWord),
    (['acidified'], AddWord),
    (['syringed'], AddWord),
    (['used'], AddWord),
    (['introduced'], AddWord),
    (['injected'], AddWord),
    (['seeded'], AddWord),

    (['heated'], HeatWord),
    (['reheated'], HeatWord),
    (['warmed', Optional('up')], HeatWord),
    (['reacted'], HeatWord),
    # Immersed in an oil bath
    (['immersed'], HeatWord),
    (['allowed', 'to', 'warm', Optional('up')], HeatWord),

    (['refluxed'], RefluxWord),
    (['boiled'], RefluxWord),

    (['dissolved'], DissolveWord),
    (['redissolved'], DissolveWord),

    (['waited'], WaitWord),
    (['left'], WaitWord),
    (['kept'], WaitWord),
    (['maintained'], WaitWord),
    (['allowed', 'to', 'stand'], WaitWord),

    (['diluted'], DiluteWord),

    (['rotavapped'], EvaporateWord),
    (['evaporated'], EvaporateWord),
    (['evaporated', 'further'], EvaporateWord),

    (['extracted'], ExtractWord),
    (['back', 'extracted'], ExtractWord),
    (['back-extracted'], ExtractWord),
    (['retained'], ExtractWord),
    (['separated'], ExtractWord),
    (['separated', 'and', 'retained'], ExtractWord),
    (['partitioned'], ExtractWord),

    (['neutralised'], NeutralizeWord),
    (['neutralized'], NeutralizeWord),

    (['mixed'], MixWord),

    (['sonicated'], SonicateWord),

    (['cooled', Optional('down')], CoolWord),
    (['chilled'], CoolWord),
    (['allowed', 'to', 'cool'], CoolWord),
    (['recooled'], CoolWord),
    (['refrigerated'], CoolWord),

    (['purified'], PurifyWord),

    (['pressed'], PressWord),

    (['removed', 'under', 'vacuum'], EvaporateWord),
    (['concentrated', 'in', 'vacuo'], EvaporateWord),
    (['concentrated', 'at', 'reduced', 'pressure'], EvaporateWord),
    (['concentrated', 'under', 'reduced', 'pressure'], EvaporateWord),
    (['concentrated'], EvaporateWord),
    (['removed', 'under', 'reduced', 'pressure'], EvaporateWord),

    # Reduced should go to a ReduceWord that becomes an Evaporate or Distill
    # action based on modifiers. For now just going straight to Evaporate is
    # fine.
    (['reduced', 'in', 'volume'], EvaporateWord),

    (['recrystallised'], RecrystallizeWord),
    (['recrystallized'], RecrystallizeWord),

    (['continued'], ContinueWord),

    (['achieved'], AchieveWord),
    (['provided'], ProvideWord),

    (['distilled'], DistillWord),
    (['redistilled'], DistillWord),
    (['vacuum', 'distilled'], DistillWord),
    (['vacuum-distilled'], DistillWord),
    (['fractionally', 'distilled'], DistillWord),
    (['removed', 'by', 'vacuum', 'distillation'], DistillWord),
    (['purified', 'by', 'vacuum', 'distillation'], DistillWord),
    (['obtained', 'by', 'vacuum', 'distillation'], DistillWord),
    (['set', 'up', 'for', 'bulb-to-bulb', 'distillation'], DistillWord),

    (['subjected'], SubjectedWord),

    (['placed'], PlaceWord),

    (['collected'], CollectWord),

    (['afforded'], AffordWord),
    (['furnished'], AffordWord),

    (['evacuated'], EvacuateWord),
    (['evacuated', 'and', 'backfilled'], EvacuateWord),

    (['inserted'], ActionWord),
    (['precipitated'], ActionWord),
    (['shaken'], ActionWord),
    (['replaced'], ActionWord),
    (['decanted'], ActionWord),
    (['attached'], ActionWord),
    (['combined'], CombineWord),
    (['irradiated'], ActionWord),
    (['centrifuged'], ActionWord),
    (['chromatographed'], ActionWord),
    (['resumed'], ActionWord),
    (['analyzed'], ActionWord),
    (['emptied'], ActionWord),
    (['sublimed'], ActionWord),
    (['attained'], ActionWord),
    (['performed'], ActionWord),
    (['broken', 'up'], ActionWord),
    # Needed to make following sentence work.
    # '''A one-necked (B14, diameter: 4.5 cm) 25 mL round-bottomed flask is open
    # to air, equipped with a 3 x 10 mm egg shaped magnetic stirring bar, and
    # charged with tris(2,4-di-tert-butylphenyl)phosphite (1)
    # (0.647 g, 1.00 mmol) and chloro(dimethyl sulfide)gold (2)
    # (0.295 g, 1.00 mmol, 1.0 equiv) (Note 2).
    # '''
    (['open', 'to', 'air'], ActionWord),
]

for pattern in PAST_ACTION_PATTERNS:
    pattern[0].insert(0, Optional(AnyOf(['temporarily'])))

PAST_ACTION_PATTERNS = sorted(
    PAST_ACTION_PATTERNS, key=lambda x: 1 / len(x[0]))

PRESENT_ACTION_PATTERNS = [
    (['drying', 'under', 'vacuum'], DryWord),
    (['pressing', 'as', 'dry', 'as', 'possible'], DryWord),
    (['air-drying'], DryWord),
    (['pressing', 'dry'], DryWord),
    (['drying'], DryWord),
    (['leaving', 'to', 'dry'], DryWord),

    (['washing'], WashWord),

    (['filtering'], FilterWord),
    (['filtration'], FilterWord),
    (['vacuum-filtering'], FilterWord),
    (['vacuum', 'filtration'], FilterWord),

    (['isolating'], IsolateWord),

    (['mechanically', 'stirring'], StirWord),
    (['stirring'], StirWord),
    (['mixing'], StirWord),
    (['shaking'], StirWord),
    (['stirs'], StirWord),

    (['adding'], AddWord),
    ([Optional('the'), 'addition'], AddWord),
    (['treating'], AddWord),
    (['suspending'], AddWord),
    (['loading'], AddWord),
    (['charging'], AddWord),
    (['repeatedly', 'rinsing'], AddWord),
    (['rinsing'], AddWord),
    (['pouring'], AddWord),
    (['placing'], AddWord),
    (['transferring'], AddWord),

    (['heating'], HeatWord),
    (['warming'], HeatWord),
    (['submerged'], HeatWord),

    (['refluxing'], RefluxWord),

    (['dissolving'], DissolveWord),

    (['waiting'], WaitWord),
    (['leaving'], WaitWord),
    (['keeping'], WaitWord),
    (['storing'], WaitWord),

    (['diluting'], DiluteWord),

    (['rotavapping'], EvaporateWord),
    (['evaporating'], EvaporateWord),
    (['evaporation', 'of', 'volatiles', 'under', 'reduced', 'pressure'],
     EvaporateWord),
    (['evaporation', 'under', 'reduced', 'pressure'], EvaporateWord),
    (['evaporation'], EvaporateWord),
    (['removing'], RemoveWord),

    (['extracting'], ExtractWord),

    (['neutralising'], NeutralizeWord),
    (['neutralizing'], NeutralizeWord),

    (['mixing'], MixWord),

    (['cooling'], CoolWord),
    (['allowing'], CoolWord),
    (['allowing', 'to', 'cool'], CoolWord),

    (['purifying'], PurifyWord),
    (['purification'], PurifyWord),

    (['pressing'], PressWord),

    (['removing', 'under', 'vacuum'], EvaporateWord),

    (['requires'], RequireWord),

    (['redistilling'], DistillWord),

    (['separates'], ActionWord),

]
PRESENT_ACTION_PATTERNS = sorted(
    PRESENT_ACTION_PATTERNS, key=lambda x: 1 / len(x[0]))

DISCONTINUE_ACTION_PATTERN_STUBS = [
    [ActionWord, AuxiliaryVerbWord],
    [ActionWord, 'and', ActionWord, AuxiliaryVerbWord],
    [ActionWord, ',', 'and', ActionWord, AuxiliaryVerbWord],
    [ActionWord, ',', ActionWord, 'and', ActionWord, AuxiliaryVerbWord],
    [ActionWord, ',', ActionWord, ',', 'and', ActionWord, AuxiliaryVerbWord],
]

DISCONTINUE_ACTION_WORDS = ['discontinued', 'stopped', 'ceased']

DISCONTINUE_ACTION_PATTERNS = []
for stub in DISCONTINUE_ACTION_PATTERN_STUBS:
    # Assume incorrect grammar 'Stirring were discontinued' won't be
    # encountered.
    for discontinue_word in DISCONTINUE_ACTION_WORDS:
        new_pattern = copy.deepcopy(stub)
        new_pattern.append(discontinue_word)
        DISCONTINUE_ACTION_PATTERNS.append(new_pattern)

DISCONTINUE_ACTION_PATTERNS = sorted(
    DISCONTINUE_ACTION_PATTERNS, key=lambda x: 1 / len(x))
