from django.db import models

# Create your models here.


class Author(models.Model):
    first_name = models.CharField(max_length=64, blank=False)
    last_name = models.CharField(max_length=64, blank=False)
    birthday = models.DateTimeField(blank=False)

    class Meta:
        unique_together = ('first_name', 'last_name', 'birthday')
