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
        user_statuses = api.user_timeline(user_id)

        statuses = []
        for status in user_statuses:
            statuses.append(status.text)
        return statuses

    except Exception as e:
        print(e)
        return "not found"

def get_statuses2(user_id):
    try:
        user_statuses = api.user_timeline(user_id)
        statuses = ''
        for status in user_statuses:
            statuses +=  '{{{ (' + str(status.created_at)+') ' + status.text + '}}}'

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

    mypath='D:\Masters\Thesis\Data Sets\Ten_K_Dataset_10K'
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    f = []
    for (dirpath, dirnames, filenames) in walk(mypath):
        f.extend(filenames)
        break
    for eachfile in f:
        writer.writerow(['ID', 'Screen_Name', 'Length_of_UserName', 'Followers_to_Friends_Ratio', 'Posting_Rate'
                            , 'Location', 'URL', 'Creation_Date', 'Followers#', 'Friends#', 'Statuses_Count'
                            , 'Likes', 'Likes_Rate', 'Is_Verified', 'Has_Extended_Profile', 'Bot_Type', 'Friends',
                         'Followers', 'Statuses', eachfile])
        # , 'Source_IP','Source_port', 'Destination_IP', 'Destination_Port', 'Source_To_Destination_Bytes' , 'Destination_To_Source_Bytes', 'Input_Output_Packages_Ratio(IOPR)',

        eachfile = mypath + '\\' + eachfile
        with open(eachfile) as csvfile:
            csv_reader: object = csv.reader(csvfile, delimiter=',')
            for row in csv_reader:
                user_ = get_tweet_user(row[0])
                id_of_tweet = (row[0])

                if user_!= "not found" :
                    screen_name = user_.screen_name

                    friends_list = get_friends(screen_name)
                    followers_list = get_followers(screen_name)
                    statuses = get_statuses(screen_name)

                    length_username = len(screen_name)
                    num_folowers = user_.followers_count
                    num_friends = user_.friends_count
                    creation_date = user_.created_at
                    statuses_count = user_.statuses_count
                    diff = datetime.utcnow() - creation_date
                    location = user_.location.replace(';',',')
                    url = 'http://twitter.com/'+screen_name
                    likes = user_.favourites_count
                    is_verified = user_.verified
                    has_extended_profile = user_.has_extended_profile
                    # statuses = user_.statuses
                    # tweet = get_tweet_text(id_of_tweet)

                    writer = csv.writer(csvfile_clean, delimiter=';')
                    try :
                        if num_friends != 0:
                            followers_to_friends_ratio = num_folowers / num_friends
                        else : followers_to_friends_ratio = 0

                        if diff.days != 0:
                            avg_tweets_per_day = statuses_count / diff.days
                            avg_likes_per_day = likes / diff.days
                        else :
                            avg_tweets_per_day = 0
                            avg_likes_per_day = 0

                        usr_str = '@' + screen_name
                        bot_or_not =  (row[1])
                        # bot_or_not = bom.check_account(usr_str)
                        # is_political_bot = bot_or_not['display_scores']['english']['astroturf']
                        # is_financial_bot = bot_or_not['display_scores']['english']['financial']
                        # is_spammer_bot = bot_or_not['display_scores']['english']['spammer']
                        # is_fake_follower_bot = bot_or_not['display_scores']['english']['fake_follower']
                        #
                        # types_list = [is_political_bot, is_financial_bot, is_spammer_bot, is_fake_follower_bot]
                        # max_value_type = max(types_list)
                        # index_of_max = types_list.index(max_value_type)
                        bot_type = row[1]
                        #
                        # if(index_of_max==0): bot_type = 'Political_Bot'
                        # elif (index_of_max == 0): bot_type = 'Financial_Bot'
                        # elif (index_of_max == 0):bot_type = 'Spammer_Bot'
                        # else: bot_type = 'Fake_Follower_Bot'


                        twitterstr = screen_name + "  " + str(avg_tweets_per_day) + " " + str(avg_likes_per_day) + " " + bot_type
                        objnetworkstr = GenerateNetworkValues(twitterstr)
                        networkvalues = objnetworkstr.split(sep=";")

                        source_ip = networkvalues[0]
                        source_port = networkvalues[1]
                        destination_ip = networkvalues[2]
                        destination_port = networkvalues[3]
                        s_to_d_bytes = networkvalues[4]
                        d_to_s_bytes = networkvalues[5]
                        IOPR = networkvalues[6]

                        statuses_str = convert_list_tostr(statuses)
                        friends_str = convert_intlist_tostr(friends_list)
                        followers_str = convert_intlist_tostr(followers_list)

                        #write only twitter values to CSV
                        # writer.writerow([id_of_tweet, screen_name, length_username, followers_to_friends_ratio,
                        #                avg_tweets_per_day, location, url, creation_date, num_folowers, num_friends,
                        #                statuses_count, likes, avg_likes_per_day, is_verified, has_extended_profile,
                        #                bot_or_not])

                        # write twitter + Network values


                        writer.writerow([id_of_tweet, screen_name, length_username, followers_to_friends_ratio,
                                         avg_tweets_per_day, location, url, creation_date, num_folowers, num_friends,
                                         statuses_count, likes, avg_likes_per_day, is_verified, has_extended_profile,
                                         bot_type, friends_str, followers_str, statuses_str])

                    # , source_ip, source_port, destination_ip, destination_port, s_to_d_bytes, d_to_s_bytes, IOPR,

                    except Exception as e:
                        print(e)
                        continue

                else :
                    screen_name = "Not Found"
                    print(screen_name)




