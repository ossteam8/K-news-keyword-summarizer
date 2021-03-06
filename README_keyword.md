# Abstract
### Korean keyword extractor
Combined LDA and TextRank Algorithm 

3908개의 뉴스 기사 본문 데이터들을 대상으로 키워드를 추출합니다.
전처리 과정에서는 노동 집약적으로 만들어진 [불용어사전](keywords/keywords_extract/stop.txt)와 `사용자사전`을 이용하였습니다.
```LDA``` 알고리즘을 먼저 적용해 relevance에 기반한 ```top-20 keyword```를 추출합니다. 
이후 각 토픽에 기여하는 문서들에서 추출한 키워드들을 포함하는 문장들에 대해 ```TextRank``` 알고리즘을 재적용합니다.

# Running project 
install [requirements.txt](keywords/keywords_extract/requirements.txt)

Installing `Mecab` 

Use the line below at your terminal
```
bash <(curl -s https://raw.githubusercontent.com/konlpy/konlpy/master/scripts/mecab.sh)
```

## Actual Running
### Required
1. Articles
```["article1","article2",...,"articleN"]``` type: list
2. Id of Articles
```[1,2,3,4,...,N]``` type: list
does not need to be in-order
3. stop.txt
a,is,...,@@@ -> distinguished by commas(,) in .txt file

**[stop.txt](keywords/keywords_extract/stop.txt)** is prepared and provided by [linkyouhj](https://github.com/linkyouhj) and [Chae Hui Seon](https://github.com/chaehuiseon)

### For demo
```
python3 app.py
```
This will run with sample data (about 4000 news articles and id)

# Keyword Extracting
Reference: [https://www.koreascience.or.kr/article/JAKO202028851207548.pdf](https://www.koreascience.or.kr/article/JAKO202028851207548.pdf)

Below is the Keyword-Extracting process
1. LDA 
2. Choose news article's sentences which contributes to each topics
3. TextRank


## Preprocessing
### [preprocessor.py](keywords/keywords_extract/preprocessor.py)

LDA토픽 모델링을 위해 다음과 같은 순서로 문서들을 전처리한다.

```
(1) 명사 추출 => (2) 불용어 제거 => (3) N-gram
```

먼저, 전처리를 위해 입력되는 문서(뉴스 기사들)는 ```["기사1","기사2","기사3",....,"기사N"]```의 형식이다.

명사 추출은 한글 형태소 분석기 ```Mecab```을 사용한다.

사용자 단어 사전을 구축하여 형태소 분석이 잘 되지 않아 추출되지 않는 명사를 잘 인식할 수 있도록 돕는다.

[사용자 단어 사전 설치 방법 ] 

(http://blog.naver.com/PostView.nhn?blogId=shino1025&logNo=222179854044&categoryNo=44&parentCategoryNo=0&viewDate=&currentPage=1&postListTopCurrentPage=1&from=search)

사용자 단어 사전 적용 방법 :

(1) nnp.csv, user-nnp.csv 다운

[nnp.csv](https://github.com/ossteam8/LDA-TextRank-keyword/blob/main/nnp.csv)

[user-nnp.csv](https://github.com/ossteam8/LDA-TextRank-keyword/blob/main/user-nnp.csv)


(2)
```
cd mecab-ko-dic-2.1.1-20180720/user-dic

open .
```
파인더가 열리면 다운받은 nnp.csv파일을 기존 파일에 덮어 씌움.

(3)
```
cd ../tools
sh add-userdic.sh
cd ..
make clean
make install
```
(4)
```
open .
```
파인더가 열리면 다운받은 user-nnp.csv파일을 기존 파일에 덮어 씌움.
```
make clean
make install
```

다음으로 불용어로 판단되는 단어들을 삭제 한다.

마지막으로 복합명사를 처리하고, 뉴스 기사에 자주 등장하는 단어 중에, 연속적으로 의미 있는 단어로 구성된 문구를 처리하기 위해 ```N-gram```으로 토큰화하여 코퍼스를 준비한다.



## LDA
### [LDAkey_extractor.py](keywords/keywords_extract/LDAkey_extractor.py)
Gensim's LDA topic modeling algorithm implemented

토픽 모델링으로서 LDA는 토픽(주제)별 단어의 분포, 문서별 토픽의 분포를 추정하는 확률적 모형이다. LDA가 실제로 하는 일은 현재 문서들에 등장하는 단어들(w값들)을 보고 어떤 토픽에서 뽑힌건지 단어들의 이면적인 정보를 추론하는 것이다.

LDA 토픽 모델링을 통해 산출된 각 토픽의 상위 단어들(top-ranking terms)은 해당 토픽에 대한 단어의 출현 빈도수를 기준으로 선정된다.

한 토픽에 출현 빈도가 높은 단어가 다른 토픽에도 출현 빈도가 높을 수 있기 때문에 단순히 빈도수만을 기준으로 선택한다면 토픽 간의 분별성이 낮아진다.
따라서 Relevance Score를 사용해 분별성을 높였다.
### Relevance Score
![image](https://user-images.githubusercontent.com/55436953/120982711-f21d1e00-c7b3-11eb-8174-c7c178ab5a52.png)

```lambda```가 1이면 한 토픽에 등장하는 빈도 수만을 가지고 상위 단어를 찾는다. ```lambda```가 0이면 다른 토픽에도 자주 등장하는 단어들의 ```relevance``` 값이 낮아지고, 한 토픽에만 등장하는 단어일수록 ```relevance``` 값이 높아진다. 해당 project에서는 적절한 ```lambda``` 값(0.6)을 이용한다.

Reference: [https://lovit.github.io/nlp/2018/09/27/pyldavis_lda/](https://lovit.github.io/nlp/2018/09/27/pyldavis_lda/)

## TextRank
### [textrank.py](keywords/keywords_extract/textrank.py)

LDA를 통해 선정된 각 토픽별로 토픽에 기여하는 문서들을 대상으로 Relevance Top 20 단어를 포함하는 문장들을 추출한다. 추출된 문장들에 대해서 앞에서 한 것과 같이 전처리 한다.

따라서 TextRank에 적용되는 입력 형식은 

```[ [topic1_문장1,topic1_문장2,...,topic1_문장N],[topic2_문장1,topic2_문장2,...,topic2_문장N],...,[topicN_문장1,topicN_문장2,...,topicN_문장N] ]```이다.

이후, Textrank 알고리즘을 사용하여 각 토픽을 대표하는 단어로 토픽 키워드들을 추출한다. TextRank 알고리즘은 word graph를 구축한 뒤, Graph ranking 알고리즘인 PageRank 를 이용하여 키워드를 추출한다.

### PageRank 공식

<img width="310" alt="pagerank공식" src="https://user-images.githubusercontent.com/80442377/120992094-3a8d0980-c7bd-11eb-9ad8-1f957a45f8a9.png">

Reference: [https://lovit.github.io/nlp/2019/04/30/textrank/](https://lovit.github.io/nlp/2019/04/30/textrank/)


