#Compilador
#Academicos: Marcio J. Rios e Marcelo E. Knob
#github: marciojrios 
#Universidade Federal da Fronteira Sul- UFFS - Compiladores

import csv
import xml.etree.ElementTree as ET
import re

arq = open('lfa.txt', 'r')
texto = arq.readlines()
arq.close()

############################################################################
#################      Criacao do Automato(AFD)       ######################

print(texto)
simbolo = [] #lista de simbolos da linguagem
lista = [] #armazena os tokens em forma de string
incial = []
estadoI = 0 #Estado Inicial S
estadoA = 0 #Contador de estado atual
estadoProd = estadoA #Contador de proximo estado, e utilizado para se criar um novo estado no AF
afnd = [['$']] 
estados = list() #armazena todos os estados criados pelo AF para procurar na lista estados2 as producoes
estados2 = list() #armazena todos os estados em forma de dicionario com todas as suas producoes

for row in texto: #percorre todos os tokens e gramaticas para obter os simbolos e salvar os tokens na list lista 
	ll = []
	if "::=" in row:
		if "<" in row:
			tam = len(row)
			i = 0
		while i < tam:
			if "\n" not in row[i]:
				if row[i].islower() or row[i].isnumeric():
					aux = []
					aux.append(row[i])
					if aux not in simbolo:
						if aux[0] not in simbolo:
							simbolo.append(aux)
			i += 1
	else:
		tam = len(row)
		i=0
		while i<tam:
			if "\n" not in row[i]:
				if i==0 and row[i] not in incial:
					incial.append(row[i])
				ll.append(row[i])
				if row[i] not in afnd[0]:
					simbolo.append([row[i]])
					afnd[0].append(row[i])
			i+=1
		lista.append(ll)

def AddDict(x): #cria um novo estado em estados e um novo dicionario em estados2 com todos os simbolos da linguagem previamente vazios 
	y = x
	y = str(y)
	estados.append(y)
	y = dict()
	for item in simbolo:
		for item2 in item:
			y[item2] = None
	estados2.append(y)

def fetchIndex(): #funcao para obter o indice do estadoA na lista de estados
	j = 0
	for item in estados:
		if str(estadoA) == item:
			return j
		j = j+1

def fetchChar(row, c): #funcao para obter o indice correto que uma string(c) se encontra na linha(row)
	b = 0 
	for cha in row:
		if cha == c:
			return b
		b = b + 1

def insertInto(index, v1, v2): #funcao utilizada para inserir novos valores em um dicionario na lista de dicionarios (*index: qual dicionario na lista, *v1: chave do dicionario, *v2: valor a ser atribuido)
	if(estados2[index].get(v1) != None): #verifica se ja foi inserido algo no indice
		aux1 = (estados2[index].get(v1)) + ',' + v2 #concatena o valor que ja existe no indice com o novo
		estados2[index].update({v1: aux1})
	else:
		estados2[index].update({v1: v2})


AddDict(estadoA);	#adiciona previamente o estado S

for token in lista: #para cada string(token) na lista, executa
	i = 0; #contador da posicao atual no token
	if(i == 0): #verifica se esta na primeira posicao da linha(row)
		while(str(estadoProd) in estados): #increnta o contador de proximo estado caso o estado atual dele ja exista na lista de estados
			estadoProd = estadoProd + 1
		AddDict(estadoProd)
		insertInto(0, token[i], str(estadoProd))
		estadoA = estadoProd
		estadoProd = estadoProd + 1 #apos inserir um novo estado, prepara o contador para inserir outro
	while(i < len(token)): #enquanto o contador da posicao do token for menor que o tamanho do token, executa
		if(i+1 != len(token)): #confere se o caractere atual nao e o ultimo da string
			for item in estados:
				aux = '*'+str(estadoProd)
				if ('*'+str(estadoProd)) == item:
					estadoProd = estadoProd+1
					break
			while str(estadoProd) in estados:
					estadoProd = estadoProd + 1	
			AddDict(estadoProd) #cria um novo estado para o simbolo(producao) no token
			index = fetchIndex()
			estados2[index].update({token[i+1]: str(estadoProd)}) #preenche o estado atual(marcado pelo estadoA) no dicionario com a nova producao
			estadoA = estadoProd #o estado atual se torna o estado da producao
		else: #caso o caractere seja o ultimo da string
			index = fetchIndex()
			aux = '*' + estados[index] 
			estados.remove(str(estadoA)) #remove o nome do estado anteriormente escrito em estados e
			estados.append(aux)			 #atualiza para um estado final
			estadoProd = estadoProd+1
		i = i+1
