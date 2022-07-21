Antes de ler essa parte, sugerimos, assistir a [video-aula de DJango Models](https://www.youtube.com/watch?v=--1KwDBqhN8&list=PLwIaU1DGYV6skjkahOKtpgs9bPXlrVrIp&index=11) (mesmo se já assistiu) os [slides estão aqui](https://daniel-hasan.github.io/cefet-web-grad/classes/python3). Assim, você poderá entender melhor cada ponto mencionado aqui aqui. Vamos apresentar aqui o código implementado neste repositório como exemplo.

Este exemplo simples possui a classe Pessoa no arquivo  `[person.py](../src/models/person.py)`, junto com suas funcionalidades na classe `PersonManager` e, além disso, a classe EyeColor, no arquivo [`models.py`]((../src/models/models.py)) para definir o olho da pessoa. Como o olho da pessoa é uma quantidade já sabida e inserida pelo sistema (e não pelo usuário) chamamos ela de tabela do sistema. No presente guia, vamos explicar as decisões que tomamos para implementar essas duas classes. 

Vamos colocar aqui as duas classes para que seja mais fácil consultá-las.



# Uso do Manager

Em uma classe, para realizar busca sempre utilizamos o [atributo estático](https://daniel-hasan.github.io/cefet-web-grad/classes/python2/#25) `objects`. Por exemplo, `Pessoa.objects.all()` obtem todas as pessoas. Vamos supor que precisamos de  contabilizar a quantidade de pessoas por cor do olho. A consulta a ser feita nesse caso seria: 

```python
Pessoa.objects.values("name").annotate(Sum("eye_color__name"))
```

Vamos supor que em vários locais do seu código você precisa realizar essa mesma consulta. Dessa forma, o ideal seria fazer um método para ele. No Django, o melhor seria utilizarmos, por exemplo `Pessoa.objects.count_person_per_eye_color()`. Para fazemos isso, primeiramente, criamos uma classe subclasse de Manager com o método  count_Person_per_eye_color: 

```
class PersonManager(models.Manager):
    def count_person_per_eye_color(self):
        self.values("name").annotate(Sum("eye_color__name"))
```

Usamos o `self` pois estamos na classe que faz esse tipo de consulta para a classe `Person`. Para que isso seja possível, você deve armazená-la sobrepondo o atributo `objects` com o novo `PersonManager`: 

```
class Person(models.Model):
    ...
    objects = PersonManager()
```

Dessa forma, é possível executar o comando `Person.objects.count_person_per_eye_color()`.


# Organização dos models

Um projeto Django, geralmente, criamos um arquivo `models.py` e colocamos todas as classes do modelo nesse arquivo. Assim, usualmente, o `models.py`, `views.py` e `tests.py` do projeto estaria organizado da seguinte forma:

```
src
├── toy
|    ├── __init__.py
|    ├── models.py
|    ├── views.py
|    ├── tests.py
├── toy_example
├── db.sqlite3
├── manage.py
```

O problema disso é quando seu `models.py` possui muitas classes e além disso, muito da lógica e funcionalidades do seu sistema (conforme a apresentada na seção anterior). Assim, uma boa prática é subdividir esse arquivo. 

Uma prática que iremos fazer em nosso projeto é, sempre que há uma classe que possui mais lógica além dos atributos e relacionamentos, iremos retirá-la do arquivo `models.py` e colocarmos em um arquivo separado - igual colocamos a classe  `Person`.

Uma questão interessante: vamos supor que `Person` estivesse no arquivo `models.py` e estiver sendo usado por vários outros métodos, em outros arquivos. Ou seja, nesses outros arquivos haveria o `from toy.models import Person`. Vamos supor que essa classe precisou de um  `Manager` e decidimos retirá-la do `models.py` e colocá-la no arquivo `person.py`. Se fizemos isso sem o devido cuidado, vários arquivos vão ter erro na linha `from toy.models import Person`. O lindo do Python é que há uma forma de fazer isso e a linha `from toy.models import Person` continue funcionando. 

Para isso, você deve criar um pacote models (ou seja, uma pasta com o arquivo `__init__.py`) dentro do seu app (no nosso caso, o toy) e armazenar o `models.py` e o `person.py` lá. A estrutura de diretório ficaria assim: 

```
src
├── toy
|    ├── __init__.py
|    ├── models
|    |    ├── __init__.py
|    |    ├── models.py
|    |    ├── person.py
|    ├── views.py
|    ├── tests.py
├── toy_example
├── db.sqlite3
├── manage.py
```

LOgo após, para a linha `from toy.models import Person` funcionar, iremos no arquivo `__init__.py` da pasta `models` e fazemos os import apropriados: 

```
from toy.models.models import *
from toy.models.Person import * 
```
Assim a mágica acontece, você pode chamar `from toy.models import Person` que o Python irá entender e fazer a importação corretamente. Isso é uma ótima solução sempre que houver algum arquivo Python muito grande e desejamos dividí-lo em diferentes arquivos.

# Uso do migration

Temos que sempre lembrar que, ao alterar algo nas classes de modelo, essas alterações devem ser realizadas no banco de dados. Os arquivos migrations são usados para isso. Na primeira vez que você criar o modelo, você usará o `python manage.py makemigrations` e ele criará o seguinte arquivo em `toy/migrations`: 

```
class Migration(migrations.Migration):
    initial = True
    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EyeColor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color_name', models.CharField(choices=[('amber', 'Amber'), 
                                                        ( 'hazel', 'Hazel'), 
                                                        ('blue', 'Blue'), 
                                                        ('green', 'Green'), 
                                                        ('brown', 'Brown'), 
                                                        ('dark-brown', 'Dark Brown')], 
                                                max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('age', models.IntegerField()),
                ('eye_color', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='toy.eyecolor')),
            ],
        ),
    ]
```


Esse arquivo é um script para criar as tabelas no banco de dados e ao usar `python manage.py migrate` as alterações ainda não realizadas no banco de dados são aplicadas. Logo após, se desejar alterar algo, por exemplo, nessa classe `Person`, há um atributo idade (age). Não é muito recomendável ter um atributo idade, pois, ele na verdae é calculado pela data de nascimento da pessoa. Tendo um atributo idade, a pessoa envelhece mas não no banco de dados. 
Dessa forma, vamos troca-lo para um atributo de data de narcimento `birth_date`. Assim, sempre saberemos a idade do usuário. Assim, após remover o atributo `age` da classe `Person` e adicionar o atributo `birth_date`,  executamos o `makemigrations` novamente para criar o arquivo com a alteração. Ao executar o `makemigrations` ele irá solicitar que você forneça uma data inicial para essa coluna. Pois, como adicionamos um campo não nulo, as linhas que já existiam no banco de dados devem ter um valor padrão para essa coluna. Foi colocado a data de hoje `datetime.date.today()` para facilitar. O resultado do migration será o seguinte: 
```python
class Migration(migrations.Migration):

    dependencies = [
        ('toy', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='age',
        ),
        migrations.AddField(
            model_name='person',
            name='birth_date',
            field=models.DateField(default=datetime.date.today()),
            preserve_default=False,
        ),
    ]

```



Dessa forma, é possivel fazer alterações no banco mesmo quando as tabelas já foram criadas. Sempre que obter alterações em desenvolvimento, é importante verificar se tais alterações não adicionaram colunas/linhas novas. Caso seja o caso, você deve executar o `migrate` para atualizar seu modelo. 


Outra dica importante. Vamos supor que o branch de desenvolvimento criou o arquivo `0001_initial` e você está no seu branch e fez 3 alterações no seu modelo em instantes diferentes, gerando 3 arquivos `0002_alteração2`, `0003_alteração3` e `0004_alteração4`. Antes de mudar para o desenvolvimento, para evitar muitos arquivos desencessários: 

- Exclua os três arquivos de migration criados no seu branch
- Exclua o seu banco de dados - pois, ele está com as tabelas novas
- Faça um `python manage.py migrate` para criar o banco apenas com o `0001_initial` 
- Faça `python manage.py makemigrations` para criar mais um arquivo com todas as alterações dos três arquivos. 

Caso haja algum arquivo de dados iniciais (falaremos na proxima seção) ele não deverá ser excluído - mova para um lugar e, após fazer a todo o processo, adicione-o com dependencia do último arquivo. 

Algumas vezes temos problemas com o banco de dados e temos que executar esse procedimento. 


# Criação dos dados iniciais

Existem tabelas que precisam de dados iniciais, por exemplo, tabelas de sistemas. Existem duas formas de adicionar os dados iniciais. Podemos criar um código no [migration](https://docs.djangoproject.com/en/4.0/topics/migrations/#data-migrations) para isso, por exemplo, para adicionarmos todas as cores dos olhos, podemos fazer o seguinte ,igration: 

```python
from django.db import migrations

def add_eyes(apps, schema_editor):
    # Não é possivel importar a classe Pssoa diretamente já que a versão atual
    # pode ser mais nova que o migration necessitaria. 
    EyeColor = apps.get_model('toy', 'EyeColor')
    for eye_color, eye_color_human_read in EyeColor.color_name.field.choices:
        EyeColor.objects.create(color_name=eye_color)


class Migration(migrations.Migration):

    dependencies = [
        #ele deve ser executado após o 0001_initial
        ('toy', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_eyes),
    ]
```



# Uso do Jupyter 

Existem vários usos do notebook no Django, alguns exemplos:

- **Testes:**: Você pode usar o Jupyter para testar e "brincar" com o modelo. Isso é muito útil para implementar um código mais complexo ou uma consulta no banco de dados. Existe um exemplo disso em [`/notebooks/bd_models/Person PlayGround.ipynb`](../notebooks/bd_models/Person PlayGround.ipynb). Todo o notebook para teste, colocamos o sufixo `Playground` nele. 
- **Guias:** Você pode fazer guias e explicações/documentações de algo mais complexo. Criamos a pasta `guides` para isso
- **Relatórios e análises:** Ainda podemos fazer relatorios e analises usando também a biblioteca [Pandas](https://pandas.pydata.org/) e o [Seaborn](https://seaborn.pydata.org/), por exemplo.
