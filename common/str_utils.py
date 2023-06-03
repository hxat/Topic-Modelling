import unicodedata
import re

def replace_all(replacer: dict, value:str):
    """
    Replaces all occurrences of specified substrings in a string with their corresponding replacements.

    Args:
        replacer (dict): a dictionary where keys are the substrings to be replaced and values are their corresponding replacements.
        value (str): the string in which the replacements are to be made.

    Returns:
        str: a new string where all occurrences of the substrings in `replacer` have been replaced with their corresponding replacements.
    """
    for old, new in replacer.items():
        value = value.replace(old, new)
    return value

def normalized(text, blacklist_patterns=None, stopwords=None, folding=None,
               max_words=None, delimiter=' '):
    """
    Simple normalization of the text by folding, convert to lower, remove
    pattern remove stopwords
    """
    def tokenized(text, stopwords=None, folding=None, max_words=None):
        def fold(text):
            s = ''
            for c in unicodedata.normalize('NFD', text):
                if c == 'đ' or c == 'ð':
                    s = s + 'd'
                elif unicodedata.category(c) != 'Mn':
                    s = s + c
            return s

        if text is None:
            return None

        pattern = re.compile(r"\W+", re.UNICODE)
        tokens = []
        if folding:
            text = fold(text)
        for token in pattern.split(text.lower()):
            if token and (not stopwords or token not in stopwords):
                tokens.append(token)
                if max_words and len(tokens) >= max_words:
                    break
        return tokens

    if blacklist_patterns:
        generic_pattern = '(%s)' % '|'.join(blacklist_patterns)
        pattern = re.compile(generic_pattern)
        text = pattern.sub(' ', text)
    tokens = tokenized(text, stopwords=stopwords, folding=folding, max_words=max_words)
    return delimiter.join(tokens).lower()


def remove_pattern(input_txt:str, pattern:str):
    """
    Removes all occurrences of a regular expression pattern from a given input string.

    Args:
        input_txt (str): the input string from which the pattern is to be removed.
        pattern (str): the regular expression pattern to be removed from the input string.

    Returns:
        str: a new string where all occurrences of the regular expression pattern in `input_txt` have been removed.
    """
    r = re.findall(pattern, input_txt)
    for i in r:
        input_txt = re.sub(i, '', input_txt)  
    return input_txt