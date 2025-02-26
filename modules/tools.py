import re


def model_answer_regex(response, field_name):
    regex = (
        rf'"{field_name}"'  # "field"
        r"\s*:\s*"  # : (with optional spaces)
        r'"'  # opening "
        r'([^"]*)'  # any characters except "
        r'(?:"|$)'  # ending " or end of string
    )
    match = re.search(regex, response, re.VERBOSE)
    if match:
        return match.group(1)
    return None


def convert_list_to_string(results, columns):
    """Convert list of tuples to string with column names"""
    results_str = f"COLUMNS:{','.join(columns)}\n"
    for row in results:
        results_str += str(row) + "\n"
    return results_str
