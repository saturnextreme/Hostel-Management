from django.shortcuts import render, redirect
from .models import *
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ObjectDoesNotExist
import datetime
import os 
from django.conf import settings

# Client Side 
from PyPDF2 import PdfWriter, PdfReader, Transformation
import io
from reportlab.pdfgen.canvas import Canvas


points = [(480,635),(300,610),(300,570),(300,540),(300,510),(300,470),(275,430),
          (275,418),(285,370),(480,370),(285,340),(480,340),(300,300),(300,260),
          (300,220),(275,192),(275,180),(100,115),(400,115),(100,45),(400,45)]

class GenerateFromTemplate:
    def __init__(self, template):
        self.template_pdf = PdfReader(open(template, "rb"))
        self.template_page = self.template_pdf.pages[0]

        self.packet = io.BytesIO()
        self.c = Canvas(self.packet, pagesize=(self.template_page.mediabox.width, self.template_page.mediabox.height))

    def addText(self, text, point):
        self.c.drawString(point[0], point[1], text)

    def merge(self):
        self.c.save()
        self.packet.seek(0)
        result_pdf = PdfReader(self.packet)
        result = result_pdf.pages[0]

        self.output = PdfWriter()

        op = Transformation().rotate(0).translate(tx=0, ty=0)
        result.add_transformation(op)
        self.template_page.merge_page(result)
        self.output.add_page(self.template_page)

    def generate(self, dest):
        outputStream = open(dest, "wb")
        self.output.write(outputStream)
        outputStream.close()
    



def login_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.session.get('rollno'):
            return redirect('login') 
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def admin_login_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.session.get('username'):
            return redirect('admin_login') 
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def home(request):
    return render(request, 'home.html')

def logout(request):
    request.session.clear()
    return redirect('home')

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        if email == "" and password == "":
            msg = f'Enter all Credentials'
            messages.error(request, msg)
            return redirect('login')

        try:
            stu = Student.objects.get(email=email)
            if stu is not None:
                if check_password(password, stu.password):
                    request.session['email'] = stu.email
                    request.session['fname'] = stu.firstName
                    request.session['lname'] = stu.lastName
                    request.session['rollno'] = stu.rollno
                    try:
                        request.session['imageurl'] = stu.image.url
                    except Exception as e:
                        pass
                    request.session.save()

                    return redirect('dashboard')
                else:
                    msg = f'Incorrect Password'
                    messages.error(request, msg)
                    return redirect('login')
        except Exception as e:
            msg = f'Invalid Credentials'
            messages.error(request, msg)
            return redirect('login')

    return render(request, 'client/login.html')

