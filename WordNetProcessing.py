import math
from collections import Counter
import csv
from nltk.corpus import wordnet
from sematch.semantic.similarity import WordNetSimilarity
import numpy as np


Top_Frequent_Words = []
Top_Frequencies = []
Top_Synonyms = []
AllParentWords = []
synonyms = []
AllSynonyms = []
AllLemmas = []
Syns = []
wns = WordNetSimilarity()
syns_temp = []


#reading from CSV most frequent words
with open('TokensWithSynonyms3.csv', encoding='utf-8') as csvfile:
    csv_reader: object = csv.reader(csvfile, delimiter=',')
    for row in csv_reader:
        try:
            if row[0] != 'Token':
                Top_Frequent_Words.append(row[0])
                Top_Frequencies.append(row[1])
                syns_temp = row[2].split("', '")
                syns_temp[0] = syns_temp[0].replace("['", "")
                syns_temp[len(syns_temp) - 1] = syns_temp[len(syns_temp) - 1].replace("']", "")

                AllParentWords.append(syns_temp)
                syns_temp = []
        except: pass

All_Statuses_Single_User = []
Statuses_List = []

with open('Filtered_results_top100_tweets.csv', encoding='utf-8') as csvfile:
    csv_reader: object = csv.reader(csvfile, delimiter=';')
    IDs_List = []
    Statuses_List = []
    for row in csv_reader:
        try:
            id_of_tweet = row[0]
            statuses_str = row[2]
            if id_of_tweet != 'ID':
                All_Statuses_Single_User = statuses_str.split("}}}{{{")
                All_Statuses_Single_User[0] = All_Statuses_Single_User[0].replace("{{{", "")
                All_Statuses_Single_User[len(All_Statuses_Single_User) - 1] = All_Statuses_Single_User[
                    len(All_Statuses_Single_User) - 1].replace("}}}", "")


                Statuses_List.append(All_Statuses_Single_User)

        except Exception as e:
            print(e)
            continue

#calculating TF-IDF of Method 1
    #Tf-IDF = TF x IDF
    #df
    #idf = log2 (N/df)
