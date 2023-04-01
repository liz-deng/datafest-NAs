import string
import pandas
from collections import defaultdict

def read_file(file_name):
    with open(file_name, "r", errors='replace') as f:
        return f.readlines()
    
data = read_file("questionposts.csv")[1:]

processed = []

for line in data:
    try:
        Id, StateAbbr, QuestionUno, PostTextAndCreatedUtc = line.split(",", 3)
        PostTextAndCreatedUtc = PostTextAndCreatedUtc.split(",")
        CreatedtUtc = PostTextAndCreatedUtc[-1][1:-2]
        if len(PostTextAndCreatedUtc) > 2:
            PostTextAndCreatedUtc = "".join(PostTextAndCreatedUtc[:-1])
        else:
            PostTextAndCreatedUtc = PostTextAndCreatedUtc[0]
        PostText = PostTextAndCreatedUtc.lower().strip().translate(str.maketrans('', '', string.punctuation + "'"))
        processed.append([Id, StateAbbr, QuestionUno, PostText, CreatedtUtc])
    except:
        continue

df = pandas.DataFrame(processed, columns =['Id', 'StateAbbr', 'QuestionUno', 'PostTextProcessed', 'CreatedUtc'])
df.to_csv("questionpostsprocessed.csv", index=False)