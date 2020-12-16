from django.contrib import admin
from .models import *


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('userID', 'first_name', 'last_name', 'userPhone', 'userEmail')


class ProductsAdmin(admin.ModelAdmin):
    list_display = ('productID', 'productName', 'productPrice', 'productCategory')


class RatingsAdmin(admin.ModelAdmin):
    list_display = ('customer', 'productID', 'ratings', 'timestamp', 'updated_at')


class AttributesAdmin(admin.ModelAdmin):
    list_display = ['productID']


class WishlistAdmin(admin.ModelAdmin):
    list_display = ['customer', 'timeStamp']


class WishlistItemAdmin(admin.ModelAdmin):
    list_display = ['wishlist', 'product', 'savedProductPrice']


admin.site.register(Customers, CustomerAdmin)
admin.site.register(Products, ProductsAdmin)
admin.site.register(Ratings, RatingsAdmin)
admin.site.register(Attributes, AttributesAdmin)
admin.site.register(Wishlist, WishlistAdmin)
admin.site.register(WishlistItem, WishlistItemAdmin)
