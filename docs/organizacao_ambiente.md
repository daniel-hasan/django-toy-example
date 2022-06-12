
# Estrutura de Diretórios

Um projeto não é feito apenas de códigos. Projetos de Ciência dos Dados, por exemplo, possuem dados 😱  e outros elementos interessantes. Usamos a padronização conforme apresentado em [Cookiecutter Data Science](https://drivendata.github.io/cookiecutter-data-science/) - adaptado para um projeto Django de Ciência os Dados.

```
├── LICENSE
├── Makefile           <- Makefile with commands like `make data` or `make train`
├── README.md          <- The top-level README for developers using this project.
├── data               <- data naming convention: obtation year, subject, version (for ordering) ex:  2010-bovespa-technical-features-1.0
│   ├── external       <- Data from third party sources.
│   ├── interim        <- Intermediate data that has been transformed.
│   ├── processed      <- The final, canonical data sets for modeling.
│   └── raw            <- The original, immutable data dump.
│
├── docs               <- A default Sphinx project; see sphinx-doc.org for details
│
├── models             <- Trained and serialized models, model predictions, or model summaries
│
├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
│   │                     the creator's initials, and a short `-` delimited description, e.g.
│   │                    `1.0-jqp-initial-data-exploration`.
│   ├── bd_model       <- Jupyter notebooks concerning django bd models
│   ├── visualization  <- Jupyter notebooks concerning evaluation. 
│
├── references         <- Data dictionaries, manuals, and all other explanatory materials.
│
├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
│
├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
│                         generated with `pip freeze > requirements.txt`. TODO: We do not have this yet.
│
├── setup.py           <- Make this project pip installable with `pip install -e`. TODO: We do not have this yet
├── src                <- Source code for use in this project.
│   ├── __init__.py    <- Makes src a Python module
│   │
│   ├── data           <- Package to download or generate data
│   │
│   ├── features       <- Package to turn raw data into features for modeling
│   ├── ml_models         <- Packegeto train models and then use trained models to make
│   │                     predictions. 
│   └── visualization  <- Scripts to create exploratory and results oriented visualizations (if needed )
│
```

Você pode adaptá-lo, conforme a necessidade do projeto. Super recomendável adicionar essa estrutura no `readme.MD` de seu projeto.  Também, por convenção, é utilizado inglês na documentação e no código a ser implementado.


# GitIgnore


Muitas vezes, durante o desenvolvimento, criamos arquivos que não são necessários adicionarmos no nosso repositório. Por ele ser pessoal do seu desenvolvimento (por exemplo, sua base de dados atual) e realmente desenecessários. São exemplos  eles: 

- Arquivos compilados do Python
- Caches do Python e/ou de IDEs utilizadas
- Arquivos de backup
- Imagens que vc fez download na aplicação que não seriam necessárias

Por isso, criamos o `.gitignore` na raiz do nosso repositório. Veja ele, lembrando que o Linux não exibe, por padrão, os arquivos que começam com `.`.

# Ambiente Virtual

O Python instala diversas dependencias, dependendo do projeto. Por exemplo, cada projeto seu pode estar rodando com versões do Django diferentes.  

Para facilitar o uso de um projeto instalando sempre suas dependencias que ocorra conflitos de versão, criamos um ambiente virtual por projeto. 

Para criar um ambiente virtual, faça apenas: 
- No linux: 
```
virtualenv env

```
- No Windows:

```
virtualenv env
env\Scripts\activate.bat
```
Logo após, vocẽ pode acessar o ambiente virtual usando `source env/bin/activate`, no Linux, ou `env\Scripts\activate.bat`.

**Atenção!** O `.gitignore` deve-se ter um indicador para ignorar a pasta env. Pois, não é recomendável salvar o env no respositório Git. 

Em seguida, caso seu projeto não possui o `requirements.txt` você deve criá-lo (próxima seção). Esse arquivo é onde aparecerá todas as bibliotecas usadas no seu projeto junto com sua versão. Também, ao longo do projeto, você pode precisar de bibliotecas novas. Veja o exemplo de um conteúdo de requiremnts.txt: 

```
Django==3.2.7
requests==2.26.0
xmltodict==0.12.0
```

Caso o `requirements.txt` exista, dentro do seu ambiente virtual, execute: 
```
pip install -r requirements.txt
```
Isso irá instalar todas as dependencias do projeto em seu ambiente virtual. Isso serve também para atualizar as dependencias do projeto - caso alguém tenha instalado uma dependencia e ela ainda não exista em localmente em seu computador. Dessa forma, você deve executar esse comando uma vez ao instalar o projeto em seu computador e sempre que alguém atualizar o `requirements.txt` com algo novo.

## Criando um novo  `requirements.txt` de um projeto que ainda não o possui

Caso seu projeto seja novo e você está inicializando ainda, você ainda não criou o arquivo requirements.txt.  Para criar o requirements: 

1. Acesse seu ambiente virtual usando `source env/bin/activate`, no Linux, ou `env\Scripts\activate.bat`

1. Use `pip` para instalar os pacotes e, logo após, faça `pip freeze > requirements.txt` para atualizar/criar o requirements. Cuidado para não instalar nenhuma biblioteca sem necessidade - por exemplo, se você estiver testando algo, eventualmente, você eventualmente poderá utilizar uma biblioteca e depois descartá-la. Caso tenha feito isso, entre na proxima seção e veja como atualizar o 

## Atualizando o requirements.txt com novos pacotes

Caso tenha, ao longo do desenvolvimento, instalado novos pacotes você pode atualizar o `requirements.txt` de três formas, todas devem ser executadas em seu ambiente virtual. A primeira, é manualmente: acessando ele e colocando `pacote==versão`. A segunda alternativa é usar o `pip freeze > requirements.txt` novamente, substituindo assim os pacotes antigos com o novo. Esta segunda alternativa, apesar de mais facil, corre o risco de instalar pacotes desencessários, pois, muitas vezes, instalamos pacotes durante o desenvolvimento para testar algo e, logo após, excluímos. Assim, a forma mais recomendável é a seguinte:

1. Limpe seu ambiente virtual
```
pip freeze > requirements.txt
pip uninstall -r requirements.txt
```
1. obtenha do repositório remoto o `requirements.txt` original:
```
git restore requirements.txt
``` 
1. Instale apenas os pacotes realmente necessários
1. Crie novamente o `requirements.txt` usando `pip freeze > requirements.txt`




