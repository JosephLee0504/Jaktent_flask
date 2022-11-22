# Term Frequency Analysis

import sqlite3
from matplotlib import pyplot as plt
from wordcloud import WordCloud
from PIL import Image
import  numpy as np
from nltk import sent_tokenize,word_tokenize,pos_tag
def movie():
    datalist = []
    conn = sqlite3.connect("Jaktent.db")
    cur = conn.cursor()
    sql = "select content from content "
    data = cur.execute(sql)
    for item in data:
            #print(item[0])
            datalist.append(item[0])
    s = ",".join(datalist)
    list = s.split()
    #print(s)
    dic = {}
    for i in list:
        count = list.count(i)
        dic[i] = count
    #print(dic)
    cur.close()
    conn.close()

    img = Image.open(r'.\static\assets\img\tree.jpg')
    img_array = np.array(img)
    wc = WordCloud(
         background_color='white',
         mask = img_array,
         font_path="BASKVILL.TTF"
     )
    wc.generate_from_text(s)

    # Draw figures
    fig = plt.figure(1)
    plt.imshow(wc)
    plt.axis('off')  # Whether to display the axes

    plt.show() # Show generated word cloud

    plt.savefig(r'.\static\assets\img\word.jpg',dpi = 1600)
movie()