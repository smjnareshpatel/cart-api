from django.contrib.auth import authenticate
from rest_framework import serializers

from . import models
import datetime, time

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = '__all__'

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Item
        fields = ('id','name','desc','image','cat_name','price')




class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Cart
        fields = ('id','item_name','owner','quantity','price','ordered')


    
    
class CartQuantitySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Cart
        fields = ('quantity','price')


