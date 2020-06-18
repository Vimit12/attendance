from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, QueryDict
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import *
from .models import *
from django.conf import settings
from django.db.models import Q
from datetime import datetime, timedelta,time as t
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
import re,time

def home_attendance(request):
    # logout(request)
    date_now = datetime.now()
    year = date_now.year
    
    if request.COOKIES.get('username') and request.COOKIES.get('pwd'):
        form = LoginForm(initial={'username': request.COOKIES.get(
            'username'), 'password': request.COOKIES.get('pwd')})
    else:
        form = LoginForm()
    max_age = 7 * 24 * 60 * 60
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            pwd = form.cleaned_data.get('password')
            remember = form.cleaned_data.get('remember_me')
            user = authenticate(request, username=username, password=pwd)
            if user is not None:
                login(request, user)
                response = render(
                        request, 'attendance/home.html', {'year': year})
                # response.delete_cookie('username')
                # response.delete_cookie('pwd')
                if remember:
                    response.set_cookie(
                            'username', username, max_age=max_age)
                    response.set_cookie('pwd', pwd, max_age=max_age)
                # else:
                #     response.set_cookie(
                #         'username', username, max_age=max_age)
                #     response.set_cookie('pwd', pwd, max_age=10)
                return response
            else:
                return render(request, 'attendance/home.html', {'year': year})
                         
    else:
        return render(request, 'attendance/home.html', {'year': year, 'form': form})


def sign_up_form(request):
    if request.method == 'POST':
        try:
            form = UserRegistrationForm(request.POST)
            if form.is_valid:
                form.save()
                username = QueryDict.dict(form.data).get('username')
                user = User.objects.filter(username=f'{username}').first()
                obj = Profile.objects.create(user=user)
                print("Form sign up ======>> ",obj)
                messages.success(
                    request, f'Your Account has been created!, You now login to access the page')
                return redirect('login')

        except Exception as e:
            print(e)
    else:
        form = UserRegistrationForm()

    return render(request, 'attendance/signup.html', {'form': form})


@login_required
def logout_view(request):
    duration = ""
    final_sec = ""
    final_min = ""
    user = User.objects.filter(username=request.user).first()
    user_profile = Profile.objects.get(user=user)
    try:
        emp_obj = Employee.objects.get(admin=user_profile)
    except Exception as e:
        emp_obj = None
    try:
        obj = Attendance.objects.filter(
        emp_id_attendance=emp_obj).order_by('attendance_date')[::1][-1]
    except Exception as e:
        obj = None
        logout(request)
        return render(request, 'attendance/logout.html')
        
    
    named_tuple = time.localtime()  # get struct_time
    time_string = time.strftime("%Y/%m/%d, %H:%M:%S", named_tuple)
    current_time = (time_string.split(',')[1]).split(':')
    
    in_time_cal = obj.in_time
    h1 = in_time_cal.hour
    m1 = in_time_cal.minute
    s1 = in_time_cal.second
    
    h2 = int(current_time[0])
    m2 = int(current_time[1])
    s2 = int(current_time[2])
    
    if not obj.out_time:
        obj.out_time = t(hour=h2, minute=m2, second=s2)
        
    # duration calculation
    if s2 < s1:
        s2 = s2+60
        m2 = m2-1
        final_sec = final_sec + str(s2-s1)
        if len(final_sec) == 1:
            final_sec = '0'+final_sec
    else:
       final_sec = final_sec + str(s2-s1)
       if len(final_sec) == 1:
            final_sec = '0'+final_sec
    
    
    if m2<m1:
        m2 = m2+60
        h2 = h2-1
        final_min = final_min + str(m2-m1)
        if len(final_min) == 1:
            final_min = '0'+final_min
    else:
        final_min = final_min + str(m2-m1)
        if len(final_min) == 1:
            final_min = '0'+final_min
    
    if h2:
        hr="00"
        if len(str(h2-h1)) == 1:
            hr = '0'+str(h2-h1)
        duration = hr+":"+final_min+":"+final_sec
    
        
    if not obj.duration:
        obj.duration = duration
    
    time_frame = duration.split(':')[0]
    if int(time_frame)<2:
        obj.stats = False
   
    obj.save()
    logout(request)
    
    return render(request, 'attendance/logout.html')

