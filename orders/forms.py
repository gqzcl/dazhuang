from django.forms import ModelForm
from django import forms
from .models import Book, Customer, Order
from django.forms import ModelChoiceField, EmailField


class BookForm(ModelForm):
    CATEGORY = (
        ('', ''),
        ('Arts & Music', 'Arts & Music'),
        ('Biographies', 'Biographies'),
        ('Business', 'Business'),
        ('Kids', 'Kids'),
        ('Comics', 'Comics'),
        ('Computers & Tech', 'Computers & Tech'),
        ('Cooking', 'Cooking'),
        ('Hobbies & Crafts', 'Hobbies & Crafts'),
        ('Edu & Reference', 'Edu & Reference'),
        ('Gay & Lesbian', 'Gay & Lesbian'),
        ('Health & Fitness', 'Health & Fitness'),
        ('History', 'History'),
        ('Home & Garden', 'Home & Garden'),
        ('Horror', 'Horror'),
        ('Entertainment', 'Entertainment'),
        ('Literature & Fiction', 'Literature & Fiction'),
        ('Medical', 'Medical'),
        ('Mysteries', 'Mysteries'),
        ('Parenting', 'Parenting'),
        ('Social Sciences', 'Social Sciences'),
        ('Religion', 'Religion'),
        ('Romance', 'Romance'),
        ('Science & Math', 'Science & Math'),
        ('Sci-Fi & Fantasy', 'Sci-Fi & Fantasy'),
        ('Self-Help', 'Self-Help'),
        ('Sports', 'Sports'),
        ('Teen', 'Teen'),
        ('Travel', 'Travel'),
        ('True Crime', 'True Crime'),
        ('Westerns', 'Westerns')
    )
    book_categories = forms.ChoiceField(choices=CATEGORY)

    class Meta:
        model = Book
        fields = ['isbn', 'book_name', 'author', 'price', 'stock', 'book_categories', 'publisher']


class CustomerForm(ModelForm):

    class Meta:
        model = Customer
        email = EmailField()
        fields = ['customer_name', 'phone', 'email']


class OrderForm(ModelForm):
    customer = ModelChoiceField(Customer.objects.all(), empty_label='')
    book = ModelChoiceField(Book.objects.filter(stock__gt=0), empty_label='')

    class Meta:
        model = Order
        fields = ['customer', 'book', 'quantity', 'shipping_address']
