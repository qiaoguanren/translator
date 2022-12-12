import pytest

from synthreader.tagging import tag_synthesis
from synthreader.words import (
    VolumeWord, MassWord, PressureWord, TempWord, ConcWord)
from synthreader.words.modifiers import (
    TimeModifier, TemperatureModifier, PressureModifier)

volume_example = '''
1 mL 1 ml 1 cm3 1 cc 2 millilitres 1 millilitre 2 milliliters 1 milliliter
1 L 1 l 1 litre 1 liter 2 litres 2 liters
1 dL 1 dl 1 decilitre 1 deciliter 2 decilitres 2 deciliters
1 cL 1 cl 1 centilitre 1 centiliter 2 centilitres 2 centiliters
1 uL 1 ul 1 µL 1 µl 1 microliter 1 microlitre 2 microliters 2 microlitres
'''
mass_example = '''
1 kg 1 kilogram 2 kilograms
1 g 1 gram 2 grams
1 ug 1 microgram 2 micrograms
1 mg 1 milligram 2 milligrams
'''
time_example = '''
1 s 1 sec 2 secs 1 second 2 seconds
1 m 1 min 2 mins 1 minute 2 minutes
1 h 1 hr 2 hrs 1 hour 2 hours
'''

temperature_example = '25 °C 298 K 25°C 77 F'
pressure_example = '1.5 bar 1.0 mbar 1 Pa 1 torr 1 atm 1 mmHg'
concentration_example = '1 M'

@pytest.mark.unit
def test_volumes():
    tagged_example = tag_synthesis(volume_example)
    for sentence in tagged_example:
        for word in sentence:
            assert type(word) == VolumeWord

@pytest.mark.unit
def test_masses():
    tagged_example = tag_synthesis(mass_example)
    for sentence in tagged_example:
        for word in sentence:
            assert type(word) == MassWord

@pytest.mark.unit
def test_times():
    tagged_example = tag_synthesis(time_example)
    for sentence in tagged_example:
        for word in sentence:
            assert type(word) == TimeModifier

@pytest.mark.unit
def test_temperatures():
    tagged_example = tag_synthesis(temperature_example)
    for sentence in tagged_example:
        for word in sentence:
            assert type(word) in [TempWord, TemperatureModifier]

@pytest.mark.unit
def test_pressures():
    tagged_example = tag_synthesis(pressure_example)
    for sentence in tagged_example:
        for word in sentence:
            assert type(word) in [PressureWord, PressureModifier]

@pytest.mark.unit
def test_concentrations():
    tagged_example = tag_synthesis(concentration_example)
    for sentence in tagged_example:
        for word in sentence:
            assert type(word) == ConcWord
