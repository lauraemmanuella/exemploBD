import sqlite3

import Autor


def menu():
    
    listar() #lista titulos ja cadastrados

    print('\n')
    print(' 1. Incluir um titulo')
    print(' 2. Alterar um titulo')
    print(' 3. Apagar um titulo')
    print(' 4. Sair')
    opcao = input('\nSelecione a opção: ')

    if opcao == '':
        opcao=0
    opcao = int(opcao)

    while opcao < 1 or opcao > 4:
        print('\nOpção inválida\n')
        opcao = input('\nSelecione a opção: ')
        if opcao == '':
            opcao=0
        opcao = int(opcao)

    return opcao

def listar():

    try:
        cursor.execute('''
        SELECT ID_TITULO, NOME_TITULO, COD_TITULO, NOME_AUTOR FROM  TITULO, AUTOR WHERE TITULO.ID_AUTOR = AUTOR.ID_AUTOR;
        ''')

        print('\n\n')
        print('TÍTULOS ───────────────────────────────────────────────────────────────────')
        print('Id    Nome                      Código            Autor')
        print('───── ───────────────────────── ───────────────── ─────────────────────────')
        for linha in cursor.fetchall():
            regid = str(linha[0])
            regNome = str(linha[1])
            regCodigo = str(linha[2])
            regAutor = str(linha[3])
            print('{:5} {:25} {:17} {:25} '.format(regid, regNome, regCodigo, regAutor))
        print('───────────────────────────────────────────────────────────────────────────\n')
    except sqlite3.Error as er:
        print('Erro :', er.message)
        input('Pressione <ENTER>')

def incluir():
    print('Informe o Id do autor')
    regIdAutor = Autor.principal()
    regNome = str(input('\n Título......: '))
    while regNome.__len__() == 0:
        print('\nO título precisa ser preenchido.\n')
        regNome = str(input('\n Título......: '))

    regCodigo= str(input(' Código..: '))
    while regCodigo.__len__() == 0:
        print('\n O codigo precisa ser preenchido\n')
        regCodigo = str(input('\n Código..: '))


    try:
        cursor.execute('''
        INSERT INTO TITULO (NOME_TITULO, COD_TITULO, ID_AUTOR) VALUES (?,?, ?)
        ''', (regNome, regCodigo, regIdAutor))
        conn.commit()
        input('\ntitulo incluído. Pressione uma tecla para voltar.')

    except sqlite3.Error as er:
        print('Erro :', er.message)
        input('Pressione <ENTER>')

def alterar():

    regId = str(input('\n Id do titulo.: '))
    while regId.__len__() == 0:
        print('\nO Id precisa ser preenchido.\n')
        regId = str(input('\n Id do titulo.: '))

    try:
        cursor.execute('''
            SELECT NOME_TITULO, COD_TITULO FROM TITULO WHERE ID_TITULO=?
            ''', (regId))

        linha = cursor.fetchall()
        if linha.__len__() > 0:
            regAntNome = linha[0][0]
            regAntCodigo = linha[0][1]

            print('\n─ Dados Antigos ' + '─' * 64)
            print(' Nome......: {}'.format(regAntNome))
            print(' Código..: {}'.format(regAntCodigo))

            print('\n─ Novos Dados '  + '─' * 66)
            regNome     = str(input(' Nome......: '))
            while regNome.__len__() == 0:
                print('\nO nome precisa ser preenchido.\n')
                regNome = str(input('\n Nome......: '))

            regCodigo = str(input(' Código..: '))
            while regCodigo.__len__() == 0:
                print('\nO código precisa ser preenchido\n')
                regCodigo = str(input('\n Codigo..: '))

            try:
                cursor.execute('''
                UPDATE TITULO SET NOME_TITULO = ?, COD_TITULO = ? WHERE ID_TITULO = ?
                ''', (regNome, regCodigo,regId))
                conn.commit()
                input('\nTitulo alterado. Pressione uma tecla para voltar.')
            except sqlite3.Error as er:
                print('Erro :', er.message)
                input('Pressione <ENTER>')
        else:
            input('\nNenhum título com esse Id.\nPressione uma tecla para voltar.')
    except sqlite3.Error as er:
        print('Erro :', er.message)
        input('Pressione <ENTER>')

def excluir():

    regId = str(input('\n Id do titulo.: '))
    while regId.__len__() == 0:
        print('\nO Id precisa ser preenchido.\n')
        regId = str(input('\n Id do titulo.: '))


    try:
        cursor.execute('''
            SELECT NOME_TITULO, COD_TITULO FROM titulo WHERE ID_TITULO=?
            ''', (regId))

        linha = cursor.fetchall()
        if linha.__len__() > 0:
            regAntNome = linha[0][0]
            regAntCodigo = linha[0][1]

            print('\n─ Dados do titulo '  + '─' * 61)
            print(' Nome......: {}'.format(regAntNome))
            print(' Código..: {}'.format(regAntCodigo))
            print('\nConfirma a exclusão ?\n')
            confirmar   = str(input('S/N ? '))

            if confirmar == 's' or confirmar == 'S':
                try:
                    cursor.execute('''
                    DELETE FROM TITULO WHERE ID_TITULO = ?
                    ''', (regId))
                    conn.commit()
                except sqlite3.Error as er:
                    print('Erro :', er.message)
                    input('Pressione <ENTER>')
                input('\ntitulo apagado. Pressione uma tecla para voltar.')
            else:
                input('\nPressione uma tecla para voltar.')
        else:
            input('\nNenhum titulo com esse Id.\nPressione uma tecla para voltar.')
    except sqlite3.Error as er:
        print('Erro :', er.message)
        input('Pressione <ENTER>')

##SCRIPT

# Conectando
conn = sqlite3.connect('biblioteca.db')

# Definindo um cursor
cursor = conn.cursor()

# Laço de execução da agenda
opcaoSelecionada = menu()


while opcaoSelecionada != 4:

    if opcaoSelecionada == 1:
        incluir()
    elif opcaoSelecionada == 2:
        alterar()
    else:
        excluir()

    opcaoSelecionada = menu()

# Desconectando
cursor.close()
conn.close()