print(simbolo)
replacesL = [] #lista de nao terminais{S, A, B, etc} que receberam um novo estado
replacesD = {} #dicionario que guarda a relacao do nao terminal e seu novo estado. Ex: {A: 10, B: 14}
i = 0 #index do caracter em cada linha
regra = 0 #salva em qual regra(estado) esta sendo inserido as producoes
epsilon = 0 #se for 1, a gramatica possui epsilon
for a in texto:
	row = str(a)
	print(row)
	if '::=' in row: # verifica se e uma gramatica
		if '&' in row: # verifica se possui epsilon(&)
			epsilon = 1
		else:
			epsilon = 0
		for charac in row: #para cada caractere na linha, executa
			i = fetchChar(row, charac) #pega a posicao atual do caractere na linha
			if i == 0: #verifica se e o primeiro caractere da linha (<)
				if row[i+1] == 'S': #verifica se o proximo caractere e o estado inicial
					if epsilon == 1:
						aux = '*' + 'S' 
						if '*' not in estados[0]:
							estados[0] = aux #se possui epsilon na gramatica, S se torna estado final
					regra = 0 #seta a regra para inserir no estado inicial
				else:
					if row[i+1] in replacesL: #verifica se o nao terminal da regra ja foi transformado em um estado no AF
						regra = int(replacesD.get(row[i+1]))
						if epsilon == 1:
							index = int(replacesD.get(row[i+1]))
							print(index)
							print(estados)
							if '*' not in estados[index]:
								aux = '*' + estados[index]
								estados[regra] = aux
					else: #caso o nao terminal da regra ainda nao tenha sido transformado em um estado novo
						for item in estados: 
							if ('*'+str(estadoProd)) == str(item):
								estadoProd = estadoProd+1
								break
						for item in estados: 
							if str(estadoProd) == str(item):
								estadoProd = estadoProd+1
								break
						if epsilon == 1:
							AddDict('*'+str(estadoProd))
						else:
							AddDict(estadoProd)
						newStr = str(estadoProd)
						regra = estadoProd
						estadoA = estadoProd
						m = row[i+1]
						replacesL.append(m) #adiciona o nome da regra a lista de replaces para indicar que o simbolo que da nome a regra ja tem um estado no AF
						replacesD.update({m: newStr}) #insere no dicionario de replaces o simbolo que da nome a regra e sua transformacao em estado, respectivamente
						estadoProd = estadoProd + 1
			elif [charac] in simbolo: # verifica se o caractere atual da gramatica e um simbolo(terminal)
				if row[i+1] == '<': #verifica se ha um nao terminal apos o terminal
					if row[i+2] == 'S': #verifica se e a regra inicial
						insertInto(regra, charac, '0')
					else:
						aux4 = row
						i = fetchChar(row, charac)
						auxI = i
						if row[i+2] in replacesL: #verifica se o nao terminal apos o terminal possui um estado no AF
							auxRow = row[i+2]
							aux4 = row.replace(row[i+2], (replacesD.get(row[i+2]))) #cria uma copia da gramatica com a substituicao do nao terminal pelo seu estado no AF
							i = i+1
						else:
							pass
						i = fetchChar(aux4, charac)
						var = 0 #confere se e necessario criar um novo estado para o nao terminal ou se ele ja existe
						if aux4[i+2] in estados:
							insertInto(regra, charac, str(replacesD.get(auxRow))) #insere a producao no dicionario correto
							var = 1  #nao e preciso criar um novo estado
							estadoA = estadoProd
						if ('*'+aux4[i+2]) in estados:
							insertInto(regra, charac, str(replacesD.get(auxRow)))
							var = 1  #nao e preciso criar um novo estado
							estadoA = estadoProd
						if var == 0:
							for item in estados: 
								if ('*'+str(estadoProd)) == str(item):
									estadoProd = estadoProd+1
									break
							for item in estados: 
								if str(estadoProd) == str(item):
									estadoProd = estadoProd+1
									break
							AddDict(estadoProd) #cria um novo estado para inserir a producao
							newStr = str(estadoProd)
							estadoA = estadoProd
							insertInto(regra, charac, str(estadoProd)) #verifica se ja foi inserido algo no indice, concatena o valor que ja existe no dindice com o novo
							m = row[i+2]
							replacesL.append(m)
							replacesD.update({m: newStr})
							estadoProd = estadoProd + 1
						i = auxI

				else: #caso haja apenas um terminal na producao
					for item in estados: 
						if ('*'+str(estadoProd)) == str(item):
							estadoProd = estadoProd+1
							break
					for item in estados: 
						if str(estadoProd) == str(item):
							estadoProd = estadoProd+1
							break
					AddDict('*'+str(estadoProd)) #cria o novo estado como final
					insertInto(regra, charac, str(estadoProd))
					estadoA = estadoProd
					estadoProd = estadoProd+1

			i= i+1

