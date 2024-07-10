from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Employee, Leave, Dashboard, Package
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from datetime import datetime


def indexPage(request):
    return render(request, "index.html")

def LogoutPage(request):
    return render(request, "index.html")

def HrLogin(request):
    if request.method == 'POST':
        username = request.POST.get('hr_username')
        password = request.POST.get('hr_password')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            request.session['first_name'] = user.first_name
            request.session['last_name'] = user.last_name
            return redirect('hr_dashboard')  # Redirect to HR dashboard upon successful login
        else:
            return HttpResponse("Username or password is incorrect")
    else:
        return render(request, "hr_login.html")

def EmpLogin(request):
    if request.method == 'POST':
        username = request.POST.get('emp_username')
        password = request.POST.get('emp_password')
        user = authenticate(request, username=username, password=password)
        if user is not None and not user.is_staff:
            login(request, user)
            request.session['first_name'] = user.first_name
            request.session['last_name'] = user.last_name
            return redirect('emp_dashboard')  
        else:
            return HttpResponse("Username or password is incorrect")
    return render(request, "emp_login.html")

# Manage Dashboard HR and Employee
def HrDashboard(request):
    first_name = request.session.get('first_name')
    last_name = request.session.get('last_name')
    announcements = Dashboard.objects.all()

    # Get the leave status counts
    leave_counts = Leave.objects.values('status').annotate(count=Count('status'))
    leave_stats = {'Pending': 0, 'Approved': 0, 'Rejected': 0}
    
    for leave in leave_counts:
        leave_stats[leave['status']] = leave['count']

    return render(request, "hr_dashboard.html", {
        'first_name': first_name,
        'last_name': last_name,
        'announcements': announcements,
        'leave_stats': leave_stats,
    })

def AddNewDash(request):
    if request.method == 'POST':
        title = request.POST.get('announcement_title')
        content = request.POST.get('announcement_content')
        date = request.POST.get('announcement_date')
        if title and content and date:
            Dashboard.objects.create(announcement_title=title, announcement_content=content, announcement_date=date)
            return redirect('hr_dashboard')  # Redirect to HR dashboard after saving
    return render(request, "add_dashboard.html")

def update_announcement(request, announcement_id):
    announcement = get_object_or_404(Dashboard, id=announcement_id)
    if request.method == 'POST':
        announcement.announcement_title = request.POST.get('announcement_title')
        announcement.announcement_content = request.POST.get('announcement_content')
        announcement.announcement_date = request.POST.get('announcement_date')
        announcement.save()
        return redirect('hr_dashboard')
    return render(request, 'update_dashboard.html', {'announcement': announcement})

def delete_announcement(request, announcement_id):
    announcement = get_object_or_404(Dashboard, id=announcement_id)
    announcement.delete()
    return redirect('hr_dashboard')
    

# Dashboard for Employee
def EmpDashboard(request):
    first_name = request.session.get('first_name')
    last_name = request.session.get('last_name')
    announcements = Dashboard.objects.all()
    return render(request, "emp_dashboard.html", {'first_name': first_name, 'last_name': last_name, 'announcements': announcements})




# Profile Page
@login_required
def ProfilePage(request):
    user = request.user
    employee = get_object_or_404(Employee, emp_username=user.username)
    
    context = {
        'employee': employee,
    }
    return render(request, "profile.html", context)

def UpdatePage(request, employee_ic):
    employee = get_object_or_404(Employee, employee_ic=employee_ic)
    context = {
        'employee': employee,
    }
    return render(request, "profile_update.html", context)

@login_required
def UpdateDataProfile(request, employee_ic):
    employee = get_object_or_404(Employee, employee_ic=employee_ic)
    if request.method == 'POST':
        employee.num_phone = request.POST['phone']
        employee.dob = request.POST['dob']
        employee.emergency_name = request.POST['emergency_name']
        employee.emergency_num = request.POST['emergency_number']
        employee.employee_email = request.POST['employee_email']
        
        if 'picture' in request.FILES:
            employee.profile_pic = request.FILES['picture']
        employee.save()
        return redirect(reverse("profile"))  # Redirect to ProfilePage view
    else:
        return HttpResponse("Invalid method")




