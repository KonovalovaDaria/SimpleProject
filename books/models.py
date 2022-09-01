from django.db import models

# Create your models here.


class Book(models.Model):
    title = models.CharField(max_length=64)
    info = models.CharField(max_length=256)
    date = models.DateTimeField()
    author = models.ForeignKey('authors.Author', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('title', 'author')
