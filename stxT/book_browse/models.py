from django.db import models

# Create your models here.

class Books(models.Model):
    title = models.CharField
    author = models.CharField
    publication_date = models.CharField
    ISBN_number = models.CharField
    number_of_pages = models.CharField
    cover_link = models.ImageField
    pub_language = models.CharField