import csv
import math
import numpy as np
from nltk.probability import FreqDist
from nltk.corpus import stopwords
from operator import itemgetter
from nltk.stem import PorterStemmer
from nltk.tokenize import RegexpTokenizer
from gensim import corpora
import pickle
from langdetect import detect
import gensim


from gensim.models.doc2vec import TaggedDocument, Doc2Vec

# Calculate term frequencies
import nltk
from pip._internal.utils import subprocess
from sklearn.feature_extraction.text import TfidfVectorizer

def tf(dataset, file_name):
    text = dataset[file_name]
    tokens = nltk.word_tokenize(text)
    fd = nltk.FreqDist(tokens)
    return fd

# Calculate inverse document frequency
def idf(dataset, term):
    count = [term in dataset[file_name] for file_name in dataset]
    inv_df = math.log(len(count)/sum(count))
    return inv_df

def tfidf(dataset, file_name, n):
    term_scores = {}
    file_fd = tf(dataset,file_name)
    for term in file_fd:
        if term.isalpha():
            idf_val = idf(dataset,term)
            tf_val = tf(dataset, file_name)[term]
            tfidf = tf_val*idf_val
            term_scores[term] = round(tfidf,2)
    return sorted(term_scores.items(), key=lambda x:-x[1])[:n]

IDs_List = []
Screen_Name_List = []
Length_of_UserName_List = []
Followers_to_Friends_Ratio_List = []
Posting_Rate_List = []
Location_List = []
URL_List = []
Creation_Date_List = []
Followers_Count_List = []
Friends_Count_List = []
Statuses_Count_List = []
Likes_Count_List = []
Likes_Rate_List = []
Is_Verified_List = []
Has_Extended_Profile_List = []
Friends_List = []
Followers_List = []
Statuses_List = []
test_dict = {}

word_map = {
    'Topic1': ['trump', 'obama', 'joebiden', 'schumer', 'bully', 'bleeding', 'state', 'minister', 'chairman', 'prexy', 'gov', 'primary', 'outflank', 'election', 'checks', 'heart', 'donald', 'politic', 'nominee', 'chair', 'president', 'chairperson', 'Chief_Executive', 'President_of_the_United_States', 'poll', 'platform', 'delegate', 'United_States_President', 'coattail', 'caucus', 'pulpit', 'majority', 'government', 'house', 'party', 'prim', 'senator', 'balance', 'bipartisan', 'campaign', 'vote', 'silent', 'white','biden',],
    'Topic2': ['covid', 'china', 'incubation', 'ventilator', 'asymptomatic', 'pathogen', 'vaccin', 'isolation', 'quarantine', 'epidemic', 'presymptomatic', 'anti', 'distan', 'anti-body', 'condition', 'covid19', 'underlying', 'immunity', 'patient', 'n95', 'novel', 'herd', 'strain', '19', 'coronavirus', 'outbreak', 'body', 'spread', 'mask'],
    'Topic3': ['women', 'hilary', 'clinton', 'woman', 'elizabeth', 'hostile', 'char', 'cleaning_lady', 'kamala', 'revolution', 'senate', 'hilary', 'rachel', 'misandry', 'sex', 'inferiority', 'fair_sex', 'sexism', 'charwoman', 'femin', 'misogyny', 'catherine', 'leader', 'feminist', 'levine', 'womanhood', 'victim', 'congress', 'halaand', 'harris', 'cleaning_woman', 'girl', 'cortez', 'gender', 'deb', 'equal', 'benevolent', 'empower', 'patriarchy', 'adult_female', 'history', 'women', 'power', 'right', 'clinton', 'nancy', 'pelosi']
}

def Normalize_ScreenNames(ListOfUserNames):
    corpus = [
        [word for word in ListOfUserNames]
    ]

    #corpus = [list(tokenize(text)) for text in corpus]
    corpus = [
        TaggedDocument(words, ['d{}'.format(idx)])
        for idx, words in enumerate(corpus)
    ]

    model = Doc2Vec(corpus, size=5, min_count=0)
    print(model.docvecs[0])

    # vectorize(Screen_Name_List)
    # v = DictVectorizer(sparse=False)
    # d = test_dict
    # x = v.fit_transform(d)
    # print(x)

    # encode document
    #vector = vectorizer.transform(Screen_Name_List)

    #print(vector.shape)
    #print(vector.toarray())

    return Screen_Name_List

