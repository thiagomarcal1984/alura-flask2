# Configurações do Docker
Comando do Docker para criar uma instância do MySQL no PowerShell:
```docker
docker run --name instancia -e MYSQL_ROOT_PASSWORD=admin --volume "${PWD}\mysql:/var/lib/mysql" -p 3306:3306 --detach mysql
``` 

Referencia ao diretório atual (para criação de volumes no Docker):

| CLI | Sintaxe (--volume) | Observações | Aspas duplas |
| --- | --- | --- | --- |
| PowerShell | ${PWD} | MAIÚSCULO, entre chaves e precedido de cifrão | Opcional |
| Prompt do windows | %cd% | minúsculo, entre percentuais | Obrigatório |

O parâmetro --volume em docker run precisa estar envolvido por aspas no Prompt de comando do Windows.
Por via das dúvidas, use sempre as aspas.

Para que o Docker OCUPE o terminal, use o parâmetro --rm (ele desliga a instância ao parar a linha de comando). O problema é que para desocupar, o Ctrl+C não funciona: só fechando o terminal funciona.
Para que o Docker LIBERE o termina, use o parâmetro --detach ou -d.

Comando para acessar o terminal da instância MySQL do Docker:
```docker
docker exec -it instancia bash
``` 

# Notas sobre o MySQL

No MySQL, usa-se crase para os identificadores dos elementos na criação de tabelas. Veja o código fonte de prepara_banco.py.

No CLI, mostre os bancos de dados com o comando:
```sql
SHOW DATABASES;
```

Para mudar o banco de dados em uso:
```sql
use nome_do_banco_de_dados;
```

Para mostrar as tabelas do banco de dados em uso:
```sql
SHOW TABLES;
```

# Aulas

## Gerando banco de dados
Foi necessário instalar a biblioteca **mysql-connector-python (versão 8.0.28)** para que o Python se comunique com o servidor MySQL. Veja o código em prepara_banco.py.

## Conectando ao banco de dados
As dependências anteriores eram: 
```Python
flask~=2.0.2
flask-sqlalchemy~=2.5.1
```

Mas para que o código do projeto apresentado na aula funcione, foi necessário atualizar as dependências para:
```Python
flask~=2.2
flask-sqlalchemy~=3.0.3
```
## Criando tabelas
As cabelas são criadas via flask-sqlalchemy com os seguintes comandos:

```python
from flask_sqlalchemy import SQLAlchemy

...

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = \
    """string do SqlAlchemy: 
        '{SGBD}://{usuario}:{senha}@{servidor}:{porta}/{database}'
    """

db = SQLAlchemy(app)

class Entidade(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(50), nullable=False)

    def __repr__(self) -> str:
        return '<Name %r>' % self.nome
```

O método `__repr__(self)` sobre-escrito é chamado caso o método `__str__(self)` não esteja definido. A diferença é sutil: `__repr__` é para facilitar a compreensão da estrutura do objeto para o **programador**, enquanto `__str__` é usado para facilitar a leitura pelo **usuário**.

## Recuperando a listagem persistida
Buscar dados de um modelo flask-sqlalchemy é muito simples. A documentação é bem concisa e auto-explicativa: https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/queries/:

```python
# Para lista completa.
lista = Entidade.query.order_by() # Não ordena.

ou

lista = Entidade.query.filter_by() # Não filtra.
```

A ordenação consiste em referenciar a coluna da entidade dentro de order_by, e depois inserir `.asc()` ou `.desc`, se você precisar definir ordem ascendente/crescente:
```python
lista = Entidade.query.order_by(Entidade.categoria.asc())

ou

lista = Entidade.query.order_by(Entidade.categoria.desc())
```

O filtro também é simples:
```python
objeto = Entidade.query.filter_by(coluna1=valor, col2=3).first()
```

Nesta aula, acrescentei um navbar no cabeçalho para facilitar a navegação no app.

## Faça como eu fiz: persistência com MySQL
Apenas a atualização do arquivo prepara_banco.py. As funções de fechar a sessão e a conexão não estavam inseridas até agora.

## Reestruturando o código
As configurações da aplicação Flask podem ser inseridas como strings em um arquivo .py separado, e depois carregadas pelo método `app.config.from_pyfile(arquivo.py)`. Somente variáveis declaradas com letras maiúsculas são importadas por meio do comando `app.config.from_pyfile()`.

Os novos arquivos `config.py` e `models.py` precisam importar conteúdo (variáveis `app` e `db`) do arquivo da aplicação (`jogoteca.py`).

## Editando jogos
Acréscimo de duas rotas: editar (GET) e atualizar (POST, que ainda não está implementada).

O arquivo `novo.html` teve apenas mudança na identação. O arquivo `editar.html` é apenas uma cópia do arquivo `novo.html`.

