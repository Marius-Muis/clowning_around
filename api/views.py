from django.core.exceptions import ValidationError
from clowning_around.users.models import Clown, TroupeLeader
from rest_framework import permissions, status
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateAPIView
from rest_framework.response import Response
from appointments.models import Appointment
from .serializers import AppointmentViewSerializer, AppointmentCreateSerializer, AppointmentStatusUpdateSerializer, \
    AppointmentIssueCreateSerializer, AppointmentClientDetailsRequestSerializer, ClownAppointmentViewSerializer
from datetime import datetime


class ClientsAppointmentsView(ListAPIView):
    ''' List all appointments as a client '''
    serializer_class = AppointmentViewSerializer

    def get_queryset(self):
        if self.request.user.is_client:
            appointments_queryset = Appointment.objects.filter(
                client__user=self.request.user).order_by('-date_of_appointment')
            return appointments_queryset
        else:
            raise PermissionError('You are not a client and can not access client functions.')


class ClientsAppointmentsFutureView(ListAPIView):
    ''' List all upcoming appointments as a client '''
    serializer_class = AppointmentViewSerializer

    def get_queryset(self):
        if self.request.user.is_client:
            return Appointment.objects.filter(
                client__user=self.request.user, date_of_appointment__gte=datetime.now()).order_by('-date_of_appointment')
        else:
            raise PermissionError('You are not a client and can not access client functions.')


class ClientsAppointmentsPastView(ListAPIView):
    ''' List all previous (old) appointments as a client '''
    serializer_class = AppointmentViewSerializer

    def get_queryset(self):
        if self.request.user.is_client:
            return Appointment.objects.filter(client__user=self.request.user,
                                              date_of_appointment__lt=datetime.now()).order_by('-date_of_appointment')
        else:
            raise PermissionError('You are not a client and can not access client functions.')


class ClientsAppointmentsRateView(RetrieveUpdateAPIView):
    ''' View single appointment and rate as a client. '''
    serializer_class = AppointmentViewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        if self.request.user.is_client:
            return Appointment.objects.filter(pk=self.kwargs['pk'],
                                              client__user=self.request.user)
        else:
            raise PermissionError('You are not a client and can not access client functions.')

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)


class TroupeLeaderCreateAppointmentView(CreateAPIView):
    ''' Add an appointment as a troupe leader '''
    serializer_class = AppointmentCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        if self.request.user.is_troupe_leader:
            date_of_appointment = self.request.data.get('date_of_appointment')
            troupe_leader = TroupeLeader.objects.filter(user=self.request.user).select_related('troupe')
            troupe = troupe_leader[0].troupe
            if Appointment.objects.filter(date_of_appointment=date_of_appointment, troupe=troupe).count() == 0:
                serializer.save(
                    troupe=troupe,
                    status='upcoming'
                )
            else:
                raise ValidationError('An appointment with that date already exists.')
        else:
            raise PermissionError('You are not a troupe leader and can not access troupe leader functions.')


class ClownsAppointmentsView(ListAPIView):
    ''' List all appointments as a clown '''
    serializer_class = ClownAppointmentViewSerializer

    def get_queryset(self):
        if self.request.user.is_clown:
            clown = Clown.objects.filter(user=self.request.user).select_related('troupe')[0]
            return Appointment.objects.filter(troupe=clown.troupe).order_by('-date_of_appointment')
        else:
            raise PermissionError('You are not a clown and can not access clown functions.')


class ClownsAppointmentsUpdateView(RetrieveUpdateAPIView):
    ''' View single appointment and change status as a clown '''
    # serializer_class = ClownAppointmentViewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.request.method == "PATCH":
            return AppointmentStatusUpdateSerializer
        return ClownAppointmentViewSerializer

    def get_queryset(self):
        if self.request.user.is_clown:
            clown = Clown.objects.filter(user=self.request.user).select_related('troupe')[0]
            return Appointment.objects.filter(pk=self.kwargs['pk'], troupe=clown.troupe)
        else:
            raise PermissionError('You are not a clown and can not access clown functions.')

    def update(self, request, *args, **kwargs):
        ''' Provide only the status in the body of the message; pk comes from url params '''
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)

    def perform_update(self, serializer):
        appointment = self.get_queryset()
        if appointment.exists():
            appointment = appointment[0]
            status = self.request.data.get('status')
            valid_status = ('upcoming', 'incipient', 'completed', 'cancelled')
            if status in valid_status:
                serializer.save(
                    status=status
                )
            else:
                raise ValidationError('The status you provided is not valid.')
        else:
            raise ValueError('The appointment param provided does not exist.')


class ClownsAppointmentsIssueCreateView(CreateAPIView):
    ''' Create an appointment issue as a clown '''
    serializer_class = AppointmentIssueCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        if self.request.user.is_clown:
            clown = Clown.objects.filter(user=self.request.user)[0]
            appointment = Appointment.objects.filter(pk=self.kwargs['pk'])[0]
            serializer.save(
                appointment=appointment,
                clown=clown
            )
        else:
            raise PermissionError('You are not a clown and can not access clown functions.')


class ClownsAppointmentsClientDetailsRequestView(CreateAPIView):
    serializer_class = AppointmentClientDetailsRequestSerializer
    permission_classes = [permissions.IsAuthenticated]
    appointment = None

    def perform_create(self, serializer):
        appointment = Appointment.objects.filter(pk=self.kwargs['pk']).select_related('client')[0]
        clown = Clown.objects.filter(user=self.request.user)[0]
        serializer.save(appointment=appointment, clown=clown)
        return appointment.client

    def create(self, request, *args, **kwargs):
        if self.request.user.is_clown:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            client = self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            # returning the client's details instead of the newly created 'ClownsViewClientDetails' instance
            response = {
                'name': client.contact_name,
                'email': client.contact_email,
                'number': client.contact_number
            }
            return Response(response, status=status.HTTP_201_CREATED, headers=headers)
        else:
            raise PermissionError('You are not a clown and can not access clown functions.')
