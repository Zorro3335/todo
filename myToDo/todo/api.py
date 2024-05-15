from .models import ToDo
from .serializers import *
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import APIView, api_view
from django.forms.models import model_to_dict
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password


class ToDoAPIViewList(APIView):
    def get(self, request):
        # Получаем набор всех записей из таблицы ToDo
        queryset = ToDo.objects.all() if request.query_params.get('id', None) is None else (
            ToDo.objects.filter(user_id=request.query_params.get('id')))

        # Сериализуем извлечённый набор записей
        serializer_for_queryset = ToDoSerializer(
            instance=queryset,  # Передаём набор записей
            many=True  # Указываем, что на вход подаётся именно набор записей
        )
        return Response(serializer_for_queryset.data)


class ToDoAPIViewDetailOrPut(APIView):
    def get(self, request, pk):
        # Получаем набор всех записей из таблицы ToDo
        queryset = ToDo.objects.get(pk=pk)
        serializer_for_queryset = ToDoSerializer(queryset, many=False)
        return Response(serializer_for_queryset.data)

    def put(self, request, pk):
        data = request.data
        try:
            instance = ToDo.objects.get(pk=pk)
        except ToDo.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ToDoSerializer(instance, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def patch(self, request, pk):
        todo = ToDo.objects.get(pk=pk)
        serializer = ToDoSerializer(todo, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(status=201, data=serializer.data)
        return Response(status=400, data="wrong parameters")

    def delete(self, request, pk):
        data = request.data
        try:
            instance = ToDo.objects.get(pk=pk)
        except ToDo.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        instance.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class ToDoAPIViewCreate(APIView):
    def post(self, request):
        data = request.data
        print(data)
        # Выполнение необходимых действий с данными
        # Например, создание нового объекта на основе полученных данных

        new_todo = ToDo.objects.create(
            title=data['title'],
            description=data['description'],
            create_date=data['create_date'],
            important=data['important'],
            deadline=data['deadline'],
            user_id=data['user_id']
        )

        return Response(model_to_dict(new_todo), status=status.HTTP_201_CREATED)
        # serializer = ToDoSerializer(data=data)
        #
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(serializer.data, status=status.HTTP_201_CREATED)
        #
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserAPIViewList(APIView):
    def get(self, request):
        # Получаем набор всех записей из таблицы ToDo
        queryset = User.objects.all()
        # Сериализуем извлечённый набор записей
        serializer_for_queryset = UserSerializer(
            instance=queryset,  # Передаём набор записей
            many=True  # Указываем, что на вход подаётся именно набор записей
        )
        return Response(serializer_for_queryset.data)


class UserAPIViewDetailOrPutOrDelete(APIView):
    def get(self, request, pk):
        # Получаем набор всех записей из таблицы ToDo
        queryset = User.objects.get(pk=pk)
        serializer_for_queryset = ToDoSerializer(queryset, many=False)
        return Response(serializer_for_queryset.data)

    def put(self, request, pk):
        data = request.data
        try:
            instance = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ToDoSerializer(instance, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

    def delete(self, request, pk):
        data = request.data
        try:
            instance = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        instance.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class UserAPIViewCreate(APIView):
    def post(self, request):
        data = request.data

        # Выполнение необходимых действий с данными
        # Например, создание нового объекта на основе полученных данных
        new_user = User.objects.create(
            username=data['username'],
            password=make_password(data['password'])
        )

        return Response(model_to_dict(new_user), status=status.HTTP_201_CREATED)


class CheckPassword(APIView):
    def post(self, request):
        received_password = request.data.get('password')
        user = User.objects.get(username=request.data['username'])
        correct_password = user.password
        print({'username': user, 'password': user.password})
        serializers = UserSerializer(user, many=False)
        if check_password(received_password, correct_password):

            return Response({'user': serializers.data}, status=201)
        else:
            return Response({'status': 'Пароль неверный.'}, status=401)
