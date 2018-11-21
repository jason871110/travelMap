import jieba
import os
from django.conf import settings
my_dict_path = os.path.join(settings.BASE_DIR, 'jieba_space/my_dict.txt')
site_path = os.path.join(settings.BASE_DIR, 'jieba_space/site.txt')

def find_sites(sentence):
    jieba.load_userdict(my_dict_path)
    useless_word=[' ','，','!','！','。','、','\n','\"','＂','（','）','～','～','也','的','和','與','在','再']
    words = jieba.cut(sentence, cut_all=False)
    reduced_word = []
    for w in words:
        for u in useless_word:
            if(w == u):
                break
        else:
            reduced_word.append(w)

    temp= []
    result = []
    with open(site_path, 'r') as f:
        temp = [line[:-1] for line in f]
        #print(temp)
    for w in reduced_word:
        for t in temp:
            if(w==t):
                if(result):
                    for check in result:
                        if(w==check):
                            break
                    else:
                        result.append(w)
                else:
                    result.append(w)
                break
    #print(result)
    return result 