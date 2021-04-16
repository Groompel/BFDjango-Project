from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class DefaultUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
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

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return '%s, %s %s' % (self.user.email, self.first_name, self.last_name)


class Agency(models.Model):
    name = models.CharField(verbose_name='Name',
                            max_length=250, blank=False, null=False, default='')

    class Meta:
        verbose_name = 'Agency'
        verbose_name_plural = 'Agencies'

    def __str__(self):
        return self.name


class Agent(DefaultUser):
    agency = models.ForeignKey(Agency, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Agent'
        verbose_name_plural = 'Agents'

    def __str__(self):
        return self.agency.name
