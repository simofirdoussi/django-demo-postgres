from django.db import models


class Task(models.Model):
    name = models.CharField(max_length=200)
    file = models.FileField(upload_to="files/")
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
