import mysql.connector
from time import sleep
hora = 10 #valor da mão de obra
energia_hora = 0.10 #valor gasto em energia/hora
vida_util = 1 #valor gasto de depreciação da impressora/hora
valor_embalagem = 5 #valor aproximado gasto em embalagens
margem_falha = 0.10 #10% do custo para cobrir possíveis reimpressões
comissao_market = 0.14 #14% de comissão do anúncio em marketplace, partindo do valor maior

def conectar():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='calculadora_custo'
    )
def criar_tabela():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute('''
        create table if not exists produtos (
            id int auto_increment primary key,
            nome varchar(30) not null,
            valor_filamento decimal(10,2) not null,
            peso decimal(10,2) not null,
            tempo decimal(10,2) not null,
            tempo_prod decimal(10,2) not null,
            margem decimal(10,2) not null,
            custo_tot decimal(10,2) not null,
            valor_final decimal(10,2) not null,
            valor_com_comissao decimal(10,2) not null,
            lucro decimal(10,2) not null,
            criado_em timestamp default current_timestamp
        )
    ''')
    conexao.commit()
    cursor.close()
    conexao.close()

def salvar_produto(nome, valor_filamento, peso, tempo, tempo_prod, margem, custo_tot, valor_final, valor_com_comissao, lucro):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute('''
        insert into produtos (nome, valor_filamento, peso, tempo, tempo_prod, margem, custo_tot, valor_final, valor_com_comissao, lucro)
        values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ''', (nome, valor_filamento, peso, tempo, tempo_prod, margem, custo_tot, valor_final, valor_com_comissao, lucro))
    conexao.commit()
    cursor.close()
    conexao.close()

def listar_produtos():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute('select id, nome, valor_final, criado_em from produtos order by criado_em desc')
    produtos = cursor.fetchall()
    cursor.close()
    conexao.close()
    return produtos

def carregar_produto(id):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute('select * from produtos where id = %s', (id,))
    produto = cursor.fetchone()
    cursor.close()
    conexao.close()
    return produto

def excluir_produto(id):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute('delete from produtos where id = %s', (id,))
    conexao.commit()
    cursor.close()
    conexao.close()

criar_tabela()

while True:
    print('----Calculadora Custo----')
    print('[1] Novo cálculo\n[2] Ver produtos salvos\n[3] Excluir produto salvo\n[0] Sair')
    opcao = input('').strip()
    if opcao == '0':
        break
    elif opcao == '1':
        produtos = listar_produtos()
        if produtos:
            print('Produtos salvos: ')
            for p in produtos:
                print(f' [{p[0]}] {p[1]} - R${p[2]:.2f} ({p[3].strftime("%d/%m/%Y")})')
            escolha = input('\nCarregar produto? Digite ID ou ENTER para novo: ').strip()

            if escolha.isdigit():
                prod = carregar_produto(int(escolha))
                _, nome, valor_filamento, peso, tempo, tempo_prod, margem, custo_tot, valor_final, lucro, _ = prod
                print(f'\nProduto "{nome}" carregado com sucesso!')
                print(f'Valor final: R${valor_final:.2f} | Lucro: R${lucro:.2f}')
                continue
        valor_filamento = float(input('Valor do filamento/kg: R$'))
        peso = float(input('Quantas gramas usadas: '))
        tempo = float(input('Tempo de impressão em horas: '))
        tempo_prod = float(input('Tempo de processamento do produto em horas: '))
        margem = float(input('Margem de lucro em %: '))

        margem_lucro = margem / 100
        peso_kg = peso / 1000
        custo_filam = valor_filamento * peso_kg
        custo_energia = tempo * energia_hora
        custo_mobra = tempo_prod * hora
        desgaste = vida_util * tempo

        custo_tot = custo_filam + custo_energia + custo_mobra + desgaste + valor_embalagem
        custo_ajustado = custo_tot * (1 + margem_falha)
        valor_final = (custo_ajustado * (1 + margem_lucro))
        valor_com_comissao = valor_final * (1 + comissao_market)
        lucro = valor_final - custo_ajustado

        print('-')
        sleep(0.6)
        print('--')
        sleep(0.6)
        print('---')
        sleep(0.6)

        print(f'Custo do filamento utilizado: R${custo_filam:.2f}')
        print(f'Custo em energia: R${custo_energia:.2f}')
        print(f'Custo mão de obra: R${custo_mobra:.2f}')
        print(f'Custo de desgaste: R${desgaste:.2f}')
        print(f'Custo total: R${custo_ajustado:.2f}')
        print(f'Comissão do Marketplace: R${valor_com_comissao-valor_final:.2f}')
        print('-' * 30)
        print(f'Preço final sugerido: R${valor_com_comissao:.2f}\nLucro de R${lucro:.2f}')
        print('-' * 30)
        salvar = input('Deseja salvar este produto? [S/N] ').strip().upper()
        if salvar == 'S':
            nome = input('Nome do produto: ').strip()
            salvar_produto(nome, valor_filamento, peso, tempo, tempo_prod, margem, custo_tot, valor_final, valor_com_comissao, lucro)
            print('Produto salvo com sucesso!')

        resp = str(input('Quer continuar? [S/N] ')).strip().upper()
        if resp == 'N':
            break

    elif opcao == '2':
        produtos = listar_produtos()
        if produtos:
            print('\nProdutos salvos:')
            for p in produtos:
                print(f' [{p[0]}] {p[1]} - R${p[2]:.2f} ({p[3].strftime("%d/%m/%Y")})')
        else:
            print('Nenhum produto salvo ainda.')

    elif opcao == '3':
        produtos = listar_produtos()
        if produtos:
            print('\nProdutos salvos:')
            for p in produtos:
                print(f' [{p[0]}] {p[1]} - R${p[2]:.2f} ({p[3].strftime("%d/%m/%Y")})')
            escolha = input('\nDigite o ID do produto que deseja excluir: ').strip()
            if escolha.isdigit():
                confirma = input(f'Tem certeza que deseja excluir o produto {escolha}? [S/N]').strip().upper()
                if confirma == 'S':
                    excluir_produto(int(escolha))
                    print('Produto excluído com sucesso!')
            else:
                print('ID inválido.')
        else:
            print('Nenhum produto salvo ainda.')
