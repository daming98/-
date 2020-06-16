import urllib.request
import chardet
import re

def get_artical(url):
    
    response = urllib.request.urlopen(url)

    html = response.read()
    chardit1 = chardet.detect(html)
    #print(chardit1)

    html=html.decode(chardit1['encoding'])

    #print(html)

    pattern = re.compile("<p.*?</P>" ,re.S)
    pattern2 = re.compile("<h2.*?>.*?</h2>" ,re.S)
    pattern3 = re.compile("<span class=\"time.*?</span>" ,re.S)
    #pattern = re.compile("<div.*?class=\"articalContent.*?\">" ,re.S)
    title=re.search(pattern2, html).group()
    time=re.search(pattern3, html).group()
    index1=title.find(">")
    index2=title.find("</h2>")
    title=title[index1+1:index2]
    time=time[-28:-7]
    ps=re.findall(pattern, html)
    #print(ps)
    '''
    for i in ps:
        f=i.replace("\n", "").replace("<p>", "").replace("</P>", "")
        print(f)

    '''
    artical=[]
    for i in ps:
        #f=i
        f=i.replace("&nbsp;<wbr>", "").replace("\n", "").replace("<p>", "").replace("</P>", "")
        if "<" in f:
            pass
        elif f=="" or f=="\n":
            pass
        else:
            artical.append(f)
    
    dic={}
    dic["title"]=title
    dic["time"]=time
    dic["artical"]=artical
    return dic

def get_url_list(start):
    url=start
    url_list=[]
    url_list.append(url)
    while True:
        print("访问："+url)
        response = urllib.request.urlopen(url)
        html = response.read()
        chardit1 = chardet.detect(html)
        #print(chardit1)
        html=html.decode(chardit1['encoding'])
        #print(html)
        #url_list.append(url)
        pattern = re.compile("前一篇：</span.*?a href=.*?>.*?</a>" ,re.S)
        next=re.search(pattern, html)
        if next:
            next=next.group()
            index1=next.find("href=")
            index2=next.find("\">")
            next=next[index1+6:index2]
            url_list.append(next)
            print("找到了："+next)
            url=next
        else:
            break
    print(url_list)
    return url_list

start="http://blog.sina.com.cn/s/blog_54bc9edd0102xrnl.html"

url_list=get_url_list(start)

for i in url_list:
    dic=get_artical(i)
    with open("OcarinaBlog.txt", 'a+') as f:
        f.write(dic["title"]+"\n")
        f.write(dic["time"]+"\n")
        f.write(i+"\n")
        for j in dic["artical"]:
            f.write(j+"\n")
        #f.writelines(dic["artical"])
        f.write("\n\n")
        print(dic["title"])
    