from typing import List, Dict

def get_available_languages(localisation: Dict) -> List[str]:
    """Get languages for which every step in human readable can output
    human_readable text in that language. Always return 'en' just so that error
    is not thrown if localisation not implemented on platform.

    Returns:
        List[str]: List of language codes, e.g. ['en', 'zh']
    """
    available_languages = ['en']
    for _, human_readables in localisation.items():
        for language in human_readables:
            if language not in available_languages:
                available_languages.append(language)
    return available_languages

def conditional_human_readable(step, language_human_readable):
    """Convert step and given conditional human readable Dict to human readable
    string.

    Args:
        step (Step): Step to generate human readable for.
        language_human_readable (Dict): Conditional human readable template to
            generate step human readable from.

    Returns:
        str: Human readable sentence describing step.
    """
    # Get overall template str
    template_str = language_human_readable['full']

    # Get formatted properties
    formatted_properties = step.formatted_properties()

    # Resolve conditional template fragments and apply to full
    # template str
    for fragment_identifier, condition_prop_dict\
            in language_human_readable.items():

        # Ignore full template str
        if fragment_identifier != 'full':

            # Match prop conditions
            for condition_prop, condition_val_dict\
                    in condition_prop_dict.items():

                # Get actual val
                condition_actual_val = step.properties[
                    condition_prop]
                condition_actual_val_str =\
                    str(condition_actual_val).lower()

                sub_val = ''

                # Exact match
                if (condition_actual_val_str
                        in condition_val_dict):
                    sub_val = condition_val_dict[
                        condition_actual_val_str]

                # Any match
                elif (condition_actual_val is not None
                        and 'any' in condition_val_dict):
                    sub_val = condition_val_dict['any']

                # Else match
                else:
                    sub_val = condition_val_dict['else']

                # Fragment identifier is not a property, add it
                # to formatted properties.
                if fragment_identifier not in step.properties:
                    formatted_properties[fragment_identifier] =\
                        sub_val

                # Fragment identifier is a property, replace
                # the property in the template_str with the new
                # fragment, so .format is called on the new
                # fragment.
                template_str = template_str.replace(
                    '{' + fragment_identifier + '}', sub_val)

    # Postprocess
    human_readable = template_str.format(**formatted_properties)
    human_readable = postprocess_human_readable(human_readable)
    return human_readable

def postprocess_human_readable(human_readable: str) -> str:
    """Remove whitespace issues created by conditional template system.
    Specifically ' ,', '  ' and ' .'.
    """
    while '  ' in human_readable:
        human_readable = human_readable.replace('  ', ' ')
    human_readable = human_readable.replace(' ,', ',')
    human_readable = human_readable.rstrip('. ')
    human_readable += '.'
    return human_readable