def printTable(): #exibe o AF
	i = 0
	for dicionario in estados2:
		print(estados[i])
		print(dicionario)
		print('\n')
		i = i + 1

printTable() #exibe o AFND

i = 0
for item in estados: #para cada estado criado, executa
	for simb in simbolo: #para cada simbolo no alfabeto da linguagem, executa
		aux2 = item
		estadoA = aux2
		j = fetchIndex()
		if ',' in str(estados2[j].get(simb[0])): #verifica se o valor atribuido a uma chave especifica de um dicionario possui ','
			aux = estados2[j].get(simb[0])
			aux = aux.split(',') #cria uma lista com os valores de cada lado da virgula como itens da lista
			newSt = []
			for item2 in aux:
				newSt.append(item2) 
			aux = '['  #adiciona conchetes para demarcar um estado criado pela determinizacao
			for item2 in newSt:
				aux = aux+item2 # para cada item que estava separado pela virgula, concatena com os demais
			aux = aux + ']' #fecha o demarcador de estado criado pela determinizacao
			AddDict(aux) #cria um novo estado gerado pela determinizacao
			estados2[j].update({simb[0]: aux}) #atualiza o valor que havia anteriormente atribuido a uma chave no dicionario para o novo estado
			estadoA = aux
			index = fetchIndex()
			for item2 in newSt: # para cada item que estava separado pela virgula, executa o codigo abaixo que insere as producoes dos estados envolvidos na determinizacao no novo estado
				estadoA = item2
				a = fetchIndex()
				if a == None:
					estadoA = '*'+item2
					a = fetchIndex()
				for simb2 in simbolo: #para cada simbo
					if(estados2[a].get(simb2[0])) != None: 
						value = str(estados2[a].get(simb2[0]))
						insertInto(index, simb2[0], value)
					else:
						pass
	i = i+1

printTable() #exibe o AFD
estadosAlcancaveis = ['0']

