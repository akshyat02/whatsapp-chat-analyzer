# -*- coding: utf-8 -*-
"""
Created on Sat Aug 26 03:55:54 2023

@author: Akshyat Patra
"""
from urlextract import URLExtract
extractor = URLExtract()
from wordcloud import WordCloud


def fetch_stats(selected_user, df):

    if selected_user != 'Overall':

        df = df[df['user'] == selected_user]

    no_of_msg = df.shape[0]
    words = []
    for message in df['message'][df["message"]!="<Media omitted>\n"]:
        words.extend(message.split())
    no_of_words = len(words)

    # Extracting number of media
    no_of_media = df[df['message'].str.contains('<Media omitted>')].shape[0]

    # Extracting number of links
    links = []
    for message in df['message']:
        links.extend(extractor.find_urls(message))
    no_of_links = len(links)

    return no_of_msg, no_of_words, no_of_media, no_of_links

def monthly_timeline(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline

def daily_timeline(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    daily_timeline = df.groupby('only_date').count()['message'].reset_index()

    return daily_timeline

def most_active_users(df):
    x = df['user'].value_counts().head()
    df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'user': 'Name', 'count': 'Active Percent'})
    return x,df

def week_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()

def month_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()

def create_wordcloud(selected_user,df):

    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    def remove_stop_words(message):
        y = []
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)

    wc = WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    #temp['message'] = temp['message'].apply(remove_stop_words)
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc
