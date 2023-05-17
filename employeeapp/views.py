import datetime
import os
import time
from django.contrib import messages
from django.contrib.auth import logout, authenticate
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from.models import *
from.forms import *
from Employeemanagementsystem.settings import EMAIL_HOST_USER
from django.core.paginator import Paginator


# Create your views here.
def index(request):
    return render(request,'index.html')


def adminlogin(request):
    if request.method=='POST':
        username=request.POST.get("username")
        password=request.POST.get("password")
        request.session['username'] = username
        user_obj=User.objects.filter(username=username).first()
        if user_obj is None:
            messages.success(request,'user not found!')
            return redirect(adminlogin)
        user=authenticate(username=username,password=password)
        if user is None:
            messages.success(request,'username or password is wrong')
            return redirect(adminlogin)
        return redirect(adminprofile)
    return render(request,"adminlogin.html")

def admin(request):
    return render(request,"admin.html")

def employee(request):
    return render(request,"employee.html")

def adminprofile(request):
    ad=request.session['username']
    z = employeeaddmodel.objects.all().count()
    u = employeeaddmodel.objects.filter(status='Active').values().count()
    l = employeeaddmodel.objects.filter(status='Inactive').values().count()
    h= taskmode.objects.all().count()
    x = taskmode.objects.filter(status='Submitted').values().count()
    k = taskmode.objects.filter(status='Pending').values().count()
    a = empleave.objects.all().count()
    c=empleave.objects.filter(response='Pending').values().count()
    d = empleave.objects.filter(response='Approved').values().count()
    return render(request,"adminprofile.html",{'ad':ad,'z':z,'h':h,'a':a,'c':c,'d':d,'k':k,'x':x,'u':u,'l':l})

def addemp(request):
    if request.method=='POST':
        a=employeeaddform(request.POST,request.FILES)
        if a.is_valid():
            ef=a.cleaned_data["empfname"]
            el=a.cleaned_data["emplname"]
            em=a.cleaned_data["email"]
            ph=a.cleaned_data["phonenumber"]
            eid=a.cleaned_data["empid"]
            db=a.cleaned_data["dob"]
            gn=a.cleaned_data["gender"]
            dp=a.cleaned_data["department"]
            emg=a.cleaned_data["empimg"]
            ps=a.cleaned_data["password"]
            b=employeeaddmodel(empfname=ef,emplname=el,email=em,phonenumber=ph,dob=db,gender=gn,department=dp,empimg=emg,empid=eid,password=ps)
            if employeeaddmodel.objects.filter(empid=eid).first():
                messages.success(request, "Employee id already taken")
                return redirect(addemp)
            b.save()
            send_mail_reg(em,eid,ps)
            messages.success(request,"Employee addedd....")
        else:
            messages.success(request,"Failed to add employee")
    return render(request,'addemployee.html')

def send_mail_reg(em,eid,ps):
    subject = "Your account has been created"
    message = f'Here is your employeeid and password \n employeeid : {eid} \n password : {ps} \n click the link to login : http://127.0.0.1:8000/employeeapp/emplogin/'
    # f formatter:the expressions are replaced by values
    email_from = EMAIL_HOST_USER  # from
    recipient = [em]  # to
    send_mail(subject, message, email_from, recipient)

def empdetails(request):
    a = employeeaddmodel.objects.all().order_by('id')
    paginator = Paginator(a, 10)
    page_number = request.GET.get('page')
    a = paginator.get_page(page_number)
    efnm = []
    elnm = []
    phnm = []
    eml = []
    emid = []
    dofb = []
    emig = []
    dep = []
    gnd = []
    dfjg = []
    stus = []
    empid = []
    for i in a:
        id = i.id
        empid.append(id)
        ef = i.empfname
        efnm.append(ef)
        el = i.emplname
        elnm.append(el)
        ph = i.phonenumber
        phnm.append(ph)
        em = i.email
        eml.append(em)
        eid = i.empid
        emid.append(eid)
        df = i.dob
        dofb.append(df)
        eig = i.empimg
        emig.append(str(eig).split('/')[-1])
        dp = i.department
        dep.append(dp)
        gn = i.gender
        gnd.append(gn)
        st = i.status
        stus.append(st)
        dj = i.dateofjoining
        dfjg.append(dj)
    mylist = zip(efnm, elnm, phnm, eml, emid, dofb, emig, dep, gnd, dfjg, stus, empid)
    return render(request, 'employeedetails.html', {'mylist': mylist,'a':a})


