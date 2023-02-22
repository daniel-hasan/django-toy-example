Antes de ler essa parte, sugerimos, assistir a video-aula e façam as práticas de: 

 - Django Models [[slides]](https://daniel-hasan.github.io/cefet-web-grad/classes/python4) [[video-aula]](https://www.youtube.com/watch?v=--1KwDBqhN8&list=PLwIaU1DGYV6skjkahOKtpgs9bPXlrVrIp&index=11)
 - Django Templates [[slides]](https://daniel-hasan.github.io/cefet-web-grad/classes/python4) [[video-aula]](https://www.youtube.com/watch?v=mVDPkyIs7nk&list=PLwIaU1DGYV6skjkahOKtpgs9bPXlrVrIp&index=24)


Iremos continuar com o exermplo da classe pessoa, agora fazendo as telas de visualização e edição das mesmas. Inicialmente, iremos apresentar a forma mais simples: tratando a requisição GET e POST e, logo após, mostraremos formas de simplificar e reduzir o código repetitivo. 



# GET vs POST

Na web, temos várias requisições que o navegador irá fazer para o servidor. Nelas, além da localização da página Web são enviados dados da sessão alguns dados da própria aplicação Web. As duas maneiras mais usuais para realizar isso são as requisições GET e POST. 

A requisição GET envia apenas a URL e, dentro dela, algum dado necessário. Por exemplo, a URL abaixo requisita a busca do termo `cenourinha` no Google: 

```
https://www.google.com/search?q=cenourinha
```

Essa URL pode ser criada via HTML por meio do seguinte formulário: 
```html
<form action="https://google.com/search">
    <input type="text" name="q">
    <input type="submit">
</form>
```
Em que o `name` define o nome da variável que possuirá o dado da consulta.  Ao clicar no botão de submit, você será redirecionado a página `google.com/search` e a variável `q` possuirá o valor que o usuario preencheu. 

A URL não é sempre a forma mais recomendável de requisitar dados: campos como senha devem ser enviados de forma criptografada e, além disso, a URL começa a ficar ilegivel e de dificil navegabilidade pelo usuário. Dessa forma, podemos enviar os dados de uma requisição via POST. Na requisição via POST os dados são enviados como um campo na própria requisição - não é visivel na URL. Além disso, pode ser criptografado. Vamos mostrar esse exemplo para adicionar elementos da nossa classe pessoa. 

Iremos utilizar com os seguintes arquivos: 

```
src
├── templates
|    ├── list_person.html: Template para inserção e listagem de pessoas
|    ├── person_eye_update.html: HTML para atualizar a cor do olho da pessoa
|    ├── person_update.html: HTML para atualizar os dados da pessoa
├── toy
|    ├── views
|    |    ├── get_post.py: view, usando get e post, para listar e editar os dados da pessoa
|    |    ├── with_form.py: view que tem a mesma funcionalidade do `get_post.py` porém usando forms
|    |    ├── with_generic.py: view que tem a mesma funcionalidade do `get_post.py` porém usando generic views
├── toy_example
|    ├── urls.py: Vincular as URLs nas views correspondentes
```

Inicialmente, para entendermos o get e o post, veja a página principal no navegador. Ela possui um form e uma lista de pessoas. Esse form é o seguinte: 
```html
    <form method="post">
      {% csrf_token %}
      <input type="text" name="name">
      <input type="date" name="birth_date">
      <input type="submit">
    </form>
```
Dessa forma, o form enviará via POST o nome e a data de nascimento para ser cadastrado o `csrf_token` é um campo de segurança para evitar requisições externas para seu site, o chamado ["Cross-site request forgery"](https://pt.wikipedia.org/wiki/Cross-site_request_forgery).  Use a tecla <kbd>F12</kbd> em seu navegador e entre na aba `Network`. Clique em submit e verifique a requisição enviada (a primeira). Você poderá visualizar que foi enviado os dados de nome e data de nascimento para o servidor.

Para tratar esses dados, criams a seguinte view no arquivo `get_post.py`:
```python
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
```
Veja que tratamos a requisição GET e POST. A requisição POST irá apenas salvar os dados inseridos ao ser enviado pelo formulário e redirecionar para a tela `home` que, no caso, é a propria tela, usando dessa vez o get. 

A requisição GET é realizada sempre quando abrimos o site pelo navegador ou o servidor tenha feito algum redirecionamento, por exemplo. Nela, como é possível ver no método `get` precisamos apenas de enviar os dados que serão usados para renderizar o template. Veja que o segundo parametro da função `render` é um dicionario e cada chave será uma veriável no template que, no nosso caso, seria o `list_person.html`. Veja abaixo como foi feito para renderizar a tabela usando tais variáveis:

```html
    <table>
      <caption>{{ mensagem_bonitinha }}</caption>
      <thead>
        <tr>
          <th>Nome</th>
          <th>Nascimento</th>
          <th>Olhos</th>
        </tr>
      </thead>
      <tbody>
        {% for pessoa in lista_pessoas %}
        <tr>
          <td>{{ pessoa.name }}</td>
          <td>{{ pessoa.birth_date }}</td>
          <td>{{ pessoa.eye_color.color_name  }}</td>

          <td><a href="{% url "editar_dados" pessoa.id %}"><img src="{% static 'imgs/edit.png' %}" alt="Editar"></a></td>
        </tr>
        {% endfor %}
      </tbody>
      
    </table>
```

Veja que `mensagem_bonitinha` foi a variável que enviamos, justo com `lista_pessoas` que é a lista de pessoas que realizamos a consulta. Perceba que a `lista_pessoas` é o resultado de uma consulta no banco de dados. Algo interessante também é que fizemos a parte dos links de edições em que, para cada pessoa, renderizamos uma URL de nome `editar_dados` com o seu id. Essa URL é formada de acordo com a seguinte linha no `urls.py`:
```python
path('edit/<int:person_id>/', PersonUpdate.as_view(),name="editar_dados"),
```
Por exemplo, para a pessoa de id=3 iremos gerar a URL `/edit/3/` veja no código fonte criado. Isso irá ser realizado uma requisição GET nessa URL e, como você pode ver nessa configuração, será tratado pela view `PersonUpdate` (arquivo `get_post.py`), por meio de seu método GET: 
```python
    class PersonUpdate(View):
        def get(self,request, person_id):
            try:
                person = Person.objects.get(id=person_id)
            except Person.DoesNotExist:
                return HttpResponseNotFound()

            return render(request,"person_update.html",{"person":person})
```
Ou seja, ele irá obter a pessoa (passada como parametro) e renderizá-la por meio do template `person_update.html` para editá-la.  Iremos falar sobre isso na próxima seção. 

# Redirecionamentos

Entre, no navegador, na edição de um determinada pessoa ele possui botoes para: 
- Salvar os dados e voltar para a lista de pessoas
- Dois botões que funcionam como "abas" um para editar os dados gerais da pessoa e outro para definir a cor do olho da mesma. 

Para cada um desses botões devemos: (1) salvar os dados alterados na tela dessa pessoa; (2) redirecionar para uma determinada pagina, de acordo com o botão clicado. Para isso, criamos cada URL para salvar com um parametro para redirecionamento.

Veja como salvamos os dados gerais da pessoa no método post da classe `PersonUpdate`: 
```python
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
```

Para sabermos qual pessoa estamos editando, temos uma variável que deverá existir no fomulário que é o `person_id` que, dessa forma, obtemos a pessoa. Logo após, com as variáveis `name` e `birth_date`, que também devem ser criadas no formulário html, atualizamos a pessoa. Logo após, redirecionamos para a página passada como parametro na URL. Note que esse redirecionamento poderia ser, por exemplo, para a pagina `editar_dados` (`edit/<int:person_id>/`) que espera um `person_id` dessa forma, temos que passa-lo como parametro.
 
Criamos a URL para salvar dados gerais dessa forma (com o parametro redirect_to): 
```python
path('salvar_dados/<str:redirect_to>/', PersonUpdate.as_view(),name="salvar_dados")
```

E, para renderizar no template `person_update.html`, veja que usamos o atributo `formaction` para gerar a URL e redirecionar para a página que gostaríamos. Veja os botões de submissão. 
```html
  <h1>Salvar Dados </h1>
  <form method="post">
    <nav>
      <input value="Listar" type="submit" formaction="{% url "salvar_dados" "home" %}">
      <input value="Dados" type="submit"  formaction="{% url "salvar_dados" "editar_dados" %}">
      <input value="Cor do Olho" type="submit" formaction="{% url "salvar_dados" "cor_do_olho" %}">
    </nav>
    {% csrf_token %}
    <input type="text" name="name" value="{{ person.name }}">
    <input type="date" name="birth_date" value="{{ person.birth_date|date:"Y-m-d" }}">
    <input type="hidden" value="{{ person.id }}" name="person_id">
    <input value="Salvar e Listar Pessoas" type="submit" formaction="{% url "salvar_dados" "home" %}"> 
  </form>
```

Fizemos de maneira similar para salvar os dados da cor do olho da pessoa por meio do arquivo `person_eye_update` da URL de edição  `eye_color/<int:person_id>/` e salvar dados `salvar_olho/<str:redirect_to>/` (veja em `urls.py`) e da view `EyeColorUpdate` que tratam tanto a visualização da edição  da cor do olho (método `get`) quanto o salvamento do mesmo e o seu redirecionamento (método  `post`). Note que, por simplicidade, não fizemos a validação. 


# Formas de salvar o conteúdo


É possivel verificar que há repetição de código sempre que temos que fazer edição, remoção e inserção de conteúdo: O código é praticamente o mesmo e o que muda são as classes utilizadas. Por isso, o Django possui recursos interessantes. Como o form, form model e o Generic. Por isso, aconselho a:

- Assistir a video aula sobre o tema [[video aula]](https://www.youtube.com/watch?v=CHAubzPmfaY&list=PLwIaU1DGYV6skjkahOKtpgs9bPXlrVrIp&index=29)[[slides]](https://daniel-hasan.github.io/cefet-web-grad/classes/python5/)
- Visualizar o arquivo `with_form` para ver como usamos ele e altere o `import` no arquivo `urls.py` para usarmos essas views. Veja que com isso, conseguimos fazer a validação sem precisar escrever tanto código - só relacionando as variaveis do modelo. 
- Faça a prática 1 dos slides
- Logo após, você pode melhor mais ainda usando Generic View. Faça a prática 2 para entende-la e veja o arquivo `with_generic` para verificar como iriamos fazer caso utilizássemos o generic para a tarefa do nosso exemplo
