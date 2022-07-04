import csv
import random
from datetime import datetime

import botometer
import tweepy
from os import listdir
from os.path import isfile, join
from os import walk



consumer_key = 'QhyOPxxxvJaOdp248cEBmFULw'
consumer_secret = 'nNgrjrBFnnozI7urzHeO3DduRy0mEHqBq1ASzNYuUe93l36SxL'
access_token = '102995859-ttxAcxp6nAXpSiTTVVb7zX7sk9ijVqsmYKAYKgyR'
access_token_secret = 'xHv7Vp7PJAb1u51D1eQxZS6syoicPfSg5ygYCV0SdCNuS'
rapidapi_key = 'b27285ed5emshe5f0d8e7428eb93p1ab3bcjsn07c64a6631b8'

twitter_app_auth = {
   'consumer_key': 'QhyOPxxxvJaOdp248cEBmFULw',
   'consumer_secret': 'nNgrjrBFnnozI7urzHeO3DduRy0mEHqBq1ASzNYuUe93l36SxL',
   'access_token': '102995859-ttxAcxp6nAXpSiTTVVb7zX7sk9ijVqsmYKAYKgyR',
   'access_token_secret': 'xHv7Vp7PJAb1u51D1eQxZS6syoicPfSg5ygYCV0SdCNuS',
 }

bom = botometer.Botometer(wait_on_ratelimit=True, rapidapi_key=rapidapi_key, **twitter_app_auth)

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, wait_on_rate_limit=True)

def randomly_generate_ip():
    x = [199, 188, 155, 144, 205, 169, 192, 155, 105, 100, 49, 7, 2, 25, 12, 77, 129, 214, 30, 198]

    i = random.randint(0, 19)
    j = random.randint(0, 19)
    k = random.randint(0, 19)
    l = random.randint(0, 19)

    v1 = str(x[i])
    v2 = str(x[j])
    v3 = str(x[k])
    v4 = str(x[l])

    ip = v1 + '.' + v2 + '.' + v3 + '.' + v4
    return ip

def convert_list_tostr(list):
    str = ''
    for s in list:
        st = s.strip().replace(';', ',').replace('\n', ' ').replace('\r', '')
        str += ' #*#*{' + st + '}#*#* '
    return str

def convert_list_tostr2(str):
        str = str.strip().replace(';', ',').replace('\n', ' ').replace('\r', '')
        return str

def convert_intlist_tostr(list):
    str_ = ''
    for i in list:
        str_+= '{' + str(i) + '},'
    return str_

def randomly_generate_port():
    v = str(random.randint(100, 64000))
    return v


def get_tweet_user(user_id):
    try:
        user = api.get_user(user_id)
        return user
    except: return "not found"

def get_friends(user_id):
    try:
        user_friends = api.friends_ids(user_id)
        return user_friends
    except: return "not found"

def get_followers(user_id):
        try:
            user_followers = api.followers_ids(user_id)
            return user_followers
        except:
            return "not found"

# API.user_timeline([id/user_id/screen_name][, since_id][, max_id][, count][, page]) // count – Specifies the number of statuses to retrieve.
def get_statuses(user_id):
    try:
        user_statuses = api.user_timeline(user_id, count = 100)
        statuses = []
        for status in user_statuses:
            statuses.append(status.text)
        return statuses

    except Exception as e:
        print(e)
        return "not found"

def get_statuses2(screen_name):
    try:
        user_statuses = api.user_timeline(screen_name, count = 100)
        statuses = ''
        for status in user_statuses:
            statuses += '{{{ (' + str(status.created_at)+') ' + status.text + '}}}'

        return statuses

    except Exception as e:
        print(e)
        return "not found"


def randomly_generate_bytes():
    return random.randint(20, 2000)

def randomly_generate_bps():
    return random.uniform(100000, 1000000)


def GenerateNetworkValues(twitterstr):
    source_ip = randomly_generate_ip()
    source_port = str(randomly_generate_port())
    destination_ip = randomly_generate_ip()
    destination_port = str(randomly_generate_port())
    s_to_d_bytes = randomly_generate_bytes()
    s_to_d_packets = s_to_d_bytes / 24
    d_to_s_bytes = randomly_generate_bytes()
    d_to_s_packets = d_to_s_bytes / 24
    IOPR = s_to_d_packets / d_to_s_packets

    source_bps = str(randomly_generate_bps())
    destination_bps = str(randomly_generate_bps())
    print(twitterstr)
    objnetwork = source_ip + ";" + source_port + ";" + destination_ip + ";" + destination_port + ";" + str(s_to_d_bytes) + ";" + str(d_to_s_bytes) + ";" + source_bps + ";" + destination_bps + ";" + str(IOPR)
    #print(source_ip + " " + source_port + " " + destination_ip + " " + destination_port + " " + str(s_to_d_bytes) + " " + str(d_to_s_bytes) + " " + source_bps + " " + destination_bps + " " + str(IOPR))
    return objnetwork


with open('results.csv', 'a+', newline='',  encoding='utf-8') as csvfile_clean:
    writer = csv.writer(csvfile_clean, delimiter=';')
    #User_ID, Screen_Name, Length_of_user_name, Followers_to_Friends_ratio, Posting_Rate, Location, Account_url,
    #Creation_Date, Number_of_followers, Friends_Count, Number_of_Tweets, Number_of_Likes, Likes_Rate
    #Is_Verified, Has_Extended_Profile, Botometer, Statuses

    mypath='D:\Masters\Thesis\Data Sets\Ten_K_Dataset_10K\Original'
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    f = []
    for (dirpath, dirnames, filenames) in walk(mypath):
        f.extend(filenames)
        break
    for eachfile in f:
        writer.writerow(['ID', 'Screen_Name', 'Statuses', eachfile])
        # , 'Source_IP','Source_port', 'Destination_IP', 'Destination_Port', 'Source_To_Destination_Bytes' , 'Destination_To_Source_Bytes', 'Input_Output_Packages_Ratio(IOPR)',

        eachfile = mypath + '\\' + eachfile
        with open(eachfile, encoding='utf-8') as csvfile:
            csv_reader: object = csv.reader(csvfile, delimiter=';')

            try:
                for row in csv_reader:

                    user_ = get_tweet_user(row[0])
                    id_of_tweet = (row[0])

                    if user_!= "not found" :

                        screen_name = user_.screen_name
                        usr_str = '@' + screen_name
                        statuses = get_statuses2(usr_str)

                        writer = csv.writer(csvfile_clean, delimiter=';')
                        try :
                            bot_type = row[1]

                            twitterstr = screen_name + " " + bot_type

                            statuses_str = convert_list_tostr2(statuses)

                            writer.writerow([id_of_tweet, screen_name, statuses_str])

                        except Exception as e:
                            print(e)
                            continue

                    else :
                        screen_name = "Not Found"
                        print(screen_name)
            except Exception as e:
                print(e)
                continue




