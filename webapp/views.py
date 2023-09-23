from django.shortcuts import render, redirect
from .forms import CreateUserForm, LoginForm, DailyReportForm, TaskStatusForm

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import DailyReport, GeneratedReport, Task, Group, TaskStatus, Client, User, GeneratedTaskStatus
from django.contrib import messages
import datetime
import calendar
from django.db.models import Q

from django.http import HttpResponse
import csv

# Create your views here.
def home(request):
    return render(request, 'webapp/index.html')


def register(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, "Account successfully created")
            return redirect('login')

        # else:
        #     return HttpResponse('An error occurred during registration')

    context = {'form': form}
    return render(request, 'webapp/register.html', context)


def loginUser(request):
    form = LoginForm()

    if request.method == 'POST':
        form = LoginForm(request, request.POST)

        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, "Successfully logged in!")

                return redirect('daily-monitoring')


        else:
            messages.error(request, "Invalid username and password")

    context = {'form':form}
    return render(request, 'webapp/my-login.html', context)


def logoutUser(request):
    logout(request)
    messages.success(request, "Successfully logged out!")
    return redirect('home')


@login_required(login_url='login')
def daily_monitoring(request):
    date = datetime.date.today().strftime('%B %d, %Y')
    date_number = datetime.date.today()
    records = DailyReport.objects.filter(
        date__year=date_number.year,
        date__month=date_number.month,
        date__day=date_number.day,
    )

    if request.method == "POST":
        try:
            year = (request.POST.get('date').split("-"))[0]
            month = (request.POST.get('date').split("-"))[1]
            day = (request.POST.get('date').split("-"))[2]

            month_words = calendar.month_name[int(month)]
            date = f"{month_words} {day}, {year}"

            records = DailyReport.objects.filter(
                date__year=year,
                date__month=month,
                date__day=day,
            )

            context = {'records':records,  'date': date}
            return render(request, 'webapp/daily_monitoring.html', context)

        except:
            messages.error(request, "Please Select a Date")

            return redirect('daily-monitoring')


    context = {'records': records, 'date': date}
    return render(request, 'webapp/daily_monitoring.html', context)

@login_required(login_url='login')
def dashboardProfile(request, pk):
    user = request.user
    date = datetime.date.today().strftime('%B %d, %Y')
    date_number = datetime.date.today()
    my_records = DailyReport.objects.filter(
        user__employee_id=user.employee_id,
        date__year=date_number.year,
        date__month=date_number.month,
        date__day=date_number.day,
    )

    if request.method == "POST":
        try:
            year = (request.POST.get('date').split("-"))[0]
            month = (request.POST.get('date').split("-"))[1]
            day = (request.POST.get('date').split("-"))[2]

            month_words = calendar.month_name[int(month)]
            date = f"{month_words} {day}, {year}"

            my_records = DailyReport.objects.filter(
                user__employee_id=user.employee_id,
                date__year=year,
                date__month=month,
                date__day=day,
            )

            context = {'records': my_records, 'date':date}
            return render(request, 'webapp/profile.html', context)

        except:
            messages.error(request, "Please Select a Date")
            return redirect('profile', pk=request.user.id)


    context = {'records': my_records, 'date':date}
    return render(request, 'webapp/profile.html', context)

############################# REPORT ################################
@login_required(login_url='login')
def create_record(request):
    record = 'create'
    form = DailyReportForm()
    tasks = Task.objects.all()
    clients = Client.objects.all()

    if request.method == "POST":
        time_start = datetime.datetime.strptime(request.POST.get('time_start'), '%H:%M') #for subtracting time only
        req_time_end = request.POST.get('time_end')

        if req_time_end == '':
            time_end = "--:--"
            total_time = "--:--"

        else:
            strp_time_end = datetime.datetime.strptime(request.POST.get('time_end'), '%H:%M') #for subtracting time only
            time_end = strp_time_end.strftime('%I:%M %p')
            diff_time = str(strp_time_end - time_start).split(":")
            total_time = f"{diff_time[0]}:{diff_time[1]}"

        print(request.POST.get('time_start'),time_end, total_time)

        task_name = request.POST.get('task')
        task, created = Task.objects.get_or_create(name=task_name)

        client_name = request.POST.get('client')
        client, created = Client.objects.get_or_create(name=client_name)

        DailyReport.objects.create(
            user=request.user,
            task=task,
            area_extent=request.POST.get('area_extent'),
            client=client,
            date=request.POST.get('date'),
            time_start=request.POST.get('time_start'),
            time_end=time_end,
            total_time= total_time,
            status=request.POST.get('status'),
            l_hd=request.POST.get('l_hd'),
        )
        if form.is_valid():
            form.save(commit=False)
            form.user = request.user
            form.save()
        messages.success(request, "Record successfully created")

        return redirect('profile', pk=request.user.id)

    context = {'form':form, 'record':record, 'tasks':tasks, 'clients':clients}
    return render(request, 'webapp/create-update-record.html', context)


