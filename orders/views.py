from django.shortcuts import render, redirect
from .models import Book, Customer, Order
from .forms import BookForm, CustomerForm, OrderForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models.functions import TruncDay, TruncMonth, TruncYear
from django.db.models import Sum, Count


@login_required
def order_index(request):
    orders = Order.objects.order_by('-id')
    return render(request, 'order_index.html', {'orders': orders})


@login_required
def order_by_day(request):
    summaries = Order.objects.annotate(day=TruncDay('date')).values('day').annotate(sum=Sum('total_price')).values(
        'day', 'sum').annotate(count=Count('id')).values('day', 'sum', 'count').order_by('-day')
    return render(request, 'order_by_day.html', {'summaries': summaries})


@login_required
def order_by_month(request):
    summaries = Order.objects.annotate(month=TruncMonth('date')).values('month').annotate(
        sum=Sum('total_price')).values(
        'month', 'sum').annotate(count=Count('id')).values('month', 'sum', 'count').order_by('-month')
    return render(request, 'order_by_month.html', {'summaries': summaries})


@login_required
def book_rank(request):
    ranks = Order.objects.all().values('book__book_name').annotate(count=Sum('quantity')).values('book__book_name',
                                                                                                 'count').order_by(
        '-count')
    return render(request, 'book_rank.html', {'ranks': ranks})


@login_required
def order_by_year(request):
    summaries = Order.objects.annotate(year=TruncYear('date')).values('year').annotate(sum=Sum('total_price')).values(
        'year', 'sum').annotate(count=Count('id')).values('year', 'sum', 'count').order_by('-year')
    return render(request, 'order_by_year.html', {'summaries': summaries})


@login_required
def show_order(request, order_id):
    order = Order.objects.filter(id=order_id)
    return render(request, 'show_order.html', {'order': order})


def discount(customer):
    if (customer.level() - 1) / 20 < 0.4:
        return (customer.level() - 1) / 20
    else:
        return 0.4


@login_required
def new_order(request):
    if request.POST:
        form = OrderForm(request.POST)
        current_book_id = form.data['book']
        current_customer_id = form.data['customer']
        quantity = int(form.data['quantity'])
        current_book = Book.objects.get(id=current_book_id)
        current_book.stock -= quantity
        if current_book.stock < 0:
            return redirect('/', messages.error(request, 'Book is out of stock.', 'alert-danger'))
        if form.is_valid():
            if form.save():
                current_order = Order.objects.latest('id')
                current_order.total_price = current_order.get_total_price()
                current_order.save()
                current_book.save()
                current_customer = Customer.objects.get(id=current_customer_id)
                current_customer.total_payment += current_order.total_price
                current_customer.save()
                return redirect('/', messages.success(request, 'Order was successfully created.', 'alert-success'))
            else:
                return redirect('/', messages.error(request, 'Data is not saved', 'alert-danger'))
        else:
            return redirect('/', messages.error(request, 'Form is not valid', 'alert-danger'))
    else:
        form = OrderForm()
        return render(request, 'new_order.html', {'form': form})


@login_required
def edit_order(request, order_id):
    order = Order.objects.get(id=order_id)
    last_book_id = order.book.id
    last_quantity = order.quantity
    last_customer_id = order.customer.id
    last_total_price = order.total_price
    if request.POST:
        form = OrderForm(request.POST, instance=order)
        current_book_id = form.data['book']
        current_customer_id = form.data['customer']
        quantity = int(form.data['quantity'])
        if form.is_valid():
            if form.save():
                last_book = Book.objects.get(id=last_book_id)
                last_book.stock += last_quantity
                # print(last_book.stock)
                last_book.save()
                current_book = Book.objects.get(id=current_book_id)
                current_book.stock -= quantity
                if current_book.stock < 0:
                    order.quantity = last_quantity
                    order.save()
                    last_book.stock -= last_quantity
                    last_book.save()
                    return redirect('/', messages.error(request, 'Book is out of stock.', 'alert-danger'))
                else:
                    current_book.save()
                    last_customer = Customer.objects.get(id=last_customer_id)
                    last_customer.total_payment -= last_total_price
                    last_customer.save()
                    order.total_price = order.get_total_price()
                    order.save()
                    current_customer = Customer.objects.get(id=current_customer_id)
                    current_customer.total_payment += order.total_price
                    current_customer.save()
                    return redirect('/', messages.success(request, 'Order was successfully updated.', 'alert-success'))
            else:
                return redirect('/', messages.error(request, 'Data is not saved', 'alert-danger'))
        else:
            return redirect('/', messages.error(request, 'Form is not valid', 'alert-danger'))
    else:
        form = OrderForm(instance=order)
        return render(request, 'edit_order.html', {'form': form})


