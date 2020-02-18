from django.shortcuts import render ,redirect
from django.http import HttpResponse,HttpResponseRedirect
from .models import User, Position, Account,Retour,Pack,Versement,Confirmation,Payement,Fees,Gestionnaire
from .forms import Login_form, Signup_form, Account_form, Position_form,Versement_form,Fees_form,Account_fees_form,Conf_versement_form,LogAdmin_form,Conf_payement_form
from .traitement import verif_insc, get_positions, encode, decode
from django.core.files import File
from PIL import Image
from django.urls import reverse
from datetime import date
import datetime
from django.utils import timezone

# Create your views here.

def index(request):
	inc ='0'
	return render(request,'ligdi/index.html', {'inc':inc})

def login(request):
	if request.method=='POST':
		form = Login_form(request.POST)
		if form.is_valid():
			try:
				m = User.objects.get(username=request.POST['username'])
				m.u_type ="nml"
				if m.password == request.POST['password']:
					if m.a_state == 'notFill':
						return redirect('/account')
					else: 
						try:
							a = Account.objects.get(user=m)
							userna= encode(m.username)
							return redirect('dashboard2', userna)

						except Position.DoesNotExist:
							inc =1
							return render(request,'ligdi/dashboard.html', {'m':m})

				else: 
					inc = 1
					return render(request,'ligdi/login.html', {'inc':inc})	
			except User.DoesNotExist:
				inc =2
				return render(request,'ligdi/login.html', {'inc':inc})	
	return render(request,'ligdi/login.html')

def signup(request):
	if request.method=='POST':
		form=Signup_form(request.POST)
		if form.is_valid():
			result = verif_insc(us_na=request.POST['username'],eml=request.POST['email'], pwrd=request.POST['password'], pwrdcf=request.POST['passwordconf'],cdts=request.POST['conditions'], id_n=request.POST['id_number'])
			if result['t'] != 5:
				return render(request, 'ligdi/signup.html',{'result':result})

			if result['t'] == 5:
				m = User.objects.create(username=request.POST['username'],email=request.POST['email'],password=request.POST['password'],id_number=request.POST['id_number'])
				a = Account.objects.create(user=m)
				return redirect('/account')

	return render(request,'ligdi/signup.html')


def account(request):
	if request.method =='POST':
		form=Account_form(request.POST, request.FILES)
		if form.is_valid():
			try:
				m = User.objects.get(username=request.POST['username'])
				if m.password == request.POST['password']:
					a= Account.objects.get(user__username__contains=request.POST['username'])
					a.firstname=request.POST['firstname']
					a.lastname=request.POST['lastname']
					a.country=request.POST['country']
					a.phone=request.POST['phone']
					a.operator=request.POST['operator']
					m.a_state = 'Fill'
					a.id_pic = request.FILES['id_picture']
					a.save()
					m.save()
					userna= encode(m.username)
					return redirect('dashboard2',userna)
				else:
					inc =2
					return render(request, 'ligdi/compte.html',{'inc':inc})
			except:
				inc =3
				return render(request, 'ligdi/compte.html',{'inc':inc})
		else:
			inc =5
			return render(request, 'ligdi/compte.html',{'inc':inc})

	return render(request, 'ligdi/compte.html')

def engage(request,userna):
	if request.method=='POST':
		form = Position_form(request.POST)
		if form.is_valid():
			userna=decode(userna)
			try:
				a= Account.objects.get(user__username=userna)
				if a.acc_fees == 'notPaid':
					inc = 1
					return render(request,'ligdi/dashboard.html',{'inc':inc})
			except Account.DoesNotExist:
				return render(request,'ligdi/expire.html')
			else:
				pa = Pack.objects.get(pack_name=request.POST['pack'] )
				pos = Position.objects.create(pack=pa, pos_date=date.today(), account=a )
				ret_am = (pa.pack_pos_amount*2)
				ret = Retour.objects.create(position=pos,ret_amount=ret_am,ret_date_max=date.today())
				m=User.objects.get(account=a)
				ver=Versement.objects.create(vers_date=date.today(),position=pos)
				a.pos_en_cour = True
				a.save()

				userna = encode(m.username)
				return redirect('dashboard2', userna)
				
		else:
			return redirect('dashboard2', userna)


def dashboard(request, userna): 
	try:
		userna=decode(userna)
		a=Account.objects.get(user__username=userna)
		m = User.objects.get(account=a)
		all_pos = Position.objects.filter(account__user=m).order_by('-id')
		now= date.today()
		data = {'positions':all_pos,'m':m,'now':now}
		return render(request,'ligdi/dashboard.html',{'data':data})
	except User.DoesNotExist:
		return render(request,'ligdi/expire.html')
	except Account.DoesNotExist:
		return render(request,'ligdi/expire.html')

	if request.method=='POST':
		form = Posistion_form(request.POST)
		if form.is_valid():
			m=User.objects.get(username=request.POST['username'])
			a=Account.objects.get(user=m)
			if a.acc_fees == 'notPaid':
				inc = 1
				return render(request,'ligdi/dashboard.html',{'inc':inc})
			else:
				pa = request.POST['pack'] 
				pos = Position.objects.create(pos_date=date.today(),pack=pa, account=a, pos_duration=0 )
				ret_am = (pa.pack_pos_amount*2)
				ret = Retour.objects.create(position=pos,ret_amount=ret_am)
				userna= encode(m.username)
				return redirect('dashboard2', userna)

