import datetime
from .models import Services
import jwt
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
import requests
from .forms import ImageForm
from .models import User
from .serializer import *
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import NotFound


# Create your views here.
class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        refresh = RefreshToken.for_user(serializer.Meta.model)
        temp = serializer.data
        temp['refresh'] = str(refresh)
        temp['access'] = str(refresh.access_token)
        print(temp)
        # serializer.data.__setattr__('access',)
        # print(serializer.data)
        return Response(temp)


class Service(APIView):
    def get(self, request):
        services = Services.objects.all()
        print(services)
        serializer = ServicesSerializer(services, many=True).data
        return Response(serializer)


class ServicesStatus(APIView):
    def post(self, request, status):
        if status == 'process':
            form = ImageForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                url = Services.objects.get(id=1)
                print(form.data)
                res = requests.request('post', url, data=form.data)
                # Get the current instance object to display in the template
                img_obj = form.instance
                return render(request, 'index.html', {'form': form, 'img_obj': img_obj})
        else:
            raise NotFound

    def get(self, request, status):
        if status == 'status':
            pass
        else:
            raise NotFound

# def image_upload_view(request):
#     """Process images uploaded by users"""
#     if request.method == 'POST':
#         form = ImageForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             url = 'http://localhost:4255/process'
#             res = requests.request('post', url, data=form.data)
#             # Get the current instance object to display in the template
#             img_obj = form.instance
#             return render(request, 'index.html', {'form': form, 'img_obj': img_obj})
#     else:
#         form = ImageForm()
#         return render(request, 'index.html', {'form': form})
