from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class DefaultUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone_number = models.CharField(
        verbose_name='Phone number', max_length=40, blank=False, null=False, default='+7')
    first_name = models.CharField(
        verbose_name='First name', max_length=100, blank=False, null=False, default='')
    last_name = models.CharField(
        verbose_name='Last name', max_length=100, blank=False, null=False, default='')
    GENDERS = [('male', 'Male'),  ('female', 'Female')]
    gender = models.CharField(verbose_name='Gender',
                              choices=GENDERS, default='male', max_length=6)
    birth_date = models.DateField(verbose_name='Birth date')


class Agency(models.Model):
    name = models.CharField(verbose_name='Name',
                            max_length=250, blank=False, null=False, default='')


class Agent(DefaultUser):
    agency = models.ForeignKey(Agency, on_delete=models.CASCADE)
