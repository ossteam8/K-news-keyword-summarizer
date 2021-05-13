from django.db import models
from picklefield.fields import PickledObjectField

#   memo = JSONField(default={}, dump_kwargs={'ensure_ascii': False})s


# Create your models here.
class Category(models.Model):
    caterory = models.CharField(max_length=64)
    keywords = models.JSONField(default=dict)
# politic, economic, social

class SearchWord(models.Model):
    search_word = models.CharField(max_length=64)
    keywords = models.JSONField(default=dict)


class Article(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    search_word = models.ForeignKey(SearchWord, on_delete=models.CASCADE, null=True, blank=True)

    title = models.CharField(max_length=128)
    contents = models.TextField()
    url = models.URLField()

    summary = models.TextField()
    vectors = PickledObjectField()
    similarity = models.FloatField()  # localize=False 일 때 NumberInput, 그 외 TextInput
    register_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
            return self.title

    
    # pickle 예시
    # from picklefield.fields import PickledObjectField
    #     class SomeObject(models.Model):
    #         args = PickledObjectField()

    #     obj = SomeObject()
    #     obj.args = ['fancy', {'objects': 'inside'}]
    #     obj.save()


    
