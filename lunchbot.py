from datetime import datetime, time, timedelta 
import random
import os
import requests
import urllib

def run():
    lunchtime, leaving_time = get_lunch_time()
    print(leaving_time.strftime("%I:%M:%S"))
    token = os.environ["SLACK_API_TOKEN"]
    members = get_group_members(token)
    for member in members:
        send_slack_reminder(token, "meet in the lobby in two minutes ({0})"
            .format(lunchtime.strftime("%I:%M:%S")),"at {0}"
            .format(leaving_time.strftime("%I:%M:%S"))), member)

def get_lunch_time():
    #timedelta requires a datetime, we don't care about date
    basetime = datetime(100, 1, 1, 11, 47, 00)
    r = timedelta(seconds=(random.randint(0, 299))) 
    lunchtime = (basetime + r).time()
    leaving_time = (basetime + r - timedelta(seconds=120)).time()
    return lunchtime, leaving_time

def get_group_members(token, group="G2V24RAV6"):
    r = requests.get('https://slack.com/api/groups.info?token={0}&channel={1}'
        .format(token, group))
    return r.json()["group"]["members"]

def send_slack_reminder(token, text, time, user):
    payload = {'token':token,'text':text,'time':time,'user':user}
    r = requests.get('https://slack.com/api/reminders.add', params=payload)
    print r.url
    if(r.json()["ok"] != True):
        print(str(r.json()))
        raise Exception("the slack reminder failed. please contact your system administrator")

if __name__ == '__main__':
    run()
