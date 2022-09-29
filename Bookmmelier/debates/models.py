from django.db import models
from books.models import Book
from users.models import User
from django.db.models import Count


class Debate(models.Model):
    debate_id = models.AutoField(primary_key=True)
    book = models.ForeignKey(Book, models.DO_NOTHING, db_column='isbn13',related_name='debates')
    user = models.ForeignKey(User, models.DO_NOTHING)
    time_created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=50)
    subtitle = models.TextField()
    class Meta:
        db_table = u'debates'

    def message_count(self):
        return self.messages.aggregate(count=Count('user'))['count']
    def user_count(self):
        return self.messages.aggregate(count=Count('user',distinct=True))['count']

class Message(models.Model):
    message_id = models.AutoField(primary_key=True)
    debate = models.ForeignKey(Debate, models.CASCADE, db_column='debate_id',related_name='messages')
    user = models.ForeignKey(User, models.CASCADE)
    time_created = models.DateTimeField(auto_now_add=True)
    contents = models.TextField()
    class Meta:
        db_table = u'debates_message'