@login_required(login_url='login')
def update_record(request, pk):
    record = DailyReport.objects.get(id=pk)
    form = DailyReportForm(instance=record)
    tasks = Task.objects.all()
    clients = Client.objects.all()

    if request.method == "POST":
        try:
            time_start = datetime.datetime.strptime(request.POST.get('time_start'), '%H:%M:%S')
        except:
            time_start = datetime.datetime.strptime(request.POST.get('time_start'), '%H:%M')

        req_time_end = request.POST.get('time_end')

        if req_time_end == '':
            time_end = "--:--"
            total_time = "--:--"

        else:
            strp_time_end = datetime.datetime.strptime(request.POST.get('time_end'),
                                                       '%H:%M')  # for subtracting time only
            time_end = strp_time_end.strftime('%I:%M %p')
            diff_time_end = datetime.datetime.strptime(request.POST.get('time_end'), '%H:%M') #for subtracting time only
            diff_time = str(diff_time_end - time_start).split(":")
            total_time = f"{diff_time[0]}:{diff_time[1]}"

        task_name = request.POST.get('task')
        task, created = Task.objects.get_or_create(name=task_name)

        client_name = request.POST.get('client')
        client, created = Client.objects.get_or_create(name=client_name)

        record = form.save(commit=False)
        record.task = task
        record.area_extent = request.POST.get('area_extent')
        record.client = client
        record.date = request.POST.get('date')
        record.time_start = request.POST.get('time_start')
        record.time_end = time_end
        record.total_time = total_time
        record.status = request.POST.get('status')
        record.save()

        messages.success(request, "Record successfully updated")

        return redirect('profile', pk=request.user.id)

        # messages.error(request, "Error")

    context = {'record':record, 'form':form, 'tasks':tasks, 'clients':clients}
    return render(request, 'webapp/create-update-record.html', context)


@login_required(login_url='login')
def view_record(request, pk):
    record = DailyReport.objects.get(id=pk)


    context = {'record':record}
    return render(request, 'webapp/view-record.html', context)


@login_required(login_url='login')
def delete_record(request, pk):
    record = DailyReport.objects.get(id=pk)

    if request.method == "POST":
        record.delete()
        messages.success(request, "Record successfully deleted")
        return redirect('daily-monitoring')

    return render(request, 'webapp/delete.html', {'obj':record})


############################## STATUS ####################################
############################## STATUS ####################################
############################## STATUS ####################################
def taskStatus(request, pk):
    user = User.objects.get(id=pk)
    records = user.taskstatus_set.all()

    context={'records': records}
    return render(request, 'webapp/status.html', context)


def createTaskStatus(request):
    record = 'create'
    form = TaskStatusForm()
    tasks = Task.objects.all()
    clients = Client.objects.all()
    groups = Group.objects.all()

    if request.method == "POST":
        task_name = request.POST.get('task')
        task, created = Task.objects.get_or_create(name=task_name)

        client_name = request.POST.get('client')
        client, created = Client.objects.get_or_create(name=client_name)

        group_name = request.POST.get('group')
        group, created = Group.objects.get_or_create(name=group_name)

        req_date_finish = request.POST.get('date_finish')

        if req_date_finish == "":
            date_finish = "-- -- --"
        else:
            strp_date_finish = datetime.datetime.strptime(req_date_finish, "%Y-%m-%d")
            date_finish = strp_date_finish.strftime('%a, %b %d, %Y')

        # print(request.POST.get('date_start'), date_finish)
        TaskStatus.objects.create(
            user=request.user,
            name=task,
            area_extent=request.POST.get('area_extent'),
            count=request.POST.get('count'),
            group=group,
            client=client,
            date_start=request.POST.get('date_start'),
            date_finish=date_finish,
            status=request.POST.get('status'),
            progress=request.POST.get('progress'),
            pts_ref=request.POST.get('pts_ref'),
            invoice=request.POST.get('invoice'),
            remarks=request.POST.get('remarks'),
        )
        messages.success(request, "Task successfully created")

        return redirect('status-report', pk=request.user.id)

    context = {'record':record ,'form':form, 'tasks':tasks, 'clients':clients, 'groups':groups}
    return render(request, 'webapp/create-update-status.html', context)


def view_status(request, pk):
    record = TaskStatus.objects.get(id=pk)

    context = {'record':record}
    return render(request, 'webapp/view-status.html', context)

