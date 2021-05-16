from django.db import models
from django.db.models.signals import post_delete, post_save
from django.dispatch.dispatcher import receiver
import logging

logger = logging.getLogger(__name__)

# Create your models here.


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


@receiver(post_save, sender=BusinessCenter)
def post_save_business_center_receiver(sender, instance, created, *args, **kwargs):
    s = 'Created new business center'

    if not created:
        s = 'Updated a business center'

    logger.info('%s. ID: %s' % (s, instance.id))


@receiver(post_delete, sender=BusinessCenter)
def post_delete_business_center_receiver(sender, instance, *args, **kwargs):
    logger.info('Deleted a business center. ID: %s' % (instance.id))


class ResidentialComplex(models.Model):
    name = models.CharField(verbose_name='Name', blank=False,
                            null=False, default='', max_length=150)
    number_of_floors = models.PositiveIntegerField(
        verbose_name='Number of floors', blank=False, null=False, default=1)

    class Meta:
        verbose_name = 'Residential complex'
        verbose_name_plural = 'Residential complexes'

    def __str__(self):
        return self.name


@receiver(post_save, sender=ResidentialComplex)
def post_save_residential_complex_receiver(sender, instance, created, *args, **kwargs):
    s = 'Created new residential complex'

    if not created:
        s = 'Updated a residential complex'

    logger.info('%s. ID: %s' % (s, instance.id))


@receiver(post_delete, sender=ResidentialComplex)
def post_delete_residential_complex_receiver(sender, instance, *args, **kwargs):
    logger.info('Deleted a residential complex. ID: %s' % (instance.id))
