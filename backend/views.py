from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.core import serializers
from django.http import HttpResponse

from .forms import *
from .models import JsonFile

# Create your views here.


def loginView(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            return HttpResponseRedirect('/')

    return render(request, 'loginFrom.html')


def logoutView(request):
    logout(request)
    return HttpResponseRedirect('/')

def whoView(request):
    if not request.user.is_anonymous:
        return HttpResponse(request.user, content_type="text/plain")
    return HttpResponse('W R R R R R', content_type="text/plain")

def registerView(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return HttpResponseRedirect("/")
    form = NewUserForm()
    return render(request=request, template_name="registerFrom.html", context={"register_form": form})


def allJsonView(request):
    user = request.user

    if not user.is_anonymous:
        jsons = JsonFile.objects.filter(user=user).order_by('-size')
        return JsonResponse({"jsons": [{"id": jsonid.id, "name": jsonid.__str__(), "size": jsonid.size} for jsonid in jsons]})
    else:
        return HttpResponse("Please log in", content_type="text/plain")


def jsonUploadView(request):
    if not request.user.is_anonymous:
        if request.method == 'POST':
            print(request)
            print(request.POST)
            print(request.FILES)
            for file in request.FILES.getlist('file'):
                JsonFile.objects.create(file=file, user=request.user)

            return HttpResponse("done", content_type="text/plain")
        else:
            form = UploadJsonForm()
            context = {
                "page_title": "xD",
                "form": form
            }
            return render(request, 'fileForm.html', context)
    else:
        return HttpResponseRedirect('/')


def jsonDataView(request, **kwargs):
    json = JsonFile.objects.get(id=kwargs['id'])
    persons = list(p for p in Person.objects.filter(conversation=json))

    data = {}
    for person in persons:
        data[person.name] = {}
        messages = list((str(message.date), message.to_dict())
                        for message in Messages.objects.filter(sender=person).order_by('date'))
        for date, d in messages:
            data[person.name][date] = d

    if json.user == request.user:
        return JsonResponse(data)
    else:
        return HttpResponse("Please log in", content_type="text/plain")
