from ligdi.models import User
from django.utils import timezone

def verif_insc(us_na,eml, pwrd, pwrdcf,cdts, id_n):

	result1 = {'e':0,'i':0,'p':0,'c':0, 't':0, 'n':0}

	try:
		a = User.objects.get(username=us_na)
		if us_na == a.username:
			result1['n'] = 1
	except :
		result1['t']+=1

	try:
		e = User.objects.get(email=eml)
		if eml == e.email:
			result1['e'] = 1
	except :
		result1['t']+=1

	try:
		i = User.objects.get(id_number=id_n) 
		if id_n == i.id_number:
			result1['i'] = 1
	except : 
		result1['t']+=1


	if (pwrd != pwrdcf and pwrd.length < 8):
		result1['p'] = 1
	else:
		result1['t']+=1

	if cdts != 'on' :
		result1['c'] = 1
	else:
		result1['t']+=1

	return result1


def encode(nbr1):
	a = timezone.now()
	b = str(a)
	i=0
	c=''
	d=''
	while i<=14:
		c=c+ b[i]
		i+=1
	for h in c:
		if h=='-' or h==' ' or h==':':
			continue
		d=d+h
	s=0
	z=''
	for r in d:
		if s>=6:
			z=z+r
		s+=1

	d=int(z)
	code=''
	for x in nbr1:
		temp = ord(x)*d
		temp = str(temp)
		code = code+temp+'%'

	return code

	

def decode(code):
	a = timezone.now()
	b = str(a)
	i=0
	c=''
	d=''
	while i<=14:
		c=c+ b[i]
		i+=1
	for h in c:
		if h=='-' or h==' ' or h==':':
			continue
		d=d+h
	s=0
	z=''
	for r in d:
		if s>=6:
			z=z+r
		s+=1

	d=int(z)
	temp=''
	nbr1=''
	for x in code:
		if x=='%':
			temp = int(temp)/d
			temp=chr(int(temp))
			nbr1=nbr1+temp
			temp=''
			continue
		temp = temp+x

	return nbr1


def get_positions(us_na):
	result = []
	all_pos = Position.objects.get(account__user__username=us_na)
	result.append(all_pos)
	i = all_pos.length
	return result