def Normalize_List_Int(ListofInt):
    norm = np.linalg.norm(ListofInt)  # To find the norm of the array
    print(norm)  # Printing the value of the norm
    i=0
    NewList = []
    while i < len(ListofInt):
        NewList.append(float(ListofInt[i]) / norm) # Formula used to perform array normalization
        i+=1
    print(NewList)
    return NewList

def Normalize_List_Int_2(ListofInt):
    i=0
    NewList = []
    while i < len(ListofInt):
        NewList.append((float(ListofInt[i]) - float(min(ListofInt))) / (float(max(ListofInt))-float(min(ListofInt))) ) # Formula used to perform array normalization
        i+=1
    print(NewList)
    return NewList

def Standardize_List_Int(ListofInt):
    data = np.array(ListofInt).astype(np.float)
    new_data = (data-data.mean())/data.std()
    print(new_data)
    return new_data

def Normalize_List_Int_np(ListofInt):
    data = np.array(ListofInt).astype(np.float)
    new_data = (data - np.min(data)) / (np.max(data) - np.min(data))
    print(new_data)
    return new_data

def Normalize_List_Bool(Bool_List):
    Int_List = []
    i = 0
    while i<len(Bool_List):
        if Bool_List[i]=="True":
            Int_List.append(1)
        else: Int_List.append(0)

        i+=1

    return  Int_List

def Normalize_Creation_Date(Creation_Date_List):
    Int_List = []
    i = 0
    #2018-10-08 04:59:24
    while i < len(Creation_Date_List):
        if Creation_Date_List[i].find('2021')!=-1:
            Int_List.append(1.0)
        elif Creation_Date_List[i].find('2020')!=-1:
            Int_List.append(0.9)
        elif Creation_Date_List[i].find('2019') != -1:
            Int_List.append(0.8)
        elif Creation_Date_List[i].find('2018') != -1:
            Int_List.append(0.7)
        elif Creation_Date_List[i].find('2017') != -1:
            Int_List.append(0.6)
        elif Creation_Date_List[i].find('2016') != -1:
            Int_List.append(0.5)
        elif Creation_Date_List[i].find('2015') != -1:
            Int_List.append(0.4)
        elif Creation_Date_List[i].find('2014') != -1:
            Int_List.append(0.3)
        elif Creation_Date_List[i].find('2013') != -1:
            Int_List.append(0.2)
        elif Creation_Date_List[i].find('2012') != -1:
            Int_List.append(0.1)
        else:
            Int_List.append(0.0)
        i+=1

    return Int_List

def Normalize_Location(Location_List):
    Int_List = []
    i = 0
    while i < len(Location_List):
        if (len(Location_List[i])):
            Int_List.append(1)
        else:
            Int_List.append(0)
        i+=1

    return Int_List

#find the Most frequent 200 IDs in lists then normalize based on that.
def Normalize_Friends_Followers_Lists(Friends_List, X_Top_Frequencies):
    i = 0

    Normalized_List = []
    All_Friends_All_Users = []
    Top_X_Friends = []
    while(i<len(Friends_List)):
        if (Friends_List[i] and Friends_List[i] != '{n},{o},{t},{ },{f},{o},{u},{n},{d},'):

            All_Friends_Single_User = Friends_List[i].split("},{")
            All_Friends_Single_User[0] = All_Friends_Single_User[0].replace("{","")
            All_Friends_Single_User[len(All_Friends_Single_User)-1] = All_Friends_Single_User[len(All_Friends_Single_User)-1].replace("},", "")

            j = 0
            while(j < len(All_Friends_Single_User)):
                All_Friends_All_Users.append(All_Friends_Single_User[j])
                j = j+1

        i = i + 1


    fdist = FreqDist(All_Friends_All_Users)
    str_word_freq = ""
    for word, frequency in fdist.most_common(X_Top_Frequencies):
        str_word_freq = str_word_freq + '{ ' + str(word) + ':' + str(frequency) + '}; '
        Top_X_Friends.append(word)
    print(str_word_freq)

    m = 0
    while (m < len(Friends_List)):
        normalized_value = 0.0
        if (Friends_List[m] and Friends_List[m] != '{n},{o},{t},{ },{f},{o},{u},{n},{d},'):
            k = 0
            while (k<len(Top_X_Friends)):
                if(Top_X_Friends[k] in Friends_List[m]):
                    normalized_value = normalized_value + (1/X_Top_Frequencies)
                k = k+1

        Normalized_List.append((normalized_value))
        m= m+1



    return Normalized_List

