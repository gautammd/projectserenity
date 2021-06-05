from django.db import models


class User(models.Model):

    id = models.AutoField(primary_key=True)
    email = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = "user"
