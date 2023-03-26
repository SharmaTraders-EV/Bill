from django.shortcuts import render,redirect,HttpResponse
from .models import Product,Bill,CoustomersData
from datetime import date,datetime
from django.contrib import messages
import json
from num2words import num2words
from django.conf import settings
import os
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.core.mail import send_mail
import random
# Create your views here.

def index(request):
    if not request.user.is_authenticated:
        return redirect("/login/")
    if request.user.is_superuser:
        logout(request)
        return redirect("/login/")


    return render(request,"index.html")


def create(request):
    if not request.user.is_authenticated:
        return redirect("/login/")
    if request.method=="POST":
        pname=request.POST.get("pname")
        pcode=request.POST.get("pcode")
        pprice=request.POST.get("pprice")
        try:
            pimg = request.FILES["pimg"]
        except:
            pimg=""
        if len(Product.objects.filter(pcode=pcode))>0:
            messages.error(request,"Code already exists")
            return redirect("/create/")
        else:
            product=Product(pname=pname,pcode=pcode,pprice=pprice,pimg=pimg)
            product.save()
        
    return render(request,'create.html')


def generate(request,origin):
    if not request.user.is_authenticated:
        return redirect("/login/")
    if request.method=="POST":
        fdata = request.POST.get("fdata")
        count = request.POST.get("counterG")
        purchaser = request.POST.get("purchaser")
        purchaser_num = request.POST.get("purchaser_num")
        purchaser_address = request.POST.get("purchaser_address")
        purchaser_city = request.POST.get("purchaser_city")
        disscount = request.POST.get("disscount")
        received = request.POST.get("received")
        print(received)
        data = json.loads(fdata)
        prod=[]
        total_amount=0
        finall_total = 0
        total_quantity = 0
        prod_code_lists = []
        for i in range(1,int(count)):
            j=i
            code = data[f"productCode{i}"]
            quantity = data[f"productQuantity{i}"]
            product=Product.objects.filter(pcode=code)[0]
            amount=float(product.pprice)*float(quantity)
            if product.pcode in prod_code_lists:
                k = prod_code_lists.index(product.pcode)
                prod[k][3] = int(prod[k][3])+int(quantity)
                prod[k][4]+=amount
                total_amount+=amount
                total_quantity+=int(quantity)
                j-=1
                continue
            prod.append([j,product.pname,product.pprice,quantity,amount,product.pcode])
            prod_code_lists.append(product.pcode)
            total_amount+=amount
            total_quantity+=int(quantity)
            now = datetime.now()
        finall_total = total_amount-(((total_amount)//100)*float(disscount))
        if len(received)>0:
            finall_total-=float(received)
        else:
            received="0"
        bill_of_products = {"products":prod,"total_quantity":total_quantity,"received":received}
        bill_of_products = json.dumps(bill_of_products,default=str)
    
        coust = CoustomersData.objects.filter(c_name=purchaser,c_number=purchaser_num)
        if len(coust)<1:
            coust = CoustomersData(c_name=purchaser,c_number=purchaser_num,c_address=purchaser_address,c_city=purchaser_city)
            coust.save()
            coust = [coust]
        
        bill=Bill(purchaser=purchaser,total_amount=total_amount,bill_time=now,bill_data=bill_of_products,purchaser_num=purchaser_num,disscount=disscount,final_amount=finall_total,purchaser_address=purchaser_address,purchaser_city=purchaser_city,purchaser_id=coust[0])
        bill.save()

        return redirect(f"/bill/{bill.bill_id}/show")
        # return render(request,"bill.html",bill_of_products)
    all_products = Product.objects.all()
    all_codes = [int(i.pcode) for i in all_products]
    c_data = []
    if origin[:3]=="old":
        c_data = CoustomersData.objects.filter(c_id=origin[4:])[0]
        origin = origin[:3]
    return render(request,'generate.html',{"all_codes":all_codes,"prod":all_products,"origin":origin,"c_data":c_data})

def bill(request,id,mode):
    if not request.user.is_authenticated:
        return redirect("/login/")
    bill_info = Bill.objects.get(bill_id=id)
    bill_data = json.loads(bill_info.bill_data)
    totalEntry= len(bill_data["products"])
    received_amount = bill_data["received"]
    total_amount_recevied = eval(received_amount)
    final_amount = float(bill_info.final_amount)
    bill_amount = bill_info.total_amount
    bill_disscount = bill_info.disscount
    disscount_value = (((float(bill_amount))//100)*float(bill_disscount))
    if mode=="change":
        final_amount=float(bill_amount)-float(total_amount_recevied)-disscount_value
        bill_info.final_amount = final_amount
        bill_info.save()
        return redirect(f"/bill/{id}/show")
    bill_id = bill_info.bill_id
    bill_time = bill_info.bill_time
    bill_purchaser = bill_info.purchaser
    bill_purchaser_num = bill_info.purchaser_num
    bill_purchaser_city = bill_info.purchaser_city
    bill_purchaser_address = bill_info.purchaser_address
    
    final_amount_words = num2words(round(final_amount,2))

    received_list_X = received_amount.split("+")
    received_list = [round(float(i),2) for i in received_list_X]
    if received_list[0]==0:
        received_list=received_list[1:]

    bill_of_products = {"products":bill_data["products"],"total_amount":bill_amount,"time":bill_time,"id":id,"purchaser":bill_purchaser,"phone":bill_purchaser_num,"disscount":bill_disscount,"final_amount":round(final_amount,2),"disValue":round(disscount_value,2),"city":bill_purchaser_city,"address":bill_purchaser_address,"amount_word":final_amount_words,"total_qun":bill_data["total_quantity"],"bill_id":bill_id,"totalEntry":totalEntry,"received":(round(total_amount_recevied,2)),"received_list":received_list}
    return render(request,"bill2.html",bill_of_products)

def modify(request):
    if not request.user.is_authenticated:
        return redirect("/login/")
    if request.method=="GET":
        dic = request.GET
        if "productcode" in dic:
            data = Product.objects.filter(pcode=dic["productcode"])
            if len(data)>0:
                d = {"prod":data[0]}
                return render(request,"modify.html",d)
            else:
                messages.error(request,"code you enter not exist!")
    elif request.method=="POST":
        name = request.POST.get("pname")
        code = request.POST.get("pcode")
        price = request.POST.get("pprice")
        dic = request.GET
        # print(dic["productcode"],name,code,price)
        data = Product.objects.filter(pcode=dic["productcode"])[0]
        data.pname = name
        data.pcode = code
        data.pprice = price
        data.save()
        messages.success(request,"updated")
            

    return render(request,"modify.html")

def showBills(request,origin):
    
    if not request.user.is_authenticated:
        return redirect("/login/")
    obj = Bill.objects.all()[::-1]
    if origin[:4]=="spec":
        c = CoustomersData.objects.filter(c_id=origin[5:])[0]
        obj = Bill.objects.filter(purchaser_id=c)
    try:
        search=request.GET['search']
        obj = searchfunc(request.path,search)
    except:
        pass
    data = {"bills":obj}
    return render(request,"allBill.html",data)
    
def showItems(request):
    if not request.user.is_authenticated:
        return redirect("/login/")
    obj = Product.objects.all()[::-1]
    try:
        search=request.GET['search']
        obj = searchfunc(request.path,search)
    except:
        pass
    data = {"prod":obj}

    return render(request,"allItems.html",data)

def editbill(request,id):
    if not request.user.is_authenticated:
        return redirect("/login/")
    bill_info = Bill.objects.get(bill_id=id)
    bill_data = json.loads(bill_info.bill_data)
    data = {"bill":bill_info,"allReadyReceived":bill_data["received"]}
    if request.method=="POST":
        recived = request.POST.get("recived")
        bill_data["received"]+="+"
        bill_data["received"]+=recived
        bill_data = json.dumps(bill_data)
        bill_info.bill_data = bill_data
        bill_info.save()
        return redirect(f"/bill/{id}/change")

    return render(request,"editBill.html",data)

def dele(request,id):
    if not request.user.is_authenticated:
        return redirect("/login/")
    if id=="all":
        Bill.objects.all().delete()
        return redirect("/showBills/orignal/")

    Bill.objects.get(bill_id=id).delete()
    return redirect("/showBills/orignal/")

def login_(request):
    if request.method=="POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(username=email,password=password)
        if user is not None:
            login(request,user)
            return redirect("/")
        else:
            return HttpResponse("Wrong")
    
    return render(request,"login.html")


key_for_registration = "0.0.0.0@billApp.com"
def register(request):
    if request.method=="POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        cpassword = request.POST.get("cpassword")
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        key = request.POST.get("key")

        if key==key_for_registration:
            if password==cpassword:
                obj = User.objects.filter(username=email)
                if len(obj):
                    messages.error(request,"email already exist try to login or change email")
                else:
                    obj = User(username=email,email=email,first_name=fname,last_name=lname)
                    obj.set_password(password)
                    obj.save()
                    messages.success(request,"Register Successfull now please login")
                    return redirect("/login/")
            else:
                messages.error(request,"Password miss match try again")
        else:
            messages.error(request,"Wrong key")
    return render(request,"register.html")

def logouti(request):
    logout(request)
    return redirect("/")

def viewProfile(request,user):
    if not request.user.is_authenticated:
        return redirect("/login/")
    return render(request,"viewProfile.html")

def showCoustomers(request):
    if not request.user.is_authenticated:
        return redirect("/login/")
    data = CoustomersData.objects.all()
    try:
        search=request.GET['search']
        data = searchfunc(request.path,search)
    except:
        pass
    params = {"coustomer":data}
    return render(request,"coustomers.html",params)



def searchfunc(path,search):
    if "showBills" in path:
        obj = Bill.objects.filter(purchaser__icontains=search)
        return obj
    elif "showItems" in path:
        obj = Product.objects.filter(pname__icontains=search)
        if len(obj)==0:
            obj = Product.objects.filter(pcode__icontains=search)

        return obj
    elif "showCoustomers" in path:
        obj = CoustomersData.objects.filter(c_name__icontains=search)
        return obj

    # obj3 = Books.objects.filter(bookname__icontains=search)

def changepassword(request,email):
    verify = False
    if request.method=="GET":
        dic = request.GET
        if "otp_recived" in dic:
            print(r)
            print(dic["otp_recived"])
            if str(r)==str(dic["otp_recived"]):
                verify = True
                # return render(request,"changepass.html",{"verify":verify})
            else:
                messages.error(request,"Verification fail try again")
                return redirect("/")
    r = sendmail("changepass",email)
    return render(request,"changepass.html",{"verify":verify})

def sendmail(forwhat,x):
    if forwhat=="changepass":
        otp = random.randint(100000,999999)
        subject = "Change password otp verification"
        msg = f"your 6 digit otp is {otp}"
        to = x
        r = otp

    send_mail(
        subject,
        msg,
        'sharma.traders.ev@gmail.com',
        [to],
        fail_silently=False
    )

    return r
