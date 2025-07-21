from django.shortcuts import render, redirect

# Create your views here.

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import transaction
from .models import Account

from django.views.decorators.cache import never_cache

from django.views.decorators.csrf import csrf_exempt #FLAW 1! This flaw is fixed by removing all @csrf_exempt

@login_required
@never_cache #This could lead to security issues. In this app it prevents a serious security issue of being able to view account information after logging out.
@csrf_exempt #fix by removing
def transferView(request):
	
	if request.method == 'POST':
		receiver_name = User.objects.get(username=request.POST.get('to'))
		amount = request.POST.get('amount')

		if not amount:
			return redirect('/')
		
		amount = int(amount)
		
		#FLAW 2! Allowing transfer of negative amounts leaving other accounts vulnerable. Very simple fix the two rows below.
		#if amount <= 0:
		#	return redirect('/')
		

		sender = Account.objects.get(user = request.user) 
		receiver = Account.objects.get(user = receiver_name)

		if sender.balance < amount:
			return redirect('/')
		

		with transaction.atomic():    
			sender.balance -= amount
			sender.save()

			receiver.balance += amount
			receiver.save()

	return redirect('/')



@login_required
@never_cache
@csrf_exempt #fix by removing
def homeView(request):
	accounts = Account.objects.all() #FLAW 3! This allows all accounts to be shown.
	#accounts = Account.objects.exclude(user_id = request.user.id) ## Using this in combination with the fix in index.html will fix the flaw. 
	#Using this in combination with the flawed index.html code will not fix the problem, it will only exclude the logged in users own account from the accounts shown.

	#PART OF FLAW 5! We get the users account and their password and pass it to the template. This in it self is not the security flaw.
	user = request.user.account
	insecurely_stored_password = user.recovery_password

	return render(request, 'polls/index.html', {'accounts': accounts, 'insecurely_stored_password': insecurely_stored_password})
