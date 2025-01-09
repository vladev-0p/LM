from django.db import models


# Create your models here.


class AskModel(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)  # Дата создания
    updated_at = models.DateTimeField(auto_now=True)
    remove = models.deletion

    def __str__(self):
        return self.question