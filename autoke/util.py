import re


def clean_list(lst):
    """Clean a list by removing empty entries, casting them to strings and lowering the case"""
    lst = list(map(lambda item: str(item).strip().lower(), lst))
    lst = list(filter(lambda item: item, lst))
    return lst


def get_words(string):
    """Split a string into words"""
    words = re.compile("[^a-zA-Z]").split(string)
    return clean_list(words)


def get_sentences(string):
    """Get sentences, by punctuation"""
    sentences = re.compile("[.!?,;:']").split(string)
    return clean_list(sentences)
