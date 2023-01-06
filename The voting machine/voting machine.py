# João Pedro Rodrigues Vieira | 32281730
# Jônatas de Brito Silva | 32283792
# Projeto de Urna Eletrônica - Algoritmos e Programação I


# Função que emite uma mensagem para confirmação de uma ação
def verificacao(prompt=" "):
    perg = str(input(f'{prompt} SIM/NÃO: ')).strip().upper()
    while perg not in 'SIMNÃO':
        perg = str(input(f'{prompt} SIM/NÃO: ')).strip().upper()
    return True if perg == 'SIM' else False


# Calcula a quantidade de votos para uma categoria
def apuracao(lista, modo="total"):
    branco = lista[0][-1]
    nulo = lista[0][-2]
    total_invalidos = sum(lista[0])
    total_validos = 0
    for quant in lista[1::]:
        total_validos += quant[0]
    if modo.lower() == "branco":
        return branco
    elif modo.lower() == "nulo":
        return nulo
    elif modo.lower() == "valido":
        return total_validos
    return total_invalidos + total_validos


# Gera uma tabela referente aos dados da votação de uma categoria
def tabela(lista, titulo):
    print(f"{f'| RANKING DO RESULTADO PARA {titulo.upper()} |':=^80}")
    posicao = 1
    total = apuracao(lista)
    total_val = apuracao(lista, 'valido')
    brancos = apuracao(lista, 'branco')
    nulos = apuracao(lista, 'nulo')
    if total_val > 0:
        print(f"{'Nome':^30}|{'Partido':^10}|{'Total de Votos':^20}|{'% votos válidos':^20}")
        for candidato in sorted(lista[1::], key= lambda lista: lista[0], reverse=True):
            porc_validos = (candidato[0] / total_val) * 100
            print(f"{f'{posicao}°':<3}{candidato[1]:^27}|{candidato[3]:^10}|{candidato[0]:^20}|{porc_validos:^20.2f}")
            posicao += 1
        print("="*80)
        print(f"Total de Votos = {total}")
        print(f"Total de Votos válidos e % = {total_val} ({100*(total_val/total):.2f} %)")
        print(f"Total de brancos e % = {brancos} ({100*(brancos/total):.2f} %)")
        print(f"Total de nulos e % = {nulos} ({100*(nulos/total):.2f} %)")
        print("="*80)
    else:
        print()
        print(f"Não foram computados votos válidos para {titulo.capitalize()}")
    print()


# Listas temporárias
candidato = list()
eleitor = list()

# Lista verificadora
num_eleitoral_pref = [-2, -1]
num_eleitoral_gov = [-2, -1]
num_eleitoral_pres = [-2, -1]
cpf_dos_eleitores = list()

# Lista de armazenamento de dados
presidente = [[0, 0]]
governador = [[0, 0]]
prefeito = [[0, 0]]
eleitorado = [[], []]
partidos = list()

