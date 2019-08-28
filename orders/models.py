from django.db import models
import math


# Create your models here.

class Book(models.Model):
    isbn = models.CharField(max_length=20)
    book_name = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    price = models.FloatField()
    stock = models.IntegerField()
    book_categories = models.CharField(max_length=50)
    publisher = models.CharField(max_length=50)

    def __str__(self):
        return self.book_name


class Customer(models.Model):
    customer_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    email = models.CharField(max_length=50)
    total_payment = models.FloatField(default=0)

    def level(self):
        return round((math.sqrt(self.total_payment) / 5) + 1)

    def __str__(self):
        return self.customer_name


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    shipping_address = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    total_price = models.FloatField(default=0)

    @staticmethod
    def discount(customer):
        if (customer.level() - 1) / 20 < 0.4:
            return (customer.level() - 1) / 20
        else:
            return 0.4

    def get_discount_percent(self):
        return (1 - self.total_price / (self.book.price * self.quantity)) * 100

    def get_total_price(self):
        return self.book.price * self.quantity * (1 - self.discount(self.customer))

    def get_original_total_price(self):
        return self.book.price * self.quantity
