from django.db import models

class Question(models.Model):
    right_prompt = models.CharField(max_length=100)
    wrong_prompt = models.CharField(max_length=100)

    def __str__(self):
        #TODO: can I return the ID??
        return self.right_prompt
