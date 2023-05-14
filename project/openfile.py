def pickup():
    with open('keyword.txt',mode='r',encoding='utf-8') as file:
        keywords = file.readlines()
        for i in range(len(keywords)):
            keywords[i]=keywords[i].replace('\n','')
    return keywords+pickup3()+pickup4()

def pickup2():
    with open('keyword_2.txt',mode='r',encoding='utf-8') as file:
        keywords_2 = file.readlines()
        for i in range(len(keywords_2)):
            keywords_2[i]=keywords_2[i].replace('\n','')
    return keywords_2

def pickup3():
    keywords_2= pickup2()
    new = []
    with open('keyword_3.txt',mode='r',encoding='utf-8') as file:
        keywords_3 = file.readlines()
        for i in range(len(keywords_3)):
            keywords_3[i]=keywords_3[i].replace('\n','')
        tmp='_'
        for i in range(len(keywords_2)):
            for j in range(len(keywords_3)):
                keywords_3[j]=keywords_3[j].replace(tmp,keywords_2[i])
            tmp = keywords_2[i]
            new+=keywords_3
    return new

def pickup4():
    keywords_2= pickup2()
    new = []
    with open('keyword_3.txt',mode='r',encoding='utf-8') as file:
        keywords_3 = file.readlines()
        for i in range(len(keywords_3)):
            keywords_3[i]=keywords_3[i].replace('\n','')
        for i in range(len(keywords_2)):
            keywords_2[i]=keywords_2[i].replace('客家','')
        tmp='_'
        for i in range(len(keywords_2)):
            for j in range(len(keywords_3)):
                keywords_3[j]=keywords_3[j].replace(tmp,keywords_2[i])
            tmp = keywords_2[i]
            new+=keywords_3
    return new
def pickup_img(text):
    dict1 = {
        '客家鹹湯圓':'https://etaiwan.blog/wp-content/uploads/20171222014903_81.jpg',
        '客家菜包':'https://tokyo-kitchen.icook.network/uploads/recipe/cover/183051/be1b55497e28f2b5.jpg',
        '客家擂茶':'https://i2.wp.com/cdn02.pinkoi.com/wp-content/uploads/sites/7/2021/06/02152858/6.jpeg?resize=1024%2C683&ssl=1',
        '客家鹹豬肉':'https://d3l76hx23vw40a.cloudfront.net/recipe/webp/whk088-025a.webp',
        '客家小炒':'https://tokyo-kitchen.icook.network/uploads/recipe/cover/246719/cc263a64dcaba612.jpg',
        '客家粄條':'https://d3l76hx23vw40a.cloudfront.net/recipe/webp/bk164-038.webp'
    }
    return dict1[text]
if __name__ == '__main__':
    print(pickup())