with open("Top 300 - All similarity matrices + results-2.txt", "w+") as text_file:
    Total_Num_of_Posts = 50000 #N
    IDF = []
    df_counter = 0
    for word in Top_Frequent_Words:
        for Statuses_Single_U in Statuses_List:
            for Single_Status in Statuses_Single_U:
                if word in Single_Status:
                    df_counter = df_counter + 1
        if df_counter == 0:
            IDF.append(0)
        else:
            IDF.append(math.log((Total_Num_of_Posts/df_counter),2))
        df_counter = 0



    SimilaritiesMatrix = []
    SimilarityRow = []


    SimilartiesMatrixTF_IDF = []
    SmilaritiesRow_TF_IDF = []

    SmilaritiesMatrixAdel = []
    SimilaritiesRowAdel = []

    i = 0

    #Print All Tokens along with Synonyms in a CSV File

    # with open('TokensWithSynonyms.csv', 'w+', newline='', encoding='utf-8') as result_file:
    #     wr = csv.writer(result_file, dialect='excel')
    #
    #     wr.writerow(['Token','Frequency','Synonyms'])
    #     m = 0
    #     while m < len(AllParentWords):
    #         wr.writerow([Top_Frequent_Words[m],Top_Frequencies[m],AllParentWords[m]])
    #         m = m + 1

    #Generating Similarities matrix by comparing all synonyms of tokken i with all synonyms of tokken j and getting the average of similarities
    sum = 0
    count = 0
    avg = 0
    max_frequency = Top_Frequencies[0]
    AdelMatrixtempValue = 0

    while i<len(AllParentWords)-1:
        j = i + 1
        while j<len(AllParentWords):
            for wordList1 in AllParentWords[i]:
                for wordList2 in AllParentWords[j]:
                    sum = sum + wns.word_similarity(wordList1, wordList2)
            count = len(AllParentWords[i])*len(AllParentWords[j])
            avg = sum / count
            SimilarityRow.append(avg)

            SmilaritiesRow_TF_IDF.append((IDF[i]+IDF[j]+avg)/3)

            AdelMatrixtempValue = (float(Top_Frequencies[i])/float(max_frequency)+ float(Top_Frequencies[j])/float(max_frequency) + avg)/3
            SimilaritiesRowAdel.append(AdelMatrixtempValue)
            sum = 0
            j = j + 1

        SimilaritiesMatrix.append(SimilarityRow)
        SimilartiesMatrixTF_IDF.append(SmilaritiesRow_TF_IDF)
        SmilaritiesMatrixAdel.append(SimilaritiesRowAdel)
        SimilarityRow = []
        SmilaritiesRow_TF_IDF = []
        SimilaritiesRowAdel = []
        i = i+1


    text_file.write("\nOriginal Similarity Matrix:-")
    text_file.write("\n%s" %SimilaritiesMatrix)

    #Getting the list of top 10 most similar combinations / tokens Similarity Matrix Original
    top = 0
    loops = 20
    maxvalues = []
    max_I = []
    max_J = []
    max = 0
    tempmaxI = -1
    tempmaxJ = -1
    similarityrowsindex = 0
    similarityvaluesindex = 0
    Top_10_Combinations = []
    Top_10_Combinations_FullList = []

    while top < loops:
            for SimilarityRow in SimilaritiesMatrix:
                for SimilarityValue in SimilarityRow:
                    if SimilarityValue > max:
                        max = SimilarityValue
                        tempmaxI = similarityrowsindex
                        tempmaxJ = similarityvaluesindex
                    similarityvaluesindex = similarityvaluesindex + 1
                similarityrowsindex = similarityrowsindex + 1
                similarityvaluesindex = 0
            similarityrowsindex = 0


            maxvalues.append(max)
            max_I.append(tempmaxI)
            max_J.append(tempmaxJ)

            combination = Top_Frequent_Words[tempmaxI]
            combination = combination + " x " + Top_Frequent_Words[tempmaxI + tempmaxJ + 1]
            Top_10_Combinations.append(combination)
            Top_10_Combinations_FullList.append(Top_Frequent_Words[tempmaxI])
            Top_10_Combinations_FullList.append(Top_Frequent_Words[tempmaxI + tempmaxJ + 1])

            SimilaritiesMatrix[tempmaxI][tempmaxJ] = 0
            max = 0
            tempmaxI = 0
            tempmaxJ = 0
            top = top +1

    #top topics is the most frequent repeated tokens in the list of
    text_file.write("\n%s" %Top_10_Combinations)
    word_counts = Counter(Top_10_Combinations_FullList)
    top_topics = word_counts.most_common(20)
    text_file.write("\n%s" %top_topics)

    text_file.write('\n---------------------------')
    text_file.write('\n---------------------------')
    text_file.write('\n\nTF-IDF Similarity Matrix:-')
    text_file.write("\n%s" %SimilartiesMatrixTF_IDF)



    #Getting the list of top 10 most similar combinations / tokens Similarity Matrix TF-IDF
    top = 0
    loops = 20
    maxvalues = []
    max_I = []
    max_J = []
    max = 0
    tempmaxI = -1
    tempmaxJ = -1
    similarityrowsindex = 0
    similarityvaluesindex = 0
    Top_10_Combinations = []
    Top_10_Combinations_FullList = []

    while top < loops:
            for SimilarityRow in SimilartiesMatrixTF_IDF:
                for SimilarityValue in SimilarityRow:
                    if SimilarityValue > max:
                        max = SimilarityValue
                        tempmaxI = similarityrowsindex
                        tempmaxJ = similarityvaluesindex
                    similarityvaluesindex = similarityvaluesindex + 1
                similarityrowsindex = similarityrowsindex + 1
                similarityvaluesindex = 0
            similarityrowsindex = 0


            maxvalues.append(max)
            max_I.append(tempmaxI)
            max_J.append(tempmaxJ)

            combination = Top_Frequent_Words[tempmaxI]
            combination = combination + " x " + Top_Frequent_Words[tempmaxI + tempmaxJ + 1]
            Top_10_Combinations.append(combination)
            Top_10_Combinations_FullList.append(Top_Frequent_Words[tempmaxI])
            Top_10_Combinations_FullList.append(Top_Frequent_Words[tempmaxI + tempmaxJ + 1])

            SimilartiesMatrixTF_IDF[tempmaxI][tempmaxJ] = 0
            max = 0
            tempmaxI = 0
            tempmaxJ = 0
            top = top +1

    #top topics is the most frequent repeated tokens in the list of
    text_file.write("\n%s" %Top_10_Combinations)
    word_counts = Counter(Top_10_Combinations_FullList)
    top_topics = word_counts.most_common(20)
    text_file.write("\n%s" %top_topics)

    text_file.write('\n---------------------------')
    text_file.write('\n---------------------------')
    text_file.write('\n\nAdel Similarity Matrix:-')
    text_file.write("\n%s" %SmilaritiesMatrixAdel)

    #Getting the list of top 10 most similar combinations / tokens Similarity Matrix Adel
    top = 0
    loops = 20
    maxvalues = []
    max_I = []
    max_J = []
    max = 0
    tempmaxI = -1
    tempmaxJ = -1
    similarityrowsindex = 0
    similarityvaluesindex = 0
    Top_10_Combinations = []
    Top_10_Combinations_FullList = []

    while top < loops:
            for SimilarityRow in SmilaritiesMatrixAdel:
                for SimilarityValue in SimilarityRow:
                    if SimilarityValue > max:
                        max = SimilarityValue
                        tempmaxI = similarityrowsindex
                        tempmaxJ = similarityvaluesindex
                    similarityvaluesindex = similarityvaluesindex + 1
                similarityrowsindex = similarityrowsindex + 1
                similarityvaluesindex = 0
            similarityrowsindex = 0


            maxvalues.append(max)
            max_I.append(tempmaxI)
            max_J.append(tempmaxJ)

            combination = Top_Frequent_Words[tempmaxI]
            combination = combination + " x " + Top_Frequent_Words[tempmaxI + tempmaxJ + 1]
            Top_10_Combinations.append(combination)
            Top_10_Combinations_FullList.append(Top_Frequent_Words[tempmaxI])
            Top_10_Combinations_FullList.append(Top_Frequent_Words[tempmaxI + tempmaxJ + 1])

            SmilaritiesMatrixAdel[tempmaxI][tempmaxJ] = 0
            max = 0
            tempmaxI = 0
            tempmaxJ = 0
            top = top +1

    #top topics is the most frequent repeated tokens in the list of
    text_file.write("\n%s" %Top_10_Combinations)
    word_counts = Counter(Top_10_Combinations_FullList)
    top_topics = word_counts.most_common(20)
    text_file.write("\n%s" %top_topics)



    # Old way to compare between lists
    # i = 0
    # while i<len(AllParentWords)-1:
    #     j = i + 1
    #     while j<len(AllParentWords):
    #         for word in AllParentWords[i]:
    #             if word not in combinedwords:
    #                 combinedwords.append(word)
    #         for word in AllParentWords[j]:
    #             if word not in combinedwords:
    #                 combinedwords.append(word)
    #
    #         k = 0
    #         sum = 0
    #         count = (len(combinedwords) * (len(combinedwords) -1)) / 2
    #         while k < len(combinedwords)-1:
    #             l = k + 1
    #             while l< len(combinedwords):
    #                 similarity = wns.word_similarity(combinedwords[k], combinedwords[l])
    #                 sum = sum + similarity
    #                 l = l + 1
    #             k = k + 1
    #         SimilarityRow.append(sum / count)
    #         combinedwords = []
    #         j = j + 1
    #     SimilaritiesMatrix.append(SimilarityRow)
    #     SimilarityRow = []
    #     i = i + 1
    #
    # print(SimilaritiesMatrix)

    # str1 = 'woman'
    # str2 = 'girl'
    #strlst = ['woman', 'girl']
    # print(wns.word_similarity(str1, str2))
    # print(wns.word_similarity('woman', 'girl'))
