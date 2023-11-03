from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth import logout
from .models import Transaction

@login_required
def home(request):
    transactions = Transaction.objects.all()
    balance = sum(transaction.amount for transaction in transactions)

    runningTotal = []
    data = []
    label = []


    for i in range(len(transactions)):

        runningTotal.append(int(transactions[i].amount))

        data.append(sum(runningTotal))
        
        label.append(i + 1)
    

    return render(request, 'transactions/home.html', {'transactions': transactions, 'balance': balance, 'data' : data, 'label' : label})

@login_required
def deposit(request):
    if request.method == 'POST':
        amount = request.POST.get('amount')
        reason = request.POST.get('reason')
        category = request.POST.get('category')
        if amount:
            Transaction.objects.create(amount=amount, reason=reason, category=category)
    return redirect('home')

@login_required
def withdraw(request):
    if request.method == 'POST':
        amount = request.POST.get('amount')
        reason = request.POST.get('reason')
        category = request.POST.get('category')
        if amount:
            Transaction.objects.create(amount=-float(amount), reason=reason, category=category)
    return redirect('home')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def custom_logout(request):
    logout(request)
    return redirect('home')

def faq(request):
    return render(request, 'transactions/faq.html')