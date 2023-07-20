from django.shortcuts import render
from django.http.response import JsonResponse
from . models import *

from rest_framework.decorators import api_view  # تسخدم لل function
from rest_framework.views import APIView        # تسخدم لل class
from . serializers import *
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404

from rest_framework import generics, mixins
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework.authentication import BasicAuthentication ,TokenAuthentication
from rest_framework.permissions import IsAuthenticated
# Create your views here.

# اول طريقه طلعنا بيه جسون فورمات 
#1 without REST and no model query
def no_rest_no_model(request):
    guests = [
        {
            'id':1,
            'name':"mohammed",
            'mobile':123456,
        }
        ,
        {
            'id':2,
            'name':"ahmed",
            'mobile':98763,
        }
    ]

    return JsonResponse(guests,safe=False)

# الطريقه هي اعمل امبورت للمودل واطلع منه ال بيانات
#2  model data defult django without rest
def no_rest_from_model(request):
    data = Guest.objects.all()
    response = {
        'guests': list(data.values('name','mobile')) # نحصل على البيانات ونخليه بل ليست وحسب الحاجه للبيانات 
    }

    return JsonResponse(response)




# توضيح لبعض المفاهيم 
# list ==  GET  # يجلب لنا البيانات ك سلسله
# Create == POST #  انشاء بيانات جديده
# UPdate == PUT # تحدث على البيانات الموجوده
# Delete == DELETE  # حذف البيانات التي لا نريدها


#3  الطريقه الثالثه
#3 function based views
#3.1 use GET and POST

@api_view(['GET','POST'])
def FBV_view(request):
    # GET 
    if request.method == 'GET':
        guests = Guest.objects.all()
        serializer = Guestserializer(guests, many=True) # ان وضع (مني يساوي صح ) لانه يتعامل مع اكثر من عنصر
        return Response(serializer.data)
    elif request.method == 'POST':
        serailizer = Guestserializer(data = request.data)
        if serailizer.is_valid():
            serailizer.save()
            # نرجع الداتا الذي تم تكوينه
            return Response(serailizer.data,status=status.HTTP_201_CREATED)
        return Response(serailizer.data,status=status.HTTP_400_BAD_REQUEST)

#3.2  من الطريقه الثالثه
@api_view(['GET','PUT','DELETE'])
def FBV_pk(request,pk):
    # استدعاء عنصر واحد لكي ستم التعديل والحذف عليه
    # try نخليه دائما من يكون عدنا عنصر واحد 
    try:
        guest = Guest.objects.get(pk=pk)
    except Guest.DoesNotExist:
        Response(status=status.HTTP_404_NOT_FOUND)
    # GET 
    if request.method == 'GET':
        serializer = Guestserializer(guest) #  لانه يتعامل مع  عنصر واحد لا يحتاج many = True
        return Response(serializer.data)
    
    # PUT من خلاله يتم التعديل على العنصر المحدد
    elif request.method == 'PUT':
        serailizer = Guestserializer(guest,data = request.data)
        if serailizer.is_valid():
            serailizer.save()
            return Response(serailizer.data)
        return Response(serailizer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        guest.delete()
        Response(status=status.HTTP_204_NO_CONTENT)
    


# هذه الطريقه نستخدم الكلاسات
# CBV Class based views
#4.1 List and create == GET and POST
class CBV_List(APIView):
    def get(self,request):
        guests = Guest.objects.all()
        serializer = Guestserializer(guests,many = True)
        return Response(serializer.data)
    
    def post(self,request):
        serializer = Guestserializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.data,status=status.HTTP_400_BAD_REQUEST)

# هذه الطريقه نستخدم الكلاسات
# CBV Class based views
#4.2 List and Update and Delete == GET and PUT and DELETE
class CBV_Pk(APIView):

    def get_object(self,pk):
        try:
            guest = Guest.objects.get(pk=pk)
            return guest
        except Guest.DoesNotExist:
            raise Http404
        
    def get(self,request,pk):
        guest = self.get_object(pk)
        serializer = Guestserializer(guest)
        return Response(serializer.data)
    
    def put(self,request,pk):
        guest = self.get_object(pk)
        serializer = Guestserializer(guest,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.data,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk):
        guest = self.get_object(pk)
        guest.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



# هذه الطريقه نستخدم الكلاسات
#5.1 List and create == GET and POST  
# with class mixins
class Mixins_List(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    
    queryset = Guest.objects.all()
    serializer_class = Guestserializer

    def get(self,request):
        return self.list(request)
    def post(self,request):
        return self.create(request)
    
# هذه الطريقه نستخدم الكلاسات
#5.2 List and Update and Delete == GET and PUT and DELETE
# with mixins
class Mixins_Pk(mixins.RetrieveModelMixin,
                mixins.DestroyModelMixin,
                mixins.UpdateModelMixin,
                generics.GenericAPIView
                ):
    queryset = Guest.objects.all()
    serializer_class = Guestserializer
    # لارجاع قيمه واحده فقط
    
    def get(self,request,pk):
        return self.retrieve(request)
    def put(self,request,pk):
        return self.update(request)
    def delete(self,request):
        return self.destroy(request)



# هذه الطريقه نستخدم الكلاسات
#6.1 List and create == GET and POST  
# with class generics
# تأمين الكلاس
class Generic_List(generics.ListCreateAPIView):
    queryset =Guest.objects.all()
    serializer_class = Guestserializer
    # يهذا السطرين نحن نؤمن هذا الكلاس 
    #authentication_classes = [BasicAuthentication]
    authentication_classes = [TokenAuthentication]
    #permission_classes = [IsAuthenticated]


# هذه الطريقه نستخدم الكلاسات
#6.2 List and Update and Delete == GET and PUT and DELETE
# with generics
# تأمين الكلاس
class Generic_pk(generics.RetrieveUpdateDestroyAPIView):
    queryset =Guest.objects.all()
    serializer_class = Guestserializer
    # يهذا السطرين نحن نؤمن هذا الكلاس 
    #authentication_classes = [BasicAuthentication]
    authentication_classes = [TokenAuthentication]
    #permission_classes = [IsAuthenticated]


#7
# use viewset
# هذه الطريقه هي شامله لكل العمليات
class Viewset_Guest(viewsets.ModelViewSet):
    queryset = Guest.objects.all()
    serializer_class = Guestserializer

# يحتوي على عمليه البحث
class Viewset_Movie(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = Movieserializer
    filter_backends = [SearchFilter]
    search_fields = ['movie']

class Viewset_Reservation(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = Reservationserializer




# 8 Find movie
@api_view(['GET'])
def find_movie(request):
    movies = Movie.objects.filter(
        movie = request.data['movie'],
        )
    
    serializer = Movieserializer(movies,many=True)
    return Response(serializer.data)

# 9
# create a new reservation 
@api_view(['POST'])
def create_reservation(request):
    movie = Movie.objects.get(
        hall = request.data['hall'],
        movie = request.data['movie'],
    )
    
    guest = Guest()
    guest.name = request.data['name']
    guest.mobile = request.data['mobile']
    guest.save()

    reservation = Reservation()
    reservation.guest = guest
    reservation.movie = movie
    reservation.save()

    return Response(reservation.data,status=status.HTTP_201_CREATED)




