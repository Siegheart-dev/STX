from django.db import models


# Create your models here.

class Books(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    publication_date = models.CharField(max_length=255)
    ISBN_number = models.CharField(max_length=255, unique=True)
    number_of_pages = models.CharField(max_length=255)
    cover_link = models.ImageField(upload_to="images/")
    pub_language = models.CharField(max_length=255)

    def __str__(self):
        return self.title
