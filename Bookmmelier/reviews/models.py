from django.db import models
from books.models import Book
from users.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings 


class Review(models.Model):
    review_id = models.AutoField(primary_key=True)
    book = models.ForeignKey(Book, models.DO_NOTHING, db_column='isbn13',related_name='reviews')
    user = models.ForeignKey(User, models.DO_NOTHING)
    time_write = models.DateTimeField(auto_now_add=True)
    time_retouch = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=50)
    contents = models.TextField()
    rate = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    is_shared = models.IntegerField()
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_review')
    class Meta:
        db_table = u'reviews'

class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    review = models.ForeignKey(Review, models.CASCADE, db_column='review_id')
    user = models.ForeignKey(User, models.CASCADE)
    time_write = models.DateTimeField(auto_now_add=True)
    contents = models.TextField()
    class Meta:
        db_table = u'reviews_comments'