Por ora, nada de muito novo no código.

## Direcionando a edição
Como colocar parâmetros nas funções de rota, usando a URI:

```python
@app.route('/metodo/<int:id>')
def metodo(id):
    obj = Entidade.query.filter_by(id=id).first()
    ...
```

Perceba que `<int:id>` tem o tipo da variável, seguida do nome dela.

Veja no template `lista.html` que a função `url_for` precisa de parâmetros **nomeados** para gerar a URL completa, com a id de cada objeto.

O raciocínio é semelhante nas rotas: a função `render_template` precisa de parâmetros **nomeados** para que os templates consigam referencia-los. Não basta a função da rota declarar as variáveis.

Ainda precisamos implementar a rota `atualizar`.

## Atualizando dados do servidor
Não há diferença entre os comandos para criar e editar entidades no SqlAlchemy:
```python
db.session.add(entidade) 
# O comando session.add não é necessário pra atualizar,
# mas é necessário para adicionar a entidade.

db.session.commit() # Confirma as mudanças no DB.
```
## Deletando jogos
Lembre-se de usar o commit para confirmar a remoção do objeto do banco.

A formação de URIs + querystring com a função `url_for()` funciona da seguinte forma:

```python
@app.route('/rota')
def funcao_endpoint(parm1: int, parm2: str):
    return render_template('template.html')

resultado = url_for('funcao_endpoint', parm1=1, parm2='Dois')
print(resultado) # Retorno: /rota?parm1=1&parm2=Dois

```

## Para saber mais: testando url_for

Você pode testar a criação da URLs dinâmicas através do `url_for` sem o servidor rodando. Para tal, basta importar o Flask e url_for no console:
```python
from flask import Flask, url_for
```
E tendo uma rota:

```python
app = Flask(__name__)
@app.route('/editar/<int:id>')
    def editar(id): 
        pass
```

Você também pode testar a criação da URL dinâmica através do método `test_request_context()`:

```python
with app.test_request_context():
    print(url_for('editar',id=5))
```
Que imprime:
> /editar/5

## Subindo imagens para o servidor
Fomulários que recebam arquivos precisam usar a propriedade `enctype="multipart/form-data":`
```HTML
<form enctype="multipart/form-data" action="/salvar" method="POST">
```

Para limitar os formatos de arquivo no campo de arquivo, use a propriedade `accept` e coloque os formatos precedidos de ponto e separados por vírgula:
```HTML
<input type="file" name="arquivo" accept=".jpg, .png">

<!-- Qualquer imagem-->
<input type="file" name="arquivo" accept="image/*">

<!-- Qualquer áudio-->
<input type="file" name="arquivo" accept="audio/*">

```
<a href="https://developer.mozilla.org/en-US/docs/Web/HTML/Attributes/accept">Outras informações sobre accept no site do MDN</a>

### Salvar arquivos no Flask
Acessar os arquivos no Flask, e salvá-los, é muito simples:
```python
# Procura o arquivo do campo de formulário chamado 'arquivo':
arquivo = request.files.get('arquivo')
diretorio = 'caminho/para/uploads'
novo_nome = 'novo_nome.txt'

arquivo.save(f'{diretorio}/{novo_nome}')
```
## Melhorando destino de upload
Para escrever o caminho absoluto do diretório que contém o arquivo onde o código é executado, use:
```python
import os
UPLOAD_PATH = os.path.dirname(os.path.abspath(__file__))
```
A variável `__file__` é um dunder-file que se refere ao arquivo atual. A função `os.path.abspath` busca o path absoluto de um arquivo, que é o ideal para definir o path para gravação de arquivos. A função `os.path.dirname` retorna apenas o path do diretório de um arquivo.

Um código semelhante foi inserido no arquivo `config.py`.

## Mostrando a capa do jogo
A função `send_from_directory` do Flask envia um arquivo a partir de um diretório:
```python
return send_from_directory('/caminho/do/arquivo', 'arquivo.txt')
```

Dica para campos de arquivo no HTML: 
1) crie um label;
2) insira o campo de arquivo ***dentro*** dele;
3) oculte o campo de arquivo (estilo `display: none;`). 

O label inteiro vai servir para exibir a janela de seleção do arquivo! Você pode usar JavaScript posteriormente para exibir o nome do arquivo (que geralmente é `C:\fakepath\nome_do_arquivo.ext`). 

Exemplo:
```HTML
<form name="formulario" enctype="multipart/form-data">
    <label style="cursor: pointer;">
        <div style="padding: 10px; background-color: cyan;">
            Selecionar arquivo
        </div>  
        <input style="display: none;" type="file" name="arquivo">
    </label>
    <script>
        function pathArquivo() {alert(`
            Nome do arquivo: 
            ${document.forms['formulario']['arquivo'].value}
        `);}
    </script>
    <br/>
    <button type="submit" onclick="pathArquivo()">
        Mostrar o path do arquivo?
    </button>
</form>
```
Repare no exemplo que o método continua sendo `GET`. Então, o nome do arquivo acaba aparecendo na query string da URI resultante do envio do formulário.

