from django.contrib.auth.models import User
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from . import serializers
from .models import Breed, Kitten, Rate


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = serializers.MyTokenObtainPairSerializer


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    user = request.user
    serializer = serializers.ProfileSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@extend_schema(description='Регистрация пользователя')
class UserCreateAPIView(APIView):
    permission_classes = [AllowAny]
    serializer = serializers.ProfileSerializer


@extend_schema(description='Профиль пользователя')
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_profile(request, pk):
    user = User.objects.get(pk=pk)
    serializer = serializers.ProfileSerializer(user, many=False)
    return Response(serializer.data)


@extend_schema(description='Список всех котят. Возможна фильтрация по породе')
@api_view(['GET'])
def get_kittens_list(request):
    breed = request.GET.get('breed', None)
    if breed is not None:
        queryset = Kitten.objects.filter(breed=breed)
    else:
        queryset = Kitten.objects.all()
    serializer = serializers.KittenSerializer(queryset, many=True)
    return Response(serializer.data)


@extend_schema(description='Описание котенка по id')
@api_view(['GET'])
def get_kitten_by_id(request, pk):
    queryset = Kitten.objects.get(pk=pk)
    serializer = serializers.KittenSerializer(queryset, many=False)
    return Response(serializer.data)


@extend_schema(description='Список пород котят')
@api_view(['GET'])
def get_breeds_list(request):
    queryset = Breed.objects.all()
    serializer = serializers.BreedSerializer(queryset, many=True)
    return Response(serializer.data)


@extend_schema(description='Добавление котенка')
@api_view(['POST'])
def create_kitten(request):
    data = request.data
    owner = User.objects.get(id=data['owner'])
    serializer = serializers.KittenSerializer(data=data)
    if serializer.is_valid():
        serializer.save(owner=owner)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@extend_schema(description='Изменение информации о котенке')
@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_kitten(request, pk):
    try:
        kitten = Kitten.objects.get(pk=pk)
    except Kitten.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = serializers.KittenSerializer(kitten, data=request.data)
    elif request.method == 'PATCH':
        serializer = serializers.KittenSerializer(kitten, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(description='Удаление котенка')
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_kitten(request, pk):
    kitten = Kitten.objects.get(pk=pk)
    kitten.delete()
    return Response('Kitten was deleted', status=status.HTTP_204_NO_CONTENT)


@extend_schema(description='Получение оценок котенка')
@api_view(['GET'])
def get_rate(request, pk):
    rates = Rate.objects.filter(rated_kitten=pk)
    serializer = serializers.RateSerializer(rates, many=True)
    return Response(serializer.data)


@extend_schema(description='Оценить котенка')
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def rate_kitten(request):
    data = request.data
    kitten = Kitten.objects.get(pk=data['rated_kitten'])
    serializer = serializers.RateSerializer(data=data)
    if serializer.is_valid():
        serializer.save(rated_kitten=kitten)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(description='Удалить оценку')
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_rate(request, pk):
    rate = Rate.objects.get(pk=pk)
    rate.delete()
    return Response('Rate was deleted!', status=status.HTTP_204_NO_CONTENT)
