from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth import logout
from .models import Transaction
from .models import MoneyRequest
from .forms import MoneyRequestForm

@login_required
def home(request):
    transactions = Transaction.objects.all()
    money_requests = MoneyRequest.objects.all()
    balance = sum(transaction.amount for transaction in transactions)

    runningTotal = []
    data = []
    label = []

    for i in range(len(transactions)):
        runningTotal.append(int(transactions[i].amount))
        data.append(sum(runningTotal))
        label.append(i + 1)

    return render(request, 'transactions/home.html', {
        'transactions': transactions,
        'money_requests': money_requests,
        'balance': balance,
        'data': data,
        'label': label
    })

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

@login_required
def request_money(request):
    if request.method == 'POST':
        form = MoneyRequestForm(request.POST)
        if form.is_valid():
            money_request = form.save(commit=False)
            money_request.requester = request.user
            money_request.save()
            return redirect('home')
    else:
        form = MoneyRequestForm()
    
    return render(request, 'transactions/request_money.html', {'form': form})

@login_required
def money_requests(request):
    money_requests = MoneyRequest.objects.all()
    return render(request, 'transactions/money_requests.html', {'money_requests': money_requests})

@login_required
def approve_request(request, request_id):
    money_request = MoneyRequest.objects.get(id=request_id)
    if request.user == money_request.requester and money_request.status == 'pending':
        money_request.status = 'approved'
        money_request.save()
    return redirect('money_requests')

@login_required
def reject_request(request, request_id):
    money_request = MoneyRequest.objects.get(id=request_id)
    if request.user == money_request.requester and money_request.status == 'pending':
        money_request.status = 'rejected'
        money_request.save()
    return redirect('money_requests')

@login_required
def kid_view(request):
    if request.user.is_authenticated:
        transactions = Transaction.objects.all()
        money_requests = MoneyRequest.objects.filter(requester=request.user)
    else:
        transactions = []
        money_requests = []

    return render(request, 'transactions/kid_view.html', {'transactions': transactions, 'money_requests': money_requests})
