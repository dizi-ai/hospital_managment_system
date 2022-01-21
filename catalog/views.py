from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from .models import *
from django.contrib.auth import authenticate, logout, login
from django.utils import timezone
from datetime import timedelta, datetime, date


# Create your views here.

def homepage(request):
    return render(request, 'index.html')


def aboutpage(request):
    return render(request, 'about.html')


def loginpage(request):
    if request.user.is_active:
        return render(request, 'index.html')
    if request.method == 'POST':
        u = request.POST['email']
        p = request.POST['password']
        user = authenticate(request, username=u, password=p)
        try:
            if user is not None:
                login(request, user)
                error = "no"
                g = request.user.groups.all()[0].name
                if g == 'Doctor':
                    page = "doctor"
                    d = {'error': error, 'page': page}
                    return render(request, 'doctorprofile.html', d)
                elif g == 'Receptionist':
                    page = "reception"
                    d = {'error': error, 'page': page}
                    return render(request, 'receptionhome.html', d)
                elif g == 'Patient':
                    page = "patient"
                    d = {'error': error, 'page': page}
                    return render(request, 'pateintprofile.html', d)
        except Exception:
            pass
    return render(request, 'login.html')


def Logout(request):
    if not request.user.is_active:
        return render(request, 'index.html')
    logout(request)
    return render(request, 'index.html')


def createaccountpage(request):
    error = ""
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        repeatpassword = request.POST['repeatpassword']
        gender = request.POST['gender']
        phonenumber = request.POST['phonenumber']
        address = request.POST['address']
        birthdate = request.POST['dateofbirth']
        ip = request.POST['dateofbirth']
        passport = request.POST['dateofbirth']
        try:
            if password == repeatpassword:
                Patient.objects.create(name=name, email=email, password=password, gender=gender,
                                       phonenumber=phonenumber, address=address, birthdate=birthdate,
                                       insurance_policy=ip, passport=passport)
                user = User.objects.create_user(first_name=name, email=email, password=password, username=email)
                pat_group = Group.objects.get(name='Patient')
                pat_group.user_set.add(user)
                user.save()
                error = "no"
            else:
                error = "yes"
        except Exception:
            error = "yes"
    d = {'error': error}
    return render(request, 'createaccount.html', d)


def adminaddDoctor(request):
    error = ""
    if not request.user.is_staff:
        return redirect('homepage')

    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        repeatpassword = request.POST['repeatpasssword']
        gender = request.POST['gender']
        phonenumber = request.POST['phonenumber']
        address = request.POST['address']
        birthdate = request.POST['dateofbirth']
        specialization = request.POST['specialization']

        try:
            if password == repeatpassword:
                Doctor.objects.create(name=name, email=email, password=password, gender=gender, phonenumber=phonenumber,
                                      address=address, birthdate=birthdate,
                                      specialization=Department.objects.get(dep_type=specialization))
                user = User.objects.create_user(first_name=name, email=email, password=password, username=email)
                doc_group = Group.objects.get(name='Doctor')
                doc_group.user_set.add(user)
                user.save()
                error = "no"
            else:
                error = "yes"
        except Exception:
            error = "yes"
    return render(request, 'adminadddoctor.html', context={"dep_list": Department.objects.all(), 'error': error})


def adminaddReceptionist(request):
    error = ""
    if not request.user.is_staff:
        return redirect('login_admin')

    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        repeatpassword = request.POST['repeatpassword']
        gender = request.POST['gender']
        phonenumber = request.POST['phonenumber']
        address = request.POST['address']
        birthdate = request.POST['dateofbirth']

        try:
            if password == repeatpassword:
                Receptionist.objects.create(name=name, email=email, password=password, gender=gender,
                                            phonenumber=phonenumber, address=address, birthdate=birthdate)
                user = User.objects.create_user(first_name=name, email=email, password=password, username=email)
                rec_group = Group.objects.get(name='Receptionist')
                rec_group.user_set.add(user)
                user.save()
                error = "no"
            else:
                error = "yes"
        except:
            error = "yes"
    d = {'error': error}
    return render(request, 'adminaddreceptionist.html', d)


def patient_delete_appointment(request, pid):
    if not request.user.is_active:
        return redirect('loginpage')
    appointment = Appointment.objects.get(id=pid)
    appointment.delete()
    return redirect('viewappointments')


def Home(request):
    if not request.user.is_active:
        return redirect('homepage')

    g = request.user.groups.all()[0].name
    if g == 'Doctor':
        return render(request, 'doctorprofile.html')
    elif g == 'Receptionist':
        return render(request, 'receptionhome.html')
    elif g == 'Patient':
        return render(request, 'pateintprofile.html')