def updateemp(request,id):
    a=employeeaddmodel.objects.get(id=id)
    im=str(a.empimg).split('/')[-1]
    if request.method=='POST':
        if len(request.FILES):
            if len(a.empimg) > 0:
                os.remove(a.empimg.path)
            a.empimg=request.FILES['empimg']
        a.empfname=request.POST.get('empfname')
        a.emplname = request.POST.get('emplname')
        a.email = request.POST.get('email')
        a.phonenumber = request.POST.get('phonenumber')
        a.empid = request.POST.get('empid')
        a.dob = request.POST.get('dob')
        a.password = request.POST.get('password')
        a.gender = request.POST.get('gender')
        a.department = request.POST.get('department')
        a.status=request.POST.get('status')
        a.save()
        messages.success(request, "employee detail updated...")
        return redirect(empdetails)
    return render(request,"updateemployee.html",{'a':a,'im':im})

def empdelete(request,id):
    a=employeeaddmodel.objects.get(id=id)
    a.delete()
    messages.success(request, "employee deleted...")
    return redirect(empdetails)

def emplogin(request):
    if request.method == 'POST':
        a = emplogform(request.POST)
        if a.is_valid():
            ed = a.cleaned_data["empid"]
            ps = a.cleaned_data["password"]
            b = employeeaddmodel.objects.all()
            request.session['empid']=ed
            for i in b:
                if ed == i.empid and ps == i.password:
                    request.session['id']=i.id
                    return redirect(empprofile)
            else:
                messages.success(request, "inorrect employeeid or password")
        else:
            messages.success(request, "login failed")
    return render(request,"employeelogin.html")

def empprofile(request):
    ed=request.session['empid']
    return render(request,"employeeprofile.html",{'ed':ed})

def attend(request):
    a = employeeaddmodel.objects.all().order_by('id')
    paginator = Paginator(a, 10)
    page_number = request.GET.get('page')
    a = paginator.get_page(page_number)
    efnm = []
    elnm = []
    emid = []
    emig = []
    dep = []
    empid = []
    for i in a:
        id = i.id
        empid.append(id)
        ef = i.empfname
        efnm.append(ef)
        el = i.emplname
        elnm.append(el)
        eid = i.empid
        emid.append(eid)
        eig = i.empimg
        emig.append(str(eig).split('/')[-1])
        dp = i.department
        dep.append(dp)
    mylist = zip(efnm, elnm, emid, emig, dep, empid)
    return render(request,'attend.html',{'mylist':mylist,'a':a})


def addattendence(request,id):
    a=employeeaddmodel.objects.get(id=id)
    if attendencemodel.objects.filter(empid=a.empid):
        messages.success(request,"Already added.....")
        return redirect(attendencedetails)
    else:
        if request.method == 'POST':
            totaldays = request.POST.get('totaldays')
            presentdays = request.POST.get('presentdays')
            b = attendencemodel(employeeid=id,empfname=a.empfname,emplname=a.emplname,department=a.department,empid=a.empid,empimg=a.empimg,totaldays=totaldays, presentdays=presentdays)
            b.save()
            messages.success(request, "Attendence added.....")
            return redirect(attendencedetails)
        return render(request, "addattend.html")

def empattenddetail(request):
    epid=request.session['id']
    a=attendencemodel.objects.all()
    efnm = []
    elnm = []
    emid = []
    dep = []
    ttds = []
    ptds = []
    eip = []
    emig = []
    employeeid=[]
    for i in a:
        id = i.id
        eip.append(id)
        ef = i.empfname
        efnm.append(ef)
        el = i.emplname
        elnm.append(el)
        eid = i.empid
        emid.append(eid)
        dp = i.department
        dep.append(dp)
        eig = i.empimg
        emig.append(str(eig).split('/')[-1])
        tt = i.totaldays
        ttds.append(tt)
        pd = i.presentdays
        ptds.append(pd)
        ei = i.employeeid
        employeeid.append(ei)
    mylist = zip(efnm, elnm, emid, dep, ttds, ptds, emig, eip,employeeid)
    return render(request,"empattenddetails.html",{'mylist':mylist,'epid':epid})

