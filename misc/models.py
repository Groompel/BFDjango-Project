from django.db import models

# Create your models here.


class Room(models.Model):
    name = models.CharField(verbose_name='Name', max_length=50)

    class Meta:
        verbose_name = 'Room'
        verbose_name_plural = 'Rooms'

    def __str__(self):
        return self.name
