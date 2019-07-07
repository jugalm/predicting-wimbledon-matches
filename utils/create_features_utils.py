from datetime import datetime
from datetime import timedelta


def get_player_1_name(winner_name, winner_rank, loser_name, loser_rank):
    """
    :param winner_name: Name of winner
    :param winner_rank: Rank of the winner
    :param loser_name: Name of loser
    :param loser_rank: Rank of the loser
    :return: name of higher ranked player
    """
    if winner_rank < loser_rank:
        return winner_name
    else:
        return loser_name

def get_player_1_rank(winner_rank, loser_rank):
    """
    :param winner_rank: Rank of the winner
    :param loser_rank: Rank of the loser
    :return: rank of higher ranked player
    """
    if winner_rank < loser_rank:
        return winner_rank
    else:
        return loser_rank

def get_player_2_name(winner_name, winner_rank, loser_name, loser_rank):
    """
    :param winner_name: Name of winner
    :param winner_rank: Rank of the winner
    :param loser_name: Name of loser
    :param loser_rank: Rank of the loser
    :return: name of lower ranked player
    """
    if winner_rank > loser_rank:
        return winner_name
    else:
        return loser_name

def get_player_2_rank(winner_rank, loser_rank):
    """
    :param winner_rank: Rank of the winner
    :param loser_rank: Rank of the loser
    :return: rank of lower ranked player
    """
    if winner_rank > loser_rank:
        return winner_rank
    else:
        return loser_rank

def outcome(winner_rank, loser_rank):
    """
    Returns 0 if higher ranked player won and 0 otherwise
    :param winner_rank: Rank of the winner
    :param loser_rank: Rank of the loser
    :return: Odds of the Higher ranked player
    """
    if winner_rank< loser_rank:
        return 0
    else:
        return 1

def get_player_1_odd(winner_odd, winner_rank, loser_odd, loser_rank):
    """
    Returns the odds of Higher ranked player
    :param winner_odd: Odds of the winner
    :param winner_rank: Rank of the winner
    :param loser_odd: Odds of the Loser
    :param loser_rank: Rank of the Loser
    :return: Odds of the Higher ranked player
    """
    if winner_rank < loser_rank:
        return winner_odd
    else:
        return loser_odd

def get_player_2_odd(winner_odd, winner_rank, loser_odd, loser_rank):
    """
    Returns the odds of Lower ranked player
    :param winner_odd:
    :param winner_rank:
    :param loser_odd:
    :param loser_rank:
    :return:
    """
    if winner_rank > loser_rank:
        return winner_odd
    else:
        return loser_odd


def subtract_days(date_string, num_days):
    """
    Subtract n days from a specified date
    :param date_string: pass date in format '%Y/%m/%d'
    :param num_days: Number of days to be subtracting from the date
    :return: date in format '%Y/%m/%d'
    """
    date_temp = (datetime.strptime(date_string, '%Y/%m/%d') - timedelta(days=num_days))
    return date_temp.strftime("%Y/%m/%d")


