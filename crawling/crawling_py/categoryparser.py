import requests
import re
from goose3 import Goose
# meta tag의 property의 article:section을 파싱하기 위한 클래스
class Parse_category:
    def __init__(self,url):
        req = requests.get(url, verify=False)
        self.raw = req.text
        self.category_names = ["정치","사회","경제"]
        self.policy = ["정치"] # 후에 정치 서브 카테고리를 채우자
        self.economy = ["경제"] # 후에 경제 서브 카테고리를 채우자
        self.society = ["사회","칼럼"] # 후에 사회 서브 카테고리를 채우자

    def parsing_category(self):
        head = re.search('<head.*</head>',self.raw,re.I|re.S)
        head = head.group()
        head = re.sub('<script.*?>.*?</script>','',head,0,re.I|re.S)#스크립트 제거
        head = re.sub('<link.*?/>','',head,0,re.I|re.S)# link제거
        categories = []
        meta1 = re.search('<meta property="article:section".*?/>', head,re.I|re.S)
        meta2 = re.search('<meta property="article:section2".*?/>', head,re.I|re.S)
        meta3 = re.search('<meta property="article:section3".*?/>', head,re.I|re.S)

        
        try:
            meta1 = meta1.group()
            categories.append(meta1)
        except:
            pass
        try:
            meta2 = meta2.group()
            categories.append(meta2)
        except:
            pass
        try:
            meta3 = meta3.group()
            categories.append(meta3)
        except:
            pass

        for meta in categories:
            
            meta = re.search('contents=".*"',meta,re.I|re.S)#content만 뺴오기
            meta = meta.group()
            print(meta)
            meta = re.search('".*"',meta,re.I|re.S) # content안의 내용물
            meta  = meta.group()
            meta = str(meta)
            meta = meta[1:len(meta)-1]
            print(meta)
            #print(meta)
            for society in self.society:
                if society in meta:
                    return self.category_names[1]
            for policy in self.policy:
                if policy in meta:
                    return self.category_names[0]
            for economy in self.economy:
                if economy in meta:
                    return self.category_names[2]
            
        return "no category"




if __name__ == "__main__":
    g = Goose()
    article = g.extract(url="https://www.donga.com/news/Economy/article/all/20210509/106835593/1")
    A = Parse_category(url="https://www.donga.com/news/Economy/article/all/20210509/106835573/1")
    print(A.parsing_category())




