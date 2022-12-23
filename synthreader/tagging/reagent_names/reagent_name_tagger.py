from typing import List
from .probabilistic_search import naive_bayes_reagent_name_tag
from .reagent_name_fragments import reagent_name_fragment_tag
from .database_search import database_reagent_name_tag
from .rule_search import rule_reagent_name_tag
from ...words import Word, ReagentNameWord, NumberWord
from ...utils import apply_pattern

def reagent_name_tag(sentences: List[List[Word]]) -> List[List[Word]]:
    """Search for reagent names in sentences and convert words to
    ReagentNameWord objects.

    Procedure:
         1) Candidate phrases generated and searched for in a database of known
            reagent names, longest first to avoid problems with names that are
            part of other names.
         2) Database hits are combined into ReagentNameWords. Here the words
            before and after the reagent name can also be included if they are
            recognised as common prefixes or suffixes to a reagent name.
         3) Naive Bayes classifier used to predict if remaining candidate
            phrases are reagent names. Again prefixes and suffixes can be added
            to reagent names after classification.

    Args:
        sentences (List[List[Word]]): Sentences to look for reagent names in.

    Returns:
        List[List[Word]]: Sentences with words combined into ReagentNameWords.
    """
    reagent_name_fragment_tag(sentences)
    database_reagent_name_tag(sentences)
    naive_bayes_reagent_name_tag(sentences)
    rule_reagent_name_tag(sentences)
    apply_pattern(['compound', NumberWord], ReagentNameWord, sentences)
    apply_pattern([ReagentNameWord, ReagentNameWord],
                  ReagentNameWord, sentences)
    apply_pattern(['more', ReagentNameWord], ReagentNameWord, sentences)
    return sentences