@login_required
def user_window(request):
    date_now = datetime.now()
    year = date_now.year

    user = User.objects.filter(username=request.user).first()

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid and p_form.is_valid:
            u_form.save()
            p_form.save()
            messages.success(request, f'Your Account has been Updated!')
            return redirect('user-window')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'year': year,
    }
    return render(request, 'attendance/user_window.html', context)

@login_required
def create_employee_detail(request,user_id):
    date_now = datetime.now()
    year = date_now.year
    kwargs = dict()
    user = User.objects.filter(username=user_id).first()
    user_profile = Profile.objects.get(user=user)
    try:
        emp_obj = Employee.objects.get(admin=user_profile)
    except Exception as e:
        emp_obj = None
    if emp_obj:
        form = EmployeeForm(initial={'admin': user_profile, 'name':emp_obj.name ,'emp_id': emp_obj.emp_id,'gender':emp_obj.gender,'dob':emp_obj.dob,'address':emp_obj.address})
        # form.fields['gender'].disabled = True
        # form.fields['dob'].disabled = True
        if request.method == 'POST':
            form = EmployeeForm(request.POST, initial={'admin': user_profile, 'name': emp_obj.name,
                                                        'emp_id': emp_obj.emp_id, 'gender': emp_obj.gender, 'dob': emp_obj.dob, 'address': emp_obj.address}, instance=user_profile)
            if form.is_valid():
                name_update = form.cleaned_data.get('name')
                emp_id_update = form.cleaned_data.get('emp_id')
                gender_update = form.cleaned_data.get('gender')
                dob_update = form.cleaned_data.get('dob')
                address_update = form.cleaned_data.get('address')
                if name_update != emp_obj.name or emp_id_update != emp_obj.emp_id or gender_update != emp_obj.gender or dob_update != emp_obj.dob:
                    messages.warning(
                        request, f'Name or emp_id or gender or DOB can\'t be updated')
                    return HttpResponseRedirect(request.path_info)
                if address_update == emp_obj.address:
                    messages.warning(
                        request, f'Same data can\'t be updated')
                    return HttpResponseRedirect(request.path_info)
                try:
                    emp_obj.address = form.cleaned_data.get('address')
                    emp_obj.save()
                    messages.success(
                        request, f'Data has been Updated!')
                    return HttpResponseRedirect(request.path_info)
                except Exception as e:
                    messages.warning(
                        request, f'There have been some Error, Please Contact Admin {e}')
                    return HttpResponseRedirect(request.path_info)
        return render(request, 'attendance/create_employee_detail.html', {'form': form})
    else:
        form = EmployeeForm(initial={'admin': user_profile})
        if request.method == 'POST':
            form = EmployeeForm(request.POST,instance=user_profile)
            if form.is_valid():
                kwargs['admin'] = user_profile
                kwargs['name'] = form.cleaned_data.get('name')
                if not kwargs['name'] or kwargs['name']=="":
                    messages.warning(
                        request, f'Name Field is required')
                    return HttpResponseRedirect(request.path_info)
                kwargs['emp_id'] = form.cleaned_data.get('emp_id')
                kwargs['gender'] = form.cleaned_data.get('gender')
                kwargs['dob'] = form.cleaned_data.get('dob')
                kwargs['address'] = form.cleaned_data.get('address')
                try:
                    obj = Employee(**kwargs)
                    obj.save()
                    messages.success(request, f'Data has been Updated!')
                    return HttpResponseRedirect(request.path_info)
                except Exception as e:
                    messages.warning(
                        request, f'There have been some Error, Please Contact Admin {e}')
                    return HttpResponseRedirect(request.path_info)
    
        return render(request, 'attendance/create_employee_detail.html', {'form': form})


