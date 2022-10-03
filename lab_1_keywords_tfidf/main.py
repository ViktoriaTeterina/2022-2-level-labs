"""
Lab 1
Extract keywords based on frequency related metrics
"""
import math
from typing import Optional, Union, Any
import string
from string import punctuation

def clean_and_tokenize(text: str) -> Optional[list[str]]:
    """
    Removes punctuation, casts to lowercase, splits into tokens

    Parameters:
    text (str): Original text

    Returns:
    list[str]: A sequence of lowercase tokens with no punctuation

    In case of corrupt input arguments, None is returned
    """
    if not isinstance(text, str):
        return None
    text = text.lower().strip()
    punctuation = '''!@#$%^&*()_-+=[]{};:'\|,<.>/?"'''
    for symbol in punctuation:
        if symbol in text:
            text = text.replace(symbol, '')
        else:
            return None
    tokens = text.split()
    return tokens
    pass


def remove_stop_words(tokens: list[str], stop_words: list[str]) -> Optional[list[str]]:
    """
    Excludes stop words from the token sequence

    Parameters:
    tokens (List[str]): Original token sequence
    stop_words (List[str]: Tokens to exclude

    Returns:
    List[str]: Token sequence that does not include stop words

    In case of corrupt input arguments, None is returned
    """
    if not (isinstance(tokens, list) and isinstance(stop_words, list)):
        return None
    stop_words = list()
    for stop_word in stop_words:
        if stop_word in tokens:
            tokens.remove(stop_word)
        else:
            return None
    return tokens


def check(massive, type_name) -> Optional[bool]:
    if not (massive and all(isinstance(el, type_name) for el in massive)):
        return False
    return True
    pass


def calculate_frequencies(tokens: list[str]) -> Optional[dict[str, int]]:
    """
    Composes a frequency dictionary from the token sequence

    Parameters:
    tokens (List[str]): Token sequence to count frequencies for

    Returns:
    Dict: {token: number of occurrences in the token sequence} dictionary

    In case of corrupt input arguments, None is returned
    """
    frequences = {}
    if not (isinstance(tokens, list)):
        return None
    for token in tokens:
        occurance_number = token.count(token)
        frequences[token] = occurance_number
    return frequences
    pass

    def get_top_n(frequencies: dict[str, Union[int, float]], top: int, key_list=list, value_list=list) -> Optional[list[str]]:
        """"
        Extracts a certain number of most frequent tokens

        Parameters:
        frequencies (Dict): A dictionary with tokens and
        its corresponding frequency values
        top (int): Number of token to extract

        Returns:
        List[str]: Sequence of specified length
        consisting of tokens with the largest frequency

        In case of corrupt input arguments, None is returned
        """
        if not (isinstance(frequencies, dict) and top is not int):
            return None
        if check(key_list, str) and check(value_list, int) or check(value_list, float):
            value_list.sort(reserve=True)
            top_list = []

            def tokens(top_list: list[str], frequences: dict[str, Union[int, float]], value_list, float, value):
                for word, number in frequences.items():
                    if word not in top_list and number == value:
                        return word

    def get_list(length: int, value_list=list):
        if not isinstance(length, int) or length is True:
            return None
        for i in range(length):
            token = tokens(top_list, frequences, int(value_list[i]))
            top_list.append(token)
        return top_list
    if len(top_list) != top:
        if top > len(key_list):
            top_list = get_list(len(key_list))
        else:
            top_list = get_list(top)
    return top_list
    pass


def calculate_tf(frequencies: dict[str, int]) -> Optional[dict[str, float]]:
    """
    Calculates Term Frequency score for each word in a token sequence
    based on the raw frequency

    Parameters:
    frequencies (Dict): Raw number of occurrences for each of the tokens

    Returns:
    dict: A dictionary with tokens and corresponding term frequency score

    In case of corrupt input arguments, None is returned
    """
    if not check_dict(frequencies, str, int, False):
        return None
    sum_freq = sum(frequencies.values())
    tf_dict = {word: (frequency / sum_freq) for word, frequency in frequencies.items()}
    return tf_dict


