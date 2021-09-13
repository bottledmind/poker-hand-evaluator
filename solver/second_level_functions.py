from textwrap import wrap
import itertools
import pandas as pd
import numpy as np


CARDS_ORDER = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']


def ordered_flush(row):
    """
    Returns ```ordered``` if ```is flush``` is True, False otherwise

    row: Pandas Series
        A row from a dataframe
    """
    if row['is flush']:
        return row['ordered']
    return np.nan


def ordered_cards_ids(hand_blocks):
    """
    Returns a list of lists of ordered card ranks

    hand_blocks: list-like
        List-like of strings containing card blocks
    """
    out = []
    for block in hand_blocks:
        ranks = list(block[::2])  # ranks only
        # getting the ids from CARDS_ORDER and sorting
        ranks_idx = sorted([CARDS_ORDER.index(i) for i in ranks])
        # hardcode check for lowest straight
        if ranks_idx == [0, 9, 10, 11, 12]:
            ranks_idx = [9, 10, 11, 12, 13]
        out.append(ranks_idx)
    return out


def is_full_house(row):
    """
    row: Pandas Series
        A row from a dataframe
    """
    return row['is three of a kind'] and row['is pair']


def is_flush(hand_block):
    """
    Returns a list of booleans.
    Each element of the list is True if a corresponding card block is a flush and False otherwise

    hand_blocks: list-like
        List-like of strings containing card blocks
    """
    out = []
    for block in hand_block:
        suits = list(block[1::2])  # only suits
        suit_counts = pd.Series(suits).value_counts()
        flag = 5 in suit_counts.values  # is there a suit occurring 5 times
        out.append(flag)
    return out


def straight_flush(row):
    """
    row: Pandas Series
        A row from a dataframe
    """
    return row['is straight'] and row['is flush']


def is_straight(cards_ids):
    """
    Returns True if cards_ids form a straight

    cards_ids: list-like
        List-like of list-likes of ordered card ranks
    """
    sequence = np.array(cards_ids)
    # True if all the differences between adjacent are 1
    return (sequence[1:] - sequence[:-1]).tolist() == [1, 1, 1, 1]


def get_multiples(cards_ids):
    """
    Returns lists of multiples(pairs, three-of-a-kinds, four-of-a-kinds)

    cards_ids: list-like
        List-like of list-likes of ordered card ranks

    """
    pairs = []
    top_pairs = []
    three_of_a_kinds = []
    four_of_a_kinds = []
    for block in cards_ids:
        # Out of .value_count() is a Series that has unique values as index and their counts as values
        counts = pd.Series(block).value_counts()

        top_pair, pair = get_pairs(counts)
        top_pairs.append(top_pair)
        pairs.append(pair)

        three_of_a_kinds.append(get_three_of_a_kind(counts))

        four_of_a_kinds.append(get_four_of_a_kind(counts))
    return pairs, top_pairs, three_of_a_kinds, four_of_a_kinds


def get_pairs(counts):
    """
    Returns ranks of cards forming pairs
    Returns first NaN if there's only one pair and two NaN if no pairs at all

    counts: Pandas Series
        Result of .value_counts()
    """
    pairs_temp = list(counts[counts == 2].index)  # only ranks of cards forming pairs
    if len(pairs_temp) == 2:  # if there are 2 pairs in the block
        top_pair = min(pairs_temp)  # top pair for two pairs combination
        pair = max(pairs_temp)  # lower pair for two pairs combination
    elif len(pairs_temp) == 1:
        top_pair = np.nan
        pair = max(pairs_temp)  # rank of a single pair
    else:
        top_pair = np.nan
        pair = np.nan
    return top_pair, pair


def get_three_of_a_kind(counts):
    """
    Returns the rank of cards forming a three-of-a-kind or NaN if there's no such combination

    counts: Pandas Series
        Result of .value_counts()
    """
    three_of_a_kinds = list(counts[counts == 3].index)
    if len(three_of_a_kinds)!=0:
        return three_of_a_kinds[0]
    else:
        return np.nan


def get_four_of_a_kind(counts):
    """
    Returns the rank of cards forming a four-of-a-kind or NaN if there's no such combination

    counts: Pandas Series
        Result of .value_counts()
    """
    four_of_a_kinds = list(counts[counts == 4].index)
    if len(four_of_a_kinds)!=0:
        return four_of_a_kinds[0]
    else:
        return np.nan


def add_blocks(blocks):
    """
    Returns card blocks in non-descending order of their strength

    blocks: Pandas DataFrame
        Only ```hand``` and ```ordered``` columns
    """
    result_str = blocks['hand'][0]
    for ordered_previous, ordered_current, block_current in zip(
            blocks['ordered'][:-1],
            blocks['ordered'][1:],
            blocks['hand'][1:],
    ):
        if ordered_previous == ordered_current:  # ranks coincide
            result_str += '=' + block_current
        else:
            result_str += ' ' + block_current
    # Reversing into non-descending order
    result_str = result_str.split()
    result_str.reverse()
    return ' '.join(result_str)


def get_combinations(card_blocks, n, name):
    """
    Returns a dataframe with combinations of n cards from card_blocks

    card_blocks: str
        String of card blocks

    n: int
        Number of cards in a combination

    name:
        Name of the row containing combinations(for the sake of pure readability)

    """
    cards = wrap(card_blocks, 2)  # split string into cards
    # generating and joining each combination
    card_combinations = pd.Series(
        itertools.combinations(cards, r=n)).apply(lambda x: "".join(x))
    df_card_combinations = card_combinations.reset_index().rename({0: name}, axis=1)
    return df_card_combinations
