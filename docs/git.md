# Utilização do GIT
Comandos mais usados
- `git status`: verifica o estado dos arquivos em seu repositório local
- `git add -A`: adiciona os arquivos em seu repositório local
- `git commit -m "mensagem"`: faz commit de seus arquivos para o repositório local
- `git push origin nome-da-branch`: envia os arquivos para o respositório remoto na branch chamada `nome-da-branch`
- `git pull origin nome-da-branch`: obtém os arquivos do repositório remoto
- `git branch`: exibe as branches existentes e mostra em qual branch você está atualmente trabalhando
- `git branch nome-da-branch`: cria uma nova branch
- `git checkout nome-da-branch`: vai para uma determinada branch


# Conceito de Branches 

Branches significa ramificações. Em desenvolvimento, fazemos isso principalmente para preservar um código que já está funcionando e escrevermos outro.  Por exemplo, abaixo, você pode dever o branch de desenvolvimento e um usuário decidiu criar uma nova funcionalidade. Ele cria um novo branch chamado `alpha` a partir do branch de `desenvolvimento`, logo após, é criado também o branch `beta`. 

Um branch começa com a cópia exata do repositório do brach de origem `desenvolvimento` logo após, várias modificações são realizadas no branch `alpha` sem afetar o branch de `desenvolvimento` (os pontos na figura são as modificações). Isso é importante para garantirmos que o branch de `desenvolvimento` esteja sempre funcional enquanto estamos fazendo alterções em nossos códigos. Na figura acima, veja que o branch `alpha`  fez algumas modificações no código em varios instantes, podendo até criar bugs, porém o branch `beta` pode iniciar por meio de um código livre de bugs.  

Para finalizar um branch e enviarmos ao desenvolvimento: 

1. Verificamos e corrigimos todos os possíveis erros e vemos se o sistema passou em todos os testes automatizados

1. Fazemos um `merge` (junção) **do** desenvolvimento **para o**  branch `alpha`. Isso é importante para garantir que modificações feitas por outros usuários não tenham quebrado o seu código. No exemplo da figura acima, estamos obtendo as modificações feitas pelo branch `beta` em nosso branch `alfa`. Dessa forma quando fazemos um junção para o nosso branch `alpha`, tentamos corrigir eventuais erros dessa junção em nosso branch `alpha`, sem afetar o branch de `desenvolvimento`. 


2. Logo após, fazemos um `merge` **do** branch `alpha` **para o branch** de `desenvolvimento`. 

Nas próximas seções, iremos explicar como fazer isso usando Git e o Bitbucket. **Aqui nosso branch de desenvolvimento chamará master**

# Início de uma nova funcionalidade

- Para cada nova funcionalidade, a partir do branch desenvolvimento (chamado daqui de master), crie um novo branch chamado `feat-usuario-nom` sendo que `nom` é um nome indicando a funcionalidade e `usuario` é o nome do usuário grit.
Veja o exemplo em que o usuário é `daniel-hasan` e estamos fazendo a funcionalidade `tela-pesquisador`:


- vá para o branch de desenvolvimento (master) e crie o novo branch
```bash
git checkout master
git branch feat-daniel-hasan-tela-pesquisador
```
- Entre no branch no seu repositório local para poder começar a fazer as alterações desejadas:
```bash
git checkout feat-daniel-hasan-tela-pesquisador
```

# Enviando e obtendo alterações do repositório remoto em seu branch

Vamos assumir que sua branch chama `feat-daniel-hasan-tela-pesquisador` e você deseja obter ou enviar modificações locais no repositório remoto (nesta mesma branch).

## Enviando alterações

Para enviar as alterações para o repositório remoto (ainda em seu branch) utilize:
```bash
git add -A
git commit -m "Alterações blah feita hoje"
git push origin feat-daniel-hasan-tela-pesquisador
```

