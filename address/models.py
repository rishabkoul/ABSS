from django.db import models

# Create your models here.
# class State(models.Model):
#     code=models.IntegerField(unique=True,null=False,blank=False)
#     state=models.CharField(unique=True,max_length=100,null=False,blank=False)

#     def __str__(self):
#         return self.state

class Address(models.Model):
    state=models.CharField(null=False,max_length=100,blank=False)
    district=models.CharField(null=False,max_length=100,blank=False)
    subdistrict=models.CharField(null=False,max_length=100,blank=False)
    officename=models.CharField(null=False,max_length=100,blank=False)
    villagename=models.CharField(null=False,max_length=100,blank=False)
    pincode=models.BigIntegerField(null=False,blank=False)
