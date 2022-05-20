from django.shortcuts import render
from usermodule.models import User
from usermodule.serializers import UserSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

# Create your views here.

# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer


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
        hash = request.data['hash']
        user = User.objects.create(address=address, hash=hash)
        return Response(UserSerializer(user).data)

    @action(methods=['PUT'],detail = False)
    def update_user(self, request):
        address = request.data['address']
        hash = request.data['hash']
        user = User.objects.get(address=address)
        user_serailizer = UserSerializer(user, data=request.data)
        if user_serailizer.is_valid():
            user_serailizer.save()
            return Response(user_serailizer.data)
        else:
            return Response(user_serailizer.errors)

    @action(methods=['DELETE'], detail=False)
    def delete_user(self, request):
        address = request.data['address']
        user = User.objects.get(address=address).delete()
        return Response(UserSerializer(user).data)

    @action(methods=['file'],detail = False)
    def import_csv(self, request):
        file = request.data['file']
        with open(file, 'r') as f:
            for line in f:
                address, hash = line.split(',')
                if not User.objects.get(address=address).exists():
                    user = User.objects.create(address=address, hash=hash)
        return Response(UserSerializer(user).data)
