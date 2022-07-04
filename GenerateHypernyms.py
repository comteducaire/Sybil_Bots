import csv
from nltk import wordnet as wn

Top_Frequent_Words = []
Hypernyms = []
with open('MostFrequentWords.csv', encoding='utf-8') as csvfile:
    csv_reader: object = csv.reader(csvfile, delimiter=',')


    for row in csv_reader:
        try:
            Top_Frequent_Words.append(row[0])
        except Exception as e:
            print(e)
            continue

i = 0
Hypernyms_singletoken = []
while i < len(Top_Frequent_Words):
    synsets = wn.wordnet.synsets(Top_Frequent_Words[i])
    if len(synsets)>0:
        for synset in synsets:
            for hypernym in synset.hypernyms():
                Hypernyms_singletoken.append(hypernym.name())
        Hypernyms.append(Hypernyms_singletoken)
        Hypernyms_singletoken = []
    else: Hypernyms.append("")
    i = i + 1

#print(wn.wordnet.synset('politics.n.01').lowest_common_hypernyms(wn.wordnet.synset('president.n.01')))

#Print All Tokens along with Hypernyms in a CSV File
with open('TokensWithHypernyms.csv', 'w+', newline='', encoding='utf-8') as result_file:
    wr = csv.writer(result_file, dialect='excel')

    wr.writerow(['Token','Hypernyms'])
    m = 0
    while m < len(Top_Frequent_Words):
        wr.writerow([Top_Frequent_Words[m],Hypernyms[m]])
        m = m + 1