from django.db import models
from users.models import User

# Create your models here.

class Book(models.Model):
    isbn13 = models.CharField(primary_key=True, max_length=13)
    vol = models.CharField(max_length=20, blank=True, null=True)
    title = models.CharField(max_length=1200, blank=True, null=True)
    author = models.CharField(max_length=1000, blank=True, null=True)
    publisher = models.CharField(max_length=1000, blank=True, null=True)
    pub_date = models.CharField(max_length=10, blank=True, null=True)
    img_url = models.CharField(max_length=1000, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    kdc_class_no = models.CharField(max_length=20, blank=True, null=True)
    like_users = models.ManyToManyField(User, related_name='like_books', blank=True)

    class Meta:
        managed = False
        db_table = 'Bookmmelier_book'
    