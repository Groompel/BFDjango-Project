from _auth.models import DefaultUser
from misc.models import Address, BusinessCenter, ResidentialComplex
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_delete, post_save, pre_save
import logging

logger = logging.getLogger(__name__)

# Create your models here.


class AbstractProperty(models.Model):
    user = models.ForeignKey(DefaultUser, on_delete=models.CASCADE)
    image = models.ImageField(verbose_name='Image',
                              upload_to='posts/images', null=True, blank=True)
    deal_type = models.CharField(
        choices=[('sell', 'Sell'), ('rent', 'Rent')], default='sell', max_length=5)
    price = models.FloatField(verbose_name='Price',
                              blank=False, null=False, default=0)
    area = models.FloatField(
        verbose_name='Area', blank=False, null=False, default=0)
    built_year = models.PositiveIntegerField(
        verbose_name='Year', blank=False, null=False, default=2000)
    exploitation_year = models.PositiveIntegerField(
        verbose_name='Exploitation year', blank=False, null=False, default=2000)
    address = models.ForeignKey(
        Address, verbose_name='Address', on_delete=models.CASCADE)
    number_of_rooms = models.IntegerField(
        verbose_name='Number of rooms', blank=False, null=False, default=0)
    description = models.CharField(
        verbose_name='Description', blank=True, null=True, default='', max_length=1000)

    class Meta:
        abstract = True


class AbstractLivingProperty(AbstractProperty):
    kitchen_area = models.FloatField(
        verbose_name='Kitchen area', blank=False, null=False, default=0)
    construction_type = models.CharField(
        verbose_name='Construction type', blank=False, null=False, default='', max_length=100)
    number_of_bedrooms = models.PositiveSmallIntegerField(
        verbose_name='Number of bedrooms', blank=False, null=False, default=0)

    class Meta:
        abstract = True


class CommercialProperty(AbstractProperty):
    business_center = models.ForeignKey(
        BusinessCenter, on_delete=models.CASCADE, verbose_name='Business center', blank=True, null=True)

    class Meta:
        verbose_name = 'Commerical property'
        verbose_name_plural = 'Commerical properties'

    def __str__(self):
        return self.business_center.name


@receiver(post_save, sender=CommercialProperty)
def post_save_commercial_property_receiver(sender, instance, created, *args, **kwargs):
    s = 'Created new commercial property post'

    if not created:
        s = 'Updated commercial property post'

    logger.info('%s. ID: %s' % (s, instance.id))


@receiver(post_delete, sender=CommercialProperty)
def post_delete_commercial_property_receiver(sender, instance, *args, **kwargs):
    logger.info('Deleted a commercial property post. ID: %s' % (instance.id))


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


@receiver(post_save, sender=HouseProperty)
def post_save_house_property_receiver(sender, instance, created, *args, **kwargs):
    s = 'Created new house property post'

    if not created:
        s = 'Updated house property post'

    logger.info('%s. ID: %s' % (s, instance.id))


@receiver(post_delete, sender=HouseProperty)
def post_delete_house_property_receiver(sender, instance, *args, **kwargs):
    logger.info('Deleted a house property post. ID: %s' % (instance.id))


class FlatProperty(AbstractLivingProperty):
    floor = models.PositiveIntegerField(
        verbose_name='Floor', blank=False, null=False, default=0)
    number_of_floors_in_house = models.PositiveIntegerField(
        verbose_name='Number of floors in the house', blank=False, null=False, default=0)
    residential_complex = models.ForeignKey(
        ResidentialComplex, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        verbose_name = 'Flat property'
        verbose_name_plural = 'Flat properties'

    def __str__(self):
        return '%s, on floor %i / %i' % (self.address, self.floor, self.number_of_floors_in_house)


@receiver(pre_save, sender=FlatProperty)
def pre_save_flat_property_receiver(sender, instance, *args, **kwargs):
    instance.number_of_floors_in_house = instance.residential_complex.number_of_floors


@receiver(post_save, sender=FlatProperty)
def post_save_flat_property_receiver(sender, instance, created, *args, **kwargs):
    s = 'Created new flat property post'

    if not created:
        s = 'Updated flat property post'

    logger.info('%s. ID: %s' % (s, instance.id))


@receiver(post_delete, sender=FlatProperty)
def post_delete_flat_property_receiver(sender, instance, *args, **kwargs):
    logger.info('Deleted a flat property post. ID: %s' % (instance.id))
