from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import pre_save
from address.models import Address
from django.db.models import Q
from django.core.mail import send_mail
from django.core.mail import EmailMessage
import requests

import threading


class SMSThread(threading.Thread):

    def __init__(self, requests, url, headers, params):
        self.requests = requests
        self.url = url
        self.headers = headers
        self.params = params
        threading.Thread.__init__(self)

    def run(self):
        self.requests.request(
            "POST", self.url, headers=self.headers, params=self.params)

# Create your models here.


class RegistrationForm(models.Model):
    class MemberType(models.TextChoices):
        LIFE_MEMBER = 'Life Member'
        ACTIVE_MEMBER = 'Active Member'
        GENERAL_MEMBER = 'General Member'

    class MemberCategory(models.TextChoices):
        ORDINARY = 'Ordinary'
        TEMPLE_MANAGER = 'Temple Manager'
        PROHITS = 'Prohits'

    class Area(models.TextChoices):
        URBAN = 'Urban'
        RURAL = 'Rural'

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    membertype = models.CharField(
        max_length=50, choices=MemberType.choices, default=MemberType.GENERAL_MEMBER)
    membercategory = models.CharField(
        max_length=50, choices=MemberCategory.choices, default=MemberCategory.ORDINARY)
    area = models.CharField(
        max_length=50, choices=Area.choices, default=Area.RURAL)
    state = models.CharField(null=False, max_length=100, blank=False)
    district = models.CharField(null=False, max_length=100, blank=False)
    subdistrict = models.CharField(null=False, max_length=100, blank=False)
    postoffice = models.CharField(null=False, max_length=100, blank=False)
    village = models.CharField(null=False, max_length=100, blank=False)
    templename = models.CharField(null=True, max_length=100, blank=True)
    code = models.CharField(max_length=20, default='notgiven')
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.user.email


@receiver(pre_save, sender=RegistrationForm, dispatch_uid='approved')
def approved(sender, instance, **kwargs):
    if instance.is_approved and RegistrationForm.objects.filter(pk=instance.pk, is_approved=False).exists():

        if(instance.membertype == 'Life Member'):
            membertype = 'L'
        elif(instance.membertype == 'Active Member'):
            membertype = 'A'
        else:
            membertype = 'G'

        if(instance.membercategory == 'Ordinary'):
            membercategory = 'O'
        elif(instance.membercategory == 'Temple Manager'):
            membercategory = 'T'
        else:
            membercategory = 'P'

        if(instance.state == 'ODISHA'):
            state = '19'
        elif(instance.state == 'DELHI'):
            state = '34'

        district = list(Address.objects.filter(state=instance.state).order_by(
            'district').values_list('district', flat=True).distinct()).index(instance.district)+1
        if district < 10:
            district = str(district)
            district = '0'+district
        else:
            district = str(district)

        subdistrict = list(Address.objects.filter(state=instance.state).filter(district=instance.district).order_by(
            'subdistrict').values_list('subdistrict', flat=True).distinct()).index(instance.subdistrict)+1
        if subdistrict < 10:
            subdistrict = str(subdistrict)
            subdistrict = '0'+subdistrict
        else:
            subdistrict = str(subdistrict)

        postoffice = list(Address.objects.filter(state=instance.state).filter(district=instance.district).filter(
            subdistrict=instance.subdistrict).order_by('officename').values_list('officename', flat=True).distinct()).index(instance.postoffice)+1
        if postoffice < 10:
            postoffice = str(postoffice)
            postoffice = '0'+postoffice
        else:
            postoffice = str(postoffice)

        village = list(Address.objects.filter(state=instance.state).filter(district=instance.district).filter(subdistrict=instance.subdistrict).filter(
            officename=instance.postoffice).order_by('villagename').values_list('villagename', flat=True).distinct()).index(instance.village)+1
        if village < 100 and village >= 10:
            village = str(village)
            village = '0'+village
        elif village < 10:
            village = str(village)
            village = '00'+village
        else:
            village = str(village)

        samevillagepeople = RegistrationForm.objects.filter(state=instance.state).filter(district=instance.district).filter(
            subdistrict=instance.subdistrict).filter(postoffice=instance.postoffice).filter(village=instance.village).filter(~Q(code='notgiven')).order_by('code')
        indexn = 0
        index = 0
        for villager in samevillagepeople:
            indexn = indexn+1
            index = indexn
            if index < 100 and index >= 10:
                index = str(index)
                index = '0'+index
            elif index < 10:
                index = str(index)
                index = '00'+index
            else:
                index = str(index)
            if index != villager.code[-3:]:
                personno = index
                instance.code = membertype+membercategory+state + \
                    district+subdistrict+postoffice+village+personno

                mesagge = 'Your ABSS subscrtion is now accepted. Check out in the app'
                # sendemail = EmailMessage(
                #     subject,
                #     mesagge,
                #     from_email,
                #     [instance.user.email],
                # )
                # EmailThread(sendemail).start()
                querystring = {"from": "+13093160712", "body": mesagge,
                               "to": "+91"+str(instance.user.phone)}
                # requests.request(
                #     "POST", url, headers=headers, params=querystring)
                SMSThread(requests, settings.SMS_URL,
                          settings.SMS_HEADERS, querystring).start()
                return
        num_index = int(index)
        if(len(samevillagepeople) == num_index):
            personno = num_index+1
            print(personno)
            if personno < 100 and personno >= 10:
                personno = str(personno)
                personno = '0'+personno
            elif personno < 10:
                personno = str(personno)
                personno = '00'+personno
            else:
                personno = str(personno)
        instance.code = membertype+membercategory+state + \
            district+subdistrict+postoffice+village+personno

        mesagge = 'Your ABSS subscrtion is now accepted. Check out in the app'
        # sendemail = EmailMessage(
        #     subject,
        #     mesagge,
        #     from_email,
        #     [instance.user.email],
        # )
        # EmailThread(sendemail).start()
        querystring = {"from": "+13093160712", "body": mesagge,
                       "to": "+91"+str(instance.user.phone)}
        SMSThread(requests, settings.SMS_URL,
                  settings.SMS_HEADERS, querystring).start()