def rInalcancaveis():
	i = '0'
	cont = 0
	estadoCont = 0
	while(estadoCont != len(estadosAlcancaveis)): # Localizacao dos estados alcancaveis
		for item in simbolo:
			value = estados2[cont].get(item[0])
			if(value in estados):
				if(str(value) not in estadosAlcancaveis):
					estadosAlcancaveis.append(value)
				else:
					pass
			if('*'+str(value) in estados):
				if(str(value) not in estadosAlcancaveis):
					estadosAlcancaveis.append(value)
				else:
					pass
			#if
			#if(item.get() in estados):
			#	estadosAlcancaveis.append(item)
		if(estadoCont + 1 == len(estadosAlcancaveis)):
			estadoCont = estadoCont + 1
		else:
			j = 0
			for item in estados:
				item = item.replace('*', '')
				if(item == estadosAlcancaveis[estadoCont+1]):
					cont = j
				j = j+1
			estadoCont = estadoCont + 1

	inalcancaveis = [] # estados inalcancaveis
	for item in estados: # Eliminacao dos estados que nao estao na lista dos alcancaveis
		inalcancaveis.append(item)
	for item in estados:
		aux = item.replace('*', '')
		if aux in estadosAlcancaveis:
			inalcancaveis.remove(item)

	for item in inalcancaveis:# Eliminacao dos estados que nao estao na lista dos alcancaveis
		j = 0
		for item2 in estados:
			if item2 == item:
				estados.remove(item2)
				del estados2[j]
				break
			j = j + 1

	if(len(inalcancaveis) > 0):
		return 'false'
	else:
		return 'true'

def Reach(reach, vivos, item, index):
	for simb in simbolo:
		if(estados2[index].get(simb[0]) != None):
			aux = estados2[index].get(simb[0])
			if(('*'+aux) in estados):
				if item not in vivos:
					vivos.append(item)
			else:
				if aux not in reach:
					reach.append(aux)
		else:
			pass

def eliminacaoInuteis():
	#eliminacao de inalcancaveis
	r = rInalcancaveis()
	while(r == 'false'):
		a = 'true'
		r = rInalcancaveis()

	#eliminacao de mortos
	vivos = []
	tam = len(estados)
	i = 0
	for item in estados:
		reach = ['0']
		if('*' != item[0]):
			j = 0 #contador associado ao tamanho da lista reach
			h = i #contador associado a lista reach
			while(j < len(reach)):
				v = estados[h]
				Reach(reach, vivos, item, h)
				if(j < len(reach)-1):
					v = reach[j+1]
					h = 0
					for item2 in estados:
						if item2 == v:
							break
						else:
							h = h+1
				j = j + 1
		else:
			if item not in vivos:
				vivos.append(item)

		i = i + 1
	
	mortos = []
	for item in estados:
		if item not in vivos:
			mortos.append(item)

	if(len(mortos)>0):
		a = 'true'

	i = 0
	for dictn in estados2: # Eliminacao das producoes envolvendo mortos
		for simb in simbolo:
			if estados2[i].get(simb[0]) in mortos:
				estados2[i].update({simb[0]: None})
		i = i+1

	while(len(mortos)>0):
		i = 0
		for item in estados:
			if item == mortos[0]:
				del estados[i]
				del estados2[i]
				break
			else:
				i = i+1
		del mortos[0]

a = 'true'
while(a == 'true'):
	a = 'false'
	eliminacaoInuteis()

i = 0
for item in estados2:
	for simb in simbolo:
		if estados2[i].get(simb[0]) == None:
			estados2[i].update({simb[0]: 'Error'})
	i = i+1

Error = dict()
for simb in simbolo:
	Error.update({simb[0]: 'Error'})

estados.append('*Error')
estados2.append(Error)

############################################################################
###################       Etapa lexica       ###############################

aux = []
for item in simbolo:
	aux.append(item[0])
simbolo = aux
arquivo = [] #sentencas do arquivo de entrada
with open('CodEntrada.txt', newline='') as inputfile:
	for row in csv.reader(inputfile):
		arquivo.append(row)
		#row = row[0].split(' ')
		#for item in row:
		#	arquivo.append(item)

