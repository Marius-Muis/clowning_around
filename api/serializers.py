from clowning_around.users.models import Client, Troupe, Clown
from rest_framework import serializers
from appointments.models import Appointment, AppointmentIssues, ClownsViewClientDetails


class ClientBaseSerializer(serializers.ModelSerializer):
    ''' Used in other serializer due to the nested relationship '''
    class Meta:
        model = Client
        fields = ['user', 'contact_name', 'contact_email', 'contact_number']


class TroupeBaseSerializer(serializers.ModelSerializer):
    ''' Used in other serializer due to the nested relationship '''
    class Meta:
        model = Troupe
        fields = ['name']


class ClownBaseSerializer(serializers.ModelSerializer):
    ''' Used in other serializer due to the nested relationship '''
    class Meta:
        model = Clown
        fields = ['user', 'rank', 'troupe']


class AppointmentViewSerializer(serializers.ModelSerializer):
    ''' Client views and/or updates rating of appointment '''
    date_created = serializers.ReadOnlyField()
    date_of_appointment = serializers.ReadOnlyField()
    # inner serializers used due to the need to view these models' fields
    client = ClientBaseSerializer(read_only=True)
    troupe = TroupeBaseSerializer(read_only=True)
    status = serializers.ReadOnlyField()

    class Meta:
        model = Appointment
        fields = ['date_created', 'date_of_appointment', 'client', 'troupe', 'status', 'rating']


class AppointmentCreateSerializer(serializers.ModelSerializer):
    ''' Troupe leader creating a new appointment (deserialization only!) '''
    date_created = serializers.ReadOnlyField()
    client = serializers.PrimaryKeyRelatedField(queryset=Client.objects.all())
    troupe = serializers.PrimaryKeyRelatedField(read_only=True)
    status = serializers.ReadOnlyField()

    class Meta:
        model = Appointment
        fields = ['date_created', 'date_of_appointment', 'client', 'troupe', 'status']


class ClownAppointmentViewSerializer(serializers.ModelSerializer):
    ''' Clown views appointments '''
    date_created = serializers.ReadOnlyField()
    date_of_appointment = serializers.ReadOnlyField()
    # source param lets you pass the model and only serializes the specified field
    client = serializers.CharField(source='client.contact_name', read_only=True)
    troupe = serializers.CharField(source='troupe.name', read_only=True)
    status = serializers.ReadOnlyField()
    rating = serializers.ReadOnlyField()

    class Meta:
        model = Appointment
        fields = ['date_created', 'date_of_appointment', 'client', 'troupe', 'status', 'rating']


class AppointmentStatusUpdateSerializer(serializers.ModelSerializer):
    ''' Clown updates the status of an appointment '''
    date_created = serializers.ReadOnlyField()
    date_of_appointment = serializers.ReadOnlyField()
    client = serializers.PrimaryKeyRelatedField(read_only=True)
    troupe = serializers.PrimaryKeyRelatedField(read_only=True)
    rating = serializers.ReadOnlyField()

    class Meta:
        model = Appointment
        fields = ['date_created', 'date_of_appointment', 'client', 'troupe', 'status', 'rating']


class AppointmentIssueCreateSerializer(serializers.ModelSerializer):
    ''' Clown raises an issue with an appointment '''
    appointment = serializers.PrimaryKeyRelatedField(read_only=True)
    clown = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = AppointmentIssues
        fields = ['appointment', 'clown', 'title', 'description']


class AppointmentClientDetailsRequestSerializer(serializers.ModelSerializer):
    ''' Clown creates a new instance of ClownsViewClientDetails when they want a client's details (serialize only) '''
    appointment = serializers.PrimaryKeyRelatedField(read_only=True)
    clown = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = ClownsViewClientDetails
        fields = ['appointment', 'clown', 'reason']
