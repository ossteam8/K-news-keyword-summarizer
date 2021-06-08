from .crawling_py.main_crawling import run_crawling
from .views import save_articles

# db에 저장
def article_crawling_job():  
	politic_article_list, economy_article_list, society_article_list = run_crawling()
	print('run_crawling 끝!!')
	try:
		save_articles(politic_article_list, economy_article_list, society_article_list)
	except Exception as e:
		print(e)
	print("success!!")

	# save_articles([{"title":"save_test","contents":"save_test","url":"https://velog.io/@magnoliarfsit/ReDjango-4.-장고-ORM을-사용해서-DB-CRUD-구현하기","category":"정치"}, {"title":"save_test4","contents":"save_test4","url":"https://velog.io/@magnoliarfsit/ReDjango-4.-장고-ORM을-사용해서-DB-CRUD-구현하기","category":"정치"}, {"title":"save_test5","contents":"save_test5","url":"https://velog.io/@magnoliarfsit/ReDjango-4.-장고-ORM을-사용해서-DB-CRUD-구현하기","category":"정치"}], [{"title":"save_test2","contents":"save_test2","url":"https://velog.io/@magnoliarfsit/ReDjango-4.-장고-ORM을-사용해서-DB-CRUD-구현하기","category":"경제"}], [{"title":"save_test3","contents":"save_test3","url":"https://velog.io/@magnoliarfsit/ReDjango-4.-장고-ORM을-사용해서-DB-CRUD-구현하기","category":"사회"}])
	