- **Recomendável fazer isso constantemente**. Pois isto irá fazer backup de suas alterações. Isto também é útil quando trabalhamos em mais de um computador e queremos passar as alterações de um computador para outro.
- Além disso, caso estejameos utilizando pipelines do bitbucket, assim que você enviar suas alterações pelo repositório remoto, serão realizados testes para verificar se o seu código não criou nenhum tipo de erro em seu branch. Para verificar  tais testes, acesse o nosso repositório no Bitbucket, vá em `pipelines` e acesse o seu branch.

## Obtendo alterações

Algumas vezes, alterações em seu branch não existem em seu repositório local. Pois, você
pode ter alterado em outro computador ou alguém, que estava ajudando nesta funcionalidade,
atualizou o repositório remoto. Assim, você deverá executar o comando `pull` para obter tais alterações:

```bash
  git pull origin feat-daniel-hasan-tela-pesquisador
```

## Obtendo atualização do branch de desenvolvimento em seu Branch
- Obtenha frequentemente as atualizações do branch de desenvolvimento (chamado aqui de `master`). Assim,
menos erros ocorrerão quando for fazer o merge **para o** branch de desenvolvimento. Para isso, vá em seu branch e solicite um branch **do** de desenvolvimento **para o** seu branch:
```bash
git checkout feat-daniel-hasan-tela-pesquisador
git merge master
```
  - Caso haja conflito, corrija-os. Veja a seção que fala sobre [solução de conflitos](#markdown-header-solucao-de-conflitos)


## Finalizando funcionalidade - Enviando-as ao branch de desenvolvimento

- Antes de começar, [obtenha as atualizações do branch de desenvolvimento](#markdown-header-obtendo-atualizacao-do-branch-de-desenvolvimento-em-seu-branch) (ver seção anterior)
- Ainda em seu branch, caso tenha alterações no repositório local que não estão no repositório remoto, [envie tais alterações](#markdown-header-enviando-e-obtendo-alteracoes-em-seu-branch):
    - Você pode executar `git status` para ver se há alguma alteração no seu repositório local que ainda não foi enviada ao respositório remoto

- Acesse usando [repositório wikiquality no bitbucket](https://bitbucket.org/daniel-hasan/wiki-quality) por meio de seu login e senha.
- Acesse o menu `Pipelines` clique em seu branch e veja se
o repositório foi construído com sucesso
  - Caso haja erros na construção do repositório, veja o erro o que ocorreu, corrija-o e envie as alterações

- Após corrigir todos os erros, no menu, acesse `Pull Request` e clique em `create pull request`.

  - Faça um `Pull Request` do seu branch para o master. O administrador receberá um email para aprovar as alterações
  feitas e fazer o merge no master.

  - Caso, ao solicitar o Pull Request, haja algum arquivo com conflito (haverá um "c" no nome do arquivo), não será possível fazer o merge. Assim, você deve solicionar os conflitos para isso, [obtenha as atualizações do branch de desenvolvimento - veja a seção anterior](#markdown-header-obtendo-atualizacao-do-branch-de-desenvolvimento-em-seu-branch) e, logo após, solucione os conflitos (próxima seção).

## Solução de conflitos

Existem algumas ferramentas visuais para solução de conflitos. Aqui, explicarei a instalação da `Meld`. Primeiramente, instale a ferramenta:
```bash
sudo apt-get install meld
```

Você pode deixar ele como default ao dar merge: 
```bash
git config --global merge.tool meld
```
Logo após de verificar um conflito (por exemplo, fazendo um merge do desenvolvimento para seu branch) abra a interface do meld. 
Para execurar o meld, digite "meld" e  clique em "Version control view" e selecione a pasta raiz de nosso repositório. 
Logo após, clique nos arquivos com status "conflict" para fazer as alterações necessárias

De um lado estará o repositorio local e , do outro, o repositório remoto (veja o titulo acima do código) e, no meio, o arquivo a ser editado (com o conflito). Assim, você poderá fazer merge das edições locais (suas) e edições remotas (de outras pessoas) para o código que está no meio. Salve as alterações. É importante solucionar o conflito junto com o outro usuário envolvido no conflito. 

