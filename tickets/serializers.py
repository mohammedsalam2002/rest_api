# هذا الملف يعمل كوسيط ما بين ال views and model
# يحول البيانات في models التي هي مكتوبه ب orml لى json


from rest_framework import serializers
from tickets.models import *

class Movieserializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'

class Reservationserializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'

class Guestserializer(serializers.ModelSerializer):
    class Meta:
        model = Guest
        
        #guest = models.ForeignKey(Guest,related_name='reservation',on_delete=models.CASCADE)
        ############################################## reservation #########################    
        fields = ['pk','reservation','name','mobile']
