import sqlite3

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def bow_cosine(s1, s2):
    vectorizer = CountVectorizer()
    vectorizer.fit([s1, s2])
    X = vectorizer.transform([s1, s2])  # Get the vector of s1 and s2 represented by bag of words
    #print(X.toarray())
    a = cosine_similarity(X[0], X[1])
    b = a[0].tolist()
    print(b[0])
    #print(type(b[0]))

    #print(cosine_similarity(X[0], X[1]))

def way():
    datalist = []
    conn = sqlite3.connect("Jaktent.db")
    cur = conn.cursor()
    sql = "select content from content"
    data = cur.execute(sql)
    for item in data:
        datalist.append(item[0])
    cur.close()
    conn.close()
    # print(datalist)
    # for item in datalist :
    #     print(item)
    data = []
    for i in range(len(datalist)):
        for j in range(i+1,len(datalist)):
            bow_cosine(datalist[i],datalist[j])

way()