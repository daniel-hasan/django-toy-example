from django.test import TestCase

from toy.models import *

class PersonManagerTest(TestCase):
    def setUp(self):
        #setup é sempre executado antes de cada teste para
        #inicializar o ambiente. Por exemplo, vc pode criar elemntos 
        #na tabela Person
        color_blue = EyeColor.objects.get(color_name=EyeColor.BLUE)
        color_brown = EyeColor.objects.get(color_name=EyeColor.BROWN)
        color_green = EyeColor.objects.get(color_name=EyeColor.GREEN)
        Person.objects.bulk_create(
            [Person(name="Alice",birth_date=datetime.strptime("14/12/1984", '%d/%m/%Y'), eye_color=color_blue),
            Person(name="Bob",birth_date=datetime.strptime("14/12/1994", '%d/%m/%Y'), eye_color=color_brown),
            Person(name="Carol",birth_date=datetime.strptime("01/04/2000", '%d/%m/%Y'), eye_color=color_green)]
        )
    #por padrão, um teste para ser executado automaticamente deve possuir o 
    #prefixo test
    def test_create_from_csv(self):

        
        Person.objects.create_from_csv("../data/tests/person.csv")

        lst_person = Person.objects.all()
        #verifica se fez o cadastro de apenas essas três pessoas
        #como em setup temos 3 pessoas no db e no csv temos mais 4 pessoas,
        #com esta insercao, teremos 8 pessoas
        self.assertEqual(len(lst_person), 7, "Foi inserida uma quantidade diferente do esperado de pessoas")

        #verifica se foi inserida as pessoas certas
        arr_expected = [ ("Elisa",datetime.strptime("12/02/2022", '%d/%m/%Y'),EyeColor.GREEN),
                         ("Fabio",datetime.strptime("11/01/1999", '%d/%m/%Y'),EyeColor.BLUE),
                        ("Gabriel",datetime.strptime("11/03/2000", '%d/%m/%Y'),EyeColor.GREEN),
                        ("Hugo",datetime.strptime("14/04/1984", '%d/%m/%Y'),EyeColor.BROWN) ]

        for expected in arr_expected:
            expected_name = expected[0]
            expected_birth = expected[1]
            expected_eye = expected[2]
            lst_response = Person.objects.filter(name = expected_name,
                                                birth_date = expected_birth,
                                                eye_color__color_name = expected_eye)
            self.assertEqual(len(lst_response), 1, f"Deveria haver apenas uma instancia de {expected_name} mas há {len(lst_response)}")