def attendencedetails(request):
    a=attendencemodel.objects.all()
    efnm=[]
    elnm=[]
    emid=[]
    dep=[]
    ttds=[]
    ptds=[]
    ei=[]
    emig=[]
    for i in a:
        id=i.id
        ei.append(id)
        ef=i.empfname
        efnm.append(ef)
        el=i.emplname
        elnm.append(el)
        eid=i.empid
        emid.append(eid)
        dp=i.department
        dep.append(dp)
        eig = i.empimg
        emig.append(str(eig).split('/')[-1])
        tt = i.totaldays
        ttds.append(tt)
        pd = i.presentdays
        ptds.append(pd)
    mylist=zip(efnm,elnm,emid,dep,ttds,ptds,emig,ei)
    return render(request,'attendancedetails.html',{'mylist':mylist})

def attdelete(request,id):
    a=attendencemodel.objects.get(id=id)
    a.delete()
    messages.success(request, "attendence detail deleted...")
    return redirect(attendencedetails)


def leave(request):
    ed = request.session['empid']
    if request.method=='POST':
        fromdate =request.POST.get('fromdate')
        todate= request.POST.get('todate')
        subject=request.POST.get('subject')
        message=request.POST.get('message')
        if empleave.objects.filter(empid=ed, fromdate=fromdate, todate=todate):
            messages.success(request, "already applied")
            return redirect(leave)
        else:
            c = empleave.objects.filter(empid=ed)
            for i in c:
                x = str(i.fromdate)
                y = str(fromdate)
                xx = str(i.todate)
                yy = str(todate)
                oldfd = time.strptime(x, '%Y-%m-%d')
                newfd = time.strptime(y, '%Y-%m-%d')
                oldtd = time.strptime(xx, '%Y-%m-%d')
                newtd = time.strptime(yy, '%Y-%m-%d')
                today=str(datetime.date.today())
                todaydate=time.strptime(today,'%Y-%m-%d')
                if newfd < todaydate :
                    messages.success(request, "Invalid date!")
                    return redirect(leave)
                elif newfd > newtd or newtd <newfd:
                    messages.success(request, "Date dispatch")
                    return redirect(leave)
                elif newfd == newtd:
                    messages.success(request, "Both dates are same")
                    return redirect(leave)
                elif oldfd <= newfd <= oldtd :
                    messages.success(request, "already applied")
                    return redirect(leave)
            b = empleave(empid=ed, fromdate=fromdate, todate=todate, subject=subject, message=message)
            b.save()
            messages.success(request, "Leave applied wait for admin response")
            return redirect(empleavestatus)
    return render(request,"leave.html")


def empleavestatus(request):
    ed = request.session['empid']
    a = empleave.objects.all()
    frdt = []
    todt = []
    sbt=[]
    msg=[]
    stus=[]
    empid=[]
    lv=[]
    for i in a:
        id=i.id
        lv.append(id)
        fd=i.fromdate
        frdt.append(fd)
        td=i.todate
        todt.append(td)
        sb=i.subject
        sbt.append(sb)
        mg=i.message
        msg.append(mg)
        st=i.response
        stus.append(st)
        eid=i.empid
        empid.append(eid)
    mylist = zip(frdt,todt,sbt,msg,stus,lv,empid)
    return render(request,"empleavestatus.html",{'mylist':mylist,'ed':ed})

def leavedelete(request,id):
    a=empleave.objects.get(id=id)
    a.delete()
    messages.success(request, "leave deleted...")
    return redirect(empleavestatus)

def leavestatus(request):
    a = empleave.objects.all()
    frdt = []
    todt = []
    sbt = []
    msg = []
    stus = []
    empid=[]
    ein=[]
    for i in a:
        id = i.id
        ein.append(id)
        fd = i.fromdate
        frdt.append(fd)
        td = i.todate
        todt.append(td)
        sb = i.subject
        sbt.append(sb)
        mg = i.message
        msg.append(mg)
        eid = i.empid
        empid.append(eid)
        st = i.response
        stus.append(st)
    mylist = zip(frdt, todt, sbt, msg, stus,empid,ein)
    return render(request,"leavestatus.html",{'mylist':mylist})


def updateleave(request,id):
    a=empleave.objects.get(id=id)
    if request.method=='POST':
        a.response=request.POST.get('response')
        a.empid=request.POST.get('empid')
        a.save()
        messages.success(request, "leave updated...")
        return redirect(leavestatus)
    return render(request,"updateleave.html",{'a':a})


