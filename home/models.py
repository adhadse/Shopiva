# home\models.py
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models
from django.contrib.auth.models import User, AbstractUser, PermissionsMixin
from django.db.models import Sum, F, Count, Value, Avg
from django.db.models.functions import Length, Upper
from django.core.validators import MaxValueValidator
import uuid
from order.models import Orders, OrderItem


class CustomerManager(BaseUserManager):
    def create_user(self, userEmail, first_name, last_name,
                    password = None,
                    is_admin = False,
                    is_staff = False,
                    is_active = True):
        if not userEmail:
            raise ValueError("User must have an email")
        if not password:
            raise ValueError("User must have a password")
        if not first_name:
            raise ValueError("User must have a First Name")
        if not last_name:
            raise ValueError("User must have a Last Name")

        user = self.model(userEmail=self.normalize_email(userEmail))
        user.first_name = first_name
        user.last_name = last_name
        user.is_admin = is_admin
        user.is_staff = is_staff
        user.is_active = is_active
        user.set_password(password)
        user.save(using=self._db)

    def create_staffuser(self, userEmail, first_name, last_name,
                         password = None,):
        user = self.create_user(userEmail, first_name, last_name,
                                password, is_staff = True,)
        return user

    def create_superuser(self, userEmail, first_name, last_name,
                         password = None, **kwargs):
        if not userEmail:
            raise ValueError("User must have an email")
        if not password:
            raise ValueError("User must have a password")
        if not first_name:
            raise ValueError("User must have a First Name")
        if not last_name:
            raise ValueError("User must have a Last Name")
        user = self.model(userEmail = self.normalize_email(userEmail))
        user.first_name = first_name
        user.last_name = last_name
        user.is_admin = True
        user.is_staff = True
        user.is_active = True
        user.set_password(password)
        user.save(using=self._db)


