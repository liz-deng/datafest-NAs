import string
import pandas
from collections import defaultdict

def read_file(file_name):
    with open(file_name, "r", errors='replace') as f:
        return f.readlines()
    
# data = read_file("datamerged.csv")[1:]
# stopwords = {'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him',              'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its',              'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what',              'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am',              'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has',              'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the',              'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of',              'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into',              'through', 'during', 'before', 'after', 'above', 'below', 'to',              'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under',              'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where',              'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most',              'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same',              'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don',              'should', 'now'}
# add_stopwords = {"would", "get", "need", "help", "also", "may", "need", "know", "make", "one", "want", "take", "time", "case", "information", "since",
#                  "could", "back", "like", "name", "law", "told", "take", "home", "new", "back", "dont", "amount", "said", "even", "able", "see", "still",
#                  "find", "give", "month", "without", "filed", "going", "best", "free", "luck", "please", "let"}
# stopwords = stopwords.union(add_stopwords) # 168
# processed = defaultdict(lambda: defaultdict(float))
# sm = defaultdict(float)

# for line in data:
#     try:
#         Index, Category, PostText = line.split(",", 3)
#         texts = PostText.split(" ")

#         # if len(texts) > 1:
#         #     for i, j in zip(texts, texts[1:]):
#         #         text1 = i.strip().translate(str.maketrans('', '', string.punctuation + "'\""))
#         #         text2 = j.strip().translate(str.maketrans('', '', string.punctuation + "'\""))
#         #         if text1 not in stopwords and len(text1) > 2 and text2 not in stopwords and len(text2) > 2:
#         #             processed[Category][text1 + " " + text2] += 1
#         #             sm[Category] += 1

#         if len(texts) > 2:
#             for i, j, k in zip(texts, texts[1:], texts[2:]):
#                 text1 = i.strip().translate(str.maketrans('', '', string.punctuation + "'\""))
#                 text2 = j.strip().translate(str.maketrans('', '', string.punctuation + "'\""))
#                 text3 = k.strip().translate(str.maketrans('', '', string.punctuation + "'\""))
#                 if text1 not in stopwords and len(text1) > 2 and text2 not in stopwords and len(text2) > 2 and text3 not in stopwords and len(text3) > 2:
#                     processed[Category][text1 + " " + text2 + " " + text3] += 1
#                     sm[Category] += 1

#         # for i in texts:
#         #     text = i.strip().translate(str.maketrans('', '', string.punctuation + "'\""))
#         #     if text not in stopwords and len(text) > 2:
#         #         processed[Category][text] += 1
#     except:
#         continue

# for category, token_dict in processed.items():
#     for i, j in token_dict.items():
#         token_dict[i] /= sm[category]
#     print(category)
#     num = 20
#     top_items = sorted(token_dict.items(), key=lambda x: x[1], reverse=True)[:num]

#     for item in top_items:
#         print(item[0], ":", "{:.4f}".format(item[1]))
#     print()

def ExportEthnic_Category():

    df = pandas.read_csv("clients.csv")[["EthnicIdentity", "ClientUno"]]
    df2 = pandas.read_csv("questions.csv")[["AskedByClientUno", "Category"]]
    df2 = df2.join(df.set_index(["ClientUno"]), on=["AskedByClientUno"])

    count = defaultdict(lambda: defaultdict(float))
    sm = defaultdict(float)

    aim = ["african american", "caucasian", "latino or hispanic"]
    for _, i in df2.iterrows():
        l = i["EthnicIdentity"]
        for j in str(l).split(","):
            if j.lower().strip() in aim:
                count[j.lower().strip()][i["Category"]] += 1.0
                sm[j.lower().strip()] += 1.0
                break

    for i, j in count.items():
        print(i, j)

    li = []
    for i, j_dict in count.items():
        for j, k in j_dict.items():
            li.append([i, j, k / sm[i]])

    print(li)

    df = pandas.DataFrame(li, columns =["EthnicIdentity", "Category", "Count"])
    df.to_csv("EthnicIdentity_Category.csv", index=False)

aim = ["african american", "caucasian", "latino or hispanic"]
cnt = 0
for i in df["EthnicIdentity"]:
    k = 0
    for j in str(i).split(","):
        if j.lower().strip() in aim:
            k = 1
        count[j.lower().strip()] += 1
    cnt += k
print(cnt)
print(sorted(count.items(), key=lambda x: x[1], reverse=True))

li = []
for i, j in sorted(count.items(), key=lambda x: x[1], reverse=True):
    li.append([i, j])

df = pandas.DataFrame(li, columns =["EthnicIdentity", "Count"])
df.to_csv("EthnicIdentity.csv", index=False)