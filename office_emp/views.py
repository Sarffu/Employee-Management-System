from django.shortcuts import render, HttpResponse, get_object_or_404,redirect
from .models import Employee, Role, Department
from datetime import datetime
from django.http import JsonResponse
from .forms import EmployeeForm


# Create your views here.
def index(request):
    return render(request, "index.html")


def view_emp(request):
    employees = Employee.objects.all()

    if request.headers.get("Accept") == "application/json":
        employees_list = list(
            employees.values(
                "id",
                "first_name",
                "last_name",
                "salary",
                "bonus",
                "phone",
                "department__name",
                "role__name",
            )
        )
        return JsonResponse({"employees": employees_list})
    else:
        context = {"employees": employees}
        return render(request, "view.html", context)


def add_emp(request):
    if request.method == "POST":
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        salary = int(request.POST["salary"])
        bonus = int(request.POST["bonus"])
        phone = int(request.POST["phone"])
        department_id = int(request.POST["department"])
        role_id = int(request.POST["role"])

        try:
            department = Department.objects.get(id=department_id)
            role = Role.objects.get(id=role_id)
        except (Department.DoesNotExist, Role.DoesNotExist) as e:
            return HttpResponse("Invalid department or role", status=400)

        new_emp = Employee(
            first_name=first_name,
            last_name=last_name,
            salary=salary,
            bonus=bonus,
            phone=phone,
            department=department,
            role=role,
            hire_date=datetime.now(),
        )
        new_emp.save()
        return HttpResponse("Employee added successfully.", status=200)

    elif request.method == "GET":
        departments = Department.objects.all()
        roles = Role.objects.all()
        context = {"departments": departments, "roles": roles}
        return render(request, "add.html", context)

    else:
        return HttpResponse("An Exception Occurred.", status=400)


# from .forms import EmployeeForm


def update_emp(request):
    if request.method == "POST":
        emp_id = request.POST.get("emp_id")
        emp = get_object_or_404(Employee, id=emp_id)

        form = EmployeeForm(request.POST, instance=emp)
        if form.is_valid():
            if form.has_changed():
                form.save()
                return redirect('update_emp')  # Redirect to the same page after a successful update
            else:
                return HttpResponse("No changes detected.", status=200)
        else:
            return HttpResponse("Invalid data submitted.", status=400)
    else:
        employees = Employee.objects.all()
        forms = {emp.id: EmployeeForm(instance=emp) for emp in employees}
        return render(request, "update.html", {"forms": forms})
    
def delete_emp(request, emp_id=None):
    if emp_id:
        try:
            emp_to_remove = Employee.objects.get(id=emp_id)
            emp_to_remove.delete()
            return HttpResponse("Employee Deleted Successfully..")
        except Employee.DoesNotExist:
            return HttpResponse("Employee not found", status=404)
        except ValueError:
            return HttpResponse("Invalid employee ID", status=400)

    employees = Employee.objects.all()
    context = {"employees": employees}
    return render(request, "delete.html", context)