# Leave Page
def LeavePage(request):
    if request.method == 'POST':
        leavetype = request.POST['leave_type']
        startdate = request.POST['start_date']
        enddate = request.POST['end_date']
        reason = request.POST['reason']
        document = request.FILES.get('document')  # Retrieve uploaded file

        employee = get_object_or_404(Employee, emp_username=request.user.username)
        
        # Convert startdate and enddate from string to date objects
        startdate = datetime.strptime(startdate, '%Y-%m-%d').date()
        enddate = datetime.strptime(enddate, '%Y-%m-%d').date()

        # Calculate the leave duration
        leave_duration = (enddate - startdate).days + 1
        
        leave_request = Leave(
            leavetype=leavetype,
            startdate=startdate,
            enddate=enddate,
            reason=reason,
            status='Pending',
            employee_ic=employee,
            document=document  # Save uploaded document
        )
        leave_request.save()
        
        return redirect('leave_status')  # Redirect to leave status page after saving

    # Get the total leave for the logged-in employee
    employee = get_object_or_404(Employee, emp_username=request.user.username)
    total_leave = employee.total_leave

    return render(request, "leave.html", {'total_leave': total_leave})


def LeaveStatus(request):
    employee = get_object_or_404(Employee, emp_username=request.user.username)
    leave_requests = Leave.objects.filter(employee_ic=employee)
    return render(request, "leavestatus.html", {'leave_requests': leave_requests, 'total_leave': employee.total_leave})


# Manage Employee Page
def ManageEmpPage(request):
    alldata = Employee.objects.all()
    allemployee_ic = Employee.objects.all()
    allemployee_name = Employee.objects.all()
    allposition = Employee.objects.all()

    dict = {
        'alldata': alldata,
        'allemployee_ic': allemployee_ic,
        'allemployee_name': allemployee_name,
        'allposition': allposition,
    }
    return render(request, "manage_emp.html", dict)

def AddEmpPage(request):
    if request.method == 'POST':
        employee_ic = request.POST['employee_ic']
        employee_name = request.POST['employee_name']
        department = request.POST['department']
        position = request.POST['position']
        salary = request.POST['salary']
        emp_username = request.POST['emp_username']
        emp_password = request.POST['emp_password']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        total_leave = request.POST['total_leave']  # Capture total leave

        # Create a new Employee object and save it to the database
        new_employee = Employee(
            employee_ic=employee_ic,
            employee_name=employee_name,
            department=department,
            position=position,
            salary=salary,
            emp_username=emp_username,
            emp_password=emp_password,
            total_leave=total_leave  # Set total leave
        )
        new_employee.save()

        # Create a new User object
        user = User.objects.create_user(
            username=emp_username,
            password=emp_password,
            first_name=first_name,
            last_name=last_name
        )
        user.save()

        return redirect('manage_emp')

    else:
        return render(request, "add_emp.html")

def ViewEmp(request, employee_ic):
    employee = get_object_or_404(Employee, employee_ic=employee_ic)
    context = {
        'employee': employee,
    }
    return render(request, "view_profile.html", context)

def delete_employee(request, employee_ic):
    employee = get_object_or_404(Employee, employee_ic=employee_ic)
    employee.delete()
    return redirect('manage_emp')



# Manage Leave
def ManageLeave(request):
    if not request.user.is_staff:  # Only HR should access this view
        return redirect('hr_dashboard')
    leave_requests = Leave.objects.all()
    return render(request, "manage_leave.html", {'leave_requests': leave_requests})

def UpdateLeaveStatus(request, leave_id, status):
    if not request.user.is_staff:
        return redirect('home')
    leave_request = get_object_or_404(Leave, id=leave_id)
    
    if status == 'Approved':
        # Calculate the leave duration
        leave_duration = (leave_request.enddate - leave_request.startdate).days + 1
        # Subtract the leave duration from the employee's total leave
        employee = leave_request.employee_ic
        if employee.total_leave >= leave_duration:
            employee.total_leave -= leave_duration
            employee.save()
        else:
            return HttpResponse("Not enough leave balance")
    
    leave_request.status = status
    leave_request.save()
    return redirect('manage_leave')





