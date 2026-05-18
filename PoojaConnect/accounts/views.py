from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from users.models import UserProfile
from pandits.models import PanditProfile

# Create your views here.


def user_login(request):
    if (request.method == "POST"):
        username = request.POST["username"]
        password = request.POST["password"]
        print(username)
        print(password)

        user = authenticate(request,username=username,password = password)

        if (user):
            if UserProfile.objects.filter(user=user).exists():
                login(request, user)
                return redirect('user_dashboard')
            else:
                messages.error(request, "Not a user account")
        else:
            messages.error(request,"Invalid credentials")
    return render(request, 'accounts/user_login.html')



    


def pandit_login(request):

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        print(username)
        print(password)

        user = authenticate(request, username=username, password=password)

        if user:
            if PanditProfile.objects.filter(user=user).exists():
                login(request, user)
                return redirect("pandit_dashboard")
            else:
                messages.error(request, "Not a pandit account")
                return render(request, 'accounts/pandit_login.html')

        else:
            messages.error(request, "Invalid credentials")
            return render(request, 'accounts/pandit_login.html')

    return render(request, 'accounts/pandit_login.html')




def user_logout_view(request):
    logout(request)
    return redirect('user_login')


def pandit_logout_view(request):
    logout(request)
    return redirect('pandit_login')


