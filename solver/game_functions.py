import pandas as pd
import numpy as np

from solver.second_level_functions import ordered_cards_ids, get_multiples, is_flush, \
    is_straight, straight_flush, get_combinations, ordered_flush, add_blocks, is_full_house

# These 2 lists are rules for sorting the combinations
SORTING_RULES = ['is straight flush', 'is four of a kind',
                 'four of a kind rank', 'is full house', 'is flush',
                 'ordered_flush', 'is straight', 'is three of a kind',
                 'three of a kind rank', 'is two pairs', 'top pair rank',
                 'is pair', 'pair rank', 'ordered', 'hand']
ASCENDING = [False, False, True, False, False, True, False, False, True,
             False, True, False, True, True, True]


def texas_holdem_preprocessing(blocks):
    """
    Generates all 21 possible combinations for every player.
    Returns a list of hands and a corresponding list of combinations

    blocks: list-like
        List-like containing the community cards and the cards in players hands
    """
    board = blocks[0]  # community cards
    combinations = []
    hands = []
    for hand in blocks[1:]:
        all_cards = board + hand  # all available cards for current player
        # dataframe with a row of all combinations
        df_combinations = get_combinations(all_cards, 5, 'combination')
        combinations.extend(df_combinations['combination'])
        hands.extend([hand] * 21)  # repeating the hand 21 times so the returned lists correspond
    return hands, combinations


def omaha_holdem_preprocessing(blocks):
    """
    Generates all 60 possible combinations for every player.
    Returns a list of hands and a corresponding list of combinations

    blocks: list-like
        List-like containing the community cards and the cards in players hands
    """
    # dataframe with all possible combinations of 3 from community cards
    df_board_combinations = get_combinations(blocks[0], 3, 'board')
    hands = []
    combinations = []
    for hand in blocks[1:]:
        # dataframe with all possible combinations of 2 from player's cards
        df_hand_combinations = get_combinations(hand, 2, 'hand')
        # preparations to get all the combinations through merging(joining)
        df_hand_combinations = pd.concat([df_hand_combinations] * 10)
        df_hand_combinations['index'] = np.repeat(np.arange(10), 6)
        # getting all the combinations of 3 community cards and 2 players cards
        df_full_combinations = pd.merge(df_hand_combinations, df_board_combinations)
        full_combinations = df_full_combinations['hand'] + df_full_combinations[
            'board']  # concatenating
        hands.extend([hand] * 60)  # repeating the hand 60 times so the returned lists correspond
        combinations.extend(full_combinations)
    return hands, combinations


def five_card_draw(hands, blocks):
    """
    Single game of five card draw.
    Returns a string of hand blocks with non-decreasing strength value

    hands: list-like
        List-like of strings which contain players' cards

    blocks: list-like
        List-like of combinations corresponding to hands
    """
    cards_ids = ordered_cards_ids(blocks)
    pairs, top_pairs, three_of_a_kinds, four_of_a_kinds = get_multiples(cards_ids)
    df = pd.DataFrame()  # think of dataframe as a table in your SQL database
    # filling the dataframe one column at a time
    df['hand'] = hands
    df['ordered'] = cards_ids
    df['ordered'] = df['ordered'].apply(tuple)  # tuples are hashable, used for sorting
    df['pair rank'] = pairs
    # the result of .isna() is a boolean mask. ~ operator inverts it elementwise
    df['is pair'] = ~df['pair rank'].isna()
    df['top pair rank'] = top_pairs
    df['is two pairs'] = ~df['top pair rank'].isna()
    df['three of a kind rank'] = three_of_a_kinds
    df['is three of a kind'] = ~df['three of a kind rank'].isna()
    df['four of a kind rank'] = four_of_a_kinds
    df['is four of a kind'] = ~df['four of a kind rank'].isna()
    df['is flush'] = is_flush(blocks)
    # .apply() applies a function to a dataframe. axis=1 means rowwise application
    df['ordered_flush'] = df.apply(ordered_flush, axis=1)
    df['is full house'] = df.apply(is_full_house, axis=1)
    df['is straight'] = df['ordered'].apply(is_straight)  # elementwise to a single column
    df['is straight flush'] = df.apply(straight_flush, axis=1)

    # sorting the hands by their strength
    # .drop_duplicates('hands') leaves only the strongest combination for each hand
    # only ```hands``` and ```ordered``` columns are required further
    # .reset_index() is used because all the previous actions keep indexing
    blocks = df.sort_values(SORTING_RULES, ascending=ASCENDING).drop_duplicates('hand')[
        ['hand', 'ordered']].reset_index()

    return add_blocks(blocks)
