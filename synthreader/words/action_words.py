from .words import Word
from .modifiers import TimeModifier

class ActionWord(Word):
    def __init__(self, words):
        self.words = words
        self.modifiers = []

    def process_modifiers(self, modifiers):
        self.modifiers.extend(modifiers)

class EvacuateWord(ActionWord):
    def __init__(self, words):
        super().__init__(words)

class StirWord(ActionWord):
    def __init__(self, words):
        super().__init__(words)

class PlaceWord(ActionWord):
    def __init__(self, words):
        super().__init__(words)

class CombineWord(ActionWord):
    def __init__(self, words):
        super().__init__(words)

class AffordWord(ActionWord):
    def __init__(self, words):
        super().__init__(words)

class CollectWord(ActionWord):
    def __init__(self, words):
        super().__init__(words)

class AddWord(ActionWord):
    def __init__(self, words):
        super().__init__(words)

class RefluxWord(ActionWord):
    def __init__(self, words):
        super().__init__(words)

class DissolveWord(ActionWord):
    def __init__(self, words):
        super().__init__(words)

class ExtractWord(ActionWord):
    def __init__(self, words):
        super().__init__(words)

class EvaporateWord(ActionWord):
    def __init__(self, words):
        super().__init__(words)

class NeutralizeWord(ActionWord):
    def __init__(self, words):
        super().__init__(words)

class WaitWord(ActionWord):
    def __init__(self, words):
        super().__init__(words)

class MixWord(ActionWord):
    def __init__(self, words):
        super().__init__(words)

class CoolWord(ActionWord):
    def __init__(self, words):
        super().__init__(words)

class HeatWord(ActionWord):
    def __init__(self, words):
        super().__init__(words)

class DiluteWord(ActionWord):
    def __init__(self, words):
        super().__init__(words)

class IsolateWord(ActionWord):
    def __init__(self, words):
        super().__init__(words)

class FilterWord(ActionWord):
    def __init__(self, words):
        super().__init__(words)

class WashSolidWord(ActionWord):
    def __init__(self, words):
        super().__init__(words)

class WashWord(ActionWord):
    def __init__(self, words):
        super().__init__(words)

class DryWord(ActionWord):
    def __init__(self, words):
        super().__init__(words)

class PressWord(ActionWord):
    def __init__(self, words):
        super().__init__(words)

class PurifyWord(ActionWord):
    def __init__(self, words):
        super().__init__(words)

class DiscontinueWord(ActionWord):
    def __init__(self, words):
        super().__init__(words)

class RecrystallizeWord(ActionWord):
    def __init__(self, words):
        super().__init__(words)

class RemoveWord(ActionWord):
    def __init__(self, words):
        super().__init__(words)

class ContinueWord(ActionWord):
    def __init__(self, words):
        super().__init__(words)

class AchieveWord(ActionWord):
    def __init__(self, words):
        super().__init__(words)

class ProvideWord(ActionWord):
    def __init__(self, words):
        super().__init__(words)

class SonicateWord(ActionWord):
    def __init__(self, words):
        super().__init__(words)

class RequireWord(ActionWord):
    def __init__(self, words):
        super().__init__(words)

class DistillWord(ActionWord):
    def __init__(self, words):
        super().__init__(words)

class SubjectedWord(ActionWord):
    def __init__(self, words):
        super().__init__(words)

class Action(object):
    def __init__(self, subject, action, words, action_order_pos):
        self.subject = subject
        self.action = action
        if type(self.action) == TimeModifier:
            self.action.modifiers = []
        self.modifiers = action.modifiers
        self.words = words
        self.action_order_pos = action_order_pos
