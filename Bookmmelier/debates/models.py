from django.db import models
from books.models import Book
from users.models import User
from django.conf import settings 


class Debate(models.Model):
    debate_id = models.AutoField(primary_key=True)
    book = models.ForeignKey(Book, models.DO_NOTHING, db_column='isbn13',related_name='debates')
    user = models.ForeignKey(User, models.DO_NOTHING)
    time_created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=50)
    subtitle = models.TextField()
    class Meta:
        db_table = u'debates'

class Message(models.Model):
    message_id = models.AutoField(primary_key=True)
    debate = models.ForeignKey(Debate, models.CASCADE, db_column='debate_id')
    user = models.ForeignKey(User, models.CASCADE)
    time_created = models.DateTimeField(auto_now_add=True)
    contents = models.TextField()
    class Meta:
        db_table = u'debates_message'

    def last_30_messages(self, debate_id):
        return Message.objects.filter(debate_id=debate_id).order_by('time_created')[:30]