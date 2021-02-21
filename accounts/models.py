from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.


class Role(models.Model):
    ADMIN = 1
    CUSTOMER = 2
    STAFF = 3

    ROLE_CHOICES = (
        (ADMIN, 'admin'),
        (CUSTOMER, 'customer'),
        (STAFF, 'staff')
    )

    id = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, primary_key=True)

    def __str__(self):
        return self.get_id_display()


class User(AbstractUser):
    roles = models.ManyToManyField(Role)
    address = models.CharField(max_length=500, default='')