def calculate_tfidf(term_freq: dict[str, float], idf: dict[str, float]) -> Optional[dict[str, float]]:
    """
    Calculates TF-IDF score for each of the tokens
    based on its TF and IDF scores

    Parameters:
    term_freq (Dict): A dictionary with tokens and its corresponding TF values
    idf (Dict): A dictionary with tokens and its corresponding IDF values

    Returns:
    Dict: A dictionary with tokens and its corresponding TF-IDF values

    In case of corrupt input arguments, None is returned
    """
    if not (check_dict(term_freq, str, float, False) and check_dict(idf, str, float, True)):
        return None
    tfidf_dict = {}
    for word in term_freq.keys():
        tfidf_dict[word] = term_freq[word] * idf.get(word, log(47))
    return tfidf_dict


def calculate_expected_frequency(
    doc_freqs: dict[str, int], corpus_freqs: dict[str, int]
) -> Optional[dict[str, float]]:
    """
    Calculates expected frequency for each of the tokens based on its
    Term Frequency score for both target document and general corpus

    Parameters:
    doc_freqs (Dict): A dictionary with tokens and its corresponding number of occurrences in document
    corpus_freqs (Dict): A dictionary with tokens and its corresponding number of occurrences in corpus

    Returns:
    Dict: A dictionary with tokens and its corresponding expected frequency

    In case of corrupt input arguments, None is returned
    """
    if not (check_dict(doc_freqs, str, int, False) and check_dict(corpus_freqs, str, int, True)):
        return None
    dict_exp_freqs = {}
    for word, freq in doc_freqs.items():
        except_word_doc_freq = sum(doc_freqs.values()) - freq
        corpus_freq = corpus_freqs.get(word, 0)
        except_word_corpus_freq = sum(corpus_freqs.values()) - corpus_freq
        dict_exp_freqs[word] = ((freq + corpus_freq) * (freq + except_word_doc_freq)) /\
                                (freq + corpus_freq + except_word_doc_freq + except_word_corpus_freq)
    return dict_exp_freqs


def calculate_chi_values(expected: dict[str, float], observed: dict[str, int]) -> Optional[dict[str, float]]:
    """
    Calculates chi-squared value for the tokens
    based on their expected and observed frequency rates

    Parameters:
    expected (Dict): A dictionary with tokens and
    its corresponding expected frequency
    observed (Dict): A dictionary with tokens and
    its corresponding observed frequency

    Returns:
    Dict: A dictionary with tokens and its corresponding chi-squared value

    In case of corrupt input arguments, None is returned
    """
    if not (check_dict(expected, str, float, False) and check_dict(observed, str, int, False)):
        return None
    chi_dict = {}
    for word, freq in expected.items():
        chi_dict[word] = ((observed.get(word, 0) - freq) ** 2) / freq
    return chi_dict


def extract_significant_words(chi_values: dict[str, float], alpha: float) -> Optional[dict[str, float]]:
    """
    Select those tokens from the token sequence that
    have a chi-squared value greater than the criterion

    Parameters:
    chi_values (Dict): A dictionary with tokens and
    its corresponding chi-squared value
    alpha (float): Level of significance that controls critical value of chi-squared metric

    Returns:
    Dict: A dictionary with significant tokens
    and its corresponding chi-squared value

    In case of corrupt input arguments, None is returned
    """
    criterion = {0.05: 3.842, 0.01: 6.635, 0.001: 10.828}
    if not (check_dict(chi_values, str, float, False) and check_float(alpha)\
            and alpha in criterion.keys()):
        return None
    significant_words_dict = {}
    for word, chi_value in chi_values.items():
        if chi_value > criterion[alpha]:
            significant_words_dict[word] = chi_value
    return significant_words_dict
