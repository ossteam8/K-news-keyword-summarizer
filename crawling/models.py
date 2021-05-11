from django.db import models
from picklefield.fields import PickledObjectField
# from jsonfield import JSONField
#   memo = JSONField(default={}, dump_kwargs={'ensure_ascii': False})s


# Create your models here.

# class Article(models.Model):
#     category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
#     search_word = models.ForeignKey(SearchWord, on_delete=models.CASCADE, null=True, blank=True)

#     title = models.CharField(max_length=128)
#     contents = models.TextField()
#     url = models.URLField()

#     summary = models.TextField()
    # vectors = PickledObjectField()
#     similarity = models.FloatField(localize=False)  # localize=False 일 때 NumberInput, 그 외 TextInput

    # def __str__(self):
    #         return self.title

    
    # pickle 예시
    # from picklefield.fields import PickledObjectField
    #     class SomeObject(models.Model):
    #         args = PickledObjectField()

    #     obj = SomeObject()
    #     obj.args = ['fancy', {'objects': 'inside'}]
    #     obj.save()


    # CATEGORY_CHOICES = [
    #     ('정치', 'politic'),
    #     ('경제', 'economic'),
    #     ('사회', 'social'),
    # ]
    # category = models.CharField(max_length=64, choices=CATEGORY_CHOICES)


# class Category(models.Model):
#     caterory = models.CharField(max_length=64)


# class SearchWord(models.Model):
#     search_word = models.CharField(max_length=64)