def versement(request,userna):
	if request.method=="POST":
		form = Versement_form(request.POST)
		if form.is_valid():
			pos=Position.objects.get(id=request.POST['position'])
			pa=pos.pack
			ver=Versement.objects.get(position=pos)
			ver.vers_amount = pa.pack_pay_tot
			ver.vers_compte = request.POST['vers_compte']
			ver.vers_num = request.POST['vers_num']
			ver.vers_nom = request.POST['vers_nom']
			ver.vers_tel = request.POST['vers_tel']
			ver.vers_state = True
			ver.save()
			conf = Confirmation.objects.create(conf_date=date.today(),versement=ver,conf_state=False)
			ret=Retour.objects.get(position=pos)
			ret.ret_date_max= timezone.now() + datetime.timedelta(days=7)
			ret.save()
			return redirect('dashboard2', userna)
		else:
			return render(request,'ligdi/login')

def fees(request,userna):
	if request.method == 'POST':
		form = Fees_form(request.POST)
		if form.is_valid():
			a=Account.objects.get(id=request.POST['account'])
			fee = Fees.objects.create(account=a,fees_date=date.today(),fees_exp_date=timezone.now() + datetime.timedelta(days=30))
			a.acc_fees = 'Pending'
			a.save()
			return redirect('dashboard2',userna)


def administration(request,userna):
	try:
		ges = decode(userna)
		gest = Gestionnaire.objects.get(ges_username=ges)
		return render(request,'ligdi/administration.html',{'gest':gest})
	except Gestionnaire.DoesNotExist:	
		return redirect(logAdmin)	

def frai_compte_exp(request,userna):
	try:
		ges = decode(userna)
		gest=Gestionnaire.objects.get(ges_username=ges)
		all_account = Account.objects.all()
		return render(request,'ligdi/frai_compte_exp.html',{'all_account':all_account})
	except Gestionnaire.DoesNotExist:
		return redirect(logAdmin)


def conf_frai_compte(request):
	if request.method=="POST":
		form = Account_fees_form(request.POST)
		if form.is_valid():
			a = Account.objects.get(user__username=request.POST['username'])
			a.acc_fees = 'Paid'
			a.save()
			return redirect(frai_compte_exp)

def vers_list(request,userna):
	try:
		ges=decode(userna)
		gest = Gestionnaire.objects.get(ges_username=ges)
		vers= Versement.objects.all()
		return render(request,'ligdi/vers_list.html',{'vers':vers})
	except Gestionnaire.DoesNotExist:
		return redirect(logAdmin)

def conf_versement(request,userna):
	if request.method=='POST':
		form = Conf_versement_form(request.POST)
		if form.is_valid():
			vers = Versement.objects.get(id=request.POST['versement'])
			conf = Confirmation.objects.get(versement=vers)
			conf.conf_state = True
			conf.conf_date = date.today()
			conf.conf_admin = decode(userna)
			a = Account.objects.get(position__versement=vers)
			a.pos_en_cour = False
			conf.save()
			vers.save()
			a.save()
			pay = Payement.objects.create(versement=vers,pay_state=False,pay_date=date.today())
			return redirect(vers_list,userna)

def conf_payement(request,userna):
	try:
		ges = decode(userna)
		gest = Gestionnaire.objects.get(ges_username=ges)
		positions=Position.objects.all()
		if request.method=='POST':
			form = Conf_payement_form(request.POST)
			if form.is_valid():
				pos = Position.objects.get(id=request.POST['position'])
				vers = Versement.objects.get(position=pos)
				pay = Payement.objects.get(versement=vers)
				pay.pay_state=True
				pay.pay_date=date.today()
				pay.pay_amount=request.POST['pay_amount']
				pay.pay_trans_num=request.POST['trans_id']
				pay.save()
				pos.pos_state=True
				pos.save()
				return render(request,'ligdi/conf_payement.html',{'positions':positions})
		else:
			return render(request,'ligdi/conf_payement.html',{'positions':positions})
	except Gestionnaire.DoesNotExist:
		return redirect(logAdmin)

		
def list_payement(request,userna):
	try:
		ges = decode(userna)
		gest = Gestionnaire.objects.get(ges_username=ges)
		positions=Position.objects.all()
		if request.method=='POST':
			form = Conf_payement_form(request.POST)
			if form.is_valid():
				pos = Position.objects.get(id=request.POST['position'])
				vers = Versement.objects.get(position=pos)
				pay = Payement.objects.get(versement=vers)
				pay.pay_state=True
				pay.pay_date=date.today()
				pay.pay_amount=request.POST['pay_amount']
				pay.pay_trans_num=request.POST['trans_id']
				pay.save()
				pos.pos_state=True
				pos.save()
				return render(request,'ligdi/conf_payement.html',{'positions':positions})
		else:
			return render(request,'ligdi/conf_payement.html',{'positions':positions})
	except Gestionnaire.DoesNotExist:
		return redirect(logAdmin)


def logAdmin(request):
	if request.method=='POST':
		form = LogAdmin_form(request.POST)
		if form.is_valid():
			try:
				gest = Gestionnaire.objects.get(ges_username=request.POST['ges_username'])
				if gest.ges_password == request.POST['ges_password']:
					userna = encode(gest.ges_username)
					gest.ges_las_log = timezone.now()
					gest.save()
					return redirect(administration,userna)
				else:
					inc=1
					return render(request,'ligdi/logAdmin.html',{'inc':inc})
			except Gestionnaire.DoesNotExist:
				inc=2
				return render(request,'ligdi/logAdmin.html',{'inc':inc})
		else:
			return render(request,'ligdi/logAdmin.html')
	return render(request,'ligdi/logAdmin.html')