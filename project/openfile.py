def pickup():
    with open('keyword.txt',mode='r',encoding='utf-8') as file:
        keywords = file.readlines()
        for i in range(len(keywords)):
            keywords[i]=keywords[i].replace('\n','')
    print(keywords)
    return keywords