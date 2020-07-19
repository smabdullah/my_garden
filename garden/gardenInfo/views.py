from django.shortcuts import render

def home(request):
    if 'user_login' in request.session:
        data = True
    else:
        data = False

    return render(
        request = request,
        template_name = 'index.html',
        context = {'user_login': data}
        )
