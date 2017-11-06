import socket
import threading


#####################################################################
#                       DECLARAÇÃO DE VARIÁVEIS                     #
#####################################################################

# COMANDOS PARA O SERVIDOS
listaComandosServidor = ['privado', 'lista()', 'nome', 'sair()']


# dicionario com os nomes e enderecos IPs dos clientes
listaNomesClientes = {}

# contem todos os clientes que se conectam
listaSocketsClientes = {}


#####################################################################
#                      FIM DECLARAÇÃO DE VARIÁVEIS                  #
#####################################################################


#####################################################################
#                       DECLARAÇÃO DE FUNÇÕES                       #
#####################################################################

# funcao que sera executada na thread
def receivedMessages(socketClient, address): 
    
    message = socketClient.recv(1024)
    # primeira mensagem recebida eh o nome
    name = str(message)
    
    global listaNomesClientes
    # usa o IP como chave para achar os nomes dos usuarios do chat
    listaNomesClientes[address] = name

    #lista de quem esta no chat
    for key in listaNomesClientes:
        print('<' + str(key[0]) + ', ' + str(key[1]) + ', '+ str(listaNomesClientes[key]) + '>')

    
    message = listaNomesClientes[address] + ' entrou no chat'

    # envia mensagem de que um novo usuario entrou na sala
    sendBroadcastMessages(listaSocketsClientes, message, address)


    while(True):
        message = str(socketClient.recv(1024))
        sendBroadcastMessages(listaSocketsClientes, message, address)
        print(message.split())
        message = str(message)
        opcao = message.split("'")
        print(opcao)
        
        # index = listaComandosServidor.index(opcao[1])
        print(opcao[1])
        command = opcao[1]
        # ['privado', 'list()', 'nome', 'sair()']
        if command[:len('privado(')] == 'privado(':
            nomeOutroUsuario = opcao[1].split('(')
            

            print('Conversar com ' + str(nomeOutroUsuario[1]).split(')'))
            
            #while command.split("'").split(''):
            #    sendMessages(listaNomesClientes[nomeOutroUsuario], address,message):

        elif command[:len('lista()')] == 'lista()':
            enviaListaConectados(address)
        
        elif command == 2:
            print(2)
        elif command[:len('sair()')] == 'sair()':
            sendBroadcastMessages(listaSocketsClientes, name + ' saiu do chat', address)
            del listaNomesClientes[address]
            break
            

    socketClient.close()
    


# envia mensagens na sala de chat
def sendBroadcastMessages(listSockets, message, sender):
    # listConnected = {}
    listConnected = listSockets

    for key in listConnected:
        if key is not sender:
            msg = str(listaNomesClientes[sender]) + ' says: ' + str(message)
            listSockets[key].sendall(bytes(msg, 'utf-8'))



# envia mensagens particulares
def sendMessages(destiny, sender,message):
    if sender == 'server':
        listaSocketsClientes[destiny].sendall(bytes(message, 'utf-8'))
    else:
        msg = listaNomesClientes[sender] + ' says: ' + message
        listaSocketsClientes[destiny].sendall(bytes(msg, 'utf-8'))
             


def enviaListaConectados(address):
    
    listaNomes = []

    for key in listaNomesClientes:
        listaNomes.append(listaNomesClientes[key])
    
    sendMessages(address,'server',str(listaNomes))

#####################################################################
#                       FIM DECLARAÇÃO DE FUNÇÕES                   #
#####################################################################



# Declaração do Servidor

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind(('', 10000))




serverSocket.listen(5)
print('Servidor esperando conexões na porta 10000')

while(True):
    
    (clientSocket, address) = serverSocket.accept()
    #listaSocketsClientes
    #print('O cliente ' + str(address) + ' entrou no chat')
    

    listaSocketsClientes[address] = clientSocket
    
    listen_thread = threading.Thread(target=receivedMessages, args = (clientSocket, address))
    listen_thread.start()
    
    
    #listaSocketsClientes[address].sendall(bytes('Teste', 'utf-8'))

    '''
    for key in listaSocketsClientes:
        if key is not address:
            listaSocketsClientes[key].sendall(bytes(str(listaNomesClientes[key]) + ' entrou no chat', 'utf-8') )
            # listaSocketsClientes[key].sendall(bytes(' entrou no chat', 'utf-8') )
    '''
    