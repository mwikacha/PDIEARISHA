from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponse, JsonResponse
from .models import EmpProf,ManagerProf,Employee, LeaveApplication


def homepage(request):
    return render (request,"homepage.html")

def login2(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        
        try:
            user = ManagerProf.objects.get(username2=username)
            if user.password2 == password:
                return redirect('manager1')
            else:
                error_message1 = "Incorrect password. Please try again."
        except ManagerProf.DoesNotExist:
            error_message1 = "Username does not exist. Please try again."

        return render(request, "login2.html", {"error_message": error_message1})
    return render(request, "login2.html")

def login3(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        
        try:
            user = EmpProf.objects.get(username1=username)
            if user.password1 == password:
                request.session['username'] = username
                return redirect('employeeprofile')
            else:
                error_message = "Incorrect password. Please try again."
        except EmpProf.DoesNotExist:
            error_message = "Username does not exist. Please try again."

        return render(request, "login3.html", {"error_message": error_message})

    return render(request, "login3.html")


def login_details(request, employee_name):
    employee = get_object_or_404(Employee, name=employee_name)
    emp_prof = EmpProf.objects.filter(username1=employee_name).first()

    if request.method == 'POST':
        password = request.POST.get('password')
        if emp_prof is None:
            EmpProf.objects.create(username1=employee_name, password1=password)
        else:
            emp_prof.password1 = password
            emp_prof.save()
        return render(request, 'login_details.html', {'employee': employee, 'message': 'Login account created'})

    return render(request, 'login_details.html', {'employee': employee, 'emp_prof': emp_prof})

def employeeprofile(request):
    if 'username' in request.session:
        username = request.session['username']
        employee = Employee.objects.get(name=username)
        context = {
            'employee': employee,
        }
        return render(request, "employeeprofile.html", context)
    else:
        return redirect('login3')

def leaveapplication(request):

    if request.method == 'POST':
        # Create a new LeaveApplication object and save it to the database
        leave_application = LeaveApplication(
            startDate=request.POST['startDate'],
            employeeName=request.POST['employeeName'],
            endDate=request.POST['endDate'],
            totalDays=request.POST['totalDays'],
            reason=request.POST['reason']
        )
        if 'medicalCertificate' in request.FILES:
            leave_application.medicalCertificate = request.FILES['medicalCertificate']
        leave_application.save()
        # Display a message
        request.session['application_sent'] = True
        return render(request, 'leaveapplication.html', {'application_sent': True})
    return render(request, 'leaveapplication.html', {'application_sent': False})



def leavehistory(request):
    leave_histories = LeaveApplication.objects.all()
    context = {'leave_histories':leave_histories}
    return render(request, 'leavehistory.html', context)

def leavestatus(request):
    return render (request,"leavestatus.html")

def leaveoverview(request):
    return render (request,"leaveoverview.html")

def manager1(request):
    total_employees = Employee.objects.count()
    total_leave_requests = LeaveApplication.objects.filter(status='Pending').count()
    accepted_leaves = LeaveApplication.objects.filter(status='Accepted').count()
    rejected_leaves = LeaveApplication.objects.filter(status='Rejected').count()

    context = {
        'total_employees': total_employees,
        'total_leave_requests': total_leave_requests,
        'accepted_leaves': accepted_leaves,
        'rejected_leaves': rejected_leaves,
    }

    return render(request, "manager1.html", context)


def manageleave(request):
    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        action = request.POST.get('action')
        
        try:
            leave = LeaveApplication.objects.get(startDate=start_date)
            if action == 'accept':
                leave.status = 'Accepted'
            elif action == 'reject':
                leave.status = 'Rejected'
            leave.save()
            return JsonResponse({'message': 'Action successful'}, status=200)
        except LeaveApplication.DoesNotExist:
            return JsonResponse({'message': f'Leave application not found for start date: {start_date}', }, status=404)
        except Exception as e:
            return JsonResponse({'message': f'An error occurred: {str(e)}'}, status=500)
    
    leave_requests = LeaveApplication.objects.filter(status='Pending')
    return render(request, 'manageleave.html', {'leave_requests': leave_requests})


def editleave(request, start_date):
    leave = get_object_or_404(LeaveApplication, startDate=start_date)
    
    if request.method == 'POST':
        leave.startDate = request.POST.get('start_date')
        leave.endDate = request.POST.get('end_date')
        leave.reason = request.POST.get('reason')
        leave.totalDays = request.POST.get('total_days')
        if 'medical_certificate' in request.FILES:
            leave.medicalCertificate = request.FILES['medical_certificate']
        leave.save()
        return redirect('manageleave')
    
    return render(request, 'editleave.html', {'leave': leave})

def deleteleave(request, start_date):
    leave = get_object_or_404(LeaveApplication, startDate=start_date)
    
    if request.method == 'POST':
        leave.delete()
        return redirect('manageleave')
    
    return render(request, 'deleteleave.html', {'leave': leave})




def employeelist(request):
    return render (request,"employeelist.html")

def addemployee(request):
    if request.method == 'POST':
        name = request.POST['name']
        address = request.POST['address']
        telephone = request.POST['phone']
        gender = request.POST['gender']
        employment_type = request.POST['employment_type']
        salary = request.POST['salary']
        date = request.POST['date_of_hire']
        
        Employee.objects.create(
            name=name,
            address=address,
            telephone=telephone,
            gender=gender,
            employment_type=employment_type,
            salary=salary,
            date=date
        )
        
        return render(request, "addemployee.html", {'success': True})
    
    return render(request, "addemployee.html")

def employeelist(request):
    return render(request, "employeelist.html")

def employeelist2(request):
    query = request.GET.get('search')
    if query:
        employees = Employee.objects.filter(name__icontains=query)
    else:
        employees = Employee.objects.all()
    
    emp_profs = {emp.name: EmpProf.objects.filter(username1=emp.name).first() for emp in employees}
    
    context = {
        'employees': employees,
        'query': query,
        'emp_profs': emp_profs,
    }
    return render(request, 'employeelist2.html', context)

def edit_employee(request, employee_name):
    employee = get_object_or_404(Employee, name=employee_name)
    if request.method == 'POST':
        employee.name = request.POST['name']
        employee.address = request.POST['address']
        employee.telephone = request.POST['phone']
        employee.gender = request.POST['gender']
        employee.employment_type = request.POST['employment_type']
        employee.salary = request.POST['salary']
        employee.date = request.POST['date_of_hire']
        employee.save()
        return redirect('employeelist2')

    context = {'employee': employee}
    return render(request, 'edit_employee.html', context)

def delete_employee(request, employee_name):
    employee = get_object_or_404(Employee, name=employee_name)
    employee.delete()
    return redirect('employeelist2')
