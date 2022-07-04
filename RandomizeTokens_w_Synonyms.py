import csv
import random

Tokens = []
Frequencies = []
Synonyms = []
new_Synonyms = []
with open('TokensWithSynonyms.csv', encoding='utf-8') as csvfile:
    csv_reader: object = csv.reader(csvfile, delimiter=',')


    for row in csv_reader:
        try:
            if row[0] != 'Token':
                Tokens.append(row[0])
                Frequencies.append(row[1])
                Synonyms.append(row[2])
        except Exception as e:
            print(e)
            continue
    All_Synonyms_Single_User = []
    i = 0
    for Syn in Synonyms:
        All_Synonyms_Single_User = Syn.split("', '")
        All_Synonyms_Single_User[0] = All_Synonyms_Single_User[0].replace("{'", "")
        All_Synonyms_Single_User[len(All_Synonyms_Single_User) - 1] = All_Synonyms_Single_User[
            len(All_Synonyms_Single_User) - 1].replace("'}", "")
        random.shuffle(All_Synonyms_Single_User)
        if Tokens[i] in All_Synonyms_Single_User:
            All_Synonyms_Single_User.remove(Tokens[i])
        All_Synonyms_Single_User.insert(0, Tokens[i])

        new_Synonyms.append(All_Synonyms_Single_User)
        All_Synonyms_Single_User = []
        i = i+1

with open('TokensWithSynonyms2.csv', 'w+', newline='', encoding='utf-8') as result_file:
    wr = csv.writer(result_file, dialect='excel')

    wr.writerow(['Token','Frequency','Synonyms'])
    m = 0
    while m < len(Tokens):
        wr.writerow([Tokens[m],Frequencies[m],new_Synonyms[m]])
        m = m + 1