import re
import pandas as pd 
import streamlit as st

def preprocess(data):
    pattern= "\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s[\w][\w][\s]-"
    dates= re.findall(pattern,data)
    msgs=re.split(pattern,data)[1:]

    df=pd.DataFrame({"message_date":dates,"user_msgs":msgs})

    df["message_date"]= pd.to_datetime(df["message_date"],format="%d/%m/%Y, %I:%M %p -")

    df['date']= df['message_date'].dt.date
    df['time']= df['message_date'].dt.time

    user=[]
    msgs=[]
    for message in df['user_msgs']:
        entry= re.split('([\w\W]+?):\s', message)
        if entry[1:]:
            user.append(entry[1])
            msgs.append(entry[2])
        else:
            for i in entry:
                entry2= re.split('([\w\W]+?)\sjoined', i)
                if entry2[1:]:
                    user.append(entry2[1])
                    msgs.append('joined to group')
                else:
                    for i in entry2:
                        entry3= re.split('([\w\W]+?)\sadded',i)
                        if entry3[1:]:
                            user.append(entry3[2])
                            msgs.append("added to group")
                        else:
                            user.append('group_notification')
                            msgs.append(entry2[0])
    
    df["user"]=user
    df['msgs']= msgs
    df.drop (columns=["user_msgs"], inplace=True)

    df['year']= df['message_date'].dt.year
    df['month_num']= df['message_date'].dt.month
    df['month']= df['message_date'].dt.month_name()
    df['day']= df['message_date'].dt.day
    df['day_name']= df['message_date'].dt.day_name()
    df['hour']= df['message_date'].dt.hour
    df['minute']= df['message_date'].dt.minute
    df.drop(columns=['message_date'], inplace= True)


    return df 
