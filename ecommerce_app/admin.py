from django.contrib import admin
from .models import *
# Register your models here.

class ItemAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'cat_name', 'price')


class CartAdmin(admin.ModelAdmin):
    list_display = ('id','owner','item_name', 'quantity', 'price')

admin.site.register(Item)
admin.site.register(Cart)
admin.site.register(Category)