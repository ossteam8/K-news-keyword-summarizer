from django.db import models
from picklefield.fields import PickledObjectField


# Create your models here.
class Category(models.Model):
	id = models.AutoField(primary_key=True)
	category = models.CharField(max_length=64)
	keywords = PickledObjectField(default=dict, null=True, blank=True)
	# {1: [ ['k1', ,,,], {id: rate, id: rate, id: rate, ,,,} ] , 2: [ ['k2', ,,,], {id: rate, id: rate, id: rate, ,,,} ] ,,,}
	topics = PickledObjectField(null=True, blank=True)  

	def __str__(self):
		return self.category

	class Meta:
		db_table = 'category'


class Article(models.Model):
	category = models.ForeignKey(Category, on_delete=models.CASCADE)

	id = models.BigAutoField(primary_key=True)
	title = models.TextField()
	contents = models.TextField()
	url = models.URLField()
	register_date = models.DateTimeField(auto_now_add=True)  # public date

	summary = models.TextField(null=True, blank=True)
	
	def __str__(self):
		return self.title
	
	class Meta:
		db_table = 'article'

	
	


	
