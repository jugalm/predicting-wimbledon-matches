from utils.create_features_utils import *
import pandas as pd

df = pd.DataFrame()

for i in range(2005, 2020):
    if i <=2012:
        link = 'data/mens/' + str(i) + '.xls'
    else:
        link = 'data/mens/' + str(i) + '.xlsx'
    df_temp = pd.read_excel(link)
    df = df.append(df_temp, sort=False)

df = df.reset_index()

df = df[df.Date.notnull()]

df['Date'] = df.apply(lambda row: datetime.strptime(str(row['Date']), "%Y-%m-%d %H:%M:%S").strftime("%Y/%m/%d"), axis=1)

df.reset_index(inplace=True)

del (df['index'])

df = df[df.Comment == 'Completed']

df.loc[:,'best_of_5'] = (df['Best of'] ==5).astype(int)
df['W3'] = pd.to_numeric(df['W3'], errors='coerce')
df['L3'] = pd.to_numeric(df['L3'], errors='coerce')

df = df.fillna(0)

print(df.dtypes)

df_combined = df[['Tournament',  'Date', 'Surface', 'Round']].copy()

df_combined.loc[:,'player_0'] = df.apply(lambda row: get_player_1_name(row['Winner'], row['WRank'], row['Loser'], row['LRank']), axis=1)
df_combined.loc[:,'player_0_rank'] = df.apply(lambda row: get_player_1_rank(row['WRank'], row['LRank']), axis=1)
df_combined.loc[:,'player_0_odd'] = df.apply(lambda row: get_player_1_odd(row['B365W'], row['WRank'], row['B365L'], row['LRank']), axis=1)


df_combined.loc[:,'player_1'] = df.apply(lambda row: get_player_2_name(row['Winner'], row['WRank'], row['Loser'], row['LRank']), axis=1)
df_combined.loc[:,'player_1_rank'] = df.apply(lambda row: get_player_2_rank(row['WRank'], row['LRank']), axis=1)
df_combined.loc[:,'player_1_odd'] = df.apply(lambda row: get_player_2_odd(row['B365W'], row['WRank'], row['B365L'], row['LRank']), axis=1)

df_combined.loc[:,'outcome'] = df.apply(lambda row: outcome(row['WRank'], row['LRank']), axis=1)

df_combined = df_combined[df_combined.Tournament == 'Wimbledon']

df_combined = df_combined[df_combined.Date > '2010/01/01']

df_combined = create_features(df_combined, df)

print(df_combined.columns)

df_combined.to_csv('data/wimbledon_matches_with_feature.csv', index=False)

df.to_csv('data/mens/combined_raw_data.csv', index=False)