@login_required
def destroy_order(request, order_id):
    order = Order.objects.get(id=order_id)
    last_book = order.book
    last_quantity = order.quantity
    last_customer = order.customer
    last_total_price = order.total_price
    last_book = Book.objects.get(book_name=last_book)
    last_book.stock += last_quantity
    last_book.save()
    last_customer = Customer.objects.get(customer_name=last_customer)
    last_customer.total_payment -= last_total_price
    last_customer.save()
    order.delete()
    return redirect('/', messages.success(request, 'Order was successfully deleted.', 'alert-success'))


@login_required
def customer_index(request):
    customers = Customer.objects.order_by('-id')
    return render(request, 'customer_index.html', {'customers': customers})


@login_required
def new_customer(request):
    if request.POST:
        form = CustomerForm(request.POST)
        if form.is_valid():
            if form.save():
                return redirect('/customers',
                                messages.success(request, 'Customer was successfully created.', 'alert-success'))
            else:
                return redirect('/customers', messages.error(request, 'Data is not saved', 'alert-danger'))
        else:
            return redirect('/customers', messages.error(request, 'Form is not valid', 'alert-danger'))
    else:
        form = CustomerForm()
        return render(request, 'new_customer.html', {'form': form})


@login_required
def edit_customer(request, customer_id):
    customer = Customer.objects.get(id=customer_id)
    if request.POST:
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            if form.save():
                return redirect('/customers',
                                messages.success(request, 'Customer was successfully updated.', 'alert-success'))
            else:
                return redirect('/customers', messages.error(request, 'Data is not saved', 'alert-danger'))
        else:
            return redirect('/customers', messages.error(request, 'Form is not valid', 'alert-danger'))
    else:
        form = CustomerForm(instance=customer)
        return render(request, 'edit_customer.html', {'form': form})


@login_required
def destroy_customer(request, customer_id):
    customer = Customer.objects.get(id=customer_id)
    customer.delete()
    return redirect('/customers', messages.success(request, 'Customer was successfully deleted.', 'alert-success'))


@permission_required('is_superuser', raise_exception=True)
def book_index(request):
    books = Book.objects.order_by('-id')
    return render(request, 'book_index.html', {'books': books})


@permission_required('is_superuser', raise_exception=True)
def new_book(request):
    if request.POST:
        form = BookForm(request.POST)
        if form.is_valid():
            if form.save():
                return redirect('/books', messages.success(request, 'Book was successfully added.', 'alert-success'))
            else:
                return redirect('/books', messages.error(request, 'Data is not saved', 'alert-danger'))
        else:
            return redirect('/books', messages.error(request, 'Form is not valid', 'alert-danger'))
    else:
        form = BookForm()
        return render(request, 'new_book.html', {'form': form})


@permission_required('is_superuser', raise_exception=True)
def edit_book(request, book_id):
    book = Book.objects.get(id=book_id)
    if request.POST:
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            if form.save():
                return redirect('/books', messages.success(request, 'Book was successfully updated.', 'alert-success'))
            else:
                return redirect('/books', messages.error(request, 'Data is not saved', 'alert-danger'))
        else:
            return redirect('/books', messages.error(request, 'Form is not valid', 'alert-danger'))
    else:
        form = BookForm(instance=book)
        return render(request, 'edit_book.html', {'form': form})


@permission_required('is_superuser', raise_exception=True)
def destroy_book(request, book_id):
    book = Book.objects.get(id=book_id)
    book.delete()
    return redirect('/books', messages.success(request, 'Book was successfully deleted.', 'alert-success'))
