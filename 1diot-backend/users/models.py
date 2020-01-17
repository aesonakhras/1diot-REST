from django.db import models

class User(models.Model):
    username = models.CharField("username", max_length=20)

    def __str__(self):
        return self.username
