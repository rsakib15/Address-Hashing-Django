from audioop import add
from django.shortcuts import render
import json
from usermodule.models import User
from usermodule.serializers import UserSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        pk = self.kwargs['pk']
        address = User.objects.get(address=pk)
        return UserSerializer(address).data
    
    @action(methods=['POST'],detail = False)
    def create_user(self, request):
        address = request.data['address']
        hash = json.loads(request.data['hash'])
        already_exists = User.objects.filter(address=address).exists()
        if already_exists:
            return Response({"message": "User already exists"})
        user = User.objects.create(address=address, hash=hash)
        return Response(UserSerializer(user).data)

    @action(methods=['PUT'],detail = False)
    def update_user(self, request):
        address = request.data['address']
        hash = json.loads(request.data['hash'])
        user_exists = User.objects.filter(address=address).exists()
        if user_exists:
            user = User.objects.get(address=address)
            user.hash = hash
            user.save()
            return Response(UserSerializer(user).data)
        else:
            return Response({"error": "Account does not exist"})

    @action(methods=['DELETE'], detail=False)
    def delete_user(self, request):
        address = request.data['address']

        user_exists = User.objects.filter(address=address).exists()
        if not user_exists:
            user_list = User.objects.all()
            return Response({"error": "Account does not exist"})
        else:
            User.objects.get(address=address).delete()
            user_list = User.objects.all()
            return Response({"success": "Account deleted"})

    @action(methods=['file'],detail = False)
    def import_csv(self, request):
        file = request.data['file']
        with open(file, 'r') as f:
            for line in f:
                address, hash = line.split(',')
                hash = json.loads(hash)
                if not User.objects.get(address=address).exists():
                    user = User.objects.create(address=address, hash=hash)
        return Response(UserSerializer(user).data)
