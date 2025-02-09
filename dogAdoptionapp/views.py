from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Dog,CustomUser,AdoptionRequest
from django.urls import reverse


# Create your views here.
def index(request):
    return render(request,'index.html')


def logout_view(request):
    logout(request)
    return redirect('/')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('uname')
        password1 = request.POST.get('pwd')
        
        user = authenticate(request, username=username, password=password1)
        if user is not None:
            data = CustomUser.objects.get(username = username)
            login(request, user)
            if data.user_type == 'admin':
                return redirect('/adminn') 
            else:
                return redirect('/home') 
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, "login.html")

from django.http import HttpResponseForbidden

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

@login_required
def adminn(request):
    if request.user.username != "adminuser":  # Change to actual admin username
        return HttpResponse("""
            <html>
            <head>
                <title>Access Denied</title>
                <style>
                    body {
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        height: 100vh;
                        background-color: #f8d7da;
                        font-family: Arial, sans-serif;
                        text-align: center;
                    }
                    .error-container {
                        background: #ffffff;
                        padding: 30px;
                        border-radius: 10px;
                        box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
                    }
                    .error-title {
                        color: #721c24;
                        font-size: 24px;
                        font-weight: bold;
                    }
                </style>
            </head>
            <body>
                <div class="error-container">
                    <h2 class="error-title">Access Denied</h2>
                    <p>You are not authorized to view this page.</p>
                </div>
            </body>
            </html>
        """)

    unverified_dogs = Dog.objects.filter(verification=False)

    if request.method == 'POST':
        dog_id = request.POST.get('dog_id')
        dog = get_object_or_404(Dog, id=dog_id)
        dog.verification = True
        dog.save()
        return redirect('/adminn')

    return render(request, 'adminn.html', {'unverified_dogs': unverified_dogs})


def signup(request):
    if request.method == 'POST':
        uname1 = request.POST.get('uname')
        pwd1 = request.POST.get('pwd')
        repwd1 = request.POST.get('repwd')
        contact = request.POST.get('contact')  # phNo
        email = request.POST.get('email')
        
        if pwd1 != repwd1:
            messages.error(request, "Passwords do not match")
            return redirect('/signup')
        
        if CustomUser.objects.filter(username=uname1).exists():
            messages.error(request, 'Username is already taken')
            return redirect('/signup')
        
        if pwd1 and repwd1:
            # Create the CustomUser object with phone number (phNo)
            user = CustomUser.objects.create_user(username=uname1, password=pwd1, email=email, phNo=contact, user_type='user')
            user.save()
            
            messages.success(request, "Registration successful!")
            messages.success(request, "Login here.")
            return redirect('/login')
            
    return render(request, 'signup.html')

@login_required
def home(request):
    return render(request,'home.html')

@login_required
def rehome(request):
    if request.method=='POST':
        dog_name=request.POST.get('dog_name')
        age=request.POST.get('age')
        breed=request.POST.get('breed')
        gender=request.POST.get('gender')
        vaccinated = request.POST.get('vaccinated') == "Yes"
        training = request.POST.get('training') == "Yes"
        reason=request.POST.get('reason')
        dog_image=request.FILES.get('dog_images')
        Dog.objects.create(owner=request.user,dog_name=dog_name,age=age,breed=breed,gender=gender,vaccinated=vaccinated,training=training,reason=reason,dog_image=dog_image,verification=False)
    a = Dog.objects.filter(owner=request.user)
    return render(request,'rehome.html',{'data':a})

def edit(request, edit_id):
    a = get_object_or_404(Dog, id=edit_id)
    
    if request.method == 'POST':
        # a.owner_name=request.POST.get('owner_name')
        # a.contact=request.POST.get('contact')
        # a.email=request.POST.get('email')
        a.dog_name=request.POST.get('dog_name')
        a.age=request.POST.get('age')
        a.breed=request.POST.get('breed')
        a.gender=request.POST.get('gender')
        a.vaccinated = request.POST.get('vaccinated') == "Yes"
        a.training = request.POST.get('training') == "Yes"
        a.reason=request.POST.get('reason')
        
        if 'dog_image' in request.FILES:
            if a.dog_image:
                a.dog_image.delete(save=False)
            a.dog_image = request.FILES['dimg']
        
        a.save()
        return redirect(reverse("profile", kwargs={"id": a.id}))
    
    return render(request, 'edit.html', {'data': a})

@login_required
def delete(request, delete_id):
    del_obj = Dog.objects.get(id=delete_id)
    del_obj.dog_image.delete()
    del_obj.delete()
    
    return redirect('/rehome')

@login_required
def availabledogs(request):
    a = Dog.objects.filter(is_rehomed=False, verification=True).exclude(owner=request.user)
    return render(request, 'availabledogs.html', {'data': a})


@login_required
def moreDetails(request, id):
    dog = get_object_or_404(Dog, id=id)
    return render(request, 'moreDetails.html', {'dog': dog})

@login_required
def adopt_dog(request, id):
    dog = get_object_or_404(Dog, id=id)

    # Ensure the user is not the owner
    if request.user == dog.owner:
        messages.error(request, "You cannot adopt your own dog!")
        return redirect("moreDetails", id=id)  # redirect to moreDetails with the correct id

    # Check if the user has already requested adoption for this dog
    existing_request = AdoptionRequest.objects.filter(adopter=request.user, dog=dog).exists()
    if existing_request:
        messages.warning(request, "You have already requested to adopt this dog.")
        return redirect("moreDetails", id=id)  # redirect to moreDetails with the correct id

    # Create a new adoption request
    adoption_request = AdoptionRequest.objects.create(
        adopter=request.user,
        dog=dog,
        owner=dog.owner,
        status="Pending"
    )
    messages.success(request, "Your adoption request has been submitted successfully!")
    return redirect("moreDetails", id=id)  

@login_required
def dashboard(request):
    # Fetch requests where the logged-in user is the adopter (requests they made)
    my_adoption_requests = AdoptionRequest.objects.filter(adopter=request.user).select_related("dog")

    # Fetch requests where the logged-in user is the owner (requests they received)
    received_requests = AdoptionRequest.objects.filter(owner=request.user, status="Pending").select_related("adopter", "dog")

    return render(request, "dashboard.html", {
        "my_adoption_requests": my_adoption_requests,
        "received_requests": received_requests
    })




@login_required
def update_adoption_status(request, id):
    adoption_request = get_object_or_404(AdoptionRequest, id=id, owner=request.user)

    if request.method == "POST":
        status = request.POST.get("status")
        if status in ["Accepted", "Rejected"]:
            adoption_request.status = status
            adoption_request.save()

            # ✅ If accepted, mark the dog as rehomed
            if status == "Accepted":
                adoption_request.dog.is_rehomed = True
                adoption_request.dog.save()

    return redirect("/dashboard")

@login_required
def profile(request, id):
    data=CustomUser.objects.get(id=id)
    a = Dog.objects.filter(owner=request.user)
    return render(request, 'profile.html', {'data':data,'data1':a})


@login_required
def edit_profile(request):
    user = request.user  # Get logged-in user

    if request.method == "POST":
        user.username = request.POST.get("username")
        user.email = request.POST.get("email")
        user.phNo = request.POST.get("phNo")

        if "profile_pic" in request.FILES:
            user.profile_pic = request.FILES["profile_pic"]

        user.save()

        # ✅ Redirect to the profile page with the user's ID
        return redirect(reverse("profile", kwargs={"id": user.id}))

    return render(request, "edit_profile.html", {"user": user})