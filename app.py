# -*- coding: utf-8 -*-
"""
Created on Sat Aug 26 02:06:33 2023

@author: Akshyat Patra
"""

import streamlit as st
import matplotlib.pyplot as plt
import re

import preprocessor, helper

st.set_page_config(
    page_title="WhatsAnalyzer",
    page_icon="💬",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": 'https://www.linkedin.com/in/akshyat02',
        "Report a bug": "mailto:mail.akshyat@gmail.com?subject=Bug%20Report%20from%20WCA&body=Report%20your%20bug%20here",
        "About": "# WhatsAnalyzer \n *by Akshyat Patra* \n\n A web app platform that analyzes WhatsApp chats to extract insights such as sentiment, topics, and keywords ana many more." 
    }
)


st.sidebar.title("WhatsApp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Upload whatsapp .txt file in 12hr format")

def get_text(text):
  pattern = r"WhatsApp Chat with (.*).txt"
  match = re.search(pattern, text)
  if match:
    return match.group(1)
  else:
    return text

if uploaded_file:
   fname = uploaded_file.name
   heading = get_text(fname)
   st.title(heading)
else:
    st.title("WhatsAnalyzer")

if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)
    
    
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,"Overall")
    
    selected_user = st.sidebar.selectbox("Show analysis wrt",user_list)
    if selected_user == 'Overall':
        st.dataframe(df[df["user"]!="group_notification"][df["message"]!="This message was deleted\n"][df["message"]!="<Media omitted>\n"][["user", "message", "only_date","day_name", "hour", "minute"]].rename(columns={'minute':'min', "only_date":"date","day_name":"day"}))
    else:
        #st.text(selected_user)
        st.code(selected_user)
        st.dataframe(df[df["user"]==selected_user][df["message"]!="This message was deleted\n"][df["message"]!="<Media omitted>\n"][["only_date","message", "month", "day_name", "hour", "minute"]].rename(columns={'minute':'min',"day_name":"day"}))
    #st.dataframe(df)
    if True:
        st.title("Total")
        total_messages, total_words, total_media, total_links = helper.fetch_stats(selected_user, df[df["message"]!="This message was deleted\n"])

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.subheader("Messages")
            st.title(total_messages)
        with col2:
            st.subheader("Words")
            st.title(total_words)
        with col3:
            st.subheader("Media")
            st.title(total_media)
        with col4:
            st.subheader("Links")
            st.title(total_links)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.header("Monthly Timeline")
            timeline = helper.monthly_timeline(selected_user,df[df["message"]!="This message was deleted\n"][df["message"]!="<Media omitted>\n"])
            fig,ax = plt.subplots()
            ax.plot(timeline['time'], timeline['message'],color='green')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col2:
            # daily timeline
            st.header("Daily Timeline")
            daily_timeline = helper.daily_timeline(selected_user, df[df["message"]!="This message was deleted\n"][df["message"]!="<Media omitted>\n"])
            fig, ax = plt.subplots()
            ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='black')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        st.title("Most Active")
        if selected_user == 'Overall':
            x,new_df = helper.most_active_users(df[df["user"]!="group_notification"])
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                st.header('Most Active Users')
                ax.bar(x.index, x.values,color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)
                
        #Most Active        
        col1,col2 = st.columns(2)

        with col1:
            st.header("Most Active day")
            busy_day = helper.week_activity_map(selected_user,df[df["user"]!="group_notification"])
            fig,ax = plt.subplots()
            ax.bar(busy_day.index,busy_day.values,color='purple')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header("Most Active month")
            busy_month = helper.month_activity_map(selected_user, df[df["user"]!="group_notification"])
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values,color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
            
        # WordCloud
        st.title("Most Common Words")
        df_wc = helper.create_wordcloud(selected_user,df[df["user"]!="group_notification"][df["message"]!="This message was deleted\n"][df["message"]!="<Media omitted>\n"])
        fig,ax = plt.subplots()
        ax.imshow(df_wc)
        plt.xticks([]) 
        plt.yticks([])
        st.pyplot(fig)
    else:
        st.header("Don't forget to click on - Show Analysis")
else:
    st.caption("by Akshyat Patra")
    c1 = '''Rest assured, your privacy is our priority. 
We never transmit chat data to any external server! 
Every line of code operates right within your browser.'''
    st.code(c1, language='java')
    c2 = '''We believe in transparency!
This project is open-source, 
and all our code is available for public scrutiny on GitHub.
Feel free to verify it yourself!'''
    st.code(c2, language='java')
        