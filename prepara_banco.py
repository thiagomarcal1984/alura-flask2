import mysql.connector
from mysql.connector import errorcode

print("Conectando...")

try:
    conn = mysql.connector.connect(
        host = 'localhost',
        user='root',
        password='admin'
    )
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print('Existe algo errado no nome do usuário ou senha.')
    else:
        print(err)

cursor = conn.cursor()

cursor.execute("DROP DATABASE IF EXISTS `jogoteca`;")

cursor.execute("CREATE DATABASE `jogoteca`;")
cursor.execute("USE `jogoteca`;")

# Criando tabelas
TABLES = {}
TABLES['Jogos'] = ('''
    CREATE TABLE `jogos` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `nome` varchar(50) NOT NULL,
    `categoria` varchar(40) NOT NULL,
    `console` varchar(20) NOT NULL,
    PRIMARY KEY (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
''')

TABLES['Usuarios'] = ('''
    CREATE TABLE `usuarios` (
    `nome` varchar(20) NOT NULL,
    `nickname` varchar(8) NOT NULL,
    `senha` varchar(100) NOT NULL,
    PRIMARY KEY (`nickname`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
''')

for tabela_nome in TABLES:
    tabela_sql = TABLES[tabela_nome]
    try: 
        print(f'Criando tabela {tabela_nome}: ')
        cursor.execute(tabela_sql)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print('Já existe.')
        else:
            print(err.msg)
    else:
        print('OK')

# Inserindo usuários.
usuario_sql = 'INSERT INTO usuarios (nome, nickname, senha) VALUES (%s, %s, %s)'
usuarios = [
    ("Bruno Divino", "BD", "alohomora"), 
    ("Camila Ferreira", "Mila", "paozinho"), 
    ("Guilherme Louro", "Cake", "python_eh_vida"), 
]
cursor.executemany(usuario_sql, usuarios)

cursor.execute('select * from jogoteca.usuarios')
print('----------------- Usuários: -----------------')
for user in cursor.fetchall():
    print(user[1])

# Inserindo jogos
jogos_sql = 'INSERT INTO jogos (nome, categoria, console) VALUES (%s, %s, %s)'
jogos = [
    ('Tetris', 'Puzzle', 'Atari'), 
    ('God of War', 'Hack n Slash', 'PS2'), 
    ('Mortal Kombat', 'Luta', 'PS2'), 
]
cursor.executemany(jogos_sql, jogos)

cursor.execute('select * from jogoteca.jogos')
print('----------------- Jogos: -----------------')
for jogo in cursor.fetchall():
    print(jogo[1])

# Commit se nada tem efeito.
conn.commit()