def adminlogout(request):
    return render(request, "index.html")

def emplogout(request):
    logout(request)
    return render(request, "index.html")

def payroll(request,id):
    a = employeeaddmodel.objects.get(id=id)
    if request.method == 'POST':
        month=request.POST.get('month')
        basicsalary=request.POST.get('basicsalary')
        allowance=request.POST.get('allowance')
        b=payrollmodel(employeeid=id,department=a.department,empid=a.empid,month=month,basicsalary=basicsalary,allowance=allowance)
        if payrollmodel.objects.filter(empid=a.empid,month=b.month):
            messages.success(request, "already added...")
            return redirect(payrolldetail)
        b.save()
        messages.success(request, "payroll added...")
        return redirect(payrolldetail)
    return render(request,"payroll.html",{'a':a})

def addpayroll(request):
    a = employeeaddmodel.objects.all().order_by('id')
    paginator = Paginator(a, 10)
    page_number = request.GET.get('page')
    a = paginator.get_page(page_number)
    efnm = []
    elnm = []
    emig=[]
    emid=[]
    dep=[]
    empid=[]
    for i in a:
        id = i.id
        empid.append(id)
        ef = i.empfname
        efnm.append(ef)
        el = i.emplname
        elnm.append(el)
        eid = i.empid
        emid.append(eid)
        dp = i.department
        dep.append(dp)
        eig = i.empimg
        emig.append(str(eig).split('/')[-1])
    mylist = zip(efnm,elnm,emid,dep,emig,empid)
    return render(request,"addpayroll.html",{'mylist':mylist,'a':a})

def payrolldetail(request):
    a = payrollmodel.objects.all()
    emid = []
    dep = []
    mnth = []
    bsly = []
    allw=[]
    fipy=[]
    eip=[]
    for i in a:
        id=i.id
        eip.append(id)
        eid = i.empid
        emid.append(eid)
        dp = i.department
        dep.append(dp)
        mt=i.month
        mnth.append(mt)
        bs=i.basicsalary
        bsly.append(bs)
        al=i.allowance
        allw.append(al)
        fp = bs + al
        fipy.append(fp)
    mylist = zip( emid,  dep, mnth, bsly, allw, fipy,eip)
    return render(request,"payrolldetail.html",{'mylist':mylist})

def payrolldelete(request,id):
    a=payrollmodel.objects.get(id=id)
    a.delete()
    messages.success(request, "payroll deleted...")
    return redirect(payrolldetail)

def notice(request):
    e = datetime.date.today()
    f = str(e)
    g = time.strptime(f, '%Y-%m-%d')
    if request.method == 'POST':
        date=request.POST.get('date')
        title=request.POST.get('title')
        description=request.POST.get('description')
        notes=request.POST.get('notes')
        k = str(date)
        dt = time.strptime(k, '%Y-%m-%d')
        if dt < g:
            messages.success(request, "Invalid date!")
            return redirect(notice)
        b=noticemodel(date=date,title=title,description=description,notes=notes)
        b.save()
        messages.success(request, "Notice added")
        return redirect(noticedetails)
    return render(request,"notice.html")


def noticedetails(request):
    a=noticemodel.objects.all()
    dat=[]
    titl=[]
    desc=[]
    note=[]
    ein=[]
    for i in a:
        id=i.id
        ein.append(id)
        dt=i.date
        dat.append(dt)
        ti=i.title
        titl.append(ti)
        ds=i.description
        desc.append(ds)
        nt=i.notes
        note.append(nt)
    mylist=zip(dat,titl,desc,note,ein)
    return render(request,"noticedetails.html",{'mylist':mylist})

def noticedelete(request,id):
    a=noticemodel.objects.get(id=id)
    a.delete()
    messages.success(request, "notice deleted...")
    return redirect(noticedetails)

def noticeempdetails(request):
    a=noticemodel.objects.all()
    dat=[]
    titl=[]
    desc=[]
    note=[]
    for i in a:
        dt=i.date
        dat.append(dt)
        ti=i.title
        titl.append(ti)
        ds=i.description
        desc.append(ds)
        nt=i.notes
        note.append(nt)
    mylist=zip(dat,titl,desc,note)
    return render(request,"empnotice.html",{'mylist':mylist})


