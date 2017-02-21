from datetime import datetime, time, timedelta 
import random
import os
import requests

token = None
slack_url = 'https://slack.com/api/'

def run():
    lunchtime, leaving_time = get_lunch_time()
    print(leaving_time.strftime("%I:%M:%S"))
    members = send_to_slack('groups.info', channel="G2V24RAV6")["group"]["members"]
    for member in members:
        send_slack_reminder("reminders.add", text="meet in the lobby in two minutes ({0})"
            .format(lunchtime.strftime("%I:%M:%S")), time="at {0}"
            .format(leaving_time.strftime("%I:%M:%S"))), user=member)

def get_lunch_time():
    #timedelta requires a datetime, we don't care about date
    basetime = datetime(100, 1, 1, 11, 47, 00)
    r = timedelta(seconds=(random.randint(0, 299))) 
    lunchtime = (basetime + r).time()
    leaving_time = (basetime + r - timedelta(seconds=120)).time()
    return lunchtime, leaving_time

def send_to_slack(method, **payload):
    payload['token'] = token
    r = requests.get("{0}{1}".format(slack_url, method), payload)
    if(r.json()["ok"] != True):
        print(str(r.json()))
        raise Exception("the slack message failed. please contact your system administrator")
    return r.json()

if __name__ == '__main__':
    token = os.environ["SLACK_API_TOKEN"]
    run()
