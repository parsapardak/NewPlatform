from django.http import HttpResponse

def homepage(request):
    return HttpResponse("<h1>Welcome to the News Platform</h1>")