def doc(request):
    a = employeeaddmodel.objects.all().order_by('id')
    paginator = Paginator(a, 10)
    page_number = request.GET.get('page')
    a = paginator.get_page(page_number)
    efnm = []
    elnm = []
    emid = []
    emig = []
    dep = []
    empid = []
    for i in a:
        id = i.id
        empid.append(id)
        ef = i.empfname
        efnm.append(ef)
        el = i.emplname
        elnm.append(el)
        eid = i.empid
        emid.append(eid)
        eig = i.empimg
        emig.append(str(eig).split('/')[-1])
        dp = i.department
        dep.append(dp)
    mylist = zip(efnm, elnm, emid, emig, dep, empid)
    return render(request,'doc.html',{'mylist':mylist,'a':a})

def documents(request,id):
    a = employeeaddmodel.objects.get(id=id)
    if documentmodel.objects.filter(empid=a.empid):
        messages.success(request,"already added......")
        return redirect(docdetails)
    else:
        if request.method == 'POST':
            appointorder=request.FILES['appointorder']
            joinorder=request.FILES['joinorder']
            appraisalorder=request.FILES['appraisalorder']
            b = documentmodel(employeeid=id,empfname=a.empfname, emplname=a.emplname, department=a.department, empid=a.empid,empimg=a.empimg,appointorder=appointorder,joinorder=joinorder,appraisalorder=appraisalorder)
            b.save()
            messages.success(request, "documents uploaded")
            return redirect(docdetails)
        return render(request,"adddocuments.html",{'a':a})

def docdetails(request):
    b = documentmodel.objects.all()
    empid = []
    apod = []
    jood = []
    assod = []
    eid = []
    dep=[]
    employeeid = []
    for i in b:
        ei = i.employeeid
        employeeid.append(ei)
        id = i.id
        eid.append(id)
        ed = i.empid
        empid.append(ed)
        de = i.department
        dep.append(de)
        ao = i.appointorder
        apod.append(str(ao).split('/')[-1])
        jo = i.joinorder
        jood.append(str(jo).split('/')[-1])
        ap = i.appraisalorder
        assod.append(str(ap).split('/')[-1])
    mylist = zip(empid, apod, jood, assod,dep, employeeid,eid)
    return render(request,"docdetails.html",{'mylist':mylist})

def docdelete(request,id):
    a=documentmodel.objects.get(id=id)
    a.delete()
    messages.success(request, "document deleted...")
    return redirect(docdetails)

def addshift(request):
    a = employeeaddmodel.objects.all().order_by('id')
    paginator = Paginator(a, 10)
    page_number = request.GET.get('page')
    a = paginator.get_page(page_number)
    emid = []
    emig = []
    dep = []
    empid = []
    for i in a:
        id = i.id
        empid.append(id)
        eid = i.empid
        emid.append(eid)
        eig = i.empimg
        emig.append(str(eig).split('/')[-1])
        dp = i.department
        dep.append(dp)
    mylist = zip( emid, emig, dep, empid)
    return render(request,"addshift.html",{'mylist':mylist,'a':a})


def shift(request,id):
    e = datetime.date.today()
    f = str(e)
    g = time.strptime(f, '%Y-%m-%d')
    a = employeeaddmodel.objects.get(id=id)
    if request.method == 'POST':
        shiftdate=request.POST.get('shiftdate')
        shifttime=request.POST.get('shifttime')
        k = str(shiftdate)
        sd = time.strptime(k, '%Y-%m-%d')
        if sd <= g:
            messages.success(request, "Invalid date!")
            return redirect(addshift)
        b = shiftmodel(employeeid=id,empid=a.empid,shiftdate=shiftdate,shifttime=shifttime)
        if shiftmodel.objects.filter(empid=a.empid,shiftdate=b.shiftdate):
            messages.success(request, "Already added...")
            return redirect(shiftdetails)
        b.save()
        messages.success(request, "Shift scheduled...")
        return redirect(shiftdetails)
    return render(request,'shiftadd.html',{'a':a})

def shiftdetails(request):
    a=shiftmodel.objects.all()
    emid=[]
    sfdy=[]
    sftm=[]
    eip=[]
    for i in a:
        id=i.id
        eip.append(id)
        ed=i.empid
        emid.append(ed)
        sd=i.shiftdate
        sfdy.append(sd)
        st=i.shifttime
        sftm.append(st)
    mylist=zip(emid,sfdy,sftm,eip)
    return render(request,"shiftdetails.html",{"mylist":mylist})

