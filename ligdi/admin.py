from django.contrib import admin
# Register your models here.
from ligdi.models import User,Account,Pack,Position,Retour, Payement, Confirmation,Fees,Versement



class AccountAdmin(admin.ModelAdmin):
	list_display = ('id','user','acc_fees','acc_state','phone','operator')
	list_filter = ('id','user')
	search_fields = ('user__username', 'id')

class PositionAdmin(admin.ModelAdmin):
	list_display = ('id','pos_date','pack','account','pos_state')
	list_filter = ('pos_state','id','account')
	search_fields = ('id','pos_date')

class PayementAdmin(admin.ModelAdmin):
	list_display = ('id','pay_amount','versement','pay_state','pay_date','pay_trans_num')
	list_filter = ('id','versement__position__account','pay_state')
	search_fields = ('id','pay_trans_num')

class RetourAdmin(admin.ModelAdmin):
	list_display = ('id','position','ret_amount')
	list_filter = ('id','position__account')
	search_fields = ('id','position__id')

class UserAdmin(admin.ModelAdmin):
	list_display = ('username','email','id_number')
	list_filter = ('username','id_number')
	search_fields = ('id','position__id')

class ConfirmationAdmin(admin.ModelAdmin):
	list_display = ('conf_date','versement','conf_admin','conf_state')
	list_filter = ('id','conf_admin')
	search_fields = ('id','account')

class FeesAdmin(admin.ModelAdmin):
	list_display = ('id','account','fees_date','fees_exp_date')
	list_filter = ('id','fees_exp_date')
	search_fields = ('id','position__id')

class VersementAdmin(admin.ModelAdmin):
	list_display = ('id','vers_date','position','vers_amount','vers_compte','vers_num','vers_nom','vers_tel','vers_state')
	list_filter = ('id','vers_compte')
	search_fields = ('id','position')

admin.site.register(User,UserAdmin)
admin.site.register(Account, AccountAdmin)
admin.site.register(Pack)
admin.site.register(Fees)
admin.site.register(Position,PositionAdmin)
admin.site.register(Retour,RetourAdmin)
admin.site.register(Payement,PayementAdmin)
admin.site.register(Confirmation,ConfirmationAdmin)
admin.site.register(Versement,VersementAdmin)



