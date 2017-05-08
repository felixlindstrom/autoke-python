import re


def clean_list(lst):
    """
    Clean a list by removing empty entries, casting them to strings and lowering the case
    
    Args:
        lst (list): List to clean
        
    Returns:
        A cleaned version on the inputted list
    """
    lst = list(map(lambda item: str(item).strip().lower(), lst))
    lst = list(filter(lambda item: item, lst))
    return lst


def get_words(string):
    """
    Split a string into words
    
    Args:
        string (string): String to split into words
        
    Return:
        list with words
    """
    words = re.compile("[^a-zA-Z]").split(string)
    return clean_list(words)


def get_sentences(string):
    """
    Get sentences, by punctuation
    
    Args:
        string (string): String to split into sentences
        
    Returns:
        list with sentences
    """
    sentences = re.compile("[.!?,;:']").split(string)
    return clean_list(sentences)
