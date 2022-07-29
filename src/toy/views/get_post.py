from django.shortcuts import render
from django.views import View
from toy.models import Person
from django.http import HttpResponseRedirect,  HttpResponseNotFound

from django.urls import reverse

from toy.models.models import EyeColor

class ListPerson(View):
    def get(self, request):
        
        itens = {'lista_pessoas':Person.objects.all() ,
        "mensagem_bonitinha":"Oi esta é a mensagem bonitinha"}
         
        return render(request,"list_person.html",itens)
    def post(self, request):
        
        if "name" in request.POST:
            name = request.POST["name"]
            birth_date = request.POST["birth_date"]

            #inserção
            Person.objects.create(name=name,birth_date=birth_date)
        return HttpResponseRedirect(reverse("home") )

class PersonUpdate(View):
    def get(self,request, person_id):
        try:
            person = Person.objects.get(id=person_id)
        except Person.DoesNotExist:
            return HttpResponseNotFound()

        return render(request,"person_update.html",{"person":person})
    
    def post(self, request, redirect_to):
        #get the person by id
        try:
            person = Person.objects.get(id=request.POST["person_id"])
        except Person.DoesNotExist:
            return HttpResponseNotFound()

        #save data
        if "name" in request.POST:
            person.name = request.POST["name"]
            person.birth_date = request.POST["birth_date"]
            person.save()

        #redirect to the requested page 
        params = {}
        if redirect_to != "home":
            params = {"person_id":person.id}
        return HttpResponseRedirect(reverse(redirect_to, kwargs=params) )

class EyeColorUpdate(View):
    def get(self,request, person_id):
        try:
            person = Person.objects.get(id=person_id)
        except Person.DoesNotExist:
            return HttpResponseNotFound()
        
        template_data = {"person":person,
                        "eye_colors":EyeColor.objects.all()}
        return render(request,"person_eye_update.html",template_data)

    def post(self, request, redirect_to):
        #get the person by id
        try:
            person = Person.objects.get(id=request.POST["person_id"])
        except Person.DoesNotExist:
            return HttpResponseNotFound()
        
        #update data
        if "eye_color" in request.POST and request.POST["eye_color"]:
            person.eye_color = EyeColor.objects.get(id=int(request.POST["eye_color"])) 
            person.save()

        #redirect to the requested page 
        params = {}
        if redirect_to != "home":
            params = {"person_id":person.id}
        return HttpResponseRedirect(reverse(redirect_to, kwargs=params) )