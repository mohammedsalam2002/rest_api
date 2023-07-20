from django.db import models

from django.db.models.signals import post_save
from django.dispatch import receiver # هنا سوف يتم تنفيذ البيانات 
from rest_framework.authtoken.models import Token
from django.conf import settings



# Guest ---- Movie --- Reservation

class Movie(models.Model):
    hall = models.CharField(max_length=10)
    movie = models.CharField(max_length=10)

    def __str__(self):
        return self.movie


class Guest(models.Model):
    name = models.CharField(max_length=10)
    mobile = models.CharField(max_length=10)

    def __str__(self):
        return self.name

class Reservation(models.Model):
    # الحجز الذي يربط الزبون بلفلم
    # related_name يربط الفيلد بلفورنكي الخاص به
    guest = models.ForeignKey(Guest,related_name='reservation',on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie,related_name='reservation',on_delete=models.CASCADE)




#	الإشارةpost_saveفي هذه الحالة تحدد الإشارة التي ستتعامل معها الوظيفة.
#	الوسيطة sender: تحدد فئة النموذج التي سترسل الإشارة. في هذه الحالة ، يتم تعيينه على 
#    settings.AUTH_USER_MODEL، والذي يمثل نموذج المستخدم المخصص.
@receiver(post_save,sender=settings.AUTH_USER_MODEL)
def TokenCreate(sender,instance,created,**kwargs):
    if created:
        Token.objects.create(user= instance )
#sender: تمثل هذه المعلمة فئة النموذج التي ترسل الإشارة. في هذه الحالة ، ستكون فئة مثيل النموذج هي التي أطلقت الإشارة.
#instance: تمثل هذه المعلمة المثيل الفعلي للنموذج الذي أطلق الإشارة. سيكون مثيلًا للنموذج المحدد في معلمة المرسل.
#created: هذه المعلمة عبارة عن علامة منطقية تشير إلى ما إذا كان قد تم إنشاء مثيل النموذج (صواب) أو تم تحديثه (خطأ) أثناء عملية الحفظ التي أطلقت الإشارة.
#** kwargs: تسمح هذه المعلمة لمعالج الإشارة بقبول أي وسيطات إضافية للكلمات الرئيسية قد يتم إرسالها مع الإشارة. إنها ميزة شاملة لأي بيانات إضافية