def signup(request):
    if request.method == 'POST':
        first_name = request.POST.get('f_name')
        last_name = request.POST.get('l_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        c_password = request.POST.get('c_password')
        rollno = email.split('@')[0]
        
        if email.split('@')[1] != 'iiitt.ac.in':
            msg = f'Enter your College Email ID'
            messages.error(request, msg)
            return redirect('signup')

        if password != c_password:
            msg = f'Both password are not correct'
            messages.error(request, msg)
            return redirect('signup')

        if email == "" and password == "" and first_name == "" and last_name == "":
            msg = f'Enter all Credentials'
            messages.error(request, msg)
            return redirect('signup')

        if Student.objects.filter(email=email).exists():
            stu = Student.objects.get(email=email)
            data = {
                'name': stu.firstName,
                'email': stu.email,
                'password': stu.password
            }
            msg = f'You already have an account'
            messages.error(request, msg)
            return redirect('signup')
        
        student = Student(
            firstName=first_name,
            lastName=last_name,
            email=email,
            password=make_password(password),
            rollno=rollno
        )
        student.save()

        msg = f'Account Sucessfully Created'
        messages.success(request, msg)
        return redirect('signup')

    return render(request, 'client/signup.html')

@login_required
def dashboard(request):
    email = request.session.get('email')
    fname = request.session.get('fname')
    lname = request.session.get('lname')
    rollno = request.session.get('rollno')

    notification = Notification.objects.all().order_by('-created_at')
    data = []
    val = 0
    for i in notification:
        content = {
            'notice': i.notice,
            'user': i.username,
            'date': i.created_at
        }
        data.append(content)
        if val == 3:
            break
        val+=1

    context = {
        'email': email,
        'fname': fname,
        'lname': lname,
        'rollno': rollno,
        'display': 'block',
        'data': data
    }
    print(context)
    return render(request, 'client/dashboard.html', context)

@login_required
def profile(request):
    email = request.session.get('email')
    fname = request.session.get('fname')
    lname = request.session.get('lname')
    rollno = request.session.get('rollno')
    dob = ""
    dept = ""
    semester = ""
    course = ""
    year = ""
    block = ""
    room = ""
    father_m = ""
    mother_m = ""
    student_m = ""
    address = ""


    try:
        acad = Academics.objects.get(rollno=rollno)
        dept = acad.department
        year = acad.year
        course = acad.course
        semester = acad.semester

        hostel = Hostel.objects.get(rollno=rollno)
        room = hostel.room
        block = hostel.bg_block

        student = Student.objects.get(rollno=rollno)
        dob = student.dob
        father_m = student.father_mob
        mother_m = student.mother_mob
        student_m = student.sudent_mob
        address = student.permanent_address


    except Exception as e:
        pass

    context = {
        'email': email,
        'fname': fname,
        'lname': lname,
        'rollno': rollno,
        'dept': dept,
        'year': year,
        'room': room,
        'course': course,
        'semester': semester,
        'block_n': block,
        'dob': dob,
        'father_m':father_m,
        'mother_m':mother_m,
        'student_m':student_m,
        'address': address

    }
    return render(request, "client/profile.html", context)

@login_required
def edit_profile(request):
    if request.method == 'POST':
        dept = request.POST.get('dept')
        semester = request.POST.get('semester')
        course = request.POST.get('course')
        year = request.POST.get('year')
        block = request.POST.get('block')
        room = request.POST.get('room')
        dob = request.POST.get('dob')
        father_m = request.POST.get('father_m')
        mother_m= request.POST.get('mother_m')
        student_m= request.POST.get('student_m') 
        address = request.POST.get('address')
        if 'image' in request.FILES:
            image = request.FILES['image']

        rollno = request.session.get('rollno')

        student = Student.objects.get(rollno=rollno)

        try:
            if image:
                if student.image:
                    student.image.delete()
                student.image = image
        except Exception as e:
            pass

        if dob:
            student.dob = dob
        if father_m:
            student.father_mob = father_m
        if mother_m:
            student.mother_mob = mother_m
        if student_m:
            student.sudent_mob = student_m
        if address:
            student.permanent_address = address
        
        student.save()
        request.session['imageurl'] = student.image.url

        if Academics.objects.filter(rollno=rollno).exists():
            academics = Academics.objects.get(rollno=rollno)
            if dept:
                academics.department = str(dept)
            if year:
                academics.year = year
            if semester:
                academics.semester = semester
            if course:
                academics.course = course
            academics.save()
        else: 
            acad, created = Academics.objects.get_or_create(
                rollno=student,
                department=str(dept),
                year=year,
                semester=semester,
                course=course
            )
            acad.save()

        if Hostel.objects.filter(rollno=rollno).exists():
            hostel = Hostel.objects.get(rollno=rollno)
            if room:
                try:
                    hostel.room = int(room)
                except Exception as e:
                    pass
            if block:
                hostel.bg_block = block
            hostel.save()
        else:
            try:
                hostel, created2 = Hostel.objects.get_or_create(
                    rollno=student,
                    room=int(room),
                    bg_block = block
                )
                hostel.save()
            except Exception as e:
                pass
        
        
        return redirect('profile')
    
    return render(request, 'client/edit_profile.html')


@login_required
def complaints(request):
    rollno = request.session.get('rollno')
    if request.method == 'POST':
        complaint = request.POST.get('complaint')

        student = Student.objects.get(rollno=rollno)
        comp = Complaints.objects.create(
            rollno=student,
            complaint=complaint
        )
        comp.save()
        return redirect('complaints')
    
    comp = Complaints.objects.filter(rollno=rollno)
    context = []
    for record in comp:
        v='red'
        print(record.isverified)
        if record.isverified == True:
            v='green'

        context.append({'created_at': record.created_at, 'complaint': record.complaint, 'color': v})
    

    return render(request, 'client/complaints.html', {'context': context})

@login_required
def notification(request):

    notification = Notification.objects.all()
    data = []
    for i in notification:
        content = {
            'notice': i.notice,
            'user': i.username,
            'date': i.created_at
        }
        data.append(content)

    return render(request, "client/notification.html", {'context': data})


@login_required
def leaveform(request):
    rollno = request.session.get('rollno')
    student = Student.objects.get(rollno=rollno)
    fname = student.firstName
    lname = student.lastName
    context = {
            'rollno': rollno,
            'fname': fname,
            'lname': lname
    }

    if request.method == 'POST':
        leave_d = request.POST.get('leave_d')
        leave_t =request.POST.get('leave_t')
        arrive_d = request.POST.get('arrive_d')
        arrive_t = request.POST.get('arrive_t')
        reason = request.POST.get('reason')
        reservation_file = request.FILES.get('reservation')
        
        if leave_d == "" and leave_t == "" and arrive_d == "" and arrive_t == "" and reason == "":
            msg = f'Enter all credentials.'
            messages.error(request, msg)
            return redirect('leaveform')
    
        if not Hostel.objects.filter(rollno=student).exists() or not Academics.objects.filter(rollno=student).exists():
            msg = 'Complete your profile first. Please fill in all the required details of your Profile.'
            messages.error(request, msg)
            return redirect('leaveform')
            
        form = LeaveForm(
            form_acceptance = 'Pending',
            reason = reason,
            leave_date = leave_d,
            leave_time = leave_t,
            arrive_date = arrive_d,
            arrive_time = arrive_t,
            rollno = student,
            reservation=reservation_file
        )
        form.save()

        msg = f'Leave Form Has been Submitted.Check its status on leave for status.'
        messages.success(request, msg)
        return redirect('leaveform')


    return render(request, "client/leaveform.html", context=context)

@login_required
def leaveformstatus(request):
    rollno = request.session.get('rollno')
    student = Student.objects.get(rollno=rollno)
    fname = student.firstName
    lname = student.lastName
    formdata = LeaveForm.objects.filter(rollno=rollno)

    data = []

    view = 'orange'
    for i in formdata:
        if i.form_acceptance == 'Accepted':
            view='green'
        elif i.form_acceptance == 'Rejected':
            view='red'
        else:
            view='orange'
        content = {
            'fname': fname,
            'lname': lname,
            'rollno': rollno,
            'reason': i.reason,
            'acceptance': i.form_acceptance,
            'reservation': i.reservation.url,
            'form': i.form.name,
            'col': view
        }
        data.append(content)

    return render(request, 'client/leaveformstatus.html', {'context': data})

# Admin Side

def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username == "" and password == "":
            msg = f'Enter all Credentials'
            messages.error(request, msg)
            return redirect('admin_login')

        try:
            adm = Admin.objects.get(username=username)
            if adm is not None:
                if check_password(password, adm.password):
                    request.session['username'] = adm.username
                    request.session.save()

                    return redirect('admin_dashboard')
        except Exception as e:
            msg = f'Invalid Credentials'
            messages.error(request, msg)
            return redirect('admin_login')

    return render(request, 'admin/admin_login.html')

def admin_signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        c_password = request.POST.get('c_password')
        passphrase = request.POST.get('passphrase')

        if username == "" and password == "" and passphrase == "":
            msg = f'Enter all Credentials'
            messages.error(request, msg)
            return redirect('admin_signup')
        
        if password != c_password:
            msg = f'Both password are not correct'
            messages.error(request, msg)
            return redirect('admin_signup')

        if Admin.objects.filter(username=username).exists():
            adm = Admin.objects.get(username=username)
    
            msg = f'You already have an account'
            messages.error(request, msg)
            return redirect('admin_signup')
        
        if passphrase == 'woac':
            admin = Admin(
                username=username,
                password=make_password(password)
            )
            admin.save()
            msg = f'Account Sucessfully Created'
            messages.success(request, msg)
            return redirect('admin_signup')
    return render(request, 'admin/admin_signup.html')

@admin_login_required
def admin_dashboard(request):
    fname = request.session.get('username')

    complaints = Complaints.objects.all().order_by('-created_at')
    notification = Notification.objects.all().order_by('-created_at')
    data = []
    val = 0
    for i in complaints:
        content = {
            'notice': i.complaint,
            'date': i.created_at
        }
        data.append(content)
        if val == 3:
            break
        val+=1

    data2 = []
    val2 = 0
    for i in notification:
        content = {
            'complaint': i.notice,
            'date': i.created_at
        }
        data2.append(content)
        if val2 == 3:
            break
        val2+=1

    context = {
        'fname': fname,
        'display': 'block',
        'data': data,
        'data2': data2
    }
    print(context)
    return render(request, 'admin/admin_dashboard.html', context)

@admin_login_required
def student_detail(request):
    if request.method == 'POST':
        rollno = request.POST.get('rollno')
        return redirect('viewprofile', parameter=rollno)

    search_query = request.GET.get('search')
    if search_query:
        student = Student.objects.filter(
            Q(firstName__icontains=search_query) |
            Q(lastName__icontains=search_query) |
            Q(rollno__icontains=search_query)
        )
    else:
        student = Student.objects.all()
    hostel = ""
    academic = ""
    data = []
    for i in student:
        try:
            hostel = Hostel.objects.get(rollno=i.rollno)
            academic = Academics.objects.get(rollno=i.rollno)
            content = {
            'fname': i.firstName,
            'lname': i.lastName,
            'rollno': i.rollno,
            'hostel': hostel.room,
            'semester': academic.semester,
            'bg': hostel.bg_block
            }
            data.append(content)
        except ObjectDoesNotExist:
            content = {
            'fname': i.firstName,
            'lname': i.lastName,
            'rollno': i.rollno,
            }
            data.append(content)
    return render(request, 'admin/student_detail.html', {'context': data})

@admin_login_required
def viewprofile(request, parameter):
    rollno = parameter
    print(rollno)
    dob = ""
    dept = ""
    semester = ""
    course = ""
    year = ""
    block = ""
    room = ""
    father_m = ""
    mother_m = ""
    student_m = ""
    address = ""
    image_url = ""

    student = Student.objects.get(rollno=rollno)

    fname = student.firstName
    lname = student.lastName
    email = student.email

    try:
        acad = Academics.objects.get(rollno=rollno)
        dept = acad.department
        year = acad.year
        course = acad.course
        semester = acad.semester

        hostel = Hostel.objects.get(rollno=rollno)
        room = hostel.room
        block = hostel.bg_block
        
        dob = student.dob
        father_m = student.father_mob
        mother_m = student.mother_mob
        student_m = student.sudent_mob
        address = student.permanent_address
        image_url = student.image.url
    
    except Exception as e:
        pass

    context = {
        'email': email,
        'fname': fname,
        'lname': lname,
        'rollno': rollno,
        'dept': dept,
        'year': year,
        'room': room,
        'course': course,
        'semester': semester,
        'block_n': block,
        'dob': dob,
        'father_m':father_m,
        'mother_m':mother_m,
        'student_m':student_m,
        'address': address,
        'imageurl': image_url
    }
    return render(request, 'admin/view_profile.html', context)

@admin_login_required
def admin_notification(request):
    username = request.session.get('username')
    if request.method == 'POST':
        notification = request.POST.get('notification')

        admin = Admin.objects.get(username=username)
        comp = Notification.objects.create(
            username=admin,
            notice=notification,
            created_at = datetime.datetime.now()

        )
        comp.save()
    
    comp = Notification.objects.filter(username=username)
    context = []
    for record in comp:
        context.append({'created_at': record.created_at, 'notice': record.notice})

    return render(request, 'admin/admin_notification.html', {'context': context})

@admin_login_required
def admin_complaint(request):
    
    comp = Complaints.objects.all().order_by('-created_at')
    
    data = []
    for i in comp:
        if isinstance(i.rollno, Student):
            rollno = i.rollno.rollno 
        else:
            rollno = i.rollno 
        i.isverified = True
        i.save()
        stud = Student.objects.get(rollno=rollno)
        try:
            hostel = Hostel.objects.get(rollno=rollno)
            room_number = hostel.room
        except Hostel.DoesNotExist:
            room_number = ""
        content = {
            'rollno': i.rollno,
            'fname': stud.firstName,
            'lname': stud.lastName,
            'comp': i.complaint,
            'roomno': room_number,
            'created_at': i.created_at
        }
        data.append(content)


    return render(request, 'admin/admin_complaint.html', {'context': data})

@admin_login_required
def admin_leaveform(request):
    forms = LeaveForm.objects.all()
    data = [
        {
            'rollno': form.rollno.rollno if isinstance(form.rollno, Student) else form.rollno,
            'reason': form.reason,
            'acceptance': form.form_acceptance,
            'reservation': form.reservation.url,
        }
        for form in forms
    ]

    if request.method == 'POST':
        roll = request.POST.get('roll')
        username = request.session.get('username')
        reason = request.POST.get('reason')
        accept = request.POST.get('accept')

        if accept != 'reject':

            student = Student.objects.get(rollno=roll)
            hostel = Hostel.objects.get(rollno=student)
            academic = Academics.objects.get(rollno=student)
            leaveform = LeaveForm.objects.get(rollno=student, reason=reason)
            path = os.path.join(settings.MEDIA_ROOT, 'leave_form.pdf')
            gen = GenerateFromTemplate(path)
            current_date = datetime.date.today()
            formatted_date = current_date.strftime("%Y-%m-%d") 

            data = {
                'date': formatted_date,
                'name': f"{student.firstName} {student.lastName}",
                'roll': student.rollno,
                'room': hostel.room,
                'batch': academic.department,
                'year': academic.year,
                'reason': leaveform.reason,
                '': ' ',
                'leave_d': leaveform.leave_date,
                'leave_t': leaveform.leave_time,
                'arrive_d': leaveform.arrive_date,
                'arrive_t': leaveform.arrive_time,
                'stu': student.sudent_mob,
                'fath': student.father_mob,
                'moth': student.mother_mob,
                'address': student.permanent_address,
                ' ': ' ',
                ' ': ' ',
                'name2': student.firstName,
                'warden': f"{username} 1",
                'deputy': f"{username} 2",
                'chief': f"{username} 3"
            }

            if leaveform.form_acceptance == 'Pending' or leaveform.form_acceptance == 'Rejected' and leaveform.form.name == "": 
                for text, coords in zip(data.values(), points):
                    gen.addText(str(text), (coords[0], coords[1]))
                
                current_time = datetime.datetime.now()
                formatted_time = current_time.strftime("%Y-%m-%d%H-%M-%S")
                name = os.path.join(settings.MEDIA_ROOT, f"pdfs/form/{student.rollno}__{formatted_time}.pdf")
                print(name)
                gen.merge()
                gen.generate(name)
                
                leaveform.form_acceptance = 'Accepted'
                leaveform.form.name = f"media/pdfs/form/{student.rollno}__{formatted_time}.pdf"
                leaveform.save()
            return redirect('admin_leaveform')

        elif accept == 'reject':
            student = Student.objects.get(rollno=roll)
            leaveform = LeaveForm.objects.get(rollno=student, reason=reason)
            if leaveform.form.name == "":
                leaveform.form_acceptance = 'Rejected'
                leaveform.save()
                pass
            else:
                student = Student.objects.get(rollno=roll)
                leaveform = LeaveForm.objects.get(rollno=student, reason=reason)
                leaveform.form_acceptance = 'Rejected'

                name = leaveform.form.name
                os.remove(name)
                leaveform.form.name = ""
                leaveform.save()
            return redirect('admin_leaveform')
        
    return render(request, 'admin/admin_leaveform.html', {'context': data})