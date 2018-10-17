from django.shortcuts import render
from .forms import SignUpForm
from django.contrib.auth import login as auth_login
from django.shortcuts import redirect


def signup(request):

    if request.method=='POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('boards:home')
    else:
            form = SignUpForm()
    return render(request, "boards/signup.html", {'form': form})