@login_required
def mark_attendance(request,user_id):
    date_now = datetime.now()
    year = date_now.year
    
    if date_now:
        mn = str(date_now.month)
        if len(mn) == 1:
            mn='0'+mn

    named_tuple = time.localtime()  # get struct_time
    time_string = time.strftime("%Y/%m/%d, %H:%M:%S", named_tuple)
    current_time = (time_string.split(',')[1]).split(':')
    hour = int(current_time[0])
    minute = int(current_time[1])
    second = int(current_time[2])
    
    kwargs = dict()
    user = User.objects.filter(username=user_id).first()
    user_profile = Profile.objects.get(user=user)
    try:
        emp_obj = Employee.objects.get(admin=user_profile)
    except Exception as e:
        emp_obj = None
    
    if emp_obj:
        criterion1 = Q(emp_id_attendance=emp_obj)
        criterion2 = Q(attendance_date__icontains=f'-{mn}-')
        emp_user_all = Attendance.objects.filter(
            criterion1 & criterion2).order_by('attendance_date')[::1]
        # emp_user_all = Attendance.objects.filter(
        # emp_id_attendance=emp_obj).order_by('attendance_date')[::1]
    aform = AttendanceForm()
    
    if request.method == 'POST':
        aform = AttendanceForm(request.POST,instance=emp_obj)
        if aform.is_valid():
            date_from_form = aform.cleaned_data.get('attendance_date')
            month_from_form = request.POST.get('month')
            
            if date_from_form == None and month_from_form == "":
                messages.warning(
                    request, f'Please provide some Input')
                return HttpResponseRedirect(request.path_info)
            
            if date_from_form and month_from_form:
                messages.warning(
                    request, f'Invalid Input')
                return HttpResponseRedirect(request.path_info)
            
            if month_from_form:
                # messages.success(
                #     request, f'Valid Input')
               
                criterion1 = Q(emp_id_attendance=emp_obj)
                criterion2 = Q(
                    attendance_date__icontains=f'-{month_from_form}-')
                emp_user_all = Attendance.objects.filter(
                    criterion1 & criterion2).order_by('attendance_date')[::1]
                
                return render(request, 'attendance/mark_attendace.html', {'year': year, 'emp_obj': emp_obj, 'aform': aform, 'emp_user_all': emp_user_all})
               
            
            
            if date_from_form:
                day_form = date_from_form.day or 0
                month_form = date_from_form.month or 0
                year_form = date_from_form.year or 0
            
            if emp_user_all and eval(str(emp_user_all[-1].attendance_date).split('-')[-1]) == day_form:
                messages.warning(
                    request, f'Can\'t mark attendance of the same date')
                return HttpResponseRedirect(request.path_info)
            
            
            if ((day_form != date_now.day) or month_form != date_now.month or year_form != year):
                messages.warning(
                    request, f'Can\'t mark attendance other than today\'s date')
                return HttpResponseRedirect(request.path_info)
            
            
            kwargs['emp_id_attendance'] = emp_obj
            kwargs['attendance_date'] = date_from_form
            kwargs['in_time'] = t(hour=hour, minute=minute, second=second)
            
            criterion1 = Q(emp_id_attendance=emp_obj)
            criterion2 = Q(
                attendance_date__icontains=f'-{month_form}-')
            emp_user_all = Attendance.objects.filter(
                criterion1 & criterion2).order_by('attendance_date')[::1]
            
            try:
                obj = Attendance(**kwargs)
                obj.save()
                messages.success(request, f'Attendance Marked')
            except Exception as e:
                messages.warning(
                    request, f'There have been some Error, Please Contact Admin {e}')
                return HttpResponseRedirect(request.path_info)
                
        return render(request, 'attendance/mark_attendace.html', {'year': year, 'emp_obj': emp_obj, 'aform': aform, 'emp_user_all': emp_user_all})
        
    return render(request, 'attendance/mark_attendace.html', {'year': year, 'emp_obj': emp_obj, 'aform': aform, 'emp_user_all': emp_user_all})

