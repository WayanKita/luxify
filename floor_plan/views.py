from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import View
from django.views.generic.edit import CreateView, DeleteView
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from floor_plan.models import MyUser
from floor_plan.serializers import *
from .form import ParticipantForm
from .models import Room, Table, Chair, Window


def sandbox(request):
    all_rooms = Room.objects.all()
    template = loader.get_template('floor_plan/floorPlan.html')
    context = {
        'all_rooms': all_rooms,
    }
    return HttpResponse(template.render(context, request))


class RoomCreate(CreateView):
    model = Room
    fields = ['code', 'x_length', 'y_length']


class TableCreate(CreateView):
    model = Table
    fields = ['room', 'number', 'x_pos', 'y_pos', 'x_size', 'y_size']


class ChairCreate(CreateView):
    model = Chair
    fields = ['table', 'number', 'position', 'occupied']


class WindowCreate(CreateView):
    model = Window
    fields = ['room', 'start_pos', 'end_pos']


class DetailView(generic.DetailView):
    model = Room
    template_name = 'floor_plan/room_detail.html'


class RoomDelete(DeleteView):
    model = Room
    success_url = reverse_lazy('floor_plan:sandbox')


class RoomList(APIView):

    def get(self, request):
        rooms = Room.objects.all()
        serializer = RoomSerializer(rooms, many=True)
        return Response(serializer.data)

    def post(self):
        pass


class ParticipantFormView(View):
    form_class = ParticipantForm
    template_name = 'floor_plan/registration_form.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user.save()

            user = authenticate(username=email, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('floor_plan:sandbox')

        return render(request, self.template_name, {'form': form})


class RegisterAPI(APIView):
    form_class = ParticipantForm

    def get(self, request):
        user = User.objects.all()
        serializer = ParticipantSerializer(user, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ParticipantForm(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ShowUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ()


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password')


class MyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        exclude = ()


class UserViewSet(viewsets.ModelViewSet):
    queryset = MyUser.objects.all()
    serializer_class = MyUserSerializer

    def create(self, request, *args, **kwargs):
        serializer = CreateUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            django_user = User.objects.get(username=serializer.validated_data['email'])
        except User.DoesNotExist:
            django_user = User.objects.create_user(
                username=serializer.validated_data['email'],
                email=serializer.validated_data['email'],
                password=serializer.validated_data['password'],
            )
        mu_user = MyUser.objects.create(
            django_user=django_user
        )
        headers = self.get_success_headers(serializer.data)
        response_serializer = MyUserSerializer(instance=mu_user)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class LoginAPI(APIView):
    serializer_class = ParticipantLoginSerializer

    def post(self, request):
        serializer = ParticipantLoginSerializer(data=request.data)

        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def post(self, request, *args, **kwargs):
    #     return HttpResponse('This is POST request')

    # @api_view(['POST'])
    # def post(self, request):
    #     data = request.POST
    #     pretty_print_POST(prepared)
    #     form = UserForm(request.POST)
    #
    #     if form.is_valid():
    #         user = form.save(commit=False)
    #         email = form.cleaned_data['email']
    #         username = form.cleaned_data['username']
    #         password = form.cleaned_data['password']
    #         user.set_password(password)
    #         user.save()
    #
    #         user = authenticate(username=email, password=password)
    #         if user is not None:
    #             if user.is_active:
    #                 login(request, user)
    #                 return redirect('floor_plan:sandbox')