def Normalize_text_statue(statue, NormalizedStatue=None):
    try:
        lang = detect(statue)

        if lang == "it":
            statue = "italianlanguage"

        elif lang == "en":
            # Step 1:- Converting Upper Case to Lower Case
            statue = statue.lower()

            # Step 2:- Removing Punctuations
            puncts = '[$&+,:;=?@#|\'<>.^*()%!-]'
            for sym in puncts:
                statue = statue.replace(sym, ' ')
    except:
        statue = "otherlanguage"

    NormalizedStatue = statue
    return NormalizedStatue


def Tokkenize_statuses(Statuses_List):
    All_Tokens = []
    # ps = PorterStemmer()
    # lancaster = nltk.LancasterStemmer()
    wnlem = nltk.WordNetLemmatizer()

    i = 0
    while i < len(Statuses_List):
        statue = Statuses_List[i]
        NormalizedStatue = Normalize_text_statue(statue)

        # Tokenization Start
        tokenizer = RegexpTokenizer(r'\w+')
        tokens = tokenizer.tokenize(NormalizedStatue)

        # Normalization Step 3:- Removing Stop Words
        stop_words = set(stopwords.words('english'))

        try:
            tokens_new = [];
            flag = 0
            for token in tokens:
                flag = 0
                for stop_word in stop_words:
                    stop_word = str.lower(stop_word)
                    if token == stop_word:
                        flag = 1

                if flag != 1:
                    tokens_new.append(wnlem.lemmatize(token))  # || lancaster.stem ||  ps.stem for porter stemmer
            i += 1
            All_Tokens.append(tokens_new)

        except Exception as e:
            e = e;
    return All_Tokens

#Not used function
def RemoveCommonWords(All_Tokens_All_Statuses_All_Users):
    # RemovedWords = ["rt", "RT" , "http", "co", "di", "il", "e", "che", "la", "per", "è", "un", "l", "non",
    #                 "amp", "del", "al", "si", "da", "su", " rt", " rt ", "rt ", "le", ]

    RemovedWords = ["italianlanguage","otherlanguage", "http"]
    x = 0

    while(x<len(All_Tokens_All_Statuses_All_Users)):
        y=0
        while(y<len(RemovedWords)):
            try:
                if(len(All_Tokens_All_Statuses_All_Users[x]) !=0):
                    if(len(All_Tokens_All_Statuses_All_Users[x]) <=3 or All_Tokens_All_Statuses_All_Users[x] in RemovedWords[y]):
                        All_Tokens_All_Statuses_All_Users.remove(All_Tokens_All_Statuses_All_Users[x])
            except: pass
            y = y+1
        x = x+1

    return All_Tokens_All_Statuses_All_Users


def RemoveCommonWords2(All_Statuses_All_Users):
    RemovedWords = ["italianlanguage","otherlanguage"]

    for Status_per_User in All_Statuses_All_Users:
            for word in Status_per_User:
                for removedword in RemovedWords:
                    if word == removedword:
                        if word in Status_per_User:
                            Status_per_User.remove(word)

    return All_Statuses_All_Users

def RemoveCommonWords_AllStatus_SingleUser(All_Statuses_Single_User):
    All_words_Single_user = []
    # RemovedWords = ["rt", "RT", "http", "co", "di", "il", "e", "che", "la", "per", "è", "un", "l", "non",
    #                 "amp", "del", "al", "si", "da", "su", " rt", " rt ", "rt ", "le", "co", "con"]
    RemovedWords = ["italianlanguage", "otherlanguage", "http"]

    for words in All_Statuses_Single_User:
        for word in words:
            if word not in RemovedWords and word not in All_words_Single_user:
                All_words_Single_user.append(word)

    return All_words_Single_user

#Not used function
def check_sent(word, sentences):
    final = [all([w in x for w in word]) for x in sentences]
    sent_len = [sentences[i] for i in range(0, len(final)) if final[i]]
    return int(len(sent_len))

