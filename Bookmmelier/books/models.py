from django.db import models
from django.db.models import Avg

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

    class Meta:
        db_table = u'books'

    def ratings(self):
        return self.reviews.aggregate(avg_score=Avg('rate'))['avg_score']
