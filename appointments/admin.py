from django.contrib import admin
from .models import Appointment, AppointmentIssues, ClownsViewClientDetails

admin.site.register(Appointment)
admin.site.register(AppointmentIssues)
admin.site.register(ClownsViewClientDetails)
