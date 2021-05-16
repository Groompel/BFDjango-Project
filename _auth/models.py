from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.


class DefaultUserAgentsManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_agent=True)


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
    birth_date = models.DateField(
        verbose_name='Birth date', blank=True, null=True)
    is_agent = models.BooleanField(
        'Agent', choices=[(True, 'Yes'), (False, 'No')], default=False)
    objects = models.Manager()
    agents = DefaultUserAgentsManager()

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return '%s, %s %s' % (self.user.email, self.first_name, self.last_name)


@receiver(post_save, sender=User)
def default_user_created_handler(sender, instance, created, *args, **kwargs):
    if created:
        DefaultUser.objects.create(user=instance)


class AgencyOwnerManager(models.Manager):
    def get_agency_by_owner(self, owner):
        return super().get_queryset().get(owner=owner)


class Agency(models.Model):
    name = models.CharField(verbose_name='Name',
                            max_length=250, blank=False, null=False, default='')
    owner = models.ForeignKey(DefaultUser, on_delete=models.CASCADE, default=1)

    objects = AgencyOwnerManager()

    @property
    def agents(self):
        return Agent.objects.filter(agency=self)

    class Meta:
        verbose_name = 'Agency'
        verbose_name_plural = 'Agencies'

    def __str__(self):
        return self.name


class Agent(models.Model):
    user = models.ForeignKey(DefaultUser, on_delete=models.CASCADE)
    agency = models.ForeignKey(Agency, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Agent'
        verbose_name_plural = 'Agents'

    def __str__(self):
        return '%s %s at agency "%s"' % (self.user.first_name, self.user.last_name, self.agency.name)
