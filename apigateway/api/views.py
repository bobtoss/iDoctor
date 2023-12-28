import datetime

from django.http import HttpResponseBadRequest

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
from rest_framework import mixins
from rest_framework import viewsets
import logging


# Create your views here.
class RegisterViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    serializer_class = UserSerializer

    @staticmethod
    def generate_token(user: User):
        try:
            refresh = RefreshToken.for_user(user)
            temp = dict()
            temp.update(refresh=str(refresh))
            temp.update(access=str(refresh.access_token))
        except Exception as err:
            # logging.exception(err)
            return None, 'error'

        return temp, 'success'

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except serializers.ValidationError:
            # logging.exception("Not valid request data")
            return HttpResponseBadRequest("Not valid request data")
        serializer.save()

        temp, _ = self.generate_token(serializer.Meta.model)
        serializer.data.update(temp)

        return Response(serializer.data)


class Service(viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = ServicesSerializer

    def get(self, request):
        services = Services.objects.all()
        # logging.log(services)
        serializer = ServicesSerializer(services, many=True).data
        return Response(serializer)


class ServicesProcess(viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated,)
    base_url = 'http://localhost:8001' # port of the service_1(seedDNA)

    @staticmethod
    def convert2base64(file, file_path) -> str:
        try:
            b64 = base64.b64encode(file.read())
            decode64 = base64.b64decode(b64)
        except Exception as err:
            # logging.exception(err)
            return 'error'

        try:
            f = open(file_path, 'wb')
            f.write(decode64)
        except Exception as err:
            # logging.exception(err)
            return 'error'

        return 'success'

    def post(self, request, id):
        if id == 1:
            file = request.FILES['image']
            file_path = f'media/images/{file._name}'
            self.convert2base64(file, file_path)
            # logging.info(file_path)
            files = {'image': open(file_path, 'rb')}
            response = requests.post(url=self.base_url + '/models/predict/', files=files)
            return Response(response.json())

    def get(self, request, status):
        if status == 'status':
            uid = request.GET.get('uid', '')
            request = requests.get('/model' + '?uid=' + uid)
            return Response(request.json())
        else:
            raise NotFound


class UserInfo(viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        data = UserSerializer(request.user)
        return data.validated_data
        pass

