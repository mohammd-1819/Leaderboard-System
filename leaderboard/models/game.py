from django.db import models


class Game(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    release_date = models.DateField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
