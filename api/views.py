import cloudModules.cloudAuth as cloudAuth
import cloudModules.cloudCompute as cloudCompute
import cloudModules.cloudImages as cloudImages
import apiModules.update as update
import apiModules.registerUser as register
import configuration.globalVars as globalVars
import api.models as modelFunctions
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Image
from .serializers import ImageSerializer, UserSerializer

class Catalog(APIView):
    def get(self, request):
        images = Image.objects.all()
        serializer = ImageSerializer(images, many=True)
        return Response(serializer.data)

    def post(self):
        pass

class UpdateCatalog(APIView):
    def get(self, request):
        globalVars.init()
        my_token_id = cloudAuth.auth()
        update.updateCatalog(my_token_id)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def post(self):
        pass

class Register(APIView):
    def get(self, request):
        pass

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            globalVars.init()
            my_token_id = cloudAuth.auth()
            register.createNewUserInstances(serializer.data['username'], my_token_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LabList(APIView):
    def get(self, request):
        pass

    def post(self, request):
        labs = modelFunctions.get_labs(request.data['userid'])
        return Response(labs)





