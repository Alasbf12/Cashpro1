from django import forms
from PIL import Image
from .models import User,Account

class Login_form(forms.Form):
	username = forms.CharField(label='username', max_length = 100)
	password = forms.PasswordInput()
	
class Signup_form(forms.Form):
	username= forms.CharField(label='username')
	email = forms.EmailField(label = 'email')
	password = forms.PasswordInput()
	passwordconf = forms.PasswordInput()
	id_number = forms.CharField(label = 'id_number')
	conditions = forms.CheckboxInput()

class Account_form(forms.Form):
	firstname = forms.CharField(label='firstname')
	lastname = forms.CharField(label='lastname')
	country = forms.CharField(label='country')
	phone = forms.CharField(label='phone')
	operator = forms.CharField(label = 'operator')
	id_picture = forms.ImageField()
	username = forms.CharField(label="username", max_length=100 )
	password = forms.PasswordInput()

class Position_form(forms.Form):
	pack = forms.CharField(label='pack')
	username = forms.CharField(label='username')

class Versement_form(forms.Form):
	vers_tel = forms.CharField(label='vers_tel')
	vers_num = forms.CharField(label='vers_num')
	vers_nom = forms.CharField(label='vers_nom')
	position = forms.IntegerField(label='position')
	vers_compte = forms.CharField(label='vers_compte')

class Fees_form(forms.Form):
	vers_tel = forms.CharField(label='vers_tel')
	vers_num = forms.CharField(label='vers_num')
	vers_nom = forms.CharField(label='vers_nom')
	account = forms.IntegerField(label='account')
	vers_compte = forms.CharField(label='vers_compte')
	

class Account_fees_form(forms.Form):
	username = forms.CharField(label='username')
	checkbox = forms.CheckboxInput()

class Conf_versement_form(forms.Form):
	checkbox = forms.CheckboxInput()
	versement = forms.CharField(label='versement')

class Conf_payement_form(forms.Form):
	pay_amount=forms.IntegerField(label='pay_amount')
	checkbox = forms.CheckboxInput()
	position = forms.IntegerField(label='position')
	trans_id = forms.CharField(label='trans_id')

class LogAdmin_form(forms.Form):
	ges_username = forms.CharField(label='ges_username')
	ges_password = forms.CharField(label='ges_password')
