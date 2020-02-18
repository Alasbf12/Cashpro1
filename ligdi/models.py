from django.db import models
from PIL import Image
from datetime import date
# Create your models here.

class User(models.Model):
	username = models.CharField(max_length = 100, primary_key =True)
	email = models.CharField(max_length = 100)
	password = models.CharField(max_length = 100)
	id_number = models.CharField(max_length=100, default='B')
	a_state = models.CharField(max_length=100, default='notFill')
	
	def __str__(self):
		return self.username

class Account(models.Model):
	firstname = models.CharField(max_length = 100, default='none')
	lastname = models.CharField(max_length = 100, default='none')
	country = models.CharField(max_length=100, default = 'bf')
	phone = models.IntegerField(default=00000000)
	operator = models.CharField(max_length=100, default=' ' )
	user = models.OneToOneField(User, on_delete= models.CASCADE)
	acc_type = models.CharField(max_length = 100, default = 'normal')
	acc_state = models.CharField(max_length = 100, default = 'al')
	acc_fees = models.CharField(max_length = 100, default = 'notPaid')
	id_picture = models.ImageField(upload_to='ligdi/static/ligdi/ids')
	pos_en_cour = models.BooleanField(default=False)
	
	def __str__(self):
		return self.user.username
class Fees(models.Model):
	fees_date = models.DateField()
	fees_exp_date=models.DateField()
	account = models.ForeignKey(Account, on_delete=models.CASCADE)
	fees_tel =models.CharField(max_length=100 ,default=0)
	fees_num = models.CharField(max_length=100,default='')

class Pack(models.Model):
	pack_name = models.CharField(primary_key=True,max_length=100, default='none')
	pack_pos_fee = models.IntegerField(default=0)
	pack_pos_amount = models.IntegerField(default=0)
	pack_pay_tot = models.IntegerField(default=0)

	def __str__(self):
		return self.pack_name


class Position(models.Model):
	pos_date = models.DateField()
	pack = models.ForeignKey(Pack,on_delete=models.CASCADE)
	account = models.ForeignKey(Account,on_delete=models.CASCADE)
	pos_state = models.BooleanField(default=False)

	def __str__(self):
		x=str(self.id)
		return (" Position : "+x+" de "+self.account.user.username)


class Retour(models.Model):
	position= models.OneToOneField(Position,on_delete=models.CASCADE)
	ret_amount = models.IntegerField(default=0)
	ret_date_max = models.DateField()

	def __str__(self):
		x=str(self.position.id)
		y=str(self.position.account)
		return ("retour de la position "+x+" de "+y)

class Versement(models.Model):
	vers_date = models.DateField()
	position = models.OneToOneField(Position, on_delete=models.CASCADE)
	vers_amount = models.IntegerField(default=0)
	vers_compte = models.CharField(max_length=100, default=' ')
	vers_num = models.CharField(max_length=100, default=' ')
	vers_nom = models.CharField(max_length=100,default=' ')
	vers_tel = models.CharField(max_length=100, default=0)
	vers_state = models.BooleanField(default=False)

	def __str__(self):
		x= str(self.id)
		y= str(self.position.account)
		return("versement "+x+" de "+ y )

class Confirmation(models.Model):
	conf_date = models.DateField()
	conf_state = models.BooleanField(default=False)
	versement = models.OneToOneField(Versement,on_delete=models.CASCADE)
	conf_admin = models.CharField(max_length=100,default=' ')

	def __str__(self):
		x=str(self.versement.id)
		y=str(self.versement.position.account)
		return ("Versement "+x +" de "+ y)

class Payement(models.Model):
	pay_amount = models.IntegerField(default=0)
	versement = models.OneToOneField(Versement,on_delete=models.CASCADE)
	pay_state = models.BooleanField(default=False)
	pay_date = models.DateField()
	pay_trans_num = models.CharField(max_length=100,default=' ')

class Gestionnaire(models.Model):
	ges_username = models.CharField(max_length=100,default='')
	ges_password = models.CharField(max_length=100, default='')
	ges_firtname = models.CharField(max_length=100)
	ges_lastname =  models.CharField(max_length=100)
	ges_phone =  models.IntegerField()
	ges_email =  models.CharField(max_length=100)
	ges_is_active = models.BooleanField(default=True)
	ges_las_log = models.DateField()
	ges_conf_frai = models.BooleanField(default=False)
	ges_conf_vers = models.BooleanField(default=False)
	ges_conf_pay= models.BooleanField(default=False)
	
	def __str__(self):
		return self.ges_firstname





