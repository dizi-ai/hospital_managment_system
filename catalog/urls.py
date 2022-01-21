from django.urls import path
from . import views


urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('about/',views.aboutpage,name='aboutpage'),
    path('login/',views.loginpage,name='loginpage'),
    path('createaccount',views.createaccountpage,name='createaccountpage'),
    path('profile/',views.profile,name='profile'),
    path('home/',views.homepage,name='homepage'),
    path('appointmentresults/',views.appointmentresults,name='appointmentresult'),
    path('hospitalstay/',views.hospitalstay,name='hospitalstay'),
    path('makeappointments/',views.MakeAppointments,name='makeappointments'),
    path('viewappointments/',views.viewappointments,name='viewappointments'),
    path('PatientDeleteAppointment<int:pid>',views.patient_delete_appointment,name='patient_delete_appointment'),
    path('setshift/',views.setshift,name='setshift'),
    path('logout/',views.Logout,name='logout'),
    path('adminaddDoctor/',views.adminaddDoctor,name='adminaddDoctor'),
    path('adminaddReceptionist/',views.adminaddReceptionist,name='adminaddReceptionist'),
    path('statistic/',views.statistic,name='statistic'),
    path('patinfo/',views.patinfo,name='patinfo'),
    path('viewshift/',views.viewshifts,name='viewshift'),
]