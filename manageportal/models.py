import os
import uuid

from django.core.validators import RegexValidator
from django.db import models
from django.urls import reverse


def change_path(instance, filename):
    # name = instance.fullname.replace(' ', '_')
    return '/'.join(['images', str(uuid.uuid4().hex + ".jpg")])


class Message(models.Model):
    fullname = models.CharField(max_length=100)
    product_name = models.CharField(max_length=100, blank=True, null=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)  # validators should be a list
    email = models.EmailField()
    address = models.CharField(max_length=150)
    description = models.TextField()
    # image = models.ImageField(upload_to=change_path, blank=True, null=True)
    status = models.CharField(max_length=50, default="Waiting")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        """Returns the url to access a particular message instance."""
        return reverse('message-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return self.fullname


class MessageImages(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='images')
    image = models.FileField(upload_to=change_path)


class Transaction(models.Model):
    uid = models.CharField(max_length=11, unique=True, null=True)
    uuid = models.UUIDField(default=uuid.uuid4,
                          help_text='Unique ID for this particular request across whole system')
    message = models.OneToOneField('Message', on_delete=models.SET_NULL, null=True)
    cost = models.FloatField(default=0.0)
    money_paid = models.FloatField(default=0.0)
    money_made = models.FloatField(default=0.0)
    shipping_cost = models.FloatField(default=0.0)
    vat = models.FloatField(default=0.0)
    done_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """String for representing the Model object."""
        return str(self.uid)


def get_upload_path(instance, filename):
    return os.path.join("products_%s" % instance.event_name, filename)


class Invoice(models.Model):
    message = models.ForeignKey('Message', on_delete=models.SET_NULL, null=True)
    pdf_path = models.CharField(max_length=300)


class Receipt(models.Model):
    message = models.ForeignKey('Message', on_delete=models.SET_NULL, null=True)
    pdf_path = models.CharField(max_length=300)

#
# class FeatureProducts(models.Model):
#     slug = models.SlugField()
#
#     def save(self, *args, **kwargs):
#         self.slug = slugify(self.name)
#         super(FeatureProducts, self).save(*args, **kwargs)
#
#     event_name = models.CharField(max_length=100)
#     name = models.CharField(max_length=100)
#     price = models.FloatField(default=0.0)
#     photo = models.ImageField(upload_to=get_upload_path, unique=True)
#     shipping_cost = models.FloatField(default=0.0)
#     vat = models.FloatField(default=0.0, blank=True, null=True)
#     details = models.TextField()
#     quantity_in_stock = models.IntegerField(default=0)
#     quantity_sold = models.IntegerField(default=0)
#     status = models.BooleanField(default=False)
#     start_date = models.DateTimeField()
#     end_date = models.DateTimeField()
#
#     def __str__(self):
#         """String for representing the Model object."""
#         return self.name
#
#
# class Coupons(models.Model):
#     code = models.CharField(max_length=100, unique=True)
#     product = models.OneToOneField('FeatureProducts', on_delete=models.SET_NULL, null=True)
#     discount = models.IntegerField(default=10)
#     product_quantity = models.IntegerField(default=1)
#     product_quantity_used = models.IntegerField(default=0)
#     status = models.BooleanField(default=True)
#     start_date = models.DateTimeField()
#     end_date = models.DateTimeField()
