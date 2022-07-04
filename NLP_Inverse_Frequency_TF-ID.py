import csv
import math

from nltk.probability import FreqDist
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer

# Calculate term frequencies
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


with open('Frequecies.csv', 'a+', newline='',  encoding='utf-8') as csvfile_clean:
    writer = csv.writer(csvfile_clean, delimiter=';')
    writer.writerow(['id_of_tweet', 'tokens_by_Frequency'])


    with open('tokenization2.csv', encoding='utf-8') as csvfile:
        csv_reader: object = csv.reader(csvfile, delimiter=';')
        IDs_List = []
        Tokens_List = []
        Tokens_List_str = []
        for row in csv_reader:
            try:
                id_of_tweet = row[0]
                tokens_str = row[1]

                if id_of_tweet != 'id_of_tweet':
                    # record = {id_of_tweet, statuses_str}
                    IDs_List.append(id_of_tweet)
                    Tokens_List.append(tokens_str)
                    Tokens_List_str.append(str.replace(tokens_str, "', '", " ").replace("['", "").replace("']",""))


            except Exception as e:
                print(e)
                continue

        i = 0

        #counting word frequencies for all tweets by the user
        while i < len(Tokens_List):
            words = nltk.tokenize.word_tokenize(Tokens_List_str[i])
            fdist = FreqDist(words)
            #tfidf(dataset, "tfidf_1.txt", 5) #//Reading from normal text file (normal text)

            str_word_freq = ""

            for word, frequency in fdist.most_common(50):
                str_word_freq = str_word_freq + '{ ' + str(word) + ':' + str(frequency) + '}; '

            writer.writerow([IDs_List[i], str_word_freq])
            i += 1






            # Tokenization End


