from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views import generic
from django.template import loader
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Room, Table, Chair, Window


def sandbox(request):
    all_rooms = Room.objects.all()
    template = loader.get_template('floorPlan/table.html')
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
