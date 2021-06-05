# oss8_proj

## 프로젝트 설명
**우리 프로젝트는 일주일 간의 기사를 크롤링 한 뒤, 그 기사들의 카테고리별(정치, 경제, 사회)로 키워드를 뽑아 top keywords를 뽑아 줍니다.
top keywords를 뽑기 위하여 (무엇을 이용)이를 시각화해서 보여주기 위해, Django를 사용하여 각 날마다의 크롤링한 뉴스의 총 개수와 각 카테고리별 키워드의 가중치를 차트를 이용하여 보여줍니다
또한 그 키워드 가중치 차트를 클릭하면 키워드에 맞는 뉴스들 리스트를 보여주며, 원본 url과 요약본을 보여줍니다** => 이부분 더 설명 필요함


## Running project
### before running our project 
**we use Django version 3.2.4 and mysql for viewing and save data, use BeautifulSoup4 and goose3 for crawling
and we use (여기에 키워드랑 요약에 쓰이는 것들 적어야할듯)**  
**so if you want to run our project you need some packages.**  
### We wish you read our [requirements.txt](requirements.txt) for install packages


### After install packages
**you must create secrets.json and my_settings.py in same locate of manage.py
In secrets.json, you must write SECRET_KEY. Like:**
```python
{
    "SECRET_KEY" : "your secret key"
}
```
**In my_settings.py, you must write information of DATABASE. Like:**
```python
DATABASES = {
    'default': { 
        'ENGINE':'django.db.backends.mysql', # mysql engine
        'NAME':'oss', # database name
	'USER':'root', # user name when connected database
	'PASSWORD':'PASSWORD',# user password
        'HOST':'127.0.0.1', # database server address
        'PORT':'3306' # database server port
    }
}
```

## Contribution guidelines
**IF you want to contribute to our project, be sure to review the 
[contribution guidelines](CONTRIBUTING.md).
This project adheres to [code_of_conduct](CODE_OF_CONDUCT.md). 
By participating, we are expected to read these two md.**

**We use [GitHub issues](https://github.com/ossteam8/oss8_proj/issues) for 
tracking requests, bugs, and enhance our project.
So if you have an issue of project, then make and submit new issue.**

## Contributors list
 **- [Choi Jaeeun](https://github.com/jjaen0823)**  
 **- [linkyouhj](https://github.com/linkyouhj)**  
 **- [Chae Hui Seon](https://github.com/chaehuiseon)**  
 **- [namhyo01](https://github.com/namhyo01)**    

## License
**[MIT License](LICENSE)**



### sites for using crawling
 - [중앙일보](https://joongang.joins.com/)
 - [한겨레](https://www.hani.co.kr/arti/list.html)
 - [헤럴드경제](http://biz.heraldcorp.com/)
 - [아시아경제](https://www.asiae.co.kr/)
 - [국민일보](http://www.kmib.co.kr/news/index.asp)
 - [경향신문](http://www.khan.co.kr/)
 - [머니투데이](https://www.mt.co.kr/)
 - [동아일보](https://www.donga.com/)
 - [YTN](https://www.ytn.co.kr/)
 - [내일신문](https://www.naeil.com/)