def winning_percentage(player_id, data,  type1='matches', current_date=None, surface='All', last_n_weeks=0):
    """
    Caculate different player stats
    :param player_id: Name or ID of Player
    :param data: The raw dataframe from http://www.tennis-data.co.uk/alldata.php
    :param type1: Options: ['matches', 'total_matches', 'games', 'matches_5_sets', 'win_or_close_sets']
    :param current_date: Date of match
    :param surface: Surface options: ['All', 'Grass', 'Hard', 'Clay']
    :param last_n_weeks: Get stats from the past n weeks
    :return: Returns the players Stat for the specified parameters.
    """
    data = data[data['Date'] < current_date]

    if surface!='All':
        data = data[data['Surface'] == surface]

    if last_n_weeks>0:
        last_date = subtract_days(current_date, (last_n_weeks * 7))
        data = data[data['Date'] >= last_date]

    if type1 == 'matches':
        wins = (data['Winner'] == player_id).sum()
        loses = (data['Loser'] == player_id).sum()

    elif type1 == 'total_matches':
        return (data['Winner'] == player_id).sum() + (data['Loser'] == player_id).sum()


    elif type1 == 'matches_5_sets':
        wins = ((data['Winner'] == player_id) & (data['best_of_5'] == 1)).sum()
        loses = ((data['Loser'] == player_id) & (data['best_of_5'] == 1)).sum()


    elif type1 == 'games':
        winner_set_list = ['W1', 'W2', 'W3', 'W4', 'W5']
        loser_set_list = ['L1', 'L2', 'L3', 'L4', 'L5']

        wins = data[data['Winner'] == player_id][winner_set_list].values.sum() + data[data['Loser'] == player_id][loser_set_list].values.sum()
        loses = data[data['Loser'] == player_id][winner_set_list].values.sum() + data[data['Winner'] == player_id][loser_set_list].values.sum()


    elif type1 == 'win_or_close_sets':

        wins = 0
        loses = 0

        data_3_set = data[data['best_of_5'] == 0]
        data_5_set = data[data['best_of_5'] == 1]

        for i in range(1, 4):
            wins = wins + ((data_3_set['Winner'] == player_id) & (data_3_set[('W' + str(i))] >= 5)).sum()
            wins = wins + ((data_3_set['Loser'] == player_id) & (data_3_set[('L' + str(i))] >= 5)).sum()
            loses = loses + ((data_3_set['Winner'] == player_id) & (data_3_set[('W' + str(i))] < 5)).sum()
            loses = loses + ((data_3_set['Loser'] == player_id) & (data_3_set[('L' + str(i))] < 5)).sum()

        for i in range(1, 6):
            wins = wins + ((data_5_set['Winner'] == player_id) & (data_5_set[('W' + str(i))] >= 5)).sum()
            wins = wins + ((data_5_set['Loser'] == player_id) & (data_5_set[('L' + str(i))] >= 5)).sum()
            loses = loses + ((data_5_set['Winner'] == player_id) & (data_5_set[('W' + str(i))] < 5)).sum()
            loses = loses + ((data_5_set['Loser'] == player_id) & (data_5_set[('L' + str(i))] < 5)).sum()

    total = wins + loses

    if total <2:
        win_percent = 0

    else:
        win_percent = wins / total
    return win_percent


def winning_percent_hh(player_name, opponent_name, data, type1='matches', current_date=None, surface='All', last_n_weeks=0):
    """
    :param player_name: Name of player
    :param opponent_name: Name of opponent
    :param data: The raw dataframe from http://www.tennis-data.co.uk/alldata.php
    :param type1: Options: ['matches', 'games', ]
    :param current_date: Date of the match
    :param surface: Surface options: ['All', 'Grass', 'Hard', 'Clay']
    :param last_n_weeks: Get stats from the past n weeks
    :return: Returns the players Head to Head Stat.
    """
    data = data[data['Date'] < current_date]

    if surface!='All':
        data = data[data['Surface'] == surface]

    if last_n_weeks>0:
        last_date = subtract_days(current_date, (last_n_weeks * 7))
        data = data[data['Date'] >= last_date]

    if type1 == 'matches':
        wins = ((data['Winner'] == player_name) & (data['Loser'] == opponent_name)).sum()
        loses = ((data['Winner'] == opponent_name) & (data['Loser'] == player_name)).sum()

    elif type1 == 'games':
        winner_set_list = ['W1', 'W2', 'W3', 'W4', 'W5']
        loser_set_list = ['L1', 'L2', 'L3', 'L4', 'L5']

        wins = data[(data['Winner'] == player_name) & (data['Loser'] == opponent_name)][winner_set_list].values.sum() + \
               data[(data['Winner'] == opponent_name) & (data['Loser'] == player_name)][loser_set_list].values.sum()

        loses = data[(data['Winner'] == opponent_name) & (data['Loser'] == player_name)][winner_set_list].values.sum() + \
                data[(data['Winner'] == player_name) & (data['Loser'] == opponent_name)][loser_set_list].values.sum()

    total = wins + loses

    if total == 0:
        win_percent = 0

    else:
        win_percent = wins / total
    return win_percent

