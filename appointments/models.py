from django.db import models
from clowning_around.users.models import Client, Troupe, Clown


class Appointment(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_of_appointment = models.DateTimeField(blank=False)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    troupe = models.ForeignKey(Troupe, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, blank=False)
    rating = models.CharField(max_length=128, blank=True)

    def __str__(self):
        return f'{self.pk}:{self.client} -> {self.date_of_appointment} -> {self.troupe}'


class AppointmentIssues(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    clown = models.ForeignKey(Clown, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, blank=False)
    description = models.CharField(max_length=200, blank=False)

    def __str__(self):
        return f'{self.appointment} -> {self.clown} -> {self.title}'


class ClownsViewClientDetails(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    clown = models.ForeignKey(Clown, on_delete=models.CASCADE)
    reason = models.CharField(max_length=100, blank=False)

    def __str__(self):
        return f'{self.clown} -> {self.appointment.client} -> {self.reason}'
