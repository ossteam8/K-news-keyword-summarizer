from django.shortcuts import render
from django.views.generic.detail import DetailView

from crawling.models import Article

# -*- coding: cp949 -*- 
import platform
import kss
import numpy as np
from functools import partial
from sklearn.preprocessing import normalize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import pairwise_distances

if platform.system() == "Windows":
    try:
        from eunjeon import Mecab
    except:
        print("please install eunjeon module")
else:  # Ubuntu일 경우
    from konlpy.tag import Mecab

from typing import List, Callable, Union, Any, TypeVar, Tuple, Dict



# summary 화면
class SummaryView(DetailView):
	# id = article id !! (pk)
	template_name = 'crawling/summary.html'

	def get(self, request, article_id):
		article_obj = Article.objects.get(pk=article_id)
		article_query = article_obj.contents + article_obj.title
		summary(article_query)

		return render(request, self.template_name, {'article':article_obj})


def get_tokenizer(tokenizer_name):
    tokenizer = Mecab()
    return tokenizer


def get_tokens(sent: List[str], noun=False, tokenizer="mecab") -> List[str]:
    tokenizer = get_tokenizer(tokenizer)
    
    if noun:
        nouns = tokenizer.nouns(sent)
        nouns = [word for word in nouns if len(word) > 1]
        return nouns

    return tokenizer.morphs(sent)




def vectorize_sents(
    sents: List[str],
    stopwords=None,
    min_count=2,
    tokenizer="mecab",
    noun=False
):

    vectorizer = TfidfVectorizer(
        stop_words=stopwords,
        tokenizer=partial(get_tokens, noun=noun, tokenizer="mecab"),
        min_df=min_count,
    )

    vec = vectorizer.fit_transform(sents)
    vocab_idx = vectorizer.vocabulary_
    idx_vocab = {idx: vocab for vocab, idx in vocab_idx.items()}
    return vec, vocab_idx, idx_vocab



def similarity_matrix(x, min_sim=0.3, min_length=1):

    # binary csr_matrix
    numerators = (x > 0) * 1

    #문장간 유사도 계산, 문장간 유사도가 0.3이하면 간선 연결하지 않음.
    min_length = 1
    denominators = np.asarray(x.sum(axis=1))
    denominators[np.where(denominators <= min_length)] = 10000
    denominators = np.log(denominators)
    denom_log1 = np.matmul(denominators, np.ones(denominators.shape).T)
    denom_log2 = np.matmul(np.ones(denominators.shape), denominators.T)

    sim_mat = np.dot(numerators, numerators.T)
    sim_mat = sim_mat / (denom_log1 + denom_log2)
    sim_mat[np.where(sim_mat <= min_sim)] = 0

    return sim_mat



def sent_graph(
    sents: List[str],
    min_count=2,
    min_sim=0.3,
    tokenizer="mecab",
    noun=False,
    stopwords: List[str] = ["연합뉴스", "중앙일보","한겨레","국민일보","머니투데이","동아일보"]
):
    
    # TF-IDF + Cosine similarity 

    mat, vocab_idx, idx_vocab = vectorize_sents(
        sents, stopwords, min_count=min_count, tokenizer=tokenizer
    )

    
    mat = similarity_matrix(mat, min_sim=min_sim)

    return mat, vocab_idx, idx_vocab


def pagerank(mat: np.ndarray, df=0.85, max_iter=50):
    
    assert 0 < df < 1

    A = normalize(mat, axis=0, norm="l1")
    N = np.ones(A.shape[0]) / A.shape[0]

    R = np.ones(A.shape[0])
    # iteration
    for _ in range(max_iter):
        R = df * np.matmul(A, R) + (1 - df) * N


    return R


def summary(article_query):
	#즉, 입력값 str 형태

	sents= kss.split_sentences(article_query)
	mat, vocab_idx, idx_vocab = sent_graph(sents)
	R = pagerank(mat)
	topk = 3
	idxs = R.argsort()[-topk:]
	keysents = [(sents[idx]) for idx in sorted(idxs)]

	return keysents