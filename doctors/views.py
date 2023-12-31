from django.shortcuts import render,redirect
from patients.models import Doctors
from patients.models import Patients




def doctors(request):

    # Important! patient_diplay should initially be hidden and should only be viewable after
    # entering the correct password
    login_display = "block"
    patient_display = "none"

    #These values should be defined here to prevent 'referenced before assignment error' because
    #these values are called but is not assigned before the submit using request.POST.
    doctor_qs = None
    patient_list = None
    msg = ""
    error_msg = ""
     

    if request.method=='POST':
        got_username = request.POST['username']
        got_password = request.POST['password']
        try:
            doctor_qs = Doctors.objects.get(username=got_username)
            real_password = doctor_qs.password

          
            patients_qs = doctor_qs.patients_set.all()
            patient_list = list(patients_qs)

            if len(patient_list)==0:
                msg="No patients yet"


            if got_password == real_password:
                patient_display = "block"
                login_display = "none"
            else:
                error_msg = "wrong password"
        except:
            error_msg = "invalid username"
        


    context = {
        'doctor_qs':doctor_qs,
        # 'doctor_objects': doctor_objects,
        'patient_list': patient_list,
        # 'master_list':master_list,
        'patient_display':patient_display,
        'login_display':login_display,
        'msg':msg,
        'error_msg':error_msg,
    }
        
    return render(request,'doctors.html',context)



def signup(request):
        error_msg = ""

        if request.method=='POST':
            firstname=request.POST['fname']
            lastname=request.POST['lname']
            username=request.POST['username']
            password=request.POST['password']
            input_len = len(firstname)*len(username)*len(password)
            if not input_len == 0:
                try:
                    doctor_qs = Doctors.objects.get(username=username)
                    error_msg = "username already exists!"
                except:
                    doctor = Doctors(firstname=firstname,lastname=lastname,username=username,password=password)
                    doctor.save()
                    return redirect('/doctors/signup/success')

                
        context = {
            'error_msg':error_msg,
        }

        return render(request,'signup.html',context)


def register_success(request):
    return render(request,'register_success.html')