class Customers(AbstractBaseUser, PermissionsMixin):
    userID = models.UUIDField(primary_key=True, auto_created=True, default=uuid.uuid4, editable=False, unique=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    userPhone = models.PositiveIntegerField(unique=True, null=True, blank=True)
    userEmail = models.EmailField(unique=True)
    userImage = models.ImageField(blank=True, null=True)
    timeStamp = models.DateTimeField(auto_now_add=True)

    objects = CustomerManager()
    is_active = models.BooleanField(default=True, blank=True)
    is_admin = models.BooleanField(default=False, blank=True)
    is_staff = models.BooleanField(default=False, blank=True)
    USERNAME_FIELD = 'userEmail'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    @property
    def userName(self):
        return '{} {}'.format(self.first_name, self.last_name)

    def get_full_name(self):
        # The user is identified by their email address
        return self.userName

    def get_short_name(self):
        return self.first_name

    def get_user_id(self):
        return self.userID

    @staticmethod
    def has_perm(perm, obj = None ):
        # "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    @staticmethod
    def has_module_perms(app_label):
        # "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    def __str__(self):
        return self.userName

    class Meta:
        verbose_name_plural = "Customers"


class Products(models.Model):
    CATEGORY = (
        ('Wearable', 'Wearable'),
        ('Electronics', 'Electronics'),
        ('Books', 'Books'),
        ('Footwear', 'Footwear'),
        ('Stationary', 'Stationary')
    )
    productID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    productName = models.CharField(max_length=255)
    productPrice = models.DecimalField(max_digits=10, decimal_places=0)
    productCategory = models.CharField(max_length=32, choices= CATEGORY)
    productImage = models.ImageField(upload_to='images/')
    productDescription = models.CharField(max_length=512, null=True)
    timeStamp = models.DateTimeField(auto_now_add=True)

    @property
    def productRating(self):
        return Products.objects.get(productID=self.productID).ratings_set.aggregate(Avg('ratings'))['ratings__avg'] or 0
        # {'ratings__avg':5.0}

    @property
    def productReviews(self):
        return int(Products.objects.get(productID=self.productID).ratings_set.count())
        # 2

    @property
    def productOrders(self):
        return Products.objects.get(productID=self.productID).orderitem_set.all().filter(order__status='Delivered').aggregate(Sum('quantity'))['quantity__sum']

    def __str__(self):
        return ' ProductID: {} | ProductName: {}'.format(str(self.productID), str(self.productName))

    class Meta:
        verbose_name_plural = "Products"


class Wishlist(models.Model):
    """
        Each customer, ie. user may have one or more wishlists to remember items
        for later acquisition.
    """
    customer = models.ForeignKey(Customers, on_delete=models.CASCADE, null=True)
    timeStamp = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def add_to_cart(self, productID):
        product = Products.objects.get(productID=productID)
        cart, created = Orders.objects.get_or_create(customer=self.customer, status='In Cart')
        cartItem, created = OrderItem.objects.get_or_create(order=cart, product=product)
        cartItem.quantity = 1
        cartItem.save()
        self.delete_item(productID)
        return cart.get_cartitems_quantity

    @property
    def get_wishlist_quantity(self):
        """
        :return: Number of items in wishlist
        """
        return self.wishlistitem_set.all().count()

    def add_item(self, productID):
        """
            Adds the exact product to this wishlist, if it is not already there.
        """
        product = Products.objects.get(productID=productID)
        items = WishlistItem.objects.filter(wishlist=self, product=product)
        if not items.exists():
            item = WishlistItem.objects.create(wishlist=self, product=product)
            item.savedProductPrice = product.productPrice
            item.save()
        self.save()  # to get the last updated timestamp for this wishlist

    def get_all_items(self):
        """
        :returns: all items of this wishlist
        """
        return WishlistItem.objects.filter(wishlist=self)

    def find_item(self, productID):
        """
            For a given product and its variation, find an entry in this wishlist
            and return the found WishlistItem or None.
        """
        product = Products.objects.get(productID=productID)
        return WishlistItem.objects.filter(wishlist=self, product=product)

    def delete_item(self, productID):
        """
            A simple convenience method to delete an item from the wishlist.
        """
        product = Products.objects.get(productID=productID)
        WishlistItem.objects.get(wishlist=self, product=product).delete()
        self.save()

    class Meta(object):
        verbose_name = 'Wishlist'
        verbose_name_plural = 'Wishlists'


class WishlistItem(models.Model):
    """
        This is a holder for the item in the wishlist.
    """
    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Products, on_delete=models.CASCADE, null=True)
    savedProductPrice = models.IntegerField(null=True, blank=True)
    # variation = models.JSONField(null=True, blank=True)
    # variation_hash = models.CharField(max_length=64, null=True)

    class Meta(object):
        verbose_name = 'Wishlist item'
        verbose_name_plural = 'Wishlist items'


class Ratings(models.Model):
    customer = models.ForeignKey(Customers, on_delete=models.SET_NULL, null=True)
    productID = models.ForeignKey(Products, on_delete=models.CASCADE, null=True)
    ratings = models.PositiveIntegerField(validators=[MaxValueValidator(5)], null=True, blank=True, default=0)
    subject = models.CharField(max_length=63, blank=True, null=True)
    comment = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_created=True, auto_now=True)

    def __str__(self):
        return 'Product ID: {} | Rating : {}'.format(str(self.productID), str(self.ratings))

    class Meta:
        verbose_name_plural = "Ratings"


class Attributes(models.Model):
    productID = models.ForeignKey(Products, on_delete=models.SET_NULL, null=True)
    bulletin1 = models.CharField(null=True, blank=True, max_length=64)
    bulletin2 = models.CharField(null=True, blank=True, max_length=64)
    bulletin3 = models.CharField(null=True, blank=True, max_length=64)
    bulletin4 = models.CharField(null=True, blank=True, max_length=64)
    bulletin5 = models.CharField(null=True, blank=True, max_length=64)

    def __str__(self):
        return str(self.productID)

    class Meta:
        verbose_name_plural = "Attributes"
