import csv
import ast

from build_vocab import to_pickle


with open('../BokeScraping/output.csv') as f:
    h = next(csv.reader(f))
    reader = csv.reader(f)
    cnt = 0
    text_list = []
    imagepath_list = []
    for row in reader:
        cnt += 1
        if row == ['bokes', 'image_url', 'number']:
            continue
        dic = eval(row[0][1:-1])
        text_list.append(dic['text'])
        imagepath_list.append(row[1])


to_pickle('./data/text_list.pkl', text_list)

to_pickle('./data/imagepath_list.pkl', imagepath_list)


