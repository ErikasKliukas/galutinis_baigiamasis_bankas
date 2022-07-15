from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
import random
from . models import *
from . forms import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def home(request):
    return render(request, 'account/base.html')


def signup(request):
    if request.method == 'GET':
        return render(request, 'account/signup.html', {'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('index')
            except IntegrityError:
                return render(request, 'account/signup.html', {'form':UserCreationForm(), 'error':'That username has already been taken. Please choose a new username'})
        else:
            return render(request, 'account/signup.html', {'form':UserCreationForm(), 'error':'Passwords did not match'})


def loginuser(request):
    if request.method == 'GET':
        return render(request, 'account/login.html', {'form':AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'account/login.html', {'form':AuthenticationForm(), 'error':'Username and password did not match'})
        else:
            login(request, user)
            return redirect('index')


@login_required
def logoutuser(request):
    logout(request)
    return redirect('home')


def randomGen():
    # return a 6 digit random number
    return int(random.uniform(100000, 999999))


@login_required
def index(request):
    try:
        status = Account.objects.get(user=request.user) # getting details of current user
    except:
        # if no details exist (new user), create new details
        status = Account()
        status.account_number = randomGen() # random account number for every new user
        status.balance = 0
        status.user = request.user
        status.save()
    return render(request, "account/index.html", {"curr_user": status})


@login_required
def deposit_view(request):
    form = DepositForm(request.POST or None)
    status = Account.objects.get(user=request.user)

    if form.is_valid():
        deposit = form.save(commit=False)
        deposit.user = request.user
        deposit.save()
        # adds users deposit to balance.
        status.balance += deposit.amount
        status.save()
        messages.success(request, 'You Have Deposited {} $.'
                         .format(deposit.amount))
        return redirect("index")

    context = {
        "title": "Deposit",
        "form": form,
        "curr_user": status,
    }
    return render(request, "account/form.html", context)


@login_required
def withdrawal_view(request):
    status = Account.objects.get(user=request.user)
    form = WithdrawalForm(request.POST or None, user=request.user, status = status)

    if form.is_valid():
        withdrawal = form.save(commit=False)
        withdrawal.user = request.user
        withdrawal.save()
        # subtracts users withdrawal from balance.
        status.balance -= withdrawal.amount
        status.save()

        messages.success(
            request, 'You Have Withdrawn {} $.'.format(withdrawal.amount)
        )
        return redirect("index")

    context = {
        "title": "Withdraw",
        "form": form,
        "curr_user": status,
    }
    return render(request, "account/form.html", context)


@login_required
def transfer_view(request):
    account = Account.objects.get(user=request.user)
    form = Transfer(request.POST or None, account = account)

    if form.is_valid():
        transfer = form.save(commit=False)
        transfer.user = request.user
        transfer.save()

        transfered_to = Account.objects.get(account_number=transfer.to_account)
        transfered_to.balance += transfer.amount
        account.balance -= transfer.amount
        account.save()
        transfered_to.save()

        messages.success(
            request, 'You Have Transfered {} $.'.format(transfer.amount)
        )
        return redirect("index")

    context = {
        "title": "Transfer",
        "form": form,
        "curr_user": account,
    }
    return render(request, "account/form.html", context)


@login_required
def transactions_list_view(request):
    transactions = []
    transfers = models.Transfer.objects.filter(user=request.user).values()
    deposits = models.Deposit.objects.filter(user=request.user).values()
    withdrawals = models.Withdrawal.objects.filter(user=request.user).values()
    for transfer in transfers:
        transfered_to_acc = Account.objects.get(account_number=transfer['to_account'])
        user = transfered_to_acc.user
        data = {
            'amount': f"Transfered {transfer['amount']} to {str.capitalize(user.username)}",
            'timestamp': str(transfer['timestamp']).split('.')[0]
        }
        transactions.append(data)

    for deposit in deposits:
        data = {
            'amount': f"Deposited {deposit['amount']}",
            'timestamp': str(deposit['timestamp']).split('.')[0]
        }
        transactions.append(data)
        
    for withdrawal in withdrawals:
        data = {
            'amount': f"Withdrawed {withdrawal['amount']}",
            'timestamp': str(withdrawal['timestamp']).split('.')[0]
        }
        transactions.append(data)

    return render(request, "account/list.html", {"transactions": transactions})
    