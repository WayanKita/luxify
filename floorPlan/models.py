from django.db import models


class Room(models.Model):
    room_code = models.CharField(max_length=10)
    x_length = models.CharField(max_length=5)
    y_length = models.CharField(max_length=5)

    def __str__(self):
        return self.room_code


class Table(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    number = models.CharField(max_length=5)
    x_pos = models.CharField(max_length=5)
    y_pos = models.CharField(max_length=5)
    x_size = models.CharField(max_length=5)
    y_size = models.CharField(max_length=5)

    def __str__(self):
        return self.number

    def load_rooms(request):
        return render(request, 'hr/city_dropdown_list_options.html', {'cities': cities})


class Chair(models.Model):
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    table_number = models.CharField(max_length=2)
    position = models.CharField(max_length=3)
    occupied = models.BooleanField(default=False)


class Window(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    start_pos = models.CharField(max_length=3)
    end_pos = models.CharField(max_length=3)
