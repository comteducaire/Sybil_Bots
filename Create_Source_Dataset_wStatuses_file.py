import csv
from os import listdir, walk
from os.path import isfile, join

def try_parse_int(s, base=10, val=None):
  try:
    return int(s, base)
  except ValueError:
    return -1

with open('filtered_source.csv', 'a+', newline='',  encoding='utf-8') as csvfile_clean:
    writer = csv.writer(csvfile_clean, delimiter=';')

    mypath='D:\Masters\Thesis\Data Sets\Ten_K_Dataset_10K\Original'
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    f = []
    for (dirpath, dirnames, filenames) in walk(mypath):
        f.extend(filenames)
        break
    for eachfile in f:
        writer.writerow(['ID', 'Statuses'])
        # , 'Source_IP','Source_port', 'Destination_IP', 'Destination_Port', 'Source_To_Destination_Bytes' , 'Destination_To_Source_Bytes', 'Input_Output_Packages_Ratio(IOPR)',

        eachfile = mypath + '\\' + eachfile
        with open(eachfile, encoding='utf-8') as csvfile:
            csv_reader: object = csv.reader(csvfile, delimiter=';')
            for row in csv_reader:

                try :
                    id_of_tweet = row[0]
                    statuses_str = row[18]

                    screen_name = row[1]
                    length_username = row[2]
                    followers_to_friends_ratio = row[3]
                    posting_rate = row[4]
                    location = row[5]
                    url = row[6]
                    creation_date = row[7]
                    followers_num = row[8]
                    friends_num = row[9]
                    statuses_count = row[10]
                    likes = row[11]
                    likes_rate = row[12]
                    is_verified = row[13]
                    has_extended_profile = row[14]
                    bot_type = row[15]
                    friends_str = row[16]
                    followers_str = row[17]


                    #and float(posting_rate) > 2.0
                    if posting_rate != 'Posting_Rate' and bot_type == 'Political_Bot' and float(posting_rate) > 2.0:
                        writer.writerow([id_of_tweet, statuses_str])

                # , source_ip, source_port, destination_ip, destination_port, s_to_d_bytes, d_to_s_bytes, IOPR,

                except Exception as e:
                    print(e)
                    continue