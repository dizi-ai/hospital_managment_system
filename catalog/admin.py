from django.contrib import admin
from .models import *


class AdminPatient(admin.ModelAdmin):
    fields = list_display = ['name', 'passport', 'insurance_policy', 'address', 'phonenumber']
    list_filter = ['name']
admin.site.register(Patient, AdminPatient)

class AdminPrescription(admin.ModelAdmin):
    fields = list_display = ['pres']
admin.site.register(Prescription, AdminPrescription)

class AdminPositions(admin.ModelAdmin):
    fields = list_display = ['pos_type']
admin.site.register(Positions, AdminPositions)

class AdminDepartment(admin.ModelAdmin):
    fields = list_display = ['dep_type']
admin.site.register(Department, AdminDepartment)

class AdminHospitalStay(admin.ModelAdmin):
    list_display = ['patient', 'room', 'date_beg', 'date_end']
    list_filter = ['room', 'date_beg', 'date_end']
    fieldsets = ((None,{'fields':('patient', 'room',)}),
                 ('Not available',{'fields':('date_beg', 'date_end'),}),)
admin.site.register(HospitalStay, AdminHospitalStay)

class AdminDiseases(admin.ModelAdmin):
    fields = list_display = ['name']
admin.site.register(Diseases, AdminDiseases)

class AdminRoom(admin.ModelAdmin):
    fields = list_display = ['rtype', 'free']
    list_filter = list_display
admin.site.register(Room)

class AdminRoomType(admin.ModelAdmin):
    fields = list_display = ['rtype']
    list_filter = list_display
admin.site.register(RoomType, AdminRoomType)

class AdminAppointmentResult(admin.ModelAdmin):
    fields = ['appointment', 'prescription']
    list_display = ['appointment', 'prescription']
admin.site.register(AppointmentResult,AdminAppointmentResult)

class AdminOnShift(admin.ModelAdmin):
    list_display = ['worker', 'date_beg', 'date_end']
    fieldsets = ((None,{'fields':('worker',)}),
                 ('working from/to',{'fields':('date_beg','date_end')}),)
    list_filter = list_display
admin.site.register(OnShift, AdminOnShift)

class AdminDoctor(admin.ModelAdmin):
    fields = ['name', 'email', 'password', 'gender', 'phonenumber', 'address', 'birthdate', 'specialization']
    list_display = ['name', 'email', 'password', 'gender', 'phonenumber', 'address', 'birthdate', 'specialization']
    list_filter = list_display
admin.site.register(Doctor, AdminDoctor)

class AdminReceptionost(admin.ModelAdmin):
    fields = ['name', 'email', 'password', 'gender', 'phonenumber', 'address', 'birthdate']
    list_display = ['name', 'email', 'password', 'gender', 'phonenumber', 'address', 'birthdate']
admin.site.register(Receptionist, AdminReceptionost)

