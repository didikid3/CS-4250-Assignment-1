#-------------------------------------------------------------------------
# AUTHOR: Brandon Chao
# FILENAME: search_engine.py
# SPECIFICATION: Calculate tf.idf on a csv file
# FOR: CS 4250- Assignment #1
# TIME SPENT: 
#-----------------------------------------------------------*/

#IMPORTANT NOTE: DO NOT USE ANY ADVANCED PYTHON LIBRARY TO COMPLETE THIS CODE SUCH AS numpy OR pandas. You have to work here only with standard arrays

#importing some Python libraries
import csv

import math

documents = []
labels = []

#reading the data in a csv file
with open('collection.csv', 'r') as csvfile:
  reader = csv.reader(csvfile)
  for i, row in enumerate(reader):
         if i > 0:  # skipping the header
            documents.append (row[0])
            labels.append(row[1])



#Conduct stopword removal.
#--> add your Python code here
stopWords = {'I', 'and', 'She', 'They', 'her', 'their'}

splitWords = []   #Will be used to store the document information

for document in documents:
    newList = []
    word_list = document.split()
    for word in word_list:
        if word not in stopWords:
            newList.append(word)


    splitWords.append(newList)

#Conduct stemming.
#--> add your Python code here
steeming = {
  "cats": "cat",
  "dogs": "dog",
  "loves": "love",
}

for doc in splitWords:
    for i, word in enumerate(doc):
        if word in steeming:
            doc[i] = steeming[word]

#Identify the index terms.
#--> add your Python code here
terms = []
for doc in splitWords:
    for word in doc:
        if word not in terms:
            terms.append(word)

#Build the if-idf term weights matrix.
#--> add your Python code here
docMatrix = [ [0] * len(terms) for _ in range(len(documents))]
def term_frequency(term, doc):
    count = 0
    for word in doc:
        if word == term:
            count += 1
    return count / len(doc)
def document_frequency(term, docs):
    count = 0
    for document in docs:
        if term in document:
            count += 1
    return count
def inverse_document_frequency(term, docs):
    frequency = document_frequency(term, docs)
    return math.log( ( len(docs) / frequency ) ,10)
def tf_idx(term, doc, docs):
    tf = term_frequency(term, doc)
    idx = inverse_document_frequency(term, docs)
    return tf * idx

for row in range(len(documents)):
    for col in range(len(terms)):
        docMatrix[row][col] = tf_idx(terms[col], splitWords[row], splitWords)


#Calculate the document scores (ranking) using document weigths (tf-idf) calculated before and query weights (binary - have or not the term).
#--> add your Python code here
docScores = [0] * len(documents)
query = "cat and dogs".split()
newQuery = []

for word in query:
    if word not in stopWords:
        if word in steeming:
          newQuery.append(steeming[word])
        else:
          newQuery.append(word)


for word in newQuery:
    for i in range(len(documents)):
        docScores[i] += docMatrix[i][terms.index(word)]

print("Original Doucment")
print("-----------------")
print(documents, end = "\n\n")

print("Trimmed Documents")
print("-----------------")
print(splitWords, end = "\n\n")

print("Terms")
print("-----")
print(terms, end = "\n\n")

print("TF IDX Matrix")
print("-------------")
for row in docMatrix: print(row)
print()

print("Query")
print("-----")
print(newQuery)
print()

print("Document Scores")
print("---------------")
print(docScores, end = "\n\n")


#Calculate the precision and recall of the model by considering that the search engine will return all documents with weights >= 0.1.
#--> add your Python code 

result = []   #The 'window' of selected items

groundTruth = []

for i in range(len(docScores)):
    if docScores[i] >= .1:
        result.append(i)

for j in range(len(splitWords)):
    include = [False] * len(newQuery)
    for i in range(len(newQuery)):
        if newQuery[i] in splitWords[j]:
            include[i] = True
    
    for r in include:
        if not r:
            break
    else:
      groundTruth.append(j)

relevant_retrieved = []
relevant_notRetrieved = []
for i in groundTruth:
    if i in result:
        relevant_retrieved.append(i)
    else:
        relevant_notRetrieved.append(i)

irrelevant_retrieved = []
for i in result:
    if i not in groundTruth:
        irrelevant_retrieved.append(i)

print("All Relevant Documents")
print("----------------------")
for i in groundTruth: print(i+1, end=" ")
print("\n")
    
print("Retreived Documents")
print("-------------------")
for i in result: print(i+1, end=" ")
print("\n")

print("Relevant Retrieved:", len(relevant_retrieved))
print("Relevant not Retrieved:", len(relevant_notRetrieved))
print("Not Relevant Retrieved:", len(irrelevant_retrieved))
print()

print("Precision:", str( len(relevant_retrieved) / (len(relevant_retrieved) + len(irrelevant_retrieved)) ) )
print("Recall:", str( len(relevant_retrieved) / (len(relevant_retrieved) + len(relevant_notRetrieved)) ) )