import datetime
from .models import Services
import base64
import jwt
from apigateway import settings
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
import requests
from .forms import ImageForm
from .models import User
from .serializer import *
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
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
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        services = Services.objects.all()
        print(services)
        serializer = ServicesSerializer(services, many=True).data
        return Response(serializer)


class ServicesStatus(APIView):
    permission_classes = (IsAuthenticated,)
    base_url = 'http://172.20.10.4:8001'
    def post(self, request, id, status):
        if status == 'process':
            file = request.FILES['image']
            b64 = base64.b64encode(file.read())
            decode64 = base64.b64decode(b64)
            file_path = f'media/images/{file._name}'
            print(file_path)
            with open(file_path, 'wb') as fl:
                fl.write(decode64)
            files = {'image':   open(file_path, 'rb')}
            response = requests.post(url=self.base_url+'/models/predict/', files=files)
            return Response(response.json())

    def get(self, request, status):
        if status == 'status':
            uid = request.GET.get('uid', '')
            request = requests.get('/model'+'?uid='+uid)
            return Response(request.json())
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
