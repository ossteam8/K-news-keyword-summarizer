from django.db import models
from picklefield.fields import PickledObjectField

#   memo = JSONField(default={}, dump_kwargs={'ensure_ascii': False})s


# Create your models here.
class Category(models.Model):
    caterory = models.CharField(max_length=64)
    keywords = models.JSONField(default=dict, null=True, blank=True)

    def __str__(self):
            return self.caterory

# politic, economic, social

class SearchWord(models.Model):
    search_word = models.CharField(max_length=64)
    keywords = models.JSONField(default=dict, null=True, blank=True)

    def __str__(self):
            return self.search_word


class Article(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    search_word = models.ForeignKey(SearchWord, on_delete=models.CASCADE, null=True, blank=True)

    title = models.CharField(max_length=128)
    contents = models.TextField()
    url = models.URLField()
    register_date = models.DateTimeField(auto_now_add=True)

    summary = models.TextField(null=True, blank=True)
    vectors = PickledObjectField(null=True, blank=True)
    similarity = models.FloatField(null=True, blank=True)  # localize=False 일 때 NumberInput, 그 외 TextInput

    def __str__(self):
            return self.title

    
    # pickle 예시
    # from picklefield.fields import PickledObjectField
    # class SomeObject(models.Model):
    #     args = PickledObjectField()

    #     obj = SomeObject()
    #     obj.args = ['fancy', {'objects': 'inside'}]
    #     obj.save()


    
