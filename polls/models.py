from django.db import models

from django.contrib.auth.models import User


from django.contrib.auth.hashers import make_password #Needed to fix flaw 5.


# Create your models here.

class Account(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	balance = models.IntegerField()

	#FLAW 5! My web app does not actually have a recovery option, however this is to demonstrate a possible flaw.
	#The fifth flaw is demonstrating sensitive data transmitted in plain text.
	recovery_password = models.CharField(max_length=128, blank=True, null=True)

	#FLAW 5 fix! 
	#def save(self, *args, **kwargs):
		#if self.recovery_password and not self.recovery_password.startswith('pbkdf2_'):
			#self.recovery_password = make_password(self.recovery_password)
		#super().save(*args, **kwargs)