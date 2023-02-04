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
# Deletando jogos
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