estadoA = '0' #estado atual do automato
fita = []
line = 0 # linha do arquivo
TS = [] # Tabela de simbolos
fitaS = []
for row in arquivo:
	line = line +1
	for a in row:
		tokens = a.split(' ')
		for token in tokens:
			token = token.replace('\t', '')
			tam = len(token)
			count = 0
			for char in token:
				i = 0
				count = count+1
				print('c: ',count)
				print('t: ',tam)
				for item in estados:
					if item.replace('*', '') == estadoA.replace('*', ''):
						break
					else:
						i = i+1
				#estadoAux = estadoA.replace('*', '')
				for simb in simbolo:
					if char == simb:
						estadoA = estados2[i].get(char)
					else:
						pass
				if char in simbolo:
					estadoA = estados2[i].get(char)
				else:
					print('Simbolo ', char,' nao pertence ao alfabeto da linguagem')
					break

				for item in estados: #serve para inserir o * no estado caso seja final
					if item.replace('*', '') == estadoA.replace('*', ''):
						estadoA = item
						break
				if '*' == estadoA[0]:
					if count == tam:
						fita.append(estadoA)

						break
					else:
						pass
				else:
					if count == tam:
						fita.append('*Error')
						break
					else:
						pass
			TS.append([line, estadoA, token.replace('\t', '')]) # Adiciona a linha, estado final(fita) e rotulo na TS
			estadoA = '0'

xml_parser = "grammar.xml"
tree = ET.parse(xml_parser)
root = tree.getroot()
for symbol in root.iter('Symbol'):
	i = 0
	for x in TS:
		if x[1] == symbol.attrib['Name'] and symbol.attrib['Type'] == "1":
			TS[i][1] = symbol.attrib['Index'] 
		elif x[2] == symbol.attrib['Name'] and symbol.attrib['Type'] == "1":
			TS[i][1] = symbol.attrib['Index']
		i = i+1

def AnaliseSintatica():
	for x in TS:
		fitaS.append(x[1])
		# print(x)      #DEBUG TABELA DE SÍMBOLOS
	fitaS.append(str(0))
	# print("\n Fita de saída:", fitaS, "\n")       #DEBUG FITA DE SAÍDA
	flag = 0
	for erro in TS:
		if erro[1] == '*Error':
			print('Erro Léxico: linha "{}", erro "{}"' .format(erro[0], erro[0]))
			flag = 1
	if flag == 1:
		return 0

	pilha = []
	pilha.append(0)
	erro = 0
	Rc = 0
	controle = 0
	for fita in fitaS:
		while 1:
			if erro == 1 or erro == -1:
				break
			for linha in root.iter('LALRState'):
				if erro == 1 or erro == -1:
					break
				elif linha.attrib['Index'] == str(pilha[-1]):
					for coluna in linha:
						if coluna.attrib['SymbolIndex'] == fita:

							if coluna.attrib['Action'] == '1':             
								controle = 0
								pilha.append(fita)
								pilha.append(int(coluna.attrib['Value']))
								print("\nEmpilha: ", pilha)     #DEBUG EMPILHA
								break

							elif coluna.attrib['Action'] == '2':            
								controle = 1
								for prod in root.iter('Production'):
									if prod.attrib['Index'] == coluna.attrib['Value']:
										Rx = 2 * int(prod.attrib['SymbolCount'])
										break
								if len(pilha) <= Rx:
									erro = 1
									break
								for remove in range(Rx):
									pilha.pop()
									print("\nRedução 1: ", pilha)     #DEBUG REDUÇÃO
								for linhaR in root.iter('LALRState'):
									if linhaR.attrib['Index'] == str(pilha[-1]):
										for colunaR in linhaR:
											if colunaR.attrib['SymbolIndex'] == prod.attrib['NonTerminalIndex']:
												pilha.append(prod.attrib['NonTerminalIndex'])
												pilha.append(int(colunaR.attrib['Value']))
												Rc = 1
												print("\nRedução 2: ", pilha)       #DEBUG APÓS REDUÇÃO
												break
									if Rc == 1:
										Rc = 0
										break

							elif coluna.attrib['Action'] == '4':          
								controle = 0
								erro = -1
								print("\nAceita: ", pilha)      #DEBUG ACEITA
								break
					break
			if controle == 0:
				break

	if erro != -1:
		print("\nErro de sintaxe!\n")

print(arquivo)
print(estadosAlcancaveis)
print(simbolo)
printTable()
print(fita)
print(TS)
AnaliseSintatica()