def shiftdelete(request,id):
    a=shiftmodel.objects.get(id=id)
    a.delete()
    messages.success(request, "shift deleted...")
    return redirect(shiftdetails)

def taskadd(request):
    a = employeeaddmodel.objects.all().order_by('id')
    paginator = Paginator(a, 10)
    page_number = request.GET.get('page')
    a = paginator.get_page(page_number)
    emid = []
    emig = []
    dep = []
    empid = []
    for i in a:
        id = i.id
        empid.append(id)
        eid = i.empid
        emid.append(eid)
        eig = i.empimg
        emig.append(str(eig).split('/')[-1])
        dp = i.department
        dep.append(dp)
    mylist = zip(emid, emig, dep, empid)
    return render(request,"taskadd.html",{'mylist':mylist,'a':a})


def taskfun(request,id):
    e = datetime.date.today()
    f = str(e)
    g = time.strptime(f, '%Y-%m-%d')
    a = employeeaddmodel.objects.get(id=id)
    if request.method == 'POST':
        task=request.POST.get("task")
        submitdate= request.POST.get("submitdate")
        k = str(submitdate)
        sd = time.strptime(k, '%Y-%m-%d')
        if sd < g :
            messages.success(request, "Invalid date!")
            return redirect(taskadd)
        b = taskmode(employeeid=id, empid=a.empid, task=task, submitdate=submitdate)
        if taskmode.objects.filter(empid=a.empid, submitdate=b.submitdate):
            messages.success(request, "Already assigned...")
            return redirect(taskdetails)
        b.save()
        messages.success(request, "Task assigned")
        return redirect(taskdetails)
    return render(request,"addtask.html",{'a':a})


def taskdetails(request):
    a = taskmode.objects.all()
    empid = []
    tsk=[]
    asdt=[]
    sbdt=[]
    stus=[]
    eid=[]
    for i in a:
        id = i.id
        eid.append(id)
        ed = i.empid
        empid.append(ed)
        tk=i.task
        tsk.append(tk)
        ad=i.assigndate
        asdt.append(ad)
        sd = i.submitdate
        sbdt.append(sd)
        st = i.status
        stus.append(st)
    mylist = zip(empid,tsk,asdt,sbdt,stus,eid)
    return render(request,"taskdetails.html",{'mylist':mylist})


def updatetask(request,id):
    a=taskmode.objects.get(id=id)
    if request.method == 'POST':
        a.task = request.POST.get('task')
        a.submitdate = request.POST.get('submitdate')
        a.status = request.POST.get('status')
        a.save()
        messages.success(request, "Task detail updated...")
        return redirect(taskdetails)
    return render(request,"updatetask.html",{'a':a})



def taskdelete(request,id):
    a=taskmode.objects.get(id=id)
    a.delete()
    messages.success(request, "task deleted...")
    return redirect(taskdetails)

def emptask(request):
    epid = request.session['id']
    b = taskmode.objects.all()
    empid = []
    tsk = []
    asdt = []
    sbdt=[]
    stus=[]
    eid = []
    employeeid=[]
    for i in b:
        ei = i.employeeid
        employeeid.append(ei)
        id = i.id
        eid.append(id)
        ed = i.empid
        empid.append(ed)
        tk = i.task
        tsk.append(tk)
        ad = i.assigndate
        asdt.append(ad)
        sd = i.submitdate
        sbdt.append(sd)
        st = i.status
        stus.append(st)
    mylist = zip(empid,tsk,asdt,sbdt,stus,eid,employeeid)
    return render(request,"emptaskdetails.html",{'mylist':mylist,'epid':epid})

def updateemptask(request,id):
    a=taskmode.objects.get(id=id)
    if request.method == 'POST':
        a.task = request.POST.get('task')
        a.submitdate = request.POST.get('submitdate')
        a.status = request.POST.get('status')
        a.save()
        messages.success(request, "status updated...")
        return redirect(emptask)
    return render(request,"empupdatetask.html",{'a':a})

def empshift(request):
    epid = request.session['id']
    b = shiftmodel.objects.all()
    sfdy = []
    sftm = []
    eid = []
    employeeid=[]
    for i in b:
        ei = i.employeeid
        employeeid.append(ei)
        id = i.id
        eid.append(id)
        sd = i.shiftdate
        sfdy.append(sd)
        st = i.shifttime
        sftm.append(st)
    mylist = zip(sfdy,sftm,eid,employeeid)
    return render(request,"empshiftdetails.html",{'mylist':mylist,'epid':epid})

