
def reduce_string(string: str, max_length: int = 100) -> str:
    """Reduce a string to a specified maximum length, adding ellipsis if truncated.

    Args:
        string (str): The input string to be reduced.
        max_length (int): The maximum allowed length of the output string.

    Returns:
        str: The reduced string, with ellipsis if it was truncated.
    """
    if len(string) <= max_length:
        return string
    truncated = string[:max_length - 3]
    return f"{truncated}..."
