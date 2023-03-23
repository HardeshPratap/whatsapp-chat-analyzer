import streamlit as st 
import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns

import preprocessor as pre
import analysis as ana

st.sidebar.title("WhatsApp chat Analysis")
uploader=st.sidebar.file_uploader("upload file", type=['txt'], accept_multiple_files= False)

if uploader is not None:
   data=uploader.getvalue().decode('utf-8') 
   
   df=pre.preprocess(data)

   frame= df.copy()
   list = frame['msgs']!='joined to group'
   df1= frame[list]
   list0= df1['msgs']!= 'added to group'
   df2= df1[list0]
  
   frame1=df.copy()
   list1 = ((frame1['msgs']=='joined to group')|(frame1['msgs']=='added to group'))
   df3= frame1[list1]
   user_list = df3['user'].unique().tolist() 
   user_list.sort()

   x= df2['user'] != 'group_notification'
   y= df2['msgs']!= 'left'
   df_1 = df2[x]
   df_2 = df_1[y]
   
   #user_list= df['user'].unique().tolist()
   #user_list.remove("group_notification")
   user_list.sort()
   user_list.insert(0,"Overall")
   selected_user=st.sidebar.selectbox("chat analysis" ,user_list)

   

   v1= st.title("whatsapp chat")
   v2= st.dataframe(df2)
   v3= st.header("Total members")
   v4= st.title(len(user_list))
   
   if selected_user == 'Overall':

        st.title('Most Active Members')
            
        x, new_df=ana.most_busy_user(df)
        fig, ax= plt.subplots()
            
        col1,col2 = st.columns(2)

        with col1:
            ax.bar(x.index, x.values, color='green')
            plt.xlabel("Member")
            plt.ylabel("Number of Message")
            plt.xticks(rotation=90)
            st.pyplot(fig)

        with col2:
            st.dataframe(new_df)
    
   if st.sidebar.button("show analysis"):

        
        v1.empty()
        v2.empty()
        v3.empty()
        v4.empty()

        user_df= ana.dataframe(selected_user,df2)
        st.title("Selected User's Chats")
        st.dataframe(user_df)
        st.title("Selected User's Statistic")

        num_messages, words, num_media, links = ana.fetch_stats(selected_user,df2)

        col1,col2,col3,col4=st.columns(4)

        with col1:
            st.header("Total msgs")
            st.title(num_messages)
        with col2:
            st.header("words")
            st.title(words)
        with col3:
            st.header("media shared")
            st.title(num_media)
        with col4:
            st.header("links shared")
            st.title(links)
        if user_df.empty:
            st.header("non active user")
        else:
            st.title("monthly timeline")
            timeline_df= ana.monthly_timeline(selected_user, df)
            fig, ax= plt.subplots()
            plt.bar(timeline_df['time'],timeline_df['msgs'],width=0.5)
            plt.xlabel("month")
            plt.ylabel("frequency of message")
            plt.xticks(rotation=45)
            st.pyplot(fig) 
            st.title("daily timeline")
            daily_timeline_df= ana.daily_timeline(selected_user, df)
            fig, ax= plt.subplots()
            plt.plot(daily_timeline_df['date'],daily_timeline_df['msgs'], color='black')
            plt.xlabel("days")
            plt.ylabel("frequency of message")
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        
            st.title("activity map")
            col1, col2= st.columns(2)
            
            with col1:
                st.header('most busy day')
                busy_day=ana.weekly_activity(selected_user, df)
            
                fig, ax= plt.subplots()
                ax.bar(busy_day.index, busy_day.values, color='red')
                plt.xlabel("day")
                plt.ylabel("frequency of message")
                plt.xticks(rotation=45)
                st.pyplot(fig)
                
            with col2:
                st.header('most busy month')
                busy_month=ana.month_activity(selected_user, df)
            
                fig, ax= plt.subplots()
                ax.bar(busy_month.index, busy_month.values, color='orange')
                plt.xlabel("month")
                plt.ylabel("frequency of message")
                plt.xticks(rotation=45)
                st.pyplot(fig)


            

 
       
            st.title('most common words')
            common_df= ana.most_common_words(selected_user,df)

            col1,col2 = st.columns(2)

            with col1:
                  fig, ax= plt.subplots()
                  ax.bar(common_df[0], common_df[1])
                  plt.xlabel("common words")
                  plt.ylabel("frequency of words")
                  plt.xticks(rotation=45)
                  st.pyplot(fig)

            with col2:
                  st.dataframe(common_df)
        
        
            st.title('common emoji used')
            emoji_df = ana.show_emoji(selected_user,df)
        
        
            if emoji_df.empty:
                  st.write('no emoji used')
        
            else :
                  col1,col2 = st.columns(2)
            
                  with col1:
                    st.dataframe(emoji_df)
                
                  with col2:
                    fig, ax= plt.subplots()
                    ax.bar(emoji_df[0],emoji_df[1])
                    plt.xlabel('emoji')
                    plt.ylabel('Frequency of emoji')
                    st.pyplot(fig)

    #timeline of daily activity
    # no of msgs done day by the user

    # Activity Map(users)
    # Most busy day wrt the user selected(in seperate plots)
    # Most busy month wrt to the user (in a seperate plot)
    #but both of the above two plots should be drawn side by side
    




