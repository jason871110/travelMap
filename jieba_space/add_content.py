

site= []
result = []
with open('site.txt', 'r',encoding='utf-8') as fs:
    site = [line[:-1] for line in fs]
    #print(temp)
with open('results.txt', 'r',encoding='utf-8') as fr:
    result = [line[:-1] for line in fr]
print('read ok')
for r in result:
    for s in site:
        if(r==s):
            break
    else:
        site.append(r)

with open('site.txt','w',encoding='utf-8') as fw:
    for item in site:
        fw.write("%s\n" %item)
    
    