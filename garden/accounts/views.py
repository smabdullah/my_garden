from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.urls import reverse_lazy
from django.views import generic
from django.contrib import auth, messages
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout


class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                request.session['user_login'] = True
                messages.info(request, f"You are now logged in as {username}")
                return render(
                    request = request,
                    template_name= 'index.html',
                    context= {'user_login': True}
                )
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request = request,
                    template_name = "registration/login.html",
                    context={"form":form})

def logout_request(request):
    logout(request)
    try:
        del request.session['user_login']
    except KeyError:
        pass
    return render(
                    request = request,
                    template_name= 'index.html',
                    context= {'user_login': False}
                )