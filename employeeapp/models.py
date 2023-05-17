
from django.db import models

# Create your models here.






class employeeaddmodel(models.Model):
    Department=(
        ('Administrative','Administrative'),
        ('Human Resource','Human Resource'),
        ('Operations','Operations'),
        ('Purchasing','Purchasing'),
        ('Sales','Sales'),
        ('Marketing','Marketing'),
        ('Accounting','Accounting'),
        ('Finance','Finance'),
        ('Information Technology','Information Technology')
    )
    Gender=(
        ('Female','Female'),
        ('Male','Male'),
    )
    Status=(
        ('Active','Active'),
        ('Inactive','Inactive')
    )
    empimg = models.FileField(upload_to='employeeapp/static')
    empfname=models.CharField(max_length=50)
    emplname=models.CharField(max_length=50)
    email=models.EmailField()
    phonenumber = models.CharField(max_length=10)
    department = models.CharField(choices=Department, max_length=50)
    gender = models.CharField(choices=Gender, max_length=50)
    dob=models.CharField(max_length=20)
    empid=models.CharField(max_length=10)
    dateofjoining=models.DateField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=Status, default='Active')
    password = models.CharField(max_length=50)

    def __str__(self):
        return (self.empfname) + (self.emplname)


class attendencemodel(models.Model):
    employeeid=models.IntegerField()
    empimg = models.ImageField()
    empfname = models.CharField(max_length=50)
    emplname = models.CharField(max_length=50)
    department = models.CharField(max_length=50)
    empid = models.CharField(max_length=10)
    totaldays = models.IntegerField()
    presentdays = models.IntegerField()

    def __str__(self):
        return (self.empfname) + (self.emplname)


class empleave(models.Model):
    Response=(
        ('Pending','Pending'),
        ('Approved','Approved'),
        ('Declined','Declined')
    )
    empid = models.CharField(max_length=10)
    fromdate=models.DateField()
    todate=models.DateField()
    subject=models.CharField(max_length=100)
    message=models.CharField(max_length=200)
    response = models.CharField(max_length=50, choices=Response, default='Pending')

    def __str__(self):
        return str(self.empid)


class payrollmodel(models.Model):
    Month=(('January','January'),
           ('February', 'February'),
           ('March', 'March'),
           ('April', 'April'),
           ('May', 'May'),
           ('June', 'June'),
           ('July', 'July'),
           ('August', 'August'),
           ('September', 'September'),
           ('October', 'October'),
           ('November', 'November'),
           ('December', 'December'),
           )
    employeeid = models.IntegerField()
    department = models.CharField(max_length=50)
    empid = models.CharField(max_length=10)
    basicsalary=models.IntegerField()
    allowance=models.IntegerField()
    month=models.CharField(max_length=50, choices=Month)

    def __str__(self):
        return (self.empid)

class noticemodel(models.Model):
    date=models.CharField(max_length=20)
    title=models.CharField(max_length=100)
    description=models.CharField(max_length=250)
    notes=models.CharField(max_length=250)


class documentmodel(models.Model):
    employeeid = models.IntegerField()
    empimg = models.ImageField()
    empfname = models.CharField(max_length=50)
    emplname = models.CharField(max_length=50)
    department = models.CharField(max_length=50)
    empid=models.CharField(max_length=10)
    appointorder=models.FileField(upload_to='employeeapp/static')
    joinorder=models.FileField(upload_to='employeeapp/static')
    appraisalorder=models.FileField(upload_to='employeeapp/static')

    def __str__(self):
        return (self.empfname) + (self.emplname)

class shiftmodel(models.Model):
    employeeid = models.IntegerField()
    empid = models.CharField(max_length=10)
    shiftdate=models.CharField(max_length=20)
    shifttime=models.CharField(max_length=10)

    def __str__(self):
        return str(self.empid)

class taskmode(models.Model):
    Response=(
        ('Pending','Pending'),
        ('Submitted','Submitted')
    )
    empid=models.CharField(max_length=10)
    task=models.CharField(max_length=250)
    assigndate=models.DateField(auto_now_add=True)
    submitdate=models.CharField(max_length=50)
    status=models.CharField(max_length=50, choices=Response, default='Pending')
    employeeid=models.IntegerField()

    def __str__(self):
        return str(self.empid)


class empbiodata(models.Model):
    empid = models.CharField(max_length=10)
    name=models.CharField(max_length=20)
    fathername=models.CharField(max_length=20)
    dob=models.CharField(max_length=20)
    email=models.EmailField()
    mobile=models.CharField(max_length=10)
    address=models.CharField(max_length=250)
    education=models.CharField(max_length=20)
    nationality=models.CharField(max_length=20)

    def __str__(self):
        return str(self.name)