## Usando um pouco de JavaScript
A aula em si se baseava em copiar e colar código JavaScript

O JavaScript em app.js para substituição da imagem era dependente do jQuery. Modifiquei o código para remover essa dependência:

| Código Antigo | Código Novo | O que muda |
|---|---|---|
|`form = $('form input[type="file"]')` | ` form = document.querySelector('form input[type="file"]')`| O seletor no jQuery é `$()`; no JavaScript puro é `document.querySelector()`. |
| `form.change(mudar);`| `form.onchange = mudar;` | No jQuery, a função `mudar` é **um parâmetro da função `change`** ; no JavaScript puro, a função `mudar` é **atribuída ao atributo `onchange`** . |
| `if(tipo_arquivo == 'image/jpeg') { ... }` | `if(tipo_arquivo.includes('image/')) { ... }` | O código antigo só permitia jpeg; o código novo permite qualquer tipo de arquivo cujo nome comece com `image/`. |
| `let imagem = $('<img class="img-fluid">');` | `let imagem = document.createElement('img');` | No jQuery, a criação do elemento é um parâmetro na função `$()` e permite a atribuição de classes CSS; no JavaScript puro, a criação é feita pelo método `document.createElement(tag)`, e não permite a atribuição de classes CSS. |
| `let imagem = $('<img class="img-fluid">');` | `imagem.classList.add('img-fluid');` | No jQuery, uma clsase CSS já pode ser atribuída dentro da função `$()`; no JavaScript puro, a atribuição de uma classe CSS é feita por meio do método `elemento.classList.add('classe-css')`. |
| `imagem.attr('src', window.URL.createObjectURL(arquivos[0]));` | `imagem.setAttribute('src', window.URL.createObjectURL(arquivos[0]));` | No jQuery, o método `attr(key, value)` do elemento define seu atributo; no JavaScript puro, o método `setAttribute(key, value)` do elemento define seu atributo. |

## Editando a capa dos jogos
O arquivo helpers.py contém a função que recupera uma imagem de acordo com o ID. Se ela não existir, uma imagem padrão é exibida.

O método `save` nos arquivos obtidos de `request.files` substitui o arquivo caso ele exista.

Para remover um arquivo, use:
```python
os.remove('string_path')
```
## Contornando o CACHE
O cache do navegador pode atrapalhar a exibição dos arquivos de imagem enviados ao servidor. Uma solução é inserir um nome único nos arquivos enviados com um timestamp.

A função `recupera_imagem` em `helpers.py` foi atualizada para confirmar se o texto `capa-{id}` está presente no nome do arquivo. Na prática, ele retorna o primeiro arquivo que obedece a esse padrão.

No entanto, temos o problema da geração de MUITOS arquivos de imagem associados a um mesmo ID. A próxima aula veremos como resolver isso.

## Deletando imagens duplicadas
O código em helpers.py é auto explicativo. Um único detalhe a mais é sobre como tornar o path dos arquivos independente do SO. Para isso, usamos a função `os.path.join`.

```python
import os
path = os.path.join('d:\\','alura','flask2','requirements.txt')
# No Windows, path = 'd:\\alura\\flask2\\requirements.txt'
file = open(path, 'r')
print(file.readlines()) # Imprime o conteúdo todo do arquivo.
```

## Melhorando a interface
Apenas inclusão de botões nos arquivos .html, para facilitar a navegação.

## Implementando o Flask WTF
Os modelos de formulário da aplicação vão ficar em helpers.py.

## Validando o formulário de novo jogo
Sintaxe para criação de um formulário:
```python
class Formulario(FlaskForm):
    # Cada campo precisa do label e da lista de validadores.
    nome = StringField('nome', [validators.DataRequired()])
    cpf = StringField('cpf', [validators.Length(min=11, max=11)])
    salvar = SubmitField('Salvar')

```
Sintaxe para chamar o formulário nas views (tanto na de GET quanto na de POST):
```python
@app.route('/rota')
def rota_endpoint():
    form = Formulario()
    return render_template('template.html', form=form)

@app.route('/salvar', methods=['POST',])
def rota_salvar():
    # Cria formulário a partir do POST.
    form = Formulario(request.form) 
    
    # Repare em ".data" para cada campo.
    nome = form.nome.data
    cpf = form.cpf.data
    
    # ... processamento do formulário...

    return redirect(url_for('index'))
```