def profile(request):
    if not request.user.is_active:
        return redirect('loginpage')

    g = request.user.groups.all()[0].name
    if g == 'Patient':
        patient_detials = Patient.objects.all().filter(email=request.user)
        d = {'patient_detials': patient_detials}
        return render(request, 'pateintprofile.html', d)
    elif g == 'Doctor':
        doctor_detials = Doctor.objects.all().filter(email=request.user)
        d = {'doctor_detials': doctor_detials}
        return render(request, 'doctorprofile.html', d)
    elif g == 'Receptionist':
        reception_details = Receptionist.objects.all().filter(email=request.user)
        d = {'reception_details': reception_details}
        return render(request, 'receptionprofile.html', d)


def MakeAppointments(request):
    error = ""
    if not request.user.is_active:
        return redirect('loginpage')
    alldoctors = Doctor.objects.all()
    d = {'alldoctors': alldoctors}
    g = request.user.groups.all()[0].name
    if g == 'Patient':
        if request.method == 'POST':
            doctorid = request.POST['doctorid']
            patientemail = request.user.email
            appointmentdate = request.POST['appointmentdate']
            appointmenttime = request.POST['appointmenttime']
            symptoms = request.POST['symptoms']
            date = datetime.strptime('2022-01-22','%Y-%m-%d')
            if not datetime.strptime(appointmentdate, '%Y-%m-%d') < date:
                if len(Appointment.objects.filter(appointmentdate=appointmentdate, appointmenttime=appointmenttime))==0:
                    try:
                        Appointment.objects.create(doctorid=Doctor.objects.get(id=doctorid),
                                           patientid=Patient.objects.get(email=patientemail),
                                           appointmentdate=appointmentdate,
                                           appointmenttime=appointmenttime, symptoms=symptoms)
                        error = "no"
                    except Exception as e:
                        error = "yes"
                    e = {"error": error}
                    return render(request, 'pateintmakeappointments.html', context={'error': error, 'alldoctors': alldoctors})
            else:
                error = "yes"
                e = {"error": error}
                return render(request, 'pateintmakeappointments.html', context={'error': error, 'alldoctors': alldoctors})
        elif request.method == 'GET':
            return render(request, 'pateintmakeappointments.html', d)


def viewappointments(request):
    if not request.user.is_active:
        return redirect('loginpage')

    g = request.user.groups.all()[0].name
    if g == 'Patient':
        upcomming_appointments = Appointment.objects.filter(patientid=Patient.objects.get(email=request.user.email),
                                                            status=False, ).order_by('appointmentdate')
        previous_appointments = Appointment.objects.filter(patientid=Patient.objects.get(email=request.user.email),
                                                           status=True).order_by('-appointmentdate')
        d = {"upcomming_appointments": upcomming_appointments, "previous_appointments": previous_appointments}
        return render(request, 'patientviewappointments.html', d)
    elif g == 'Doctor':
        if request.method == 'POST':
            presc = request.POST.get('prescription')
            appid = request.POST.get('idofappointment')
            disease = request.POST['disease']
            date = timezone.now().date()
            time = timezone.now().time()
            AppointmentResult.objects.create(prescription=Prescription.objects.get(pres=presc),
                                                 appointment=Appointment.objects.get(id=appid),
                                                 disease=Diseases.objects.get(name=disease),
                                                 date=date, time=time)
            Appointment.objects.filter(id=appid).update(status=True)
        upcoming_appointments = Appointment.objects.filter(doctorid=Doctor.objects.get(email=request.user.email).id,
                                                           status=False).order_by('appointmentdate')
        previous_appointments = Appointment.objects.filter(doctorid=Doctor.objects.get(email=request.user.email).id,
                                                           status=True).order_by('-appointmentdate')
        d = {"upcoming_appointments": upcoming_appointments, "previous_appointments": previous_appointments,
             'press': Prescription.objects.all(), 'diseases': Diseases.objects.all()}
        return render(request, 'doctorviewappointment.html', d)
    elif g == 'Receptionist':
        upcoming_appointments = Appointment.objects.filter(doctorid=Doctor.objects.get(email=request.user.email).id,
                                                           status=False).order_by('appointmentdate')
        previous_appointments = Appointment.objects.filter(doctorid=Doctor.objects.get(email=request.user.email).id,
                                                           status=True).order_by('-appointmentdate')
        d = {"upcomming_appointments": upcoming_appointments, "previous_appointments": previous_appointments,
             "date": timezone.now().date()}
        return render(request, 'receptionviewappointments.html', d)


