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
