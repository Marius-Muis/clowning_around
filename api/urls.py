from django.urls import path
from .views import ClientsAppointmentsView, ClientsAppointmentsFutureView, ClientsAppointmentsPastView, \
    ClientsAppointmentsRateView, TroupeLeaderCreateAppointmentView, ClownsAppointmentsView, \
    ClownsAppointmentsUpdateView, ClownsAppointmentsIssueCreateView, ClownsAppointmentsClientDetailsRequestView

urlpatterns = [
    # clients:
    path('clients/appointments', ClientsAppointmentsView.as_view()),
    path('clients/appointments/upcoming', ClientsAppointmentsFutureView.as_view()),
    path('clients/appointments/past', ClientsAppointmentsPastView.as_view()),
    path('clients/appointments/<int:pk>', ClientsAppointmentsRateView.as_view()),

    # troupe leaders:
    path('troupeleader/createappointment', TroupeLeaderCreateAppointmentView.as_view()),

    # clowns:
    path('clowns/appointments', ClownsAppointmentsView.as_view()),
    path('clowns/appointments/<int:pk>', ClownsAppointmentsUpdateView.as_view()),
    path('clowns/appointments/<int:pk>/issue', ClownsAppointmentsIssueCreateView.as_view()),
    path('clowns/appointments/<int:pk>/clientdetails', ClownsAppointmentsClientDetailsRequestView.as_view()),
]
