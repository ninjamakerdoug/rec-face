# -*- coding: utf-8 -*-

import json, time, cv2, os, WEB, sys, busca, random
import subprocess as s
import numpy as np
import constroiBancoDeDados as bd
from pygame import mixer
from BuscaWeb import BuscaWeb
import pandas as pd
from time import strftime
from datetime import datetime, timedelta
import pendulum as pl
from reportlab.pdfgen import canvas
import matplotlib.pyplot as plt



class Chatbot():
    def __init__(self, nome):
        try:
            memoria = open(nome+'.json','r')
        except FileNotFoundError:
            with open(nome+'.json','w') as memoria:
                memoria.write('[{"Bianca":{"nome":"Bianca","nascimento":"01/01/2001","admissao":"01/02/2018","Rg":"12.345.678/9","profissao":"veterinária","salario":"4.300,00","ponto":{"data":"01/05/2018","entrada":["07:00"],"pausa_ref":["12:00"],"volta_ref":["13:00"],"saida":["17:00"],"extra":[0]}}},{"tchau":"tchau"}]')
            memoria = open(nome+'.json','r')
        self.nome = nome
        self.conhecidos, self.frases = json.load(memoria)
        memoria.close()
        self.historico = [None,]



    def escuta(self,frase=None):
        if frase == None:
            frase = input('>: ')
        frase = str(frase)

        if 'executar ' in frase:
            return frase
        frase = frase.lower()
        #frase = frase.replace('é','eh')
        return frase



    def pensa(self,frase):

        lista = ['Em que posso ajudá-lo?','Pois não?','E aí, o que manda?']
        senha ='doug'

        dataEhora = datetime.now()
        ano = str(dataEhora.year)
        mes = str(dataEhora.month)
        dia = str(dataEhora.day)
        hora = str(strftime('%H:%M'))

        ultimaFrase = self.historico[-1]
        
        ################################

        if frase == 'bot':
            pesquisa = WEB.analisar()
            busca_nome = str(pesquisa).rstrip().lstrip()
            if busca_nome in self.conhecidos:
                frases_salvas = str(random.choice(lista))
                return f'{frases_salvas}'
            else:
                return 'Olá, qual o seu nome?'

        elif str(ultimaFrase) in lista:
            #o chatbot usará a api do google para te retornar uma resposta
            #existem limitações
            cb = BuscaWeb()
            resultado = cb.start(frase)
            chave = str(resultado[0])
            
            if(chave == "nenhum resultado"):
                pesquisa = busca.executaIAsmim(frase)
                resposta = str(pesquisa)
                if resposta == 'Não entendi':
                    respostas = ['Não encontrei nada em minhas fontes...','Desculpe, não achei nada relativo...','Acho que essa eu não vou conseguir te responder.',]
                    respostas = str(random.choice(respostas))
                    return (respostas)
                else:
                    return resposta
            else:
                return chave

        #######################################

        elif frase == 'salvar face':
            return 'Qual o nome da pessoa?'

        elif ultimaFrase == 'Qual o nome da pessoa?':
            self.name = self.pegaNome(frase)
            
            if self.name in self.conhecidos:
                return 'Este nome já está cadastrado, deseja alterar fotos?'
            else:
                with open('input.txt','w') as p:
                    p.write(self.name.lower())
                WEB.main()
                self.conhecidos.append(self.name)
                self.gravaMemoria()
                with open('input.txt','w') as p:
                    p.write('')
                return 'Face salva no Banco de Dados'

        elif ultimaFrase == 'Este nome já está cadastrado, deseja alterar fotos?':
            if frase == 'sim' or frase == 's':
                with open('input.txt','w') as p:
                    p.write(self.name.lower())
                WEB.main()
                with open('input.txt','w') as p:
                    p.write('')
                return ''
            else:
                return 'Cadastro cancelado'

        ###################################################

        elif frase == 'novo funcionario':
            return 'Certo, qual o nome do funcionário?'
        elif ultimaFrase == 'Certo, qual o nome do funcionário?':
            if frase in self.conhecidos:
                return 'Este nome já está cadastrado.'
            else:
                self.name = self.pegaNome(frase)
            return 'Data de nascimento? Siga o exemplo ( 02/02/2002 ).'
        elif ultimaFrase == 'Data de nascimento? Siga o exemplo ( 02/02/2002 ).':
            self.nascimento = str(frase)
            return 'Data da admissão? Siga o exemplo ( 20/10/2020 ).'
        elif ultimaFrase == 'Data da admissão? Siga o exemplo ( 20/10/2020 ).':
            self.admissao = str(frase)
            return 'Qual o RG do novo funcionário? Siga o exemplo ( 12.345.678/9 ).'
        elif ultimaFrase == 'Qual o RG do novo funcionário? Siga o exemplo ( 12.345.678/9 ).':
            self.rg = str(frase)
            return 'Qual será a profissão?'
        elif ultimaFrase == 'Qual será a profissão?':
            self.profissao = str(frase)
            return 'Salário? Siga o exemplo ( 1.200,00 ).'
        elif ultimaFrase == 'Salário? Siga o exemplo ( 1.200,00 ).':
            self.salario = str(frase)
            return 'Qual será o horário de entrada do novo funcionário? Siga o exemplo ( 07:00 ).'
        elif ultimaFrase == 'Qual será o horário de entrada do novo funcionário? Siga o exemplo ( 07:00 ).':
            self.entrada = str(frase)
            return 'Que horas ele sairá para o intervalo?'
        elif ultimaFrase == 'Que horas ele sairá para o intervalo?':
            self.pausa_ref = str(frase)
            return 'Que horas acaba o intervalo?'
        elif ultimaFrase == 'Que horas acaba o intervalo?':
            self.volta_ref = str(frase)
            return 'Horário da saída?'
        elif ultimaFrase == 'Horário da saída?':
            self.saida = str(frase)
            self.extra = 0
            return 'Coloque uma foto do funcionário em frente a câmera para o reconhecimento facial, quando estiver pronto, digite "ok".'
        elif ultimaFrase == 'Coloque uma foto do funcionário em frente a câmera para o reconhecimento facial, quando estiver pronto, digite "ok".':
            if frase == 'ok':
                with open('input.txt','w') as p:
                    p.write(self.name.lower())
                WEB.main()
                return 'Confirma o cadastro do funcionário?'
            else:
                return 'Cadastro cancelado!'
        elif ultimaFrase == 'Confirma o cadastro do funcionário?':
            if frase == 's' or frase == 'sim':
                self.conhecidos[self.name.lower()] = {"nome":self.name,"nascimento":self.nascimento,"admissao":self.admissao,"Rg":self.rg,"profissao":self.profissao,"salario":self.salario,"ponto":{"data":[f"{dia}/{mes}/{ano}"],"entrada":[self.entrada],"pausa":[self.pausa_ref],"retorno":[self.volta_ref],"saida":[self.saida],"extra":[self.extra]}}
                self.gravaMemoria()
                return 'Cadastro realizado com sucesso!'
            else:
                return 'Cadastro cancelado!'

        ###################################################

        elif frase == 'mostrar ponto':
            return 'De qual funcionário?'
        elif ultimaFrase == 'De qual funcionário?':
            if frase in self.conhecidos:
                if 'admissao' in self.conhecidos[frase]:
                    '''
                    data = self.conhecidos[frase]['ponto']['data']
                    entrada = self.conhecidos[frase]['ponto']['entrada']
                    pausa = self.conhecidos[frase]['ponto']['pausa']
                    retorno = self.conhecidos[frase]['ponto']['retorno']
                    saida = self.conhecidos[frase]['ponto']['saida']
                    num_dias = int(len(data))
                    num_entrada = int(len(entrada))
                    num_pausa = int(len(pausa))
                    num_retorno = int(len(retorno))
                    num_saida = int(len(saida))
                    '''
                    #if num_dias != num_saida:
                    try:
                        df = pd.DataFrame(self.conhecidos[frase]['ponto'])
                        return f'\n\n{df}\n\n'
                    except:
                        return 'Este funcionário não encerrou seu turno.'
                else:
                    return 'Esta pessoa está em meus registros, mais não como um funcionário.'
            else:
                return 'Não há ninguém com esse nome em meus registros.'

        ############################################################

        if frase == 'bater ponto':
            pesquisa = WEB.analisar()
            self.name = str(pesquisa).rstrip().lstrip()
            if self.name in self.conhecidos:
                if 'admissao' in self.conhecidos[self.name]:
                    return f'Olá {self.name.title()}! Qual é o ponto?'
                else:
                    return f'Olá {self.name.title()}! Você não é registrado como funcionário.'
            else:
                return 'Você não está no meu banco de dados!'
        elif 'Qual é o ponto?' in str(ultimaFrase):
            if frase == 'entrada':
                self.conhecidos[self.name]['ponto']['data'].append(f'{dia}/{mes}/{ano}')
                self.conhecidos[self.name]['ponto']['entrada'].append(f'{hora}')
                self.gravaMemoria()
                return 'Entrada Registrada!'
            elif frase == 'pausa':
                self.conhecidos[self.name]['ponto']['pausa'].append(f'{hora}')
                self.gravaMemoria()
                return 'Pausa Registrada!'
            elif frase == 'retorno':
                self.conhecidos[self.name]['ponto']['retorno'].append(f'{hora}')
                self.gravaMemoria()
                return 'Retorno Registrado!'
            elif frase == 'saída':
                #calcular hora extra
                
                #pegando a data que o funcionário entrou
                data_entrada = self.conhecidos[self.name]['ponto']['data'][-1].replace('/',' ')
                data_entrada = data_entrada.split()
                dia_entrada = int(data_entrada[0])
                mes_entrada = int(data_entrada[1])
                ano_entrada = int(data_entrada[2])

                #pegando o horário que o funcionário entrou
                hora_entrou = self.conhecidos[self.name]['ponto']['entrada'][-1].replace(':',' ')
                hora_entrou = hora_entrou.split()
                hora_entrada = int(hora_entrou[0])
                minuto_entrada = int(hora_entrou[1])
                        
                #pausa
                h_pausa = self.conhecidos[self.name]['ponto']['pausa'][-1].replace(':',' ')
                h_pausa = h_pausa.split()
                hora_pausa = int(h_pausa[0])
                minuto_pausa = int(h_pausa[1])
        
                #retorno
                h_retorno = self.conhecidos[self.name]['ponto']['retorno'][-1].replace(':',' ')
                h_retorno = h_retorno.split()
                hora_retorno = int(h_retorno[0])
                minuto_retorno = int(h_retorno[1])
                
                #saída
                h_saida = hora.replace(':',' ')
                h_saida = h_saida.split()
                hora_saida = int(h_saida[0])
                minuto_saida = int(h_saida[1])

                hora_certa = self.conhecidos[self.name]['ponto']['saida'][0].replace(':',' ')
                hora_certa = hora_certa.split()
                hora_certa_saida = int(hora_certa[0])
                minuto_certo_saida = int(hora_certa[1])

                # Comparando datas/horários de entrada e saída                 
                inicio_dia = pl.datetime(int(ano_entrada),int(mes_entrada), int(dia_entrada), int(hora_entrada), int(minuto_entrada))
                fim_dia    = pl.datetime(int(ano),int(mes), int(dia), hora_saida, minuto_saida)
                period     = pl.period(inicio_dia, fim_dia)

                #verificando quantas horas e minutos tem entre o horário de entrada e saída
                horas = period.hours
                minutos = period.minutes

                if int(horas) < 10:
                    horas = '**'
                    minutos = '**'

                if int(horas) == 10 and int(minutos) < 6:
                    horas = '--'
                    minutos = '--'

                if int(horas) == 10 and int(minutos) >= 6:
                    horas = 0

                if int(horas) > 10:
                    horas = int(horas) - 10

                if int(minutos) < 10:
                    minutos = f'0{minutos}'

                extras = f'{horas}:{minutos}'
                self.conhecidos[self.name]['ponto']['saida'].append(f'{hora}')
                self.conhecidos[self.name]['ponto']['extra'].append(f'{extras}')
                self.gravaMemoria()
                return 'Saída Registrada!'

        ############################################################
        
        elif frase == 'oi bot' or frase == 'oi':
            pesquisa = WEB.analisar()
            resposta = str(pesquisa).rstrip().lstrip()
            if resposta in self.conhecidos:
                return f'Oi {resposta}'
            else:
                return 'Olá, qual o seu nome?'
                
        elif ultimaFrase == 'Olá, qual o seu nome?' or ultimaFrase == 'Desculpe, não entendi, pode repetir por favor?':
            if frase in self.conhecidos:
                return f'Você não é {resposta}'
            else:
                self.name = self.pegaNome(frase)
                frase = self.respondeNome(self.name)
                with open('input.txt','w') as p:
                    p.write(self.name.lower())
                WEB.main()
                with open('input.txt','w') as p:
                    p.write('')
                return frase

        elif 'Qual a sua idade?' in str(ultimaFrase):
            if 'eu tenho ' in frase:
                frase = frase.replace('eu tenho ','')
                if 'anos' in frase:
                    frase = frase.replace('anos','')        
                    if frase.isnumeric():
                        self.idade = frase
                        return 'Que tipo de música você gosta?'
                else:
                    self.idade = frase
                    return 'Que tipo de música você gosta?'
            else:
                if 'anos' in frase:
                    frase = frase.replace('anos','')        
                    if frase.isnumeric():
                        self.idade = frase
                        return 'Que tipo de música você gosta?'
                else:
                    if frase.isnumeric():
                        self.idade = frase
                        return 'Que tipo de música você gosta?'

        elif ultimaFrase == 'Que tipo de música você gosta?':
            self.estilo = frase
            self.conhecidos[self.name.lower()] = {"nome":str(self.name),"idade":self.idade,"estilo":self.estilo}
            self.gravaMemoria()
            return f'Certo, prazer em conhecê- lo {self.name}!'
            
        #############################################

        elif frase == 'add cardapio':
            return 'Qual será o código do item?'
        elif ultimaFrase == 'Qual será o código do item?':
            if frase.isnumeric():
                if frase in self.frases:
                    self.codigo = frase
                    return 'Este produto já está cadastrado, deseja alterá-lo?'
                else:
                    self.codigo = frase
                    return 'Qual é o ítem?'
            else:
                'Valores informados inválidos!'
        elif ultimaFrase == 'Este produto já está cadastrado, deseja alterá-lo?':
            frase = frase.lower()
            sims = ['sim','s']
            if frase in sims:
                return 'Qual é o ítem?'
            else:
                return 'Operação cancelada!'
        elif ultimaFrase == 'Qual é o ítem?':
            self.item = frase
            return 'Qual o valor?'
        elif ultimaFrase == 'Qual o valor?':
            if frase.isnumeric():
                self.valor = float(frase)
                return 'Qual é o estoque? (Digite qualquer letra caso não queira numerar o ítem)'
        elif ultimaFrase == 'Qual é o estoque? (Digite qualquer letra caso não queira numerar o ítem)':
            if frase.isnumeric():
                self.estoque = int(frase)
                self.frases[self.codigo] = {"codigo":self.codigo,"item":str(self.item),"valor":self.valor,"estoque":self.estoque}
                self.gravaMemoria()
                return 'Ítem salvo com sucesso!'
            else:
                frase = 'x'
                self.estoque = frase
                self.frases[self.codigo] = {"codigo":self.codigo,"item":str(self.item),"valor":self.valor,"estoque":self.estoque}
                self.gravaMemoria()
                return 'Ítem salvo com sucesso!'

        elif frase == 'apagar item':
            return 'Qual o código do ítem que será apagado?'
        elif ultimaFrase == 'Qual o código do ítem que será apagado?':
            if frase in self.frases and frase.isnumeric():
                if 'estoque' in self.frases[frase]:
                    del self.frases[frase]
                    self.gravaMemoria()
                    return f'Ítem {frase} apagado do cardápio!'
                else:
                    return 'Valores informados inválidos!'
            else:
                return 'Valores informados inválidos!'
        
        elif frase == 'cardapio':
            cardapio = []
            for i in self.frases:
                if i.isnumeric():
                    if 'estoque' in self.frases[i]:
                        cardapio.append(self.frases[i])
            df = pd.DataFrame(cardapio)
            '''
            pdf = canvas.Canvas('cardapio.pdf')
            pdf.drawString(10,50,'Olá')
            pdf.save()
            '''
            fig = plt.figure(figsize=(9,2))
            ax = plt.subplot(111)
            ax.axis('off')
            ax.table(cellText=df.values, colLabels=df.columns, bbox=[0,0,1,1])
            plt.savefig('cardapio.jpg')
            return 'teste de cardapio ok'

        ###########################################################

        elif frase == 'mesas abertas':
            try:
                mesa = []
                for i in self.frases:
                    if i.isnumeric():
                        if 'responsavel' in self.frases[i]:
                            mesa.append(self.frases[i])
                df = pd.DataFrame(mesa)
                df = df[['mesa','total']]
                return f'\n\n{df}\n\n'
            except KeyError:
                return 'Nenhuma mesa aberta.'

        ###########################################################

        elif frase == 'novo cliente':
            return 'Qual será a mesa?'
        elif ultimaFrase == 'Qual será a mesa?':
            if frase.isnumeric():
                if (int(frase) < 100):
                    if frase in self.frases:
                        self.mesa = frase
                        return 'Esta mesa já está ocupada, deseja alterá-la?'
                    else:
                        self.mesa = frase
                        return 'Qual o nome do responsável pela mesa?'
                else:
                    return '99 é o número máximo de mesas. '
            else:
                'Valores informados inválidos!'
        elif ultimaFrase == 'Esta mesa já está ocupada, deseja alterá-la?':
            frase = frase.lower()
            sims = ['sim','s']
            if frase in sims:
                return 'Qual o nome do responsável pela mesa?'
            else:
                return 'Operação cancelada!'
        elif ultimaFrase == 'Qual o nome do responsável pela mesa?':
            self.responsavel = frase
            self.total = 0
            self.frases[self.mesa] = {"mesa":self.mesa,"responsavel":str(self.responsavel),"consumo": {"item":[],"qtd":[],"valor_venda":[]},"total":0}
            self.gravaMemoria()
            return 'Mesa cadastrada com sucesso!'

        ##################################################

        elif frase == 'venda' or frase == 'cancelar venda':
            self.comando = frase
            return 'Qual o número da mesa?'
        elif ultimaFrase == 'Qual o número da mesa?':
            if frase.isnumeric():
                if (int(frase) < 100):
                    if frase in self.frases:
                        self.mesa = frase
                        return 'Qual o código do ítem?'
                    else:
                        self.mesa = frase
                        return 'Não há cadastro nessa mesa'
                else:
                    return '99 é o número máximo de mesas.'
            else:
                'Valores informados inválidos!'
        elif ultimaFrase == 'Qual o código do ítem?':
            if frase in self.frases:
                if frase.isnumeric():
                    self.codigo = frase
                    self.item = self.frases[frase]['item']
                    self.valor = self.frases[frase]['valor']
                    self.estoque = self.frases[frase]['estoque']
                    return 'Quantidade?'
                else:
                    return 'Valores informados inválidos!'
            else:
                return 'Ítem não encontrado!'
        elif ultimaFrase == 'Quantidade?':
            if frase.isnumeric():
                self.quantidade = int(frase)
                self.valor_venda = int(self.valor) * self.quantidade
                
                try:
                    if self.comando == 'cancelar venda':
                        try:
                            self.atualiza_estoque = self.estoque+self.quantidade
                            self.estoque = self.atualiza_estoque
                        except:
                            self.atualiza_estoque = self.estoque
                    elif self.comando == 'venda':
                        self.atualiza_estoque = self.estoque-self.quantidade
                        self.estoque = self.atualiza_estoque
                except:
                    self.atualiza_estoque = self.estoque

                soma = self.frases[self.mesa]['total']
                if self.comando == 'cancelar venda':
                    self.total = soma - self.valor_venda
                    self.frases[self.mesa]['consumo']['item'].remove(self.item)
                    self.frases[self.mesa]['consumo']['qtd'].remove(self.quantidade)
                    self.frases[self.mesa]['consumo']['valor_venda'].remove(self.valor_venda) 
                if self.comando == 'venda':    
                    self.total = soma + self.valor_venda
                    self.frases[self.mesa]['consumo']['item'].append(self.item)
                    self.frases[self.mesa]['consumo']['qtd'].append(self.quantidade)
                    self.frases[self.mesa]['consumo']['valor_venda'].append(self.valor_venda)

                self.frases[self.mesa]['total'] = int(self.total)
                self.frases[self.codigo]['estoque'] = self.atualiza_estoque
                self.gravaMemoria()
                if self.comando == 'cancelar venda':
                    return 'Venda cancelada!'
                if self.comando == 'venda':
                    pedido = f'Mesa: {self.mesa}\nPedido: {self.item}\nQuantidade: {self.quantidade}'
                    return f'\n\n{pedido}\n\nVenda realizada com sucesso'
            else:
                return 'Valores informados inválidos!'

        ###############################################

        elif frase == 'fechar conta':
            return 'De qual mesa?'
        elif ultimaFrase == 'De qual mesa?':
            if frase in self.frases and frase.isnumeric():
                if 'total' in self.frases[frase]:
                    self.apaga_mesa = frase
                    df = pd.DataFrame(self.frases[frase]['consumo'])
                    return f"\n\nMesa {frase}\nResponsável: {self.frases[frase]['responsavel'].title()}\n\n{df}\n\nTotal R$ {self.frases[frase]['total']},00\n\nConfirma o fechamento da mesa?\n"
                else:
                    return 'Valores informados inválidos!'
            else:
                return 'Valores informados inválidos!'
        elif "Confirma o fechamento da mesa?" in str(ultimaFrase):
            sims = ['s','sim']
            if frase in sims:
                data = f'{dia}/{mes}/{ano}'
                mesa = self.apaga_mesa
                total = self.frases[self.apaga_mesa]['total']               
                self.frases['balanco']['data'].append(data)
                self.frases['balanco']['num_mesa'].append(mesa)
                self.frases['balanco']['fechamento'].append(total)
                del self.frases[self.apaga_mesa]
                self.gravaMemoria()
                return f'Conta da mesa {self.apaga_mesa} fechada!'
            else:
                return 'Operação cancelada!'

        #######################################################

        elif frase == 'cadastrar usuario':
            return 'Digite a senha de administrador'

        elif ultimaFrase == 'Digite a senha de administrador':
            if frase == senha:
                return 'Qual o ID do usuário?'
            else:
                return 'Senha inválida'
        elif ultimaFrase == 'Qual o ID do usuário?':
                with open('autorizados.txt','a') as lista_autorizados:
                    lista_autorizados.write(f' {frase}')
                    return 'ID cadastrado'

        ##############################################

        elif frase == 'mostrar total':
            df = pd.DataFrame(self.frases['balanco'])
            return f'{df}'

        ##############################################

        elif frase == 'aprende':
            return 'Qual a frase?'

        elif ultimaFrase == 'Qual a frase?':
            self.chave = frase
            return 'Digite a resposta'
        
        elif ultimaFrase == 'Digite a resposta':
            resp = frase
            self.frases[self.chave] = resp
            self.gravaMemoria()
            return 'Aprendido'

        ##############################################

        elif frase == 'gravar video':
            WEB.gravarVideo()
            return 'OK, video gravado!'

        ##############################################

        elif frase in self.frases:
            return self.frases[frase]
        
        ############################################

        try:
            resp = str(eval(frase))
            return resp
        except:
            return 'Não entendi'



    def pegaNome(self,nome):
        if 'o meu nome eh ' in nome:
            nome = nome[500:]
        nome = nome
        return nome



    def respondeNome(self,nome):
        if nome in self.conhecidos:
            frase = f'Eaew {nome}'
        else:
            frase = f'Muito prazer {nome}. Qual a sua idade?'
        return frase



    def gravaMemoria(self):
        memoria = open(self.nome+'.json','w')
        json.dump([self.conhecidos,self.frases],memoria)
        memoria.close()



    def fala(self,frase):
        if 'executar' in frase:
            plataforma = sys.platform
            comando = frase.replace('executar ','')
            if 'win' in plataforma:
                os.startfile(comando)
            else:
                try:
                    s.Popen(comando.lower())
                except FileNotFoundError:
                    s.Popen(['xdg-open',comando])                
        else:
            try:
                print(f'\n\n{frase}\n\n')
            except:
                return frase
        self.historico.append(frase)
        os.system('clear')