@login_required
def apply_leaves(request,user_id):
    date_now = datetime.now()
    year = date_now.year
    
    kwargs = dict()
    user = User.objects.filter(username=user_id).first()
    user_profile = Profile.objects.get(user=user)
    
    try:
        emp_obj = Employee.objects.get(admin=user_profile)
    except Exception as e:
        emp_obj = None
        
    try:
        attendance_obj = Attendance.objects.all().filter(
            emp_id_attendance=emp_obj)[::1][-1]
    except Exception as e:
        attendance_obj = None
    
    leave_report = LeaveReportEmployee.objects.all().filter(emp_id_leave=emp_obj).order_by(
        'from_leave_date')[::1] or None
    print("#####",leave_report)
    
    lform = LeaveReportEmployeeForm()
    
    if request.method == 'POST':
        lform = LeaveReportEmployeeForm(request.POST)
        if lform.is_valid():
            
            criterion1 = Q(emp_id_leave=emp_obj)
            criterion2 = Q(from_leave_date = lform.cleaned_data.get('from_leave_date'))
            criterion3 = Q(to_leave_date = lform.cleaned_data.get('to_leave_date'))
            
            leave_report = LeaveReportEmployee.objects.filter(
                criterion1 & criterion2 & criterion3 | criterion1 & criterion2 | criterion1 & criterion3)[::1] or None
            
            # if leave_report:
            #     messages.warning(
            #         request, f'Already Applied for the same date')
            #     return HttpResponseRedirect(request.path_info)
            
            kwargs['emp_id_leave'] = emp_obj
            kwargs['attendance_id_leave'] = attendance_obj
            kwargs['from_leave_date'] = lform.cleaned_data.get(
                'from_leave_date')
            kwargs['to_leave_date'] = lform.cleaned_data.get(
                'to_leave_date')
            kwargs['leave_message'] = lform.cleaned_data.get(
                'leave_message')
            kwargs['leave_status'] = lform.cleaned_data.get(
                'leave_status')
            
            if kwargs['from_leave_date'].month > kwargs['to_leave_date'].month:
                messages.warning(request, f'From date can\'t be greater than to date')
                return HttpResponseRedirect(request.path_info)
            elif (kwargs['from_leave_date'].month == kwargs['to_leave_date'].month) and (kwargs['from_leave_date'].day > kwargs['to_leave_date'].day):
                messages.warning(
                    request, f'From date can\'t be greater than to date')
                return HttpResponseRedirect(request.path_info)
            
            try:
                obj = LeaveReportEmployee(**kwargs)
                obj.save()
                a1 = Q(emp_id_attendance = emp_obj)
                a2 = Q(attendance_date = lform.cleaned_data.get('from_leave_date'))
                print("here this part")
                try:
                    attendance_update = Attendance.objects.all().filter(
                        a1 & a2)[::1][-1]
                except Exception as e:
                    att_obj = Attendance()
                    att_obj.emp_id_attendance = emp_obj
                    att_obj.attendance_date = kwargs['from_leave_date']
                    att_obj.in_time = '00:00:00'
                    att_obj.out_time = '00:00:00'
                    att_obj.duration = 'L'
                    att_obj.stats = False
                    att_obj.save()
                    attendance_update = None

                if attendance_update:
                    attendance_update.in_time = "00:00:00"
                    attendance_update.out_time = "00:00:00"
                    attendance_update.duration = "L"
                    attendance_update.save()
                    
                messages.success(
                    request, f'Leave Applied')
            except Exception as e:
                messages.warning(
                    request, f'There have been some Error, Please Contact Admin {e}')
                return HttpResponseRedirect(request.path_info)
            leave_report = LeaveReportEmployee.objects.all().filter(emp_id_leave=emp_obj).order_by(
                'from_leave_date')[::1] or None
            return render(request, 'attendance/apply_leave.html', {'lform': lform, 'leave_report': leave_report})
    
    return render(request, 'attendance/apply_leave.html', {'lform': lform, 'leave_report': leave_report})
