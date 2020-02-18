from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [

	path('',views.login),
	path('login/',views.login),
	path('signup/',views.signup),
	path('account/',views.account),
	path('dashboard/<str:userna>/engage/',views.engage),
	path('dashboard/<str:userna>/fees/',views.fees),
	path('dashboard/<str:userna>/',views.dashboard, name = 'dashboard2'),
	path('dashboard/<str:userna>/versement/',views.versement),
	path('gestion34/',views.logAdmin),
	path('administration/<str:userna>/',views.administration),
	path('administration/<str:userna>/frai_compte_exp/',views.frai_compte_exp),
	path('administration/<str:userna>/frai_compte_exp/conf_frai_compte',views.conf_frai_compte),
	path('administration/<str:userna>/vers_list/',views.vers_list),
	path('administration/<str:userna>/vers_list/conf_versement/',views.conf_versement),
	path('administration/<str:userna>/conf_payement/',views.conf_payement),
	path('administration/<str:userna>/conf_payement/conf_payement/',views.conf_payement),
]