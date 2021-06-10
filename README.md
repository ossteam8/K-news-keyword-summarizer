# K-news keyword summarizer
![license badge](https://img.shields.io/github/license/ossteam8/K-news-keyword-summarizer)
![python version badge](https://img.shields.io/badge/python-3.8-red)
## 프로젝트 설명
우리 프로젝트는 일주일 간의 기사를 크롤링 한 뒤, 카테고리별(정치, 경제, 사회)로 `top keywords`를 뽑아주고 기사를 요약합니다.

`top keywords`는 `LDA`와 `TextRank` 알고리즘을 결합해 활용합니다. 

`Django`를 사용하여 크롤링한 뉴스의 총 개수와 각 카테고리에서 키워드별 뉴스 개수 차트를 시각화합니다.

또한 그 키워드 차트를 클릭하면 키워드에 맞는 뉴스들을 나열하며, 원본 url과 요약본을 보여줍니다.

## 프로젝트 실행 예시
### main page
![mainpage](https://user-images.githubusercontent.com/34156840/121178743-d2f8bc00-c899-11eb-9a82-888ed68bde9c.png)
### category politics
![category_chart](https://user-images.githubusercontent.com/34156840/121184087-b2336500-c89f-11eb-9e0c-81bbbf13ab59.png)
![category_article](https://user-images.githubusercontent.com/34156840/121182781-62a06980-c89e-11eb-9064-060c873b354e.png)
### category's topic 5
![topic5](https://user-images.githubusercontent.com/34156840/121183351-efe3be00-c89e-11eb-89b7-a83cb4ae976a.png)
### article summary
![summary](https://user-images.githubusercontent.com/34156840/121185447-0ab73200-c8a1-11eb-983e-a48286aed534.png)


## Running project
### Software environment
**OS : UBUNTU Lts 20.04** 

**Python version==3.8.5**

**Django version==3.2.4**

If you have crontab error then **check your OS** first. 

**`crontab` does not support Windows**. So you must use **Linux OS** to use crontab. 

Also our project may not support python version under python3. We wish you use python version over 3.**

### Before running our project 
Django version 3.2.4 and mysql for viewing and saving data, BeautifulSoup4 and Goose3 for crawling
and LDA in gensim and TextRank to extract keywords  

**We wish you to read our [requirements.txt](requirements.txt) for installing packages**
### Installing **Mecab** 
Use the line below at your terminal
```
$ bash <(curl -s https://raw.githubusercontent.com/konlpy/konlpy/master/scripts/mecab.sh)
```
### After installing packages
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
**After setting these two files, now you have to do migrate**  
```
 $ python3 manage.py makemigrations 
```

```
 $ python3 manage.py migrate
```

**If you finish these migrate without errors then run server**  
```
 $ python3 manage.py runserver
```

Now you can use the website. But you may not have any news data and keywords.  
  
Our project use django-crontab for **crawling and keyword extractor job**  at particular time everyday.
Our project do crawling at 00:00 and keyword extract at 01:00.  Of course, you can change time by modifiy settings.py.  
```python
CRONJOBS = [
    ('0 0 * * *', 'crawling.cron.article_crawling_job', '>> log file location'),
    ('0 1 * * *', 'keywords.cron.lda_job', '>> log file location'),
]
```
change here and you can run program when you want. **But don't pull pull-request with changing time**

## Keyword Extractor 
`LDA` and `TextRank` algorithm combined
[README_keyword.md](README_keyword.md)

## Summarizer
`TextRank` algorithm implemented 
[README_summarize.md](README_summarize.md)

## Contribution guidelines
IF you want to contribute to our project, be sure to review the 
[contribution guidelines](CONTRIBUTING.md).
This project adheres to [code_of_conduct](CODE_OF_CONDUCT.md). 
By participating, we are expected to read these two md.

We use [GitHub issues](https://github.com/ossteam8/oss8_proj/issues) for 
tracking requests, bugs, and enhance our project.
So if you have an issue of project, then make and submit new issue.

## Contributors list
 - [Choi Jaeeun](https://github.com/jjaen0823)  
 - [linkyouhj](https://github.com/linkyouhj)  
 - [Chae Hui Seon](https://github.com/chaehuiseon)  
 - [namhyo01](https://github.com/namhyo01)    

## License
**[MIT License](LICENSE)**



### Websites used in crawling
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