Sintaxe para chamar os campos dos formulários nos templates:
```python
<form method="post" action="{{ url_for('rota_salvar') }}">
    <div>
        {# Use class ou class_ para atribuir CSS aos campos. #}
        {{ form.nome.label(class_='form-label') }}
        {{ form.nome(class='form-control') }}
    </div>
    <div>
        {{ form.cpf.label(class_='form-label') }}
        {{ form.cpf(class='form-control') }}
    </div>
    <div>
        {{ form.salvar(class_='btn') }}
    </div>
</form>
```
## Integrando formulário de edição
Sempre que usarmos um `FlaskForm` do flask-wtf, e usarmos o método `validate_on_submit()`, ele vai verificar o CSRF token. Se o código abaixo não estiver presente na aplicação Flask, o erro de CSRF token inválido não ficará explícito no navegador:
```python
from flask_wtf.csrf import CSRFProtect
app = Flask(__name__)
csrf = CSRFProtect(app)
```

A sintaxe para invocação do CSRF token no template com flask-wtf é diferente do Django: `{{ form.csrf_token() }}`.

## Criando novo formulário de login
O `FlaskForm` e a requisição POST são coisas diferentes. Veja o parâmetro `proxima`: ele não é parte do formulário, mas é usado na requisição para redirecionar a resposta.

Sintaxe do formulário de login: 
```python
class LoginForm(FlaskForm):
    user = StringField('Lb. User', [construtor do validador])
    senha = PasswordField('Lb. Senha', [construtor do validador])
    login = SubmitField('Login')
```

Podemos invocar métodos sem parâmetros no template **com** ou **sem** os parênteses, o resultado é o mesmo: 
- `{{ form.csrf_token() }}` é o mesmo que `{{ form.csrf_token }}`.
- `{{ form.nickname() }}` é o mesmo que `{{ form.nickname }}`.

## Refatorando a aplicação
Aplicação de CSS e distribuição dos códigos das views em arquivos separados.

## Criptografando as senhas
Algumas bibliotecas precisam de downgrades ou upgrades para manter a compatibilidade. Consulte o site dos respositórios pip (pypi.org).

A dependência recomendada para o flask-bcrypt na aula era 0.7.1; para manter a compatibilidade, usei a versão 1.0.1. Na aula também foi recomendada a instalação de uma versão específica da biblioteca werkzeug, mas como ela já é instalada pelo Flask, não acrescentei a werkzeug em requirements.txt.

### Instalação do Bcrypt no app Flask
Na aula foi proposto o seguinte código: 
```python
from flask_bcrypt import Bcrypt
app = Flask(__name__)
bcrypt = Bcrypt(app)
```
**Porém** removi essas linhas do Bcrypt na aplicação, e o código funcionou sem problemas. As modificações nos arquivos `views_user.py` e `prepara_banco.py` foram suficientes para gerar e comparar as senhas.

### A geração da senha
No arquivo `prepara_banco.py` importamos a função `generate_password_hash("senha a criptografar")`. Como a função retorna bytes (array de caracteres, não string), precisamos convertê-la para string e informar o conjunto de caracteres aplicável, por meio do método `.decode('encoding')` (no caso, o encoding é utf-8):
```python
from flask_bcrypt import generate_password_hash
senha_criptografada = generate_password_hash("senha").decode('utf-8')
```
### Checando a senha
A função `check_password_hash` recebe dois parâmetros: a senha criptografada e a senha informada. O método retorna um `bool`:

```python
from flask_bcrypt import check_password_hash

usuario = busca_usuario(request.forms.get('usuario'))
senha = request.forms.get('senha')
if usuario is not None and check_password_hash(usuario.senha, senha):
    # Login confirmado, redireciona.
    return redirect(url_for('restrito'))
else: 
    # Informa falha na autenticação.
    return render_template('login.html')

```

### Precisa mesmo baixar o Flask Bcrypt?
A documentação da biblioteca bcrypt (sem o Flask) parece muito clara sobre como gerar e checar senhas:
```python
from bcrypt import hashpw, gensalt, checkpw
hash = hashpw('senha'.encode('utf-8'), gensalt())

print(hash)
# Resultado: 
# b'$2b$12$EKJgB5EB5k.JHYfpzjvT9e4j06wNEeHtEEc2GXtVBoJ/Sual7OI62'

checkpw('senha'.encode('utf-8'), hash)
# Resultado: True

```
A desvantagem é adicionar mais um import, o do gensalt(). Por padrão, o método não precisa de parâmetros. Essa função gera um salt, que recebe os parâmetros `round` (valor padrão na biblioca bcrypt é `12`) e `prefix` (valor padrão na biblioteca bcrypt é `b"2b"`). 

O parâmetro `round` se refere ao custo para calcular o hash. E o parâmetro `prefix` só recebe apenas os valores possíveis `b"2b"` e `b"2a"`.
