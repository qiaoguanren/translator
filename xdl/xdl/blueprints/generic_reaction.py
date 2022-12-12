from typing import List
from .base_blueprint import ReactionBlueprint

class GenericReaction(ReactionBlueprint):

    PROP_TYPES = {
        'reactants': List[str],
        'solvent': str,
        'temp': float,
        'time': float,
    }

    def __init__(
        self,
        reactants: List[str],
        solvent: str,
        temp: float,
        time: float,
    ):
        super().__init__(locals())

    def build_prep(self):
        steps, reagents = [], []
        return steps, reagents

    def build_reaction(self):
        steps, reagents = [], []
        return steps, reagents

    def build_workup(self):
        steps, reagents = [], []
        return steps, reagents

    def build_purification(self):
        steps, reagents = [], []
        return steps, reagents