#Not used function
def get_top_n(dict_elem, n):
    result = dict(sorted(dict_elem.items(), key = itemgetter(1), reverse = True)[:n])
    return result


def Normalize_Statuses_Lists(Statuses_List, X_Top_Frequencies):
    i = 0

    Normalized_List = []
    All_Statuses_All_Users = []
    Top_X_Statuses = []
    Top_X_Frequencies = []

    while(i<len(Statuses_List)):
        if (Statuses_List[i]):

            All_Statuses_Single_User = Statuses_List[i].split("}#*#*  #*#*{")
            All_Statuses_Single_User[0] = All_Statuses_Single_User[0].replace("#*#*{","")
            All_Statuses_Single_User[len(All_Statuses_Single_User)-1] = All_Statuses_Single_User[len(All_Statuses_Single_User)-1].replace("}#*#*", "")

            All_Statuses_Single_User = Tokkenize_statuses(All_Statuses_Single_User)

            j = 0
            while(j < len(All_Statuses_Single_User)):
                All_Statuses_All_Users.append(All_Statuses_Single_User[j])
                j = j+1

        i = i + 1

    All_Tokens_All_Statuses_All_Users = []

    s=0
    while(s<len(All_Statuses_All_Users)):
        t = 0
        while(t<len(All_Statuses_All_Users[s])):
            if len(All_Statuses_All_Users[s][t]) > 3:
                All_Tokens_All_Statuses_All_Users.append(All_Statuses_All_Users[s][t])

            t = t+1
        s=s+1


    #All_Tokens_All_Statuses_All_Users = RemoveCommonWords(All_Tokens_All_Statuses_All_Users)
    #All_Statuses_All_Users = RemoveCommonWords2(All_Statuses_All_Users)


    All_Tokens_All_Statuses_All_Users = RemoveCommonWords(All_Tokens_All_Statuses_All_Users)
    fdist = FreqDist(All_Tokens_All_Statuses_All_Users)
    str_word_freq = ""

    for word, frequency in fdist.most_common(X_Top_Frequencies):
        str_word_freq = str_word_freq + '{ ' + str(word) + ':' + str(frequency) + '}; '
        Top_X_Statuses.append(word)
        Top_X_Frequencies.append(frequency)
    print(str_word_freq)

    with open('MostFrequentWords.csv', 'w+', newline='',  encoding='utf-8') as result_file:
        wr = csv.writer(result_file, dialect='excel')

        m = 0
        while m < len(Top_X_Statuses):
            wr.writerow([Top_X_Statuses[m], Top_X_Frequencies[m]])
            m = m +1
    #subprocess.Popen(["C:\\Program Files\Microsoft Office\Office12\winword.exe", "Top 500 Most Frequent.docx", "/mFilePrintDefault",
    #    "/mFileExit"]).communicate()

    #Normalized value for each
    m = 0
    while (m < len(Statuses_List)):
        normalized_value = 0.0
        if (Statuses_List[m]):
            k = 0
            while (k<len(Top_X_Statuses)):
                if(Top_X_Statuses[k] in Statuses_List[m]):
                    normalized_value = normalized_value + (1/X_Top_Frequencies)
                k = k+1

        Normalized_List.append((normalized_value))
        m= m+1


    #return -1
    return Normalized_List


def Get_Topic(topic_num):
    if topic_num == 1:
        return "Topic1"
    elif topic_num == 2:
        return "Topic2"
    elif topic_num == 3:
        return "Topic3"


def Normalize_Topics_Lists(Statuses_List, word_map, topic_num):
    Normalized_List = []
    All_Words_in_Statuses_Single_User = []

    i = 0
    topic = Get_Topic(topic_num)
    while (i < len(Statuses_List)):
        if (Statuses_List[i]):

            All_Statuses_Single_User = Statuses_List[i].split("}#*#*  #*#*{")
            All_Statuses_Single_User[0] = All_Statuses_Single_User[0].replace("#*#*{", "")
            All_Statuses_Single_User[len(All_Statuses_Single_User) - 1] = All_Statuses_Single_User[
                len(All_Statuses_Single_User) - 1].replace("}#*#*", "")
            All_Statuses_Single_User = Tokkenize_statuses(All_Statuses_Single_User)

        All_Words_in_Statuses_Single_User = RemoveCommonWords_AllStatus_SingleUser(All_Statuses_Single_User)

        match_score = 0

        for word in All_Words_in_Statuses_Single_User:
            if word in word_map[topic]:
                match_score += 1
        if len(All_Words_in_Statuses_Single_User) != 0:
            Normalized_List.append((float(match_score) / len(All_Words_in_Statuses_Single_User))*10)
        else:
            Normalized_List.append(0)
                # print
                # 'Prefix: %s | MatchScore: %.2fs' % (prefix, float(match_score) / len(words))

        i = i +1




    return Normalized_List


