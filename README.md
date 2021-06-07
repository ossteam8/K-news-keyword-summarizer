# oss8_proj

## 프로젝트 설명
**우리 프로젝트는 일주일 간의 기사를 크롤링 한 뒤, 그 기사들의 카테고리별(정치, 경제, 사회)로 키워드를 뽑아 top keywords를 뽑아 줍니다.
top keywords를 뽑기 위하여 LDA와 TextRank를 결합해 활용합니다. 이를 시각화해서 보여주기 위해, Django를 사용하여 각 날마다의 크롤링한 뉴스의 총 개수와 각 카테고리별 키워드의 가중치를 차트를 이용하여 보여줍니다
또한 그 키워드 가중치 차트를 클릭하면 키워드에 맞는 뉴스들 리스트를 보여주며, 원본 url과 요약본을 보여줍니다**


## Running project
### Software environment
**OS : UBUNTU Lts 20.04** 

**Python version==3.8.5**

**Django version==3.2.4**

**If you have crontab error then check your OS** first. 

If you use Windows, crontab doesn't support Windows. So you must use Linux OS for using crontab. 

Also our python may not support python version under python3. We wish you use python version over 3.**

### Before running our project 
**Django version 3.2.4 and mysql for viewing and saving data, BeautifulSoup4 and Goose3 for crawling
and LDA in gensim and TextRank to extract keywords**  

### We wish you read our [requirements.txt](requirements.txt) for install packages
### In order to install **Mecab** please use the line below at your terminal
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

**Then you can use the website. But first you may not have any data of crawling, keywords.  
Our project start crawling, and find keywords at 0:00 every day.  
So just wait until 0:00 then it will start doing jobs with crontab.  
Finishing this job, now you can see the website with data.**

## Contribution guidelines
**IF you want to contribute to our project, be sure to review the 
[contribution guidelines](CONTRIBUTING.md).
This project adheres to [code_of_conduct](CODE_OF_CONDUCT.md). 
By participating, we are expected to read these two md.**

**We use [GitHub issues](https://github.com/ossteam8/oss8_proj/issues) for 
tracking requests, bugs, and enhance our project.
So if you have an issue of project, then make and submit new issue.**

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

