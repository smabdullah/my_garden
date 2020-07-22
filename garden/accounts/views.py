from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.urls import reverse_lazy
from django.views import generic
from django.contrib import auth, messages
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required


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
                if 'redirect_to' in request.session:
                    form = PasswordChangeForm(request.user)
                    return render(
                        request=request,
                        template_name= request.session['redirect_to'],
                        context={'form': form, 'user_login': True}
                    )

                else:
                    return render(
                        request=request,
                        template_name='index.html',
                        context={'user_login': True}
                    )
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request,
                  template_name="registration/login.html",
                  context={"form": form})


def logout_request(request):
    logout(request)
    try:
        del request.session['user_login']
        del request.session['redirect_to']
    except KeyError:
        pass
    return render(
        request=request,
        template_name='index.html',
        context={'user_login': False}
    )


def change_password(request):
    if 'user_login' in request.session:
        if request.method == 'POST':
            form = PasswordChangeForm(request.user, request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)  # Important!
                messages.success(request, 'Your password was successfully updated!')
                try:
                    del request.session['redirect_to']
                except KeyError:
                    pass
                return render(
                    request=request,
                    template_name='index.html',
                    context={'user_login': True}
                )
            else:
                messages.error(request, 'Please correct the error below.')
        else:
            form = PasswordChangeForm(request.user)
            return render(
                request=request, 
                template_name="change_password.html", 
                context={"form": form}
            )
    else:
        request.session['redirect_to'] = 'change_password.html'
        return login_request(request)
