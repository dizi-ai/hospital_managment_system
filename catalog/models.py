from django.db import models
from django.urls import reverse


class Department(models.Model):
    dep_type = models.TextField()

    def __str__(self):
        return self.dep_type

    def get_absolute_url(self):
        return reverse('department-detail', args=[str(self.id)])


class Positions(models.Model):
    pos_type = models.TextField()

    def __str__(self):
        return self.pos_type

    def get_absolute_url(self):
        return reverse('positions-detail', args=[str(self.id)])


class Doctor(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=16)
    gender = models.CharField(max_length=10)
    phonenumber = models.CharField(max_length=10)
    address = models.CharField(max_length=100)
    birthdate = models.DateField()
    specialization = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Receptionist(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=16)
    gender = models.CharField(max_length=10)
    phonenumber = models.CharField(max_length=10)
    address = models.CharField(max_length=100)
    birthdate = models.DateField()

    def __str__(self):
        return self.name


class Patient(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=16)
    gender = models.CharField(max_length=10)
    phonenumber = models.CharField(max_length=10)
    address = models.CharField(max_length=100)
    birthdate = models.DateField()
    insurance_policy = models.CharField(max_length=50)
    passport = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class Diseases(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('diseases-detail', args=[str(self.id)])


class Prescription(models.Model):
    pres = models.TextField()

    def __str__(self):
        return self.pres

    def get_absolute_url(self):
        return reverse('prescription-detail', args=[str(self.id)])


class Appointment(models.Model):
    doctorid = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patientid = models.ForeignKey(Patient, on_delete=models.CASCADE)
    appointmentdate = models.DateField(max_length=10)
    appointmenttime = models.TimeField(max_length=10)
    symptoms = models.CharField(max_length=100)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.patientid.name + "you have appointment with " + self.doctorid.name


class AppointmentResult(models.Model):
    appointment = models.ForeignKey(Appointment,on_delete=models.CASCADE)
    disease = models.ForeignKey(Diseases, on_delete=models.CASCADE)
    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()


class RoomType(models.Model):
    rtype = models.TextField()

    def __str__(self):
        return self.rtype

    def get_absolute_url(self):
        return reverse('roomtype-detail', args=[str(self.id)])


class Room(models.Model):
    rtype = models.ForeignKey(RoomType, on_delete=models.CASCADE)
    free = models.BooleanField()

    def __str__(self):
        return "{0} {1}".format(self.rtype, self.free)

    def get_absolute_url(self):
        return reverse('room-detail', args=[str(self.id)])


class OnShift(models.Model):
    worker = models.ForeignKey(Receptionist, on_delete=models.CASCADE)
    date_beg = models.DateField()
    date_end = models.DateField()

    def __str__(self):
        return "{0} {1} {2}".format(self.worker, self.date_beg, self.date_end)

    def get_absolute_url(self):
        return reverse('onshift-detail', args=[str(self.id)])


class HospitalStay(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    appointmentresult = models.ForeignKey(AppointmentResult, on_delete=models.CASCADE)
    date_beg = models.DateField()
    date_end = models.DateField(null=True)

    def __str__(self):
        return "{0} {1} {2} {3}".format(self.patient, self.room, self.date_beg, self.date_end)

    def get_absolute_url(self):
        return reverse('hospitalstay-detail', args=[str(self.id)])
