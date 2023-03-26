from django.db import models

# Create your models here.


class Product(models.Model):
    pname=models.CharField(max_length=100)
    pcode=models.CharField(max_length=100,unique=True)
    pprice=models.CharField(max_length=100)
    pimg = models.FileField(upload_to="itemImage/",default="" ,max_length=200)

    def __str__(self):
        return f"{self.pname} with code {self.pcode}"
    
class CoustomersData(models.Model):
    c_id=models.AutoField(primary_key=True,unique=True,blank=False)
    c_name = models.CharField(max_length=50)
    c_number = models.CharField(max_length=50)
    c_address = models.CharField(max_length=100)
    c_city = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.c_name}"
    
class Bill(models.Model):
    bill_id=models.AutoField(primary_key=True,unique=True)
    purchaser=models.CharField(max_length=100)
    purchaser_num=models.CharField(max_length=15,default="")
    purchaser_address=models.CharField(max_length=200,default="")
    purchaser_city=models.CharField(max_length=50,default="")
    total_amount=models.CharField(max_length=30)
    disscount=models.CharField(max_length=15,default="0")
    final_amount=models.CharField(max_length=15,default="0")
    bill_time=models.DateTimeField()
    bill_data = models.TextField(max_length=10000,default=" ")
    purchaser_id = models.ForeignKey(CoustomersData,on_delete=models.CASCADE,null=True)

    def __str__(self):
        return f"{self.bill_id}"
    


