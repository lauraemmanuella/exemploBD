import sqlite3

# Conectando
conn = sqlite3.connect('biblioteca.db')

# Definindo um cursor
cursor = conn.cursor()

def principal():
    
    while True:

        opcaoSelecionada = menu()

        if opcaoSelecionada == 1:
            return escolher()
        elif opcaoSelecionada == 2:
            incluir()
        elif opcaoSelecionada == 3:
            alterar()
        elif opcaoSelecionada == 4:
            excluir()

def menu():
    
    listar() #lista autores ja cadastrados

    print('\n')
    print(' 1. Escolher um autor')
    print(' 2. Incluir um autor')
    print(' 3. Alterar um autor')
    print(' 4. Apagar um autor')
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

def escolher():
    idAutor = str(input(' Id..: '))
    while idAutor.__len__() == 0:
        print('\n O id do autor precisa ser preenchido\n')
        idAutor = str(input(' Id..: '))

    return idAutor

def listar():
    try:
        cursor.execute('''
        SELECT * FROM AUTOR
        ''')

        print('\n\n')
        print('AUTORES ─────────────────────────────────────────')
        print('Id    Nome                      Código')
        print('───── ───────────────────────── ─────────────────')
        for linha in cursor.fetchall():
            regid = str(linha[0])
            regNome = str(linha[1])
            regCodigo = str(linha[2])
            print('{:5} {:25} {:17}'.format(regid, regNome, regCodigo))
        print('─────────────────────────────────────────────────\n')
    except sqlite3.Error as er:
        print('Erro :', er.message)
        input('Pressione <ENTER>')

def incluir():
    
    regNome = str(input('\n Nome......: '))
    while regNome.__len__() == 0:
        print('\nO nome precisa ser preenchido.\n')
        regNome = str(input('\n Nome......: '))

    regCodigo= str(input(' Código..: '))
    while regCodigo.__len__() == 0:
        print('\n O codigo precisa ser preenchido\n')
        regCodigo = str(input('\n Código..: '))


    try:
        cursor.execute('''
        INSERT INTO AUTOR (NOME_AUTOR, COD_AUTOR) VALUES (?,?)
        ''', (regNome, regCodigo))
        conn.commit()
        input('\nAutor incluído. Pressione uma tecla para voltar.')

    except sqlite3.Error as er:
        print('Erro :', er.message)
        input('Pressione <ENTER>')

def alterar():

    regId = str(input('\n Id do autor.: '))
    while regId.__len__() == 0:
        print('\nO Id precisa ser preenchido.\n')
        regId = str(input('\n Id do autor.: '))

    try:
        cursor.execute('''
            SELECT NOME_AUTOR, COD_AUTOR FROM AUTOR WHERE ID_AUTOR=?
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
                UPDATE AUTOR SET NOME_AUTOR = ?, COD_AUTOR = ? WHERE ID_AUTOR = ?
                ''', (regNome, regCodigo,regId))
                conn.commit()
                input('\nAutor alterado. Pressione uma tecla para voltar.')
            except sqlite3.Error as er:
                print('Erro :', er.message)
                input('Pressione <ENTER>')
        else:
            input('\nNenhum autor com esse Id.\nPressione uma tecla para voltar.')
    except sqlite3.Error as er:
        print('Erro :', er.message)
        input('Pressione <ENTER>')

def excluir():

    regId = str(input('\n Id do autor.: '))
    while regId.__len__() == 0:
        print('\nO Id precisa ser preenchido.\n')
        regId = str(input('\n Id do autor.: '))


    try:
        cursor.execute('''
            SELECT NOME_AUTOR, COD_AUTOR FROM AUTOR WHERE ID_AUTOR=?
            ''', (regId))

        linha = cursor.fetchall()
        if linha.__len__() > 0:
            regAntNome = linha[0][0]
            regAntCodigo = linha[0][1]

            print('\n─ Dados do autor '  + '─' * 61)
            print(' Nome......: {}'.format(regAntNome))
            print(' Código..: {}'.format(regAntCodigo))
            print('\nConfirma a exclusão ?\n')
            confirmar   = str(input('S/N ? '))

            if confirmar == 's' or confirmar == 'S':
                try:
                    cursor.execute('''
                    DELETE FROM AUTOR WHERE ID_AUTOR = ?
                    ''', (regId))
                    conn.commit()
                except sqlite3.Error as er:
                    print('Erro :', er.message)
                    input('Pressione <ENTER>')
                input('\nAutor apagado. Pressione uma tecla para voltar.')
            else:
                input('\nPressione uma tecla para voltar.')
        else:
            input('\nNenhum autor com esse Id.\nPressione uma tecla para voltar.')
    except sqlite3.Error as er:
        print('Erro :', er.message)
        input('Pressione <ENTER>')


