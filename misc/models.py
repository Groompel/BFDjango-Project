from django.db import models

# Create your models here.


class Room(models.Model):
    name = models.CharField(verbose_name='Name', blank=False,
                            null=False, default='', max_length=50)

    class Meta:
        verbose_name = 'Room'
        verbose_name_plural = 'Rooms'

    def __str__(self):
        return self.name


class Address(models.Model):
    city = models.CharField(verbose_name='City', blank=False,
                            null=False, default='', max_length=100)
    district = models.CharField(
        verbose_name='District', blank=False, null=False, default='', max_length=100)
    street = models.CharField(
        verbose_name='Street', blank=False, null=False, default='', max_length=100)
    street_number = models.PositiveIntegerField(
        verbose_name='Street number', blank=False, null=False, default=1)

    class Meta:
        verbose_name = 'Address'
        verbose_name_plural = 'Addresses'

    def __str__(self):
        return '%s, %s, %s, %i' % (self.city, self.district, self.street, self.street_number)


class BusinessCenter(models.Model):
    name = models.CharField(verbose_name='Name', blank=False,
                            null=False, default='', max_length=150)
    number_of_floors = models.PositiveIntegerField(
        verbose_name='Number of floors', blank=False, null=False, default=1)

    class Meta:
        verbose_name = 'Business center'
        verbose_name_plural = 'Business centers'

    def __str__(self):
        return self.name
