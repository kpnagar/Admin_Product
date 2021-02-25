from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Product(models.Model):
    # customer = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    price = models.IntegerField()
    discount = models.FloatField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    manufacture_date = models.DateField()
    is_discount = models.BooleanField(default=False)

    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)

    FRESHMAN = 'FR'
    SOPHOMORE = 'SO'
    JUNIOR = 'JR'
    SENIOR = 'SR'
    GRADUATE = 'GR'
    YEAR_IN_SCHOOL_CHOICES = [
        (FRESHMAN, 'Freshman'),
        (SOPHOMORE, 'Sophomore'),
        (JUNIOR, 'Junior'),
        (SENIOR, 'Senior'),
        (GRADUATE, 'Graduate'),
    ]
    year_in_school = models.CharField(
        max_length=2,
        choices=YEAR_IN_SCHOOL_CHOICES,
        default=FRESHMAN,
    )
    
    def discount_price(self):
        discount = 0
        if self.is_discount == True:
            discount = self.price + 150
        return discount

    def __str__(self):
        return self.name

    # Overrite Save Method
    def save(self, *args, **kwargs):
        if self.price > 100:
            self.discount = 15.5
        super().save(*args, **kwargs)