with open('Normalized_Political_2.csv', 'w+', newline='',  encoding='utf-8') as csvfile_clean:
    writer = csv.writer(csvfile_clean, delimiter=';')
    writer.writerow(['ID', 'Screen_Name','Length_of_UserName', 'Followers_to_Friends_Ratio', 'Posting_Rate'
                        , 'Location', 'Creation_Date', 'Followers#', 'Friends#', 'Statuses_Count'
                        , 'Likes', 'Likes_Rate', 'Has_Extended_Profile', 'Friends',
                     'Followers', 'Statuses', 'Topic 1 (American Presidents)', 'Topic 2 (Covid economics)', 'Topic 3 (Women in Politics)'])


    #writer.writerow(['ID', 'Screen_Name', 'Length_of_UserName', 'Followers_to_Friends_Ratio', 'Posting_Rate'
                        #, 'Location', 'URL', 'Creation_Date', 'Followers#', 'Friends#', 'Statuses_Count'
                        #, 'Likes', 'Likes_Rate', 'Is_Verified', 'Has_Extended_Profile', 'Bot_Type', 'Friends',
                     #'Followers', 'Statuses', eachfile])



    with open('filtered_results_political_2.csv', encoding='utf-8') as csvfile:
        csv_reader: object = csv.reader(csvfile, delimiter=';')

        for row in csv_reader:
            try:
                if row[0] != 'ID':
                    IDs_List.append(row[0])
                    Screen_Name_List.append(row[1])

                    Length_of_UserName_List.append(row[2])
                    Followers_to_Friends_Ratio_List.append(row[3])
                    Posting_Rate_List.append(row[4])
                    Location_List.append(row[5])
                    URL_List.append(row[6])
                    Creation_Date_List.append(row[7])
                    Followers_Count_List.append(row[8])
                    Friends_Count_List.append(row[9])
                    Statuses_Count_List.append(row[10])
                    Likes_Count_List.append(row[11])
                    Likes_Rate_List.append(row[12])
                    Is_Verified_List.append(row[13])
                    Has_Extended_Profile_List.append(row[14])
                    Friends_List.append(row[16])
                    Followers_List.append(row[17])
                    Statuses_List.append(row[18])



            except Exception as e:
                print(e)
                continue


    method = 1 #normalization methods 3 methods + method 4 : standardization

    if method ==1:
        Length_of_UserName_List = Normalize_List_Int(Length_of_UserName_List)

        Followers_to_Friends_Ratio_List = Normalize_List_Int(Followers_Count_List)
        Posting_Rate_List = Normalize_List_Int(Posting_Rate_List)
        Location_List = Normalize_Location(Location_List)
        Creation_Date_List_Float = Normalize_Creation_Date(Creation_Date_List)
        Followers_Count_List = Normalize_List_Int(Followers_Count_List)
        Friends_Count_List = Normalize_List_Int(Friends_Count_List)
        Statuses_Count_List = Normalize_List_Int(Statuses_Count_List)
        Likes_Count_List = Normalize_List_Int(Likes_Count_List)
        Likes_Rate_List = Normalize_List_Int(Likes_Rate_List)
        # Is_Verified_List_Int = Normalize_List_Bool(Is_Verified_List)
        Has_Extended_Profile_List_Int = Normalize_List_Bool(Has_Extended_Profile_List)


    elif method == 2:
        Length_of_UserName_List = Normalize_List_Int(Length_of_UserName_List)

        Followers_to_Friends_Ratio_List = Normalize_List_Int_2(Followers_Count_List)
        Posting_Rate_List = Normalize_List_Int_2(Posting_Rate_List)
        Location_List = Normalize_Location(Location_List)
        Creation_Date_List_Float = Normalize_Creation_Date(Creation_Date_List)
        Followers_Count_List = Normalize_List_Int_2(Followers_Count_List)
        Friends_Count_List = Normalize_List_Int_2(Friends_Count_List)
        Statuses_Count_List = Normalize_List_Int_2(Statuses_Count_List)
        Likes_Count_List = Normalize_List_Int_2(Likes_Count_List)
        Likes_Rate_List = Normalize_List_Int_2(Likes_Rate_List)
        # Is_Verified_List_Int = Normalize_List_Bool(Is_Verified_List)
        Has_Extended_Profile_List_Int = Normalize_List_Bool(Has_Extended_Profile_List)
    elif method == 3:
        Length_of_UserName_List = Normalize_List_Int(Length_of_UserName_List)

        Followers_to_Friends_Ratio_List = Normalize_List_Int_np(Followers_Count_List)
        Posting_Rate_List = Normalize_List_Int_np(Posting_Rate_List)
        Location_List = Normalize_Location(Location_List)
        Creation_Date_List_Float = Normalize_Creation_Date(Creation_Date_List)
        Followers_Count_List = Normalize_List_Int_np(Followers_Count_List)
        Friends_Count_List = Normalize_List_Int_np(Friends_Count_List)
        Statuses_Count_List = Normalize_List_Int_np(Statuses_Count_List)
        Likes_Count_List = Normalize_List_Int_np(Likes_Count_List)
        Likes_Rate_List = Normalize_List_Int_np(Likes_Rate_List)
        # Is_Verified_List_Int = Normalize_List_Bool(Is_Verified_List)
        Has_Extended_Profile_List_Int = Normalize_List_Bool(Has_Extended_Profile_List)
    elif method==4:
        Length_of_UserName_List = Standardize_List_Int(Length_of_UserName_List)

        Followers_to_Friends_Ratio_List = Standardize_List_Int(Followers_Count_List)
        Posting_Rate_List = Standardize_List_Int(Posting_Rate_List)
        Location_List = Normalize_Location(Location_List)
        Creation_Date_List_Float = Normalize_Creation_Date(Creation_Date_List)
        Followers_Count_List = Standardize_List_Int(Followers_Count_List)
        Friends_Count_List = Standardize_List_Int(Friends_Count_List)
        Statuses_Count_List = Standardize_List_Int(Statuses_Count_List)
        Likes_Count_List = Standardize_List_Int(Likes_Count_List)
        Likes_Rate_List = Standardize_List_Int(Likes_Rate_List)
        #Is_Verified_List_Int = Normalize_List_Bool(Is_Verified_List)
        Has_Extended_Profile_List_Int = Normalize_List_Bool(Has_Extended_Profile_List)

    X_Top_Frequencies = 500 #number of top common Friends and Followers
    X_Top_Frequencies_Statuses = 500 #number of hot topics in statuses
    Friends_List = Normalize_Friends_Followers_Lists(Friends_List,X_Top_Frequencies)
    Followers_List = Normalize_Friends_Followers_Lists(Followers_List,X_Top_Frequencies)
    Presidents_List = Normalize_Topics_Lists(Statuses_List, word_map, 1)
    Covid_List = Normalize_Topics_Lists(Statuses_List, word_map, 2)
    Wo_List = Normalize_Topics_Lists(Statuses_List, word_map, 3)

    Statuses_List = Normalize_Statuses_Lists(Statuses_List, X_Top_Frequencies_Statuses)


    i = 0
    #counting word frequencies for all tweets by the user
    while i < len(IDs_List):
        writer.writerow([IDs_List[i], Screen_Name_List[i],Length_of_UserName_List[i],Followers_to_Friends_Ratio_List[i],
                         Posting_Rate_List[i],Location_List[i],Creation_Date_List_Float[i],Followers_Count_List[i],
                         Friends_Count_List[i],Statuses_Count_List[i],Likes_Count_List[i],
                         Likes_Rate_List[i],Has_Extended_Profile_List_Int[i],
                         Friends_List[i],Followers_List[i],Statuses_List[i], Presidents_List[i], Covid_List[i],
                        Wo_List[i]])
        i += 1
