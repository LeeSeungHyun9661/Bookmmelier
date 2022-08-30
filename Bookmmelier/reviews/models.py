from django.db import models
from books.models import Book
from users.models import User

class Review(models.Model):
    review_id = models.AutoField(primary_key=True)
    isbn13 = models.ForeignKey(Book, models.DO_NOTHING, db_column='isbn13')
    user = models.ForeignKey(User, models.DO_NOTHING)
    time_write = models.DateTimeField()
    time_retouch = models.DateTimeField()
    title = models.CharField(max_length=50)
    contents = models.TextField()
    rate = models.IntegerField()
    is_shared = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'review'
