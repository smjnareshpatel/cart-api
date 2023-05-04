from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Item(models.Model):
    name = models.CharField(max_length=200)
    desc = models.TextField()
    image = models.ImageField(upload_to='productimage')
    cat_name = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class Cart(models.Model):
    item_name = models.ForeignKey(Item, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    quantity = models.IntegerField(default=1)
    price = models.CharField(max_length=10,blank=True,null=True)
    ordered = models.BooleanField(default=False)


    def __str__(self):
        return self.item_name.name+ ' item quantity:-' + str(self.quantity)