# Menu de opções e suas funcionalidades
opcao = "0"
while opcao != "6":
    print(f"{'| MENU - SIMULADOR DO SISTEMA DE VOTAÇÃO |':=^80}")
    print('\n1. Cadastrar Candidatos\n2. Cadastrar Eleitores\n3. Votar\n4. Apurar Resultados\n5. Relatório e Estatísticas\n6. Encerrar\n')
    opcao = str(input("Opção escolhida: "))
    while opcao not in "123456":
        opcao = (input("Opção inválida, escolha novamente: "))

    if opcao == "1":

        # Cadastro de candidatos
        opc1 = True
        while opc1:
            print("="*80)
            print(f"{'| CADASTRO DE CANDIDATOS |':=^80}")
            print()
            candidato.append(0)
            candidato.append(str(input('1. Nome do candidato: ')).title().strip())
            candidato.append(int(input('2. Número: ')))
            while candidato[2] < 1:
                del candidato[2]
                candidato.append(int(input('2. Número: ')))
            candidato.append(str(input('3. Partido: ')).upper().strip())
            candidato.append(str(input('4. Cargo: ')).capitalize().strip())
            while candidato[4] not in ['Presidente', 'Governador', 'Prefeito']:
                del candidato[4]
                candidato.append(str(input('4. Cargo: ')).capitalize().strip())

            # Apresentação das  informações do candidato e a confirmação do cadastro
            print(f"Informações do candidato:")
            for info in range(len(candidato[1::])):
                print(f'{info+1}. {candidato[info+1]}')
            confirma_cadastro = verificacao("Confirma o cadastro do candidato?")

            # Atribuição da lista do candidato a sua respectiva categoria
            if confirma_cadastro:
                partido = [0, candidato[3]]
                if partido not in partidos:
                    partidos.append(partido.copy())
                if candidato[4] == 'Presidente':
                    if candidato[2] not in num_eleitoral_pres:
                        num_eleitoral_pres.append(candidato[2])
                    presidente.append(candidato.copy())
                elif candidato[4] == 'Governador':
                    if candidato[2] not in num_eleitoral_gov:
                        num_eleitoral_gov.append(candidato[2])
                    governador.append(candidato.copy())
                elif candidato[4] == 'Prefeito':
                    if candidato[2] not in num_eleitoral_pref:
                        num_eleitoral_pref.append(candidato[2])
                    prefeito.append(candidato.copy())
                candidato.clear()
            else:
                candidato.clear()
                opc1 = verificacao("Deseja continuar?")
                if opc1:
                    continue
                break
            opc1 = verificacao("Deseja continuar?")
            print()
    
    if opcao == "2":

        # Cadastro dos eleitores
        opc2 = True
        while opc2:
            print("="*80)
            print(f"{'| CADASTRO DE ELEITORES |':=^80}")
            print()
            eleitor.append(str(input("Nome do eleitor: ")).strip().title())
            eleitor.append(str(input("Número do CPF: ").strip()))
            for cpf in range(len(eleitorado[1])):
                while eleitor[1] == eleitorado[1][cpf] or (len(eleitor[1]) != 4 or eleitor[1].isnumeric() == False):
                    del eleitor[1]
                    eleitor.append(str(input("CPF inválido. Digite novamente: ")))
            eleitorado[0].append(eleitor[0])
            eleitorado[1].append(eleitor[1])
            eleitor.clear()
            opc2 = verificacao("Deseja continuar?")
            print()

    if opcao == "3":

        # Sistema de votação para prefeito, governador e presidente
        print("="*80)
        print(f"{'| VOTAÇÃO |':=^80}")
        print()

        # Entrada do CPF do eleitor e a verificação de sua situação
        cpf = str(input("CPF do eleitor: ")).strip()
        while cpf in cpf_dos_eleitores:
            print(f"O eleitor de CPF {cpf} já realizou uma votação. Digite um CPF válido.")
            cpf = str(input("CPF do eleitor: ")).strip() 
        if cpf not in eleitorado[1]:
            print(f"O CPF {cpf} não consta na base de dados do sistema.")
            continue
        cpf_dos_eleitores.append(cpf)
        print()

        # Votação para prefeito
        confirm = False
        while not confirm:
            print(f"{'| Prefeito |':-^80}")
            voto = int(input("Voto em Branco: -1\nVoto Nulo: -2\nNúmero do candidato: "))
            while voto not in num_eleitoral_pref:
                    voto = int(input("Número inválido. Digite novamente: "))
            if voto == -1:
                print("Opção selecionada: Voto em Branco.")
                confirm = verificacao("Confirma o voto?")
                if confirm:
                    prefeito[0][-1] += 1
            elif voto == -2:
                print("Opção selecionada: Voto Nulo.")
                confirm = verificacao("Confirma o voto?")
                if confirm:
                    prefeito[0][-2] += 1
            else:
                for cand in prefeito:
                    if cand != prefeito[0] and cand[2] == voto:
                        print(f"Nome: {cand[1]}")
                        print(f"Partido: {cand[3]}")
                        confirm = verificacao("Confirma o voto?")
                        if confirm:
                            cand[0] += 1
        
        # Votação para governador
        confirm = False
        while not confirm:
            print(f"{'| Governador |':-^80}")
            voto = int(input('Voto em Branco: -1\nVoto Nulo: -2\nNúmero do candidato: '))
            while voto not in num_eleitoral_gov:
                    voto = int(input("Número inválido. Digite novamente: "))
            if voto == -1:
                print("Opçao selecionada: Voto em Branco.")
                confirm = verificacao("Confirma o voto?")
                if confirm:
                    governador[0][-1] += 1
            elif voto == -2:
                print("Opção selecionada: Voto Nulo.")
                confirm = verificacao("Confirma o voto?")
                if confirm:
                    governador[0][-2] += 1
            else:
                for cand in governador:
                    if cand != governador[0] and cand[2] == voto:
                        print(f"Nome: {cand[1]}")
                        print(f"Partido: {cand[3]}")
                        confirm = verificacao("Confirma o voto?")
                        if confirm:
                            cand[0] += 1  
        
        # Votação para Presidente
        confirm = False
        while not confirm:
            print(f"{'| Presidente |':-^80}")
            voto = int(input("Voto em Branco: -1\nVoto Nulo: -2\nNúmero do candidato: "))
            while voto not in num_eleitoral_pres:
                    voto = int(input('Número inválido. Digite novamente: '))
            if voto == -1:
                print("Opção selecionada: Voto em Branco.")
                confirm = verificacao("Confirma o voto?")
                if confirm:
                    presidente[0][-1] += 1
            elif voto == -2:
                print("Opção selecionada: Voto Nulo.")
                confirm = verificacao("Confirma o voto?")
                if confirm:
                    presidente[0][-2] += 1
            else:
                for cand in presidente:
                    if cand != presidente[0] and cand[2] == voto:
                        print(f"Nome: {cand[1]}")
                        print(f"Partido: {cand[3]}")
                        confirm = verificacao("Confirma o voto?")
                        if confirm:
                            cand[0] += 1
            print(f"{'| FIM |':=^80}")
            print()

    if opcao == "4":

        # Apresentação dos resultados obtidos por meio de uma tabela estatística
        print(f"{'| CANDIDATOS ELEITOS |':=^80}")
        print()
        # Temos que ter, no mínimo, 2 elementos por lista: votos inválidos e um candidato
        quantidade_candidatos = len(prefeito) + len(governador) + len(presidente)
        if quantidade_candidatos > 5:
            candidatos_eleitos = [
                sorted(prefeito[1::], key= lambda lista: lista[0], reverse=True)[0],
                sorted(governador[1::], key= lambda lista: lista[0], reverse=True)[0],
                sorted(presidente[1::], key= lambda lista: lista[0], reverse=True)[0]
            ]
            print(f"Vencedor das eleições municipais: {candidatos_eleitos[0][1]}")
            print(f"Vencedor das eleições estaduais: {candidatos_eleitos[1][1]}")
            print(f"Vencedor das eleições federais: {candidatos_eleitos[2][1]}")
            print()
        else:
            print("Não foram cadastrados candidatos o suficiente para esta eleição.")
            print()
        tabela(prefeito, 'prefeito')
        tabela(governador, 'governador')
        tabela(presidente, 'presidente')

    if opcao == "5":

        # Verificação dos resultados e da confiabilidade do voto
        print(f"{'| RELATÓRIO E ESTATÍSTICAS |':=^80}")
        print()
        votos_totais = apuracao(presidente) + apuracao(prefeito) + apuracao(governador)
        print(f"{'| LISTA DE ELEITORES |':-^80}")
        print()
        if len(eleitorado[1]) > 0:
            for cidadao in sorted(eleitorado[0]):
                for dados in range(len(eleitorado[0])):
                    if eleitorado[0][dados] == cidadao and eleitorado[1][dados] in cpf_dos_eleitores:
                        print(f"Nome: {cidadao} - CPF: {eleitorado[1][dados]}")
            print()
            print(f"{'| AUDITORIA |':-^80}")
            if len(eleitorado) > 0:
                if votos_totais / len(cpf_dos_eleitores) == 3:
                    print("As eleições foram realizadas com sucesso.")
                    print(f"Total de votos contabilizados: {votos_totais}")
                    print(f"Quantidade total de eleitores: {len(cpf_dos_eleitores)}")
                else:
                    print(f"Há uma incompatibilidade entre o número de eleitores e os votos computados.")
                    print(f"Quantidade de votos esperados: {len(cpf_dos_eleitores)*3}")
                    print(f"Votos obtidos: {votos_totais}")
        else:
            print("Não foram cadastrados eleitores. Realize o cadastro imediatamente.")
            print()
            continue
        print("-"*80)

        # Analisando quais partidos elegeram mais ou menos candidatos
        quantidade_candidatos = len(prefeito) + len(governador) + len(presidente)
        if quantidade_candidatos > 5:
            candidatos_eleitos = [
                sorted(prefeito[1::], key= lambda lista: lista[0], reverse=True)[0],
                sorted(governador[1::], key= lambda lista: lista[0], reverse=True)[0],
                sorted(presidente[1::], key= lambda lista: lista[0], reverse=True)[0]
            ]
            for candidatos in range(len(candidatos_eleitos)):
                for siglas in range(len(partidos)):
                    if candidatos_eleitos[candidatos][3] == partidos[siglas][1]:
                        partidos[siglas][0] += 1
            maior_partido = max(partidos, key= lambda lista: lista[0])
            menor_partido = min(partidos, key= lambda lista: lista[0])
            partido_mais_elegeu = maior_partido[1]
            partido_menos_elegeu = menor_partido[1]
            for part in partidos:
                if part != maior_partido and part[0] == maior_partido[0]:
                    partido_mais_elegeu += f", {part[1]}"
                if part != menor_partido and part[0] == menor_partido[0]:
                    partido_menos_elegeu += f", {part[1]}"
            print(f"Partido ou partidos que mais elegeram: {partido_mais_elegeu}")
            print(f"Partido ou partidos que menos elegeram: {partido_menos_elegeu}")
            print('='*80)
        else:
            print("Não foram cadastrados candidatos o suficiente para esta eleição.")
        print()

print(f"{'| URNA ENCERRADA |':=^80}")
