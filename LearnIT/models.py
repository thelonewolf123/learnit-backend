from django.db import models


class NewsLetter(models.Model):

    email = models.EmailField(null=False, blank=False, max_length=200)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
