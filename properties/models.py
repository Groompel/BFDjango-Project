from misc.models import Address, BusinessCenter, ResidentialComplex, Room
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
    address = models.ForeignKey(
        Address, verbose_name='Address', on_delete=models.CASCADE)
    rooms = models.ManyToManyField(Room, verbose_name='Rooms')

    class Meta:
        abstract = True


class AbstractLivingProperty(AbstractProperty):
    kitchen_area = models.FloatField(
        verbose_name='Kitchen area', blank=False, null=False, default=0)
    construction_type = models.CharField(
        verbose_name='Construction type', blank=False, null=False, default='', max_length=100)

    class Meta:
        abstract = True


class CommercialProperty(AbstractProperty):
    business_center = models.ForeignKey(
        BusinessCenter, on_delete=models.CASCADE, verbose_name='Business center')

    class Meta:
        verbose_name = 'Commerical property'
        verbose_name_plural = 'Commerical properties'

    def __str__(self):
        return self.business_center.name


class HouseProperty(AbstractLivingProperty):
    land_area = models.FloatField(
        verbose_name='Land area', blank=False, null=False, default=0)
    number_of_floors = models.PositiveIntegerField(
        verbose_name='Number of floors', blank=False, null=False, default=0)

    class Meta:
        verbose_name = 'House property'
        verbose_name_plural = 'House properties'

    def __str__(self):
        return '%s, %i floors' % (self.address, self.number_of_floors)


class FlatProperty(AbstractLivingProperty):
    floor = models.PositiveIntegerField(
        verbose_name='Floor', blank=False, null=False, default=0)
    number_of_floors_in_house = models.PositiveIntegerField(
        verbose_name='Number of floors in the house', blank=False, null=False, default=0)
    residential_complex = models.ForeignKey(
        ResidentialComplex, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Flat property'
        verbose_name_plural = 'Flat properties'

    def __str__(self):
        return '%s, on floor %i / %i' % (self.address, self.floor, self.number_of_floors_in_house)
