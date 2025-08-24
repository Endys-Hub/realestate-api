from django.db import models
from django.contrib.auth.models import User

class Listing(models.Model):
    CATEGORY_CHOICES = [
        ('sale', 'Sale'),
        ('rent', 'Rent'),
        ('buy', 'Buy'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    is_published = models.BooleanField(default=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Enquiry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Enquiry by {self.user.username}"

'''
from django.db import models
from django.contrib.auth.models import User

class Listing(models.Model):
    CATEGORY_CHOICES = [
        ('sale', 'Sale'),
        ('rent', 'Rent'),
        ('buy', 'Buy')
    ]

    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    is_published = models.BooleanField(default=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Enquiry(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Enquiry from {self.name}"


from django.db import models
from django.contrib.auth.models import User

class Listing(models.Model):
    CATEGORY_CHOICES = [
        ('sale', 'Sale'),
        ('rent', 'Rent'),
        ('buy', 'Buy'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    is_published = models.BooleanField(default=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Enquiry(models.Model):
        user = models.ForeignKey(User, on_delete=models.CASCADE)
        listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
        message = models.TextField()
        created_at = models.DateTimeField(auto_now_add=True)
'''