from .forms import *
from django.shortcuts import render
from django.views import View
from toy.models import Person
from django.http import HttpResponseRedirect,  HttpResponseNotFound
from django.urls import reverse
from toy.models.models import EyeColor
from django.shortcuts import redirect
from django.shortcuts import render
from django.views import View
from toy.models import *
from django.http import HttpResponseRedirect,  HttpResponseNotFound

from django.urls import reverse

from toy.models.models import EyeColor

class ListPerson(View):
    def get(self, request):
        people = Person.objects.all()
        form = PersonForm()
        context = {"people":people, "form":form}
        return render(request,"list_person.html", context)
    def post(self, request):
        form = PersonForm(request.POST)

        if (form.is_valid()):
            name = form.cleaned_data["name"]
            birth_date = form.cleaned_data["birth_date"]

            #inserção
            #Person.objects.create(name=name,birth_date=birth_date)
            print(name)
            print(birth_date)
        return HttpResponseRedirect(reverse("home") )

class PersonUpdate(View):
    def get(self,request, person_id):
        try:
            person = Person.objects.get(id=person_id)
            form = PersonForm(instance=person)
            # = person.datefield
            print(person.getDate())    
        except Person.DoesNotExist:
            return HttpResponseNotFound()

        return render(request,"person_update.html",{"person":person, "form":form})
    
    def post(self, request, redirect_to):
        
        #get the person by id
        try:
            person_id = request.POST.get("person_id", False)
            person = Person.objects.get(id=person_id)
            form = PersonForm(request.POST, instance=person)
        except Person.DoesNotExist:
            return HttpResponseNotFound()

        #save data
        
        if form.is_valid():
            print(form.cleaned_data)
            person.name = form.cleaned_data.get("name")
            person.birth_date = form.cleaned_data["birth_date"]
            person.save()

        #redirect to the requested page 
        params = {}
        if redirect_to != "home":
            params = {"person_id":person.id}
        return HttpResponseRedirect(reverse(redirect_to, kwargs=params))

class EyeColorUpdate(View):
    def get(self,request, person_id):
        try:
            person = Person.objects.get(id=person_id)
            form = EyeForm(instance=person)
            print(person.eye_color.color_name)
            for i in range(6):
                if (person.eye_color.color_name == EyeColor.EYE_CHOICES[i][0]):
                    index = i
                    print(form)
                    break

        except Person.DoesNotExist:
            return HttpResponseNotFound()
        
        template_data = {"person":person, "eye_colors":EyeColor.objects.all(), "form":form}
        return render(request,"person_eye_update.html",template_data)

    def post(self, request, redirect_to):
        #get the person by id
        try:
            person = Person.objects.get(id=request.POST["person_id"])
            form = EyeForm(request.POST, instance=person)
        except Person.DoesNotExist:
            return HttpResponseNotFound()
        
        #update data
            
        #person.eye_color
        index = -1

        #if (form.is_valid()): não funciona pois o metodo is_valid() verifica se TODOS os campos estão preenchidos
        if ("colors" in request.POST and request.POST["colors"]):  
            for i in range(6):
                if (request.POST["colors"] == EyeColor.EYE_CHOICES[i][0]):
                    index = i
                    print(index+1)
                    break
        else:
            print(form.errors.as_data())

        person.eye_color = EyeColor.objects.get(id=index+1)
        person.save() 

        #redirect to the requested page 
        params = {}
        if redirect_to != "home":
            params = {"person_id":person.id}
        return HttpResponseRedirect(reverse(redirect_to, kwargs=params) )

#end of CRU