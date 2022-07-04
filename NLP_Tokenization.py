import csv

import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import RegexpTokenizer


def Normalize(statue, NormalizedStatue=None):
    #Step 1:- Converting Upper Case to Lower Case
    statue = statue.lower()

    #Step 2:- Removing Punctuations
    puncts = '[$&+,:;=?@#|\'<>.^*()%!-]'
    for sym in puncts:
        statue = statue.replace(sym, ' ')

    NormalizedStatue = statue
    return NormalizedStatue


with open('tokenization.csv', 'a+', newline='', encoding='utf-8') as csvfile_clean:
    writer = csv.writer(csvfile_clean, delimiter=';')
    writer.writerow(['id_of_tweet', 'tokens'])


    with open('filtered_results_political_2_w_statuses.csv', encoding='utf-8') as csvfile:
        csv_reader: object = csv.reader(csvfile, delimiter=';')
        IDs_List = []
        Statuses_List = []
        for row in csv_reader:
            try:
                id_of_tweet = row[0]
                statuses_str = row[1]
                statuses_str = str.replace(statuses_str, '#*#*{', '')
                statuses_str = str.replace(statuses_str, '}#*#*', '')

                if id_of_tweet != 'ID':
                    # record = {id_of_tweet, statuses_str}
                    IDs_List.append(id_of_tweet)
                    Statuses_List.append(statuses_str)

            except Exception as e:
                print(e)
                continue

        ps = PorterStemmer()
        lancaster = nltk.LancasterStemmer()
        wnlem = nltk.WordNetLemmatizer()

        i = 0
        while i < len(Statuses_List):
            statue = Statuses_List[i]
            NormalizedStatue = Normalize(statue)

            #Tokenization Start
            tokenizer = RegexpTokenizer(r'\w+')
            tokens = tokenizer.tokenize(NormalizedStatue)

            #Normalization Step 3:- Removing Stop Words
            stop_words = set(stopwords.words('english'))

            try:
                tokens_new = []; flag = 0
                for token in tokens:
                    flag = 0
                    for stop_word in stop_words:
                        stop_word = str.lower(stop_word)
                        if token == stop_word:
                            flag = 1

                    if flag != 1:
                        tokens_new.append(wnlem.lemmatize(token)) #|| lancaster.stem ||  ps.stem for porter stemmer
                i += 1
                writer.writerow([IDs_List[i], tokens_new])


            except Exception as e:
                e = e;



            # Tokenization End


