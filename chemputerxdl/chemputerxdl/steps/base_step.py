"""
.. module:: steps.base_step
    :platforms: Unix, Windows
    :synopsis: Base representation of a Chemputer XDL step

"""

from ..localisation import HUMAN_READABLE_STEPS

class ChemputerStep(object):
    localisation = HUMAN_READABLE_STEPS

    @property
    def buffer_flasks_required(self):
        buffer_flasks_required = 0
        for substep in self.steps:
            buffer_flasks_required += substep.buffer_flasks_required
        return buffer_flasks_required
