import csv
import spacy

types = []
Hot_Words = []
Hot_Words_AllTypes = []

with open('word2vec-topics.csv', encoding='utf-8') as csvfile:
    csv_reader: object = csv.reader(csvfile, delimiter=';')

    for row in csv_reader:
        try:
            types.append(row[0])
            Hot_Words = row[1].split("','")
            Hot_Words[0] = Hot_Words[0].replace("['", "")
            Hot_Words[len(Hot_Words) - 1] = Hot_Words[len(Hot_Words) - 1].replace("']", "")
            Hot_Words_AllTypes.append(Hot_Words)
        except Exception as e:
                print(e)
                continue

nlp = spacy.load('en_core_web_lg')
nlp(u'word1').similarity(nlp(u'word2'))

SimilarityRow = []
SimilarityMatrix = []

SimilarityRow_wText = []
SimilarityMatrix_wText = []

types_count = 0
for Hot_Words in Hot_Words_AllTypes:
    i = 0
    while i < len(Hot_Words) - 1:
        j = i + 1
        while j < len(Hot_Words):
            if not Hot_Words[i] == Hot_Words[j]:
                similarity_temp = nlp(Hot_Words[i]).similarity(nlp(Hot_Words[j]))
                SimilarityRow.append(similarity_temp)
                SimilarityRow_wText.append(str(similarity_temp) + " ("+Hot_Words[i]+" X "+Hot_Words[j]+")")
            j = j + 1
        SimilarityMatrix.append(SimilarityRow)
        SimilarityMatrix_wText.append(SimilarityRow_wText)
        SimilarityRow = []
        SimilarityRow_wText = []
        i = i + 1

    print(types[types_count])
    print(SimilarityMatrix)
    print(SimilarityMatrix_wText)
    print("==============================================")
    print("==============================================")
    types_count = types_count+1
    SimilarityMatrix = []
    SimilarityMatrix_wText = []
