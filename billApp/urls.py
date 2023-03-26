from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index,name="index"),
    path('create/',views.create,name="create"),
    path('generate/<str:origin>/',views.generate,name="generate"),
    path('bill/<str:id>/<str:mode>',views.bill,name="bill"),
    path('modify/',views.modify,name="modify"),
    path('showBills/<str:origin>/',views.showBills,name="showBills"),
    path('showCoustomers/',views.showCoustomers,name="showCoustomers"),
    path('showItems/',views.showItems,name="showBills"),
    path('editBill/<str:id>/',views.editbill,name="editbill"),
    path('delete/<str:id>/',views.dele,name="delete"),
    path('login/',views.login_,name="login"),
    path('register/',views.register,name="register"),
    path('logouti/',views.logouti,name="logouti"),
    path('changepassword/<str:email>/',views.changepassword,name="changepassword"),
    path('viewprofile/<str:user>/',views.viewProfile,name="viewProfile"),
    # path('printbill/',views.printbill,name="printbill"),


]