import numpy as np
import pandas as pd


def clean_portfolio(df, channel_types=['web', 'email', 'mobile', 'social']):
    """
    Cleans the raw portfolio dataframe through various cleaning steps.

    Input:
    df - the raw portfolio dataframe from portfolio.json
    channel_types - a list of str's for the different media channels

    Output:
    clean_df - the cleaned dataframe.

    Cleaning steps:
    - Takes channels column and converts it into 0/1's columns for each channel.
    - Reorder the columns.
    - Rename the id column to "offer_id".    
    """
    # Get a dataframe for channel data
    # Iterates through each list in the .channels series
    # to pull out whether each channel is present or not.
    campaigns = []
    for campaign in df.channels:
        campaign = set(campaign)
        channels = []
        for channel in channel_types:
            if channel in campaign:
                channels.append(1)
            else:
                channels.append(0)
        campaigns.append(channels)

    channel_frame = pd.DataFrame(campaigns)
    channel_frame.columns = channel_types

    # Reorder the original dataframe as well replacing the channels column
    # with the new channel dataframe
    clean_df = pd.concat([df[['id']],
                          channel_frame,
                          df[['offer_type', 'duration', 'difficulty', 'reward']]],
                         axis=1)

    # Rename id as offer_id
    clean_df = clean_df.rename(columns={'id':'offer_id'})
    
    # Convert duration in days to hours
    clean_df['duration'] = (clean_df['duration'] * 24).astype('int')
    
    return clean_df


def clean_profile(df):
    """
    Cleans the raw portfolio dataframe through various cleaning steps.

    Input:
    df - the raw profile dataframe from profile.json

    Output:
    clean_df - the cleaned dataframe.

    Cleaning steps:
    - Standardize the different types of NAs (None, age == 118) into np.nan.
    - Convert 'became_member_on' into datetime objects.
    - Reorder the columns.
    - Rename the user id.
    """
    df = df.copy()
    # Standardize NAs to numpy nan
    df['age'] = df['age'].replace(118, np.nan)
    df['gender'] = df['gender'].fillna(np.nan)
    # Convert str to datetime
    df['became_member_on'] = pd.to_datetime(
        df['became_member_on'], format='%Y%m%d')
    # Reorder the columns
    clean_df = df[['id', 'gender', 'age', 'income', 'became_member_on']]
    # Relabel id as user_id
    clean_df = clean_df.rename(columns={'id': 'customer_id'})

    return clean_df


def clean_transcript(df):
    """
    Cleans the raw transcript dataframe through various cleaning steps.

    Input:
    df - the raw transcript dataframe from transcript.json

    Output:
    clean_df - the cleaned dataframe.

    Cleaning steps:
    - Replace spaces in event strings to underscores.
    - Expand out "value" column.
    """
    df = df.copy()
    # Replace space with underscore in event column
    df['event'] = df['event'].str.replace(' ', '_')

    # Expand the value column into multiple columns
    value_frame = pd.DataFrame(df['value'].to_list())
    # Combine 'offer id' and 'offer_id' columns
    # First get the non nulls from each and check that they don't overlap
    a = value_frame['offer id'].notnull()
    b = value_frame['offer_id'].notnull()
    assert ~((a & b).any())  # True if no overlap
    # Make the combined column and drop 'offer id'
    value_frame['offer_id'] = value_frame['offer_id'].combine_first(
        value_frame['offer id'])
    value_frame = value_frame.drop(labels=['offer id'], axis=1)

    # Concatenate and reorder the columns
    clean_df = pd.concat([df, value_frame], axis=1)
    clean_df = clean_df[['person', 'time',
                         'event', 'amount', 'reward', 'offer_id']]

    # Rename the 'person column'
    clean_df = clean_df.rename(columns={'person': 'customer_id'})

    return clean_df


def reconciliate_ids(primary_df, secondary_df, id_column_name):
    """
    Takes hashed ids from two dataframes, and changes them to numbers.

    The primary dataframe should be either portfolio or profile.
    The secondary dataframe should be the transcript dataframe.

    Input:
    primary_df - either portfolio or profile dataframe
    secondary_df - the transcript dataframe
    id_column_name - a str representing the column you want to reconciliate

    Output:
    df1, df2 - dataframes with new id numbers, of the primary and secondary dfs respectively.
    """
    # Renaming for convenience
    df1 = primary_df.copy()
    df2 = secondary_df.copy()

    # Get unique ids from primary df
    unique_ids = df1[id_column_name].unique()
    # Create a dict of sequential ids
    id_dict = dict(zip(unique_ids, range(1, len(unique_ids) + 1)))
    # Map primary and secondary dataframe values using the new id dict
    df1[id_column_name] = df1[id_column_name].map(id_dict)
    df2[id_column_name] = df2[id_column_name].map(id_dict)

    return df1, df2
