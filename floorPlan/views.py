from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login
from django.views.generic import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .form import UserForm
from .models import Room, Table, Chair, Window
from .serializer import RoomSerializer



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


class UserFormView(View):
    form_class = UserForm
    template_name = 'floorPlan/registration_form.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            user = authenticate(username=email, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('floorPlan:sandbox')

        return render(request, self.template_name, {'form': form})