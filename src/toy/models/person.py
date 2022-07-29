import datetime
from django.db import models
import csv
from .models import EyeColor
from datetime import datetime
from dateutil.relativedelta import relativedelta

#non-normalized lattes structure storage and writting into the normalized tables
class PersonManager(models.Manager):
    #this class can be used to create elements and creating custumized queries
    def create_from_csv(self, csv_file:str):
        with open(csv_file, mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            
            #usamos o enumerate apenas pq precisamos saber o indice i para a exceção
            for i,row in enumerate(csv_reader):
                #como há valores predeterminados de cor de olho, caso tenha
                #algum erro, o get irá lançar uma exceção (como previsto)
                #deixaremos para outras classes tratarem a exceção - caso ocorra
                try:
                    eye_color = EyeColor.objects.get(color_name=row["eye_color"])
                except:
                    valores_validos = []
                    for cor in EyeColor.objects.all():
                        valores_validos.append(cor.color_name)
                    raise ValueError(f"A cor do olho {row['eye_color']} não existe (linha {i+1}). Valores validos: {valores_validos}")
                
                #here, "self" is the same as Person.objects - as self is the "objects" instance
                birth_date = datetime.strptime(row['birth_date'], '%d/%m/%Y')
                self.create(name=row["name"], birth_date=birth_date, eye_color=eye_color)




class Person(models.Model):
    name = models.CharField(max_length=200)
    eye_color = models.ForeignKey(EyeColor, on_delete=models.CASCADE)
    birth_date = models.DateField(null=True)

    #We can create our own methods when calling Person.objects by overriding "objects"
    objects = PersonManager()

    def getDate(self):
        return self.birth_date

    @property
    def age(self):
        return relativedelta(datetime.now(),self.birth_date).years
    #useful for printing tests
    def __str__(self) -> str:
        return f"Name: {self.name} birth: {self.birth_date}"

    def __repr__(self) -> str:
        return str(self)