def editStatus(request, pk):
    record = TaskStatus.objects.get(id=pk)
    form = TaskStatusForm(instance=record)
    clients = Client.objects.all()
    groups = Group.objects.all()
    tasks = Task.objects.all()

    if request.method == "POST":
        task_name = request.POST.get('task')
        task, created = Task.objects.get_or_create(name=task_name)

        client_name = request.POST.get('client')
        client, created = Client.objects.get_or_create(name=client_name)

        group_name = request.POST.get('group')
        group, created = Group.objects.get_or_create(name=group_name)

        req_date_finish = request.POST.get('date_finish')

        if req_date_finish == "":
            date_finish = "-- -- --"
        else:
            strp_date_finish = datetime.datetime.strptime(req_date_finish, "%Y-%m-%d")
            date_finish = strp_date_finish.strftime('%a, %b %d, %Y')

        record.name = task
        record.client = client
        record.group = group
        record.area_extent = request.POST.get('area_extent')
        record.count = request.POST.get('count')
        record.date_start = request.POST.get('date_start')
        record.date_finish = date_finish
        record.status = request.POST.get('status')
        record.progress = request.POST.get('progress')
        record.pts_ref = request.POST.get('pts_ref')
        record.invoice = request.POST.get('invoice')
        record.remarks = request.POST.get('remarks')
        record.save()
        return redirect('status-report', pk=request.user.id)

    context = {'record': record, 'form': form, 'tasks': tasks, 'clients': clients, 'groups': groups}
    return render(request, 'webapp/create-update-status.html', context)

@login_required(login_url='login')
def deleteStatus(request, pk):
    record = TaskStatus.objects.get(id=pk)

    if request.method == "POST":
        record.delete()
        messages.success(request, "Record successfully deleted")
        return redirect('status-report', pk=request.user.id)

    return render(request, 'webapp/delete.html', {'obj':record})

@login_required(login_url='login')
def viewAllStatus(request):
    GeneratedTaskStatus.objects.all().delete()
    records = TaskStatus.objects.all()

    if request.method == "POST":
        GeneratedTaskStatus.objects.all().delete()

        q = request.POST.get('q') if request.POST.get('q') != None else ''

        records = TaskStatus.objects.filter(Q(user__first_name__icontains=q) |
                                      Q(user__last_name__icontains=q) |
                                      Q(client__name__icontains=q) |
                                      Q(name__name__icontains=q) |
                                      Q(status__icontains=q)
                                      )

    for record in records:
        GeneratedTaskStatus.objects.create(
            user=record.user,
            name=record.name,
            area_extent=record.area_extent,
            count=record.client,
            client=record.client,
            group=record.group,
            ijo_no=record.ijo_no,
            date_start=record.date_start,
            date_finish=record.date_finish,
            status=record.status,
            progress=record.progress,
            pts_ref=record.pts_ref,
            invoice=record.invoice,
            remarks=record.remarks,

        )

    context = {'records': records}
    return render(request, 'webapp/view-all-status.html', context)

#################################### GENERATE CSV ##########################################
#################################### GENERATE CSV ##########################################
#################################### GENERATE CSV ##########################################
@login_required(login_url='login')
def generateReport(request):

    if request.method == "POST":
        GeneratedReport.objects.all().delete()

        q = request.POST.get('q') if request.POST.get('q') != None else ''
        try:
            date_records = DailyReport.objects.filter(
                date__range=[request.POST.get('date'), request.POST.get('date2')]
            )
        except:
            date_records = DailyReport.objects.all()

        records = date_records.filter(Q(user__first_name__icontains=q) |
                                      Q(user__last_name__icontains=q) |
                                      Q(client__name__icontains=q) |
                                      Q(task__name__icontains=q) |
                                      Q(status__icontains=q)
                                      )

        for record in records:
            GeneratedReport.objects.create(
                user=record.user,
                task=record.task,
                area_extent=record.area_extent,
                client=record.client,
                date=record.date,
                time_start=record.time_start,
                time_end=record.time_end,
                total_time=record.total_time,
                status=record.status,
                l_hd=record.l_hd,
            )

        context = {'records': records}

        return render(request, 'webapp/generate-report.html', context)

    return render(request, 'webapp/generate-report.html')


def export_csv_timeReport(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="time-report.csv"'

    writer = csv.writer(response)
    writer.writerow(['user__first_name','user__last_name', 'task', 'area_extent', 'client', 'date', 'time_start', 'time_end', 'total_time', 'status', 'l_hd'])

    reports = GeneratedReport.objects.all().values_list('user__first_name', 'user__last_name','task', 'area_extent', 'client', 'date', 'time_start', 'time_end', 'total_time', 'status', 'l_hd')
    for report in reports:
        writer.writerow(report)

    GeneratedReport.objects.all().delete()
    return response

def export_csv_task(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="task-status.csv"'

    writer = csv.writer(response)
    writer.writerow(['user__first_name', 'user__last_name', 'task', 'area_extent', 'count', 'client', 'group', 'ijo_no', 'date_start', 'date_finish', 'status', 'progress', 'pts_ref', 'invoice', 'remarks'])

    reports = GeneratedTaskStatus.objects.all().values_list('user__first_name', 'user__last_name', 'name__name', 'area_extent', 'count', 'client__name', 'group__name', 'ijo_no', 'date_start', 'date_finish', 'status', 'progress', 'pts_ref', 'invoice', 'remarks')
    for report in reports:
        writer.writerow(report)

    GeneratedTaskStatus.objects.all().delete()
    return response
