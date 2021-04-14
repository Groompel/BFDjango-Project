from django.db import models

# Create your models here.


class AbstractProperty(models.Model):
    price = models.FloatField(verbose_name='Price',
                              blank=False, null=False, default=0)
    area = models.FloatField(
        verbose_name='Area', blank=False, null=False, default=0)
    built_year = models.IntegerField(
        verbose_name='Year', blank=False, null=False, default=2000)
    exploitation_year = models.IntegerField(
        verbose_name='Exploitation year', blank=False, null=False, default=2000)

    class Meta:
        abstract = True