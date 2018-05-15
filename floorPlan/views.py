from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views import generic
from django.template import loader
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
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
