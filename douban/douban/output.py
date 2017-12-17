import json


def readMovieJson():
    inFile = open("D:\Users\Simon\movie250\items.json", 'r', 0)
    text = inFile.read()  # text是str
    movie_dict = json.loads(text)  # movie_dict是list
    for movie in movie_dict:  # movie是dict
        rank = movie["rank"][0]  # rank等都是Unicode
        title = movie["title"][0]
        link = movie["link"][0]
        star = movie["star"][0]
        rate = movie["rate"][0]
        if movie["quote"]:
            quote = movie["quote"][0]
        else:
            quote = "暂无".decode("utf-8")

        # str和Unicode不能混用，要么将Unicode类型encode为其他编码，
        # 要么将str类型decode为其他编码
        # python的内部使用Unicode，str如“电影： ”是字节串，由Unicode
        # 经过编码(encode)
        # 后的字节组成的
    # 与下句不同的另一种组合字符串方式：print "电影: " + title.encode("utf-8")
    print "top".decode("utf-8") + rank + ".".decode("utf-8") + \
          title + " 评分".dec1ode("utf-8") + star + \
          '('.decode("utf-8") + rate + ')'.decode("utf-8") + \
          "\n链接：".decode("utf-8") + link + \
          "\n豆瓣评论：".decode("utf-8") + quote + "\n"