def appointmentresults(request):
    if request.user.groups.all()[0].name != 'Doctor':
        return render(request, 'index.html')
    if request.method == 'POST':
        date_b =  request.POST['date_beg']
        app_res = request.POST['idofappres']
        room_id = request.POST['roomid']
        app = AppointmentResult.objects.get(id=app_res)
        date = datetime.strptime('2022-01-22','%Y-%m-%d')
        if not datetime.strptime(date_b, '%Y-%m-%d') < date and room_id!='не выбрано':
            if len(HospitalStay.objects.filter(patient=Patient.objects.get(id=app.appointment.patientid.id),
                                           date_end__isnull=True)) == 0:
                HospitalStay.objects.create(patient=Patient.objects.get(id=app.appointment.patientid.id),
                                        room=Room.objects.get(id=room_id), appointmentresult=app,
                                        date_beg=date_b)

                Room.objects.filter(id=room_id).update(free=False)

    appres = AppointmentResult.objects.all().order_by('-appointment__appointmentdate')
    if request.GET.get('idpat', False):
        if request.GET.get('idpat') != 'не выбрано':
            appres = AppointmentResult.objects.filter(appointment__patientid=request.GET['idpat']).order_by('-appointment__appointmentdate')
    rooms = Room.objects.filter(free=True)
    return render(request, 'appointmentresults.html', context={'results': appres,
                                                               'patient_ids': Patient.objects.all(),
                                                               'room_ids': rooms})


def setshift(request):
    if request.user.groups.all()[0].name != 'Doctor':
        return render(request, 'index.html')
    receptionists = Receptionist.objects.all()
    if request.method == 'GET' and request.GET.get('idres', False):
        idres = request.GET['idres']
        if idres != 'не выбрано':
            receptionists = OnShift.objects.filter(worker__id=idres)
        else:
            receptionists = OnShift.objects.all()
    if request.method == 'POST':
        worker = Receptionist.objects.get(id=request.POST['idres'])
        date_b = request.POST['date']
        date_e = datetime.strptime(date_b, '%Y-%m-%d').date() + timedelta(days=1)
        date = datetime.strptime('2022-01-22','%Y-%m-%d')
        if not datetime.strptime(date_b, '%Y-%m-%d') < date:
            OnShift.objects.create(worker=worker, date_beg=date_b, date_end=date_e)
    return render(request, 'setshift.html', context={'recs': Receptionist.objects.all(), 'receps': receptionists})


def viewshifts(request):
    if request.user.groups.all()[0].name != 'Receptionist':
        return render(request,'index.html')
    return render(request,'viewshift.html',context={'future_shifts': OnShift.objects.filter(
        worker=Receptionist.objects.get(email=request.user.email), date_beg__gte=timezone.now()).order_by('date_beg'),
                                                    'past_shifts': OnShift.objects.filter(
                                                        worker=Receptionist.objects.get(
                                                            email=request.user.email), date_beg__lt=timezone.now()).order_by('-date_beg')
                                                    })


def hospitalstay(request):
    if request.user.groups.all()[0].name != 'Doctor':
        return render(request, 'index.html')
    if request.method == 'POST':
        hs_id = request.POST['idofhs']
        HospitalStay.objects.filter(id=hs_id).update(date_end=timezone.now().date())
        Room.objects.filter(id=HospitalStay.objects.get(id=hs_id).room.id).update(free=True)
    hospstay = HospitalStay.objects.filter(date_end__isnull=True)
    hspstayc = HospitalStay.objects.filter(date_end__isnull=False)
    return render(request, 'hospitalstay.html', context={'hospitalstay': hospstay, 'hospitalstayc': hspstayc})


def statistic(request):
    if request.method == 'POST':
        ars = []
        if request.POST['dateb']=='':
            if request.POST['datee']=='':
                ars = AppointmentResult.objects.all()
            else:
                ars = AppointmentResult.objects.filter(date__lte=request.POST['datee'])
        else:
            if request.POST['datee']=='':
                ars = AppointmentResult.objects.filter(date__gte=request.POST['dateb'])
            else:
                ars = AppointmentResult.objects.filter(date__lte=request.POST['datee'], date__gte=request.POST['dateb'])
        diss = dict()
        for d in Diseases.objects.all():
            diss[d.name]=0
        for ar in ars:
            if diss.__contains__(ar.disease.name):
                diss[ar.disease.name]+=1

        diss_stat=[]
        for k in diss.keys():
            diss_stat.append(k+' : '+str(diss[k]))
        return render(request, 'statistic.html', context={'rooms_free': len(Room.objects.filter(free=True)),'diss': Diseases.objects.all(),'stats': diss_stat})

    return render(request, 'statistic.html', context={'rooms_free': len(Room.objects.filter(free=True)),'diss': Diseases.objects.all()})


def patinfo(request):
    if request.user.groups.all()[0].name == 'Patient':
        return render(request, 'patientinfo.html', context={'results': AppointmentResult.objects.filter(
            appointment__patientid=Patient.objects.get(email=request.user.email)).order_by(
            '-appointment__appointmentdate')})
    page = 'patinfo.html'
    if request.user.groups.all()[0].name == 'Receptionist':
        page = 'patientinfores.html'
    if request.method == 'POST':
        if request.POST['idpat'] != 'не выбрано':
            return render(request, page, context={'pats': Patient.objects.all(), 'results':
                AppointmentResult.objects.filter(appointment__patientid=request.POST['idpat'])})
    return render(request, page, context={'pats': Patient.objects.all(),
                                                'results': AppointmentResult.objects.all()})
