from django.shortcuts import render


def index(request):
    print(request.user.username)
    # print(request.user.email)
    return render(request, 'index.html')