def empdoc(request):
    epid = request.session['id']
    b = documentmodel.objects.all()
    empid = []
    apod = []
    jood = []
    assod=[]
    eid = []
    employeeid=[]
    for i in b:
        ei = i.employeeid
        employeeid.append(ei)
        id = i.id
        eid.append(id)
        ed = i.empid
        empid.append(ed)
        ao=i.appointorder
        apod.append(str(ao).split('/')[-1])
        jo=i.joinorder
        jood.append(str(jo).split('/')[-1])
        ap=i.appraisalorder
        assod.append(str(ap).split('/')[-1])
    mylist = zip(empid,apod,jood,assod,employeeid)
    return render(request,"empdocdetail.html",{'mylist':mylist,'epid':epid})

def emppayroll(request):
    epid = request.session['id']
    a = payrollmodel.objects.all().order_by('month')
    mnth = []
    bsly = []
    allw=[]
    fipy=[]
    employeeid=[]
    for i in a:
        ei = i.employeeid
        employeeid.append(ei)
        mt=i.month
        mnth.append(mt)
        bs=i.basicsalary
        bsly.append(bs)
        al=i.allowance
        allw.append(al)
        fp = bs + al
        fipy.append(fp)
    mylist = zip( mnth, bsly, allw, fipy,employeeid)
    return render(request,"emppayroll.html",{'mylist':mylist,'epid':epid})


def empdata(request):
    epid = request.session['id']
    a = employeeaddmodel.objects.all()
    efnm = []
    elnm = []
    phnm = []
    eml = []
    emid = []
    dofb = []
    emig = []
    dep = []
    gnd = []
    dfjg = []
    stus = []
    empid = []
    for i in a:
        id = i.id
        empid.append(id)
        ef = i.empfname
        efnm.append(ef)
        el = i.emplname
        elnm.append(el)
        ph = i.phonenumber
        phnm.append(ph)
        em = i.email
        eml.append(em)
        eid = i.empid
        emid.append(eid)
        df = i.dob
        dofb.append(df)
        eig = i.empimg
        emig.append(str(eig).split('/')[-1])
        dp = i.department
        dep.append(dp)
        gn = i.gender
        gnd.append(gn)
        st = i.status
        stus.append(st)
        dj = i.dateofjoining
        dfjg.append(dj)
    mylist = zip(efnm, elnm, phnm, eml, emid, dofb, emig, dep, gnd, dfjg, stus, empid)
    return render(request,"empdata.html" ,{'mylist':mylist,'epid':epid})


def empbioadd(request):
    ed = request.session['empid']
    if request.method=='POST':
        name=request.POST.get("name")
        fathername=request.POST.get("fathername")
        dob = request.POST.get("dob")
        email = request.POST.get("email")
        mobile = request.POST.get("mobile")
        address = request.POST.get("address")
        education = request.POST.get("education")
        nationality = request.POST.get("nationality")
        if empbiodata.objects.filter(empid=ed):
            messages.success(request, "Already added bio data")
            return redirect(empbioadd)
        b=empbiodata(empid=ed,name=name,fathername=fathername,dob=dob,email=email,mobile=mobile,address=address,education=education,nationality=nationality)
        b.save()
        messages.success(request, "Bio data addedd")
        return redirect(empprofile)
    return render(request,"addbio.html")

def empbiodetails(request):
    a=empbiodata.objects.all()
    nme=[]
    ftnm=[]
    dob=[]
    eml=[]
    mbl=[]
    add=[]
    edu=[]
    nty=[]
    bid=[]
    empid=[]
    for i in a:
        id=i.id
        bid.append(id)
        nm=i.name
        nme.append(nm)
        ft=i.fathername
        ftnm.append(ft)
        db=i.dob
        dob.append(db)
        em=i.email
        eml.append(em)
        mb=i.mobile
        mbl.append(mb)
        ad=i.address
        add.append(ad)
        et=i.education
        edu.append(et)
        nt=i.nationality
        nty.append(nt)
        ed=i.empid
        empid.append(ed)
    mylist=zip(nme,ftnm,dob,eml,mbl,add,edu,nty,bid,empid)
    return render(request,"biodata.html",{'mylist':mylist})




