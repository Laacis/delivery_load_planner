from django import forms
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse

from .models import *

# Create your views here.

def index(request):
    return render(request, "load_planer/index.html")


@login_required
def gateway(request):
    try:
        is_driver = Profile.objects.get(username = request.user.id)
        return render(request,"load_planer/gateway.html", {"driver": is_driver})
    except:
        driver_form = DriverForm()
        return render(request,"load_planer/gateway.html", {"driver": "You are not verified as Driver/Planer.", "driver_form": driver_form})


def tour_planing(request):
    return render(request, "load_planer/tour_planing.html")

@login_required
def trucks(request):
    form = TruckForm()
    trucks = Truck.objects.all()
    if request.method == 'POST':
        # REMEMBER TO MAKE SURE THE USER ADDING Truck is A PLANER, not a driver!!!
        truck_form = TruckForm(request.POST)
        if truck_form.is_valid():
            truck_id = truck_form.cleaned_data['truck_id']
            pallet_size = truck_form.cleaned_data['pallet_size']
            zones = truck_form.cleaned_data['zones']
            try:
                add_truck = Truck(truck_id=truck_id, pallet_size=pallet_size, zones=zones)
                add_truck.save()
                return render(request, 'load_planer/trucks.html', {"truck_form": form, "trucks": trucks})
            except: 
                return HttpResponse("Error: Unable to save this truck!")
        
        else:
            return HttpResponse("Error: Form not valid!")

    else:
        
        return render(request, 'load_planer/trucks.html', {"truck_form": form, "trucks": trucks})


def drivers(request):
    driver_list = Driver.objects.all()
    return render(request, 'load_planer/drivers.html', {"driver_list":driver_list})

@login_required
def reg_driver(request):
    if request.method != 'POST':
        return HttpResponse("Error: Forbidden method!")
    else:
        form = DriverForm(request.POST)
        if form.is_valid():
            username = User.objects.get(pk=request.user.id)
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            driver_id = form.cleaned_data["driver_id"]
            try:
                driver = Driver(
                    username=username,
                    first_name=first_name,
                    last_name=last_name,
                    driver_id=driver_id
                    )
                driver.save()
                return render(request, 'load_planer/gateway.html')
            except:
                return HttpResponse("Error: form is not valid!")
        return 0


def delivery_plans(request):
    return render(request, 'load_planer/delivery_plans.html')


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("gateway"))
        else:
            return render(request, "load_planer/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "load_planer/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "load_planer/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "load_planer/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("gateway"))
    else:
        return render(request, "load_planer/register.html")


# FORMS

class TruckForm(forms.ModelForm):
    zones = forms.TypedChoiceField(choices=[(2, 2), (3, 3)], coerce=int)
    pallet_size = forms.TypedChoiceField(choices=[(20, 20), (33, 33)], coerce=int)

    class Meta:
        model = Truck
        fields = ["truck_id", "pallet_size", "zones"]
        truck_id = forms.CharField(label="Truck ID", required=True, )
        widgets = {
            'truck_id' : forms.Textarea(attrs={'placeholder':'Truck ID: AA000', 'rows':1, 'class':"form-control"}),
        }

    
class DriverForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ["first_name", "last_name", "driver_id"]
        first_name = forms.CharField()
        last_name = forms.CharField()
        driver_id = forms.CharField()