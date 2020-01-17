#from Question import models as question_models
from django.db import models
from questions import models as question_models
from jsonfield import JSONField
from django.contrib.postgres.fields import ArrayField

# Create your models here.
class Answer(models.Model):
    user_name = models.CharField(max_length=20, default="")
    answer = models.CharField(max_length=200, default="")

    def __str__(self):
        return self.username


class Room(models.Model):
    #this will be in json form
    user_list = ArrayField(models.CharField(max_length=20, blank=True), size=10, default=list)
    host = models.CharField(max_length=20, default=[])
    room_code = models.CharField(max_length=4, unique=True)
    state = models.CharField(max_length=1, default="W")
    question_id = models.IntegerField(default=0)

    vote_wrong = models.IntegerField(default=0)
    vote_count = models.IntegerField(default=0)
    user_count = models.IntegerField(default=1) #the host is why it begins at one

    user_wrong = models.CharField(max_length=20, default="")
    time = models.IntegerField(default=0)

    answers = ArrayField(models.CharField(max_length=220, default=","), size=10, default=list)
    question_index_array = ArrayField(models.IntegerField(default=0), size=10, default=list)

    #int array that is one to one with user_list(remove nad append at the same time)
    user_points = ArrayField(models.IntegerField(default=0), size=10, default=list)
    voted_array = ArrayField(models.CharField(max_length=41, blank=True), size=10, default=list)

    caught = models.BooleanField(default=False)
    winner_determined = models.BooleanField(default=False)


    def __str__(self):
        return self.room_code

    def save_question_id(self):
        self.question_id.save()
        self.save()