from django.shortcuts import render,redirect
from authapp.models import Contact
from django.contrib import messages
from startupapp.models import Courses,Register,Payments,Attendance

# Create your views here.
def index(request):
    return render(request, "index.html")

def contact(request):
    if request.method=="POST":
        name=request.POST.get('name')
        email=request.POST.get('email')
        phoneNo=request.POST.get('num')
        description=request.POST.get('desc')
        query=Contact(name=name,email=email,phoneNumber=phoneNo,description=description)
        query.save()
        messages.success(request,"Thanks for Contacting us we will get back you soon...")
        return render(request,"contact.html")
    return render(request, "contact.html")

def about(request):
    return render(request, "about.html")

def courses(request):
    courses=Courses.objects.all()
    context={"courses":courses}
    return render(request,"courses.html",context)

def course(request,id):
    course=Courses.objects.filter(courseName=id)
    context={"course":course}
    return render(request, "course.html", context)

def enroll(request):
    if not request.user.is_authenticated:
        messages.warning(request,"Please Login & Register with us")
        return redirect("/auth/login/")
    courses=Courses.objects.all()
    context={"courses":courses}
    if request.method=="POST":
        fname=request.POST.get('fname')
        lname=request.POST.get('lname')
        fatherName=request.POST.get('fatherName')
        phone=request.POST.get('phone')
        altNumber=request.POST.get('alternateNumber')
        email=request.POST.get('email')
        collage=request.POST.get('colname')
        addre=request.POST.get('address')
        landmark=request.POST.get('landmark')
        street=request.POST.get('street')
        pincode=request.POST.get('pincode')
        city=request.POST.get('city')
        companyName=request.POST.get('comname')
        Designation=request.POST.get('desi')
        Qualification=request.POST.get('qualification')
        cknowledge=request.POST.get('cknowledge')
        scourse=request.POST.get('scourse')
        ccourse=request.POST.get('ccourse')
        emailPresent=Register.objects.filter(email=email)
        if emailPresent:
            messages.error(request,"Email is ready Taken")
            return redirect('/enroll')
        if scourse==ccourse:
            pass
        else:
            messages.error(request,"Please select valid Course...")
            return redirect('/enroll/')
        query=Register(firstName=fname,lastName=lname,fatherName=fatherName,phoneNumber=phone,alternateNumber=altNumber,email=email,collageName=collage,address=addre,landmark=landmark,street=street,pincode=pincode,city=city,companyName=companyName,designation=Designation,qualification=Qualification,computerKnowledge=cknowledge,Courses=scourse)
        query.save()
        messages.success(request,"Enrollment Successfully")
        return redirect('/candidateprofile/')
    return render(request, "enroll.html", context)

def candidateprofile(request):
    if not request.user.is_authenticated:
        messages.warning(request,"Please Login & View Your Profile")
        return redirect("/auth/login/")
    currentuser=request.user.username
    print(currentuser)
    details=Register.objects.filter(email=currentuser)
    payment=Payments.objects.all()
    paymentstatus=""
    amount=0
    balance=0
    for j in payment:
        if str(j.name)==currentuser:
            paymentstatus=j.status
            amount=j.amountPaid
            balance=j.balance
    paymentstatus={"paymentstatus":paymentstatus,"amount":amount,"balance":balance}
    attendanceStatus=Attendance.objects.filter(email=currentuser)
    context={"details":details,"status":paymentstatus,"attendanceStatus":attendanceStatus}
    return render(request, "profile.html" ,context)

def update(request,id):
    data=Register.objects.filter(candidateId=id)
    courses=Courses.objects.all()
    context={"data":data,"courses":courses}
    if request.method=="POST":
        fname=request.POST.get('fname')
        lname=request.POST.get('lname')
        fatherName=request.POST.get('fatherName')
        phone=request.POST.get('phone')
        alternateNumber=request.POST.get('alternateNumber')
        collage=request.POST.get('collage')
        addre=request.POST.get('addre')
        landmark=request.POST.get('landmark')
        street=request.POST.get('street')
        pcode=request.POST.get('pcode')
        city=request.POST.get('city')
        companyName=request.POST.get('companyName')
        Designation=request.POST.get('Designation')
        Qualification=request.POST.get('Qualification')
        scourse=request.POST.get('scourse')

        edit=Register.objects.get(candidateId=id)
        eidt.fname=fname
        edit.lname=lname
        edit.fatherName=fatherName
        edit.phone=phone
        edit.alternateNumber=alternateNumber
        edit.collageName=collageName
        edit.addre=addre
        edit.landmark=landmark
        edit.street=street
        edit.pcode=pincode
        edit.city=city
        edit.companyName=companyName
        edit.Designation=designation
        edit.Qualification=Qualification
        edit.scourse=scourse
        edit.save()
        messages.info(request, 'Data Updated Successfully......')
        return redirect("/candidateprofile")

    return render(request, "candidateupdate.html",context)



def attendance(request):
    if not request.user.is_authenticated:
        messages.warning(request,"Please Login & Apply Attendance")
        return redirect("/login")
    if request.method=="POST":
        name=request.POST.get('name')
        email=request.POST.get('email')
        date=request.POST.get('date')
        logintime=request.POST.get('logintime')
        logouttime=request.POST.get('logouttime')
        query=Attendance(name=name,email=email,date=date,logintime=logintime,logouttime=logouttime)
        query.save()
        messages.success(request,"Applied Successfully wait for the Approval")
        return redirect("/candidateprofile")
    return render(request, "attendance.html")


def search(request):
    query=request.GET['search']
    if len(query)>100:
        allPosts=Courses.objects.none()
    else:
        allPosts=Courses.objects.filter(courseName=query)
    if allPosts.count()==0:
        messages.warning(request,"No Search Results")
    params={'allPosts':allPosts,'query':query}
    return render(request,"search.html", params)