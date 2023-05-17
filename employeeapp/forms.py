from django import forms

class employeeaddform(forms.Form):
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
    empfname=forms.CharField(max_length=50)
    emplname=forms.CharField(max_length=50)
    email=forms.EmailField()
    phonenumber = forms.CharField(max_length=10)
    dob=forms.CharField(max_length=20)
    empid=forms.CharField(max_length=10)
    password = forms.CharField(max_length=50)
    gender = forms.CharField(label='Gender',widget=forms.RadioSelect(choices=Gender))
    department=forms.CharField(label='Department',widget=forms.RadioSelect(choices=Department))
    empimg=forms.FileField()

class emplogform(forms.Form):
    empid=forms.CharField(max_length=10)
    password=forms.CharField(max_length=50)













