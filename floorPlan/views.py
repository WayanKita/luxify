from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login
from django.views.generic import View
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from .form import WayanForm
from .models import Room, Table, Chair, Window
from .serializer import RoomSerializer, UserSerializer, WayanSerializer, WayanLoginSerializer


def sandbox(request):
    all_rooms = Room.objects.all()
    template = loader.get_template('floorPlan/floorPlan.html')
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
    template_name = 'floorPlan/room_detail.html'


class RoomDelete(DeleteView):
    model = Room
    success_url = reverse_lazy('floorPlan:sandbox')


class RoomList(APIView):

    def get(self, request):
        rooms = Room.objects.all()
        serializer = RoomSerializer(rooms, many=True)
        return Response(serializer.data)

    def post(self):
        pass


class WayanFormView(View):
    form_class = WayanForm
    template_name = 'floorPlan/registration_form.html'

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
                    return redirect('floorPlan:sandbox')

        return render(request, self.template_name, {'form': form})


class RegisterAPI(APIView):
    form_class = WayanForm

    def get(self, request):
        user = User.objects.all()
        serializer = WayanSerializer(user, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = WayanForm(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPI(APIView):

    serializer_class = WayanLoginSerializer

    def post(self, request):
        serializer = WayanLoginSerializer(data=request.data)

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
    #                 return redirect('floorPlan:sandbox')





