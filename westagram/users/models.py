from django.db import models

class Users(models.Model):
    username = models.CharField(max_length=50)
    #email = models.EmailField(max_length=300)
    password = models.CharField(max_length=300)

    class Meta:
        db_table = 'user_data'