def create_features(df_combined, df):
    """
    :param df_combined: All matched with player_0 as higher ranked player
    :param df: The raw dataframe from http://www.tennis-data.co.uk/alldata.php
    :return: A data_frame with player features for each match
    """

    # **************************************
    # Player Career Stats All Surface
    # **************************************
    print('Creating Player Career Stats All Surface')

    df_combined.loc[:, 'player_0_match_win_percent'] = df_combined.apply(
        lambda row: winning_percentage(row['player_0'], df, type1='matches', current_date=row['Date'], last_n_weeks=0),
        axis=1)
    df_combined.loc[:, 'player_1_match_win_percent'] = df_combined.apply(
        lambda row: winning_percentage(row['player_1'], df, type1='matches', current_date=row['Date'], last_n_weeks=0),
        axis=1)

    df_combined.loc[:, 'player_0_games_win_percent'] = df_combined.apply(
        lambda row: winning_percentage(row['player_0'], df, type1='games', current_date=row['Date'], last_n_weeks=0),
        axis=1)
    df_combined.loc[:, 'player_1_games_win_percent'] = df_combined.apply(
        lambda row: winning_percentage(row['player_1'], df, type1='games', current_date=row['Date'], last_n_weeks=0),
        axis=1)

    df_combined.loc[:, 'player_0_5_set_match_win_percent'] = df_combined.apply(
        lambda row: winning_percentage(row['player_0'], df, type1='matches_5_sets', current_date=row['Date'],
                                       last_n_weeks=0), axis=1)
    df_combined.loc[:, 'player_1_5_set_match_win_percent'] = df_combined.apply(
        lambda row: winning_percentage(row['player_1'], df, type1='matches_5_sets', current_date=row['Date'],
                                       last_n_weeks=0), axis=1)

    df_combined.loc[:, 'player_0_close_sets_percent'] = df_combined.apply(
        lambda row: winning_percentage(row['player_0'], df, type1='win_or_close_sets', current_date=row['Date'],
                                       last_n_weeks=0), axis=1)
    df_combined.loc[:, 'player_1_close_sets_percent'] = df_combined.apply(
        lambda row: winning_percentage(row['player_1'], df, type1='win_or_close_sets', current_date=row['Date'],
                                       last_n_weeks=0), axis=1)

    # **************************************
    # Player Career Stats on Grass/Clay/Hard
    # **************************************

    print('Creating Player Career Stats on Grass/Clay/Hard')

    df_combined.loc[:, 'player_0_match_win_percent_grass'] = df_combined.apply(
        lambda row: winning_percentage(row['player_0'], df, type1='matches', current_date=row['Date'],
                                       surface=row['Surface'], last_n_weeks=0), axis=1)
    df_combined.loc[:, 'player_1_match_win_percent_grass'] = df_combined.apply(
        lambda row: winning_percentage(row['player_1'], df, type1='matches', current_date=row['Date'],
                                       surface=row['Surface'], last_n_weeks=0), axis=1)

    df_combined.loc[:, 'player_0_games_win_percent_grass'] = df_combined.apply(
        lambda row: winning_percentage(row['player_0'], df, type1='games', current_date=row['Date'],
                                       surface=row['Surface'], last_n_weeks=0), axis=1)
    df_combined.loc[:, 'player_1_games_win_percent_grass'] = df_combined.apply(
        lambda row: winning_percentage(row['player_1'], df, type1='games', current_date=row['Date'],
                                       surface=row['Surface'], last_n_weeks=0), axis=1)

    df_combined.loc[:, 'player_0_5_set_match_win_percent_grass'] = df_combined.apply(
        lambda row: winning_percentage(row['player_0'], df, type1='matches_5_sets', current_date=row['Date'],
                                       surface=row['Surface'], last_n_weeks=0), axis=1)
    df_combined.loc[:, 'player_1_5_set_match_win_percent_grass'] = df_combined.apply(
        lambda row: winning_percentage(row['player_1'], df, type1='matches_5_sets', current_date=row['Date'],
                                       surface=row['Surface'], last_n_weeks=0), axis=1)

    df_combined.loc[:, 'player_0_close_sets_percent_grass'] = df_combined.apply(
        lambda row: winning_percentage(row['player_0'], df, type1='win_or_close_sets', current_date=row['Date'],
                                       surface=row['Surface'], last_n_weeks=0), axis=1)
    df_combined.loc[:, 'player_1_close_sets_percent_grass'] = df_combined.apply(
        lambda row: winning_percentage(row['player_1'], df, type1='win_or_close_sets', current_date=row['Date'],
                                       surface=row['Surface'], last_n_weeks=0), axis=1)

    # **************************************
    # Player Career Stats All Surface Last 52 Weeks
    # **************************************

    print('Creating Player Career Stats All Surface Last 52 Weeks')

    df_combined.loc[:, 'player_0_match_win_percent_52'] = df_combined.apply(
        lambda row: winning_percentage(row['player_0'], df, type1='matches', current_date=row['Date'], last_n_weeks=52),
        axis=1)
    df_combined.loc[:, 'player_1_match_win_percent_52'] = df_combined.apply(
        lambda row: winning_percentage(row['player_1'], df, type1='matches', current_date=row['Date'], last_n_weeks=52),
        axis=1)

    df_combined.loc[:, 'player_0_games_win_percent_52'] = df_combined.apply(
        lambda row: winning_percentage(row['player_0'], df, type1='games', current_date=row['Date'], last_n_weeks=52),
        axis=1)
    df_combined.loc[:, 'player_1_games_win_percent_52'] = df_combined.apply(
        lambda row: winning_percentage(row['player_1'], df, type1='games', current_date=row['Date'], last_n_weeks=52),
        axis=1)

    df_combined.loc[:, 'player_0_5_set_match_win_percent_52'] = df_combined.apply(
        lambda row: winning_percentage(row['player_0'], df, type1='matches_5_sets', current_date=row['Date'],
                                       last_n_weeks=52), axis=1)
    df_combined.loc[:, 'player_1_5_set_match_win_percent_52'] = df_combined.apply(
        lambda row: winning_percentage(row['player_1'], df, type1='matches_5_sets', current_date=row['Date'],
                                       last_n_weeks=52), axis=1)

    df_combined.loc[:, 'player_0_close_sets_percent_52'] = df_combined.apply(
        lambda row: winning_percentage(row['player_0'], df, type1='win_or_close_sets', current_date=row['Date'],
                                       last_n_weeks=52), axis=1)
    df_combined.loc[:, 'player_1_close_sets_percent_52'] = df_combined.apply(
        lambda row: winning_percentage(row['player_1'], df, type1='win_or_close_sets', current_date=row['Date'],
                                       last_n_weeks=52), axis=1)

    # **************************************
    # Player Career Stats on Grass/Clay/Hard Last 60 Weeks
    # **************************************

    print('Creating Player Career Stats on Grass/Clay/Hard Last 60 Weeks')

    df_combined.loc[:, 'player_0_match_win_percent_grass_60'] = df_combined.apply(
        lambda row: winning_percentage(row['player_0'], df, type1='matches', current_date=row['Date'],
                                       surface=row['Surface'], last_n_weeks=60), axis=1)
    df_combined.loc[:, 'player_1_match_win_percent_grass_60'] = df_combined.apply(
        lambda row: winning_percentage(row['player_1'], df, type1='matches', current_date=row['Date'],
                                       surface=row['Surface'], last_n_weeks=60), axis=1)

    df_combined.loc[:, 'player_0_games_win_percent_grass_60'] = df_combined.apply(
        lambda row: winning_percentage(row['player_0'], df, type1='games', current_date=row['Date'],
                                       surface=row['Surface'], last_n_weeks=60), axis=1)
    df_combined.loc[:, 'player_1_games_win_percent_grass_60'] = df_combined.apply(
        lambda row: winning_percentage(row['player_1'], df, type1='games', current_date=row['Date'],
                                       surface=row['Surface'], last_n_weeks=60), axis=1)

    df_combined.loc[:, 'player_0_5_set_match_win_percent_grass_60'] = df_combined.apply(
        lambda row: winning_percentage(row['player_0'], df, type1='matches_5_sets', current_date=row['Date'],
                                       surface=row['Surface'], last_n_weeks=60), axis=1)
    df_combined.loc[:, 'player_1_5_set_match_win_percent_grass_60'] = df_combined.apply(
        lambda row: winning_percentage(row['player_1'], df, type1='matches_5_sets', current_date=row['Date'],
                                       surface=row['Surface'], last_n_weeks=60), axis=1)

    df_combined.loc[:, 'player_0_close_sets_percent_grass_60'] = df_combined.apply(
        lambda row: winning_percentage(row['player_0'], df, type1='win_or_close_sets', current_date=row['Date'],
                                       surface=row['Surface'], last_n_weeks=60), axis=1)
    df_combined.loc[:, 'player_1_close_sets_percent_grass_60'] = df_combined.apply(
        lambda row: winning_percentage(row['player_1'], df, type1='win_or_close_sets', current_date=row['Date'],
                                       surface=row['Surface'], last_n_weeks=60), axis=1)

    # **************************************
    # Player Head to Head Career Stats All Surface
    # **************************************

    print('Creating Player Head to Head Career Stats All Surface')

    df_combined.loc[:, 'player_0_match_win_percent_hh'] = df_combined.apply(
        lambda row: winning_percent_hh(row['player_0'], row['player_1'], df, type1='matches', current_date=row['Date'],
                                       last_n_weeks=0), axis=1)
    df_combined.loc[:, 'player_1_match_win_percent_hh'] = df_combined.apply(
        lambda row: winning_percent_hh(row['player_1'], row['player_0'], df, type1='matches', current_date=row['Date'],
                                       last_n_weeks=0), axis=1)

    df_combined.loc[:, 'player_0_games_win_percent_hh'] = df_combined.apply(
        lambda row: winning_percent_hh(row['player_0'], row['player_1'], df, type1='games', current_date=row['Date'],
                                       last_n_weeks=0), axis=1)
    df_combined.loc[:, 'player_1_games_win_percent_hh'] = df_combined.apply(
        lambda row: winning_percent_hh(row['player_1'], row['player_0'], df, type1='games', current_date=row['Date'],
                                       last_n_weeks=0), axis=1)

    # **************************************
    # Player Head to Head Career Stats On Grass
    # **************************************

    print('Creating Player Head to Head Career Stats On Grass')

    df_combined.loc[:, 'player_0_match_win_percent_grass_hh'] = df_combined.apply(
        lambda row: winning_percent_hh(row['player_0'], row['player_1'], df, type1='matches', current_date=row['Date'],
                                       last_n_weeks=0), axis=1)
    df_combined.loc[:, 'player_1_match_win_percent_grass_hh'] = df_combined.apply(
        lambda row: winning_percent_hh(row['player_1'], row['player_0'], df, type1='matches', current_date=row['Date'],
                                       last_n_weeks=0), axis=1)

    df_combined.loc[:, 'player_0_games_win_percent_grass_hh'] = df_combined.apply(
        lambda row: winning_percent_hh(row['player_0'], row['player_1'], df, type1='games', current_date=row['Date'],
                                       last_n_weeks=0), axis=1)
    df_combined.loc[:, 'player_1_games_win_percent_grass_hh'] = df_combined.apply(
        lambda row: winning_percent_hh(row['player_1'], row['player_0'], df, type1='games', current_date=row['Date'],
                                       last_n_weeks=0), axis=1)

    # **************************************
    # Difference variables
    # **************************************

    print('Creating Difference Variables')

    df_combined.loc[:, 'diff_match_win_percent'] = df_combined['player_0_match_win_percent'] - df_combined[
        'player_1_match_win_percent']
    df_combined.loc[:, 'diff_games_win_percent'] = df_combined['player_0_games_win_percent'] - df_combined[
        'player_1_games_win_percent']
    df_combined.loc[:, 'diff_5_set_match_win_percent'] = df_combined['player_0_5_set_match_win_percent'] - df_combined[
        'player_1_5_set_match_win_percent']
    df_combined.loc[:, 'diff_close_sets_percent'] = df_combined['player_0_close_sets_percent'] - df_combined[
        'player_1_close_sets_percent']

    df_combined.loc[:, 'diff_match_win_percent_grass'] = df_combined['player_0_match_win_percent_grass'] - df_combined[
        'player_1_match_win_percent_grass']
    df_combined.loc[:, 'diff_games_win_percent_grass'] = df_combined['player_0_games_win_percent_grass'] - df_combined[
        'player_1_games_win_percent_grass']
    df_combined.loc[:, 'diff_5_set_match_win_percent_grass'] = df_combined['player_0_5_set_match_win_percent_grass'] - \
                                                               df_combined['player_1_5_set_match_win_percent_grass']
    df_combined.loc[:, 'diff_close_sets_percent_grass'] = df_combined['player_0_close_sets_percent_grass'] - \
                                                          df_combined['player_1_close_sets_percent_grass']

    df_combined.loc[:, 'diff_match_win_percent_52'] = df_combined['player_0_match_win_percent_52'] - df_combined[
        'player_1_match_win_percent_52']
    df_combined.loc[:, 'diff_games_win_percent_52'] = df_combined['player_0_games_win_percent_52'] - df_combined[
        'player_1_games_win_percent_52']
    df_combined.loc[:, 'diff_5_set_match_win_percent_52'] = df_combined['player_0_5_set_match_win_percent_52'] - \
                                                            df_combined['player_1_5_set_match_win_percent_52']
    df_combined.loc[:, 'diff_close_sets_percent_52'] = df_combined['player_0_close_sets_percent_52'] - df_combined[
        'player_1_close_sets_percent_52']

    df_combined.loc[:, 'diff_match_win_percent_grass_60'] = df_combined['player_0_match_win_percent_grass_60'] - \
                                                            df_combined['player_1_match_win_percent_grass_60']
    df_combined.loc[:, 'diff_games_win_percent_grass_60'] = df_combined['player_0_games_win_percent_grass_60'] - \
                                                            df_combined['player_1_games_win_percent_grass_60']
    df_combined.loc[:, 'diff_5_set_match_win_percent_grass_60'] = df_combined[
                                                                      'player_0_5_set_match_win_percent_grass_60'] - \
                                                                  df_combined[
                                                                      'player_1_5_set_match_win_percent_grass_60']
    df_combined.loc[:, 'diff_close_sets_percent_grass_60'] = df_combined['player_0_close_sets_percent_grass_60'] - \
                                                             df_combined['player_1_close_sets_percent_grass_60']

    df_combined.loc[:, 'diff_match_win_percent_hh'] = df_combined['player_0_match_win_percent_hh'] - df_combined[
        'player_1_match_win_percent_hh']
    df_combined.loc[:, 'diff_games_win_percent_hh'] = df_combined['player_0_games_win_percent_hh'] - df_combined[
        'player_1_games_win_percent_hh']

    df_combined.loc[:, 'diff_match_win_percent_grass_hh'] = df_combined['player_0_match_win_percent_grass_hh'] - \
                                                            df_combined['player_1_match_win_percent_grass_hh']
    df_combined.loc[:, 'diff_games_win_percent_grass_hh'] = df_combined['player_0_games_win_percent_grass_hh'] - \
                                                            df_combined['player_1_games_win_percent_grass_hh']

    return df_combined