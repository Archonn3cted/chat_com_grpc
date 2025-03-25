# Chat Simples com gRPC 💬

Trabalho de Sistemas Distribuídos implementando um sistema de chat simples utilizando gRPC em Python, onde os clientes podem enviar e receber mensagens simultaneamente através de uma estratégia bidirecional com streams de mensagens.

## Autores ✍

- [Caio Henrique] (caio14.poke@gmail.com)
- [Leonardo Lima] (leo_2002_mario@hotmail.com)
- [Marcelly Silva] (marcelly.silva@arapiraca.ufal.br)

## Estrutura do Projeto

O projeto é composto pelos seguintes arquivos:

```bash
/
├── chat.proto               # Arquivo de definição do protocolo gRPC. 
Ele descreve o serviço Chat e a estrutura das mensagens(ChatMessage). 
Ao ser compilado com o comando abaixo, gera dois arquivos Python:
├── chat_pb2.py                 # Contém as classes das mensagens definidas no .proto. 
├── chat_pb2_grpc.py            # Contém as classes e métodos para implementar o servidor e o cliente gRPC.
Comando para gerar os arquivos:
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. chat.proto
├── client.py            # Cliente gRPC.
└── server.py             # Servidor Grpc.
```

## Funcionalidades

1. **Servidor (server.py)**
Ele gerencia as conexões dos clientes e retransmite as mensagens recebidas para todos os clientes conectados.

- Gerenciamento de Clientes: Mantém uma lista de clientes conectados.

- Retransmissão de Mensagens: Recebe mensagens de um cliente e as retransmite para todos os outros clientes, exceto o remetente original.

- Thread Safety: Utiliza um Lock para garantir que a lista de clientes e mensagens seja manipulada de forma segura em um ambiente multithread.

2. **Cliente (client.py)**
Permite que o usuário envie e receba mensagens simultaneamente.

- Envio de Mensagens: Permite que o usuário digite mensagens e as envie para o servidor.

- Recepção de Mensagens: Recebe mensagens do servidor em tempo real e as exibe no terminal.

- Multithreading: Utiliza threads para enviar e receber mensagens simultaneamente.

## Detalhes da Implementação

### Servidor (server.py)
#### Inicialização
- O servidor inicia com uma lista vazia de clientes e um Lock para garantir thread safety.

- O método SendMessage é implementado para lidar com streams bidirecionais.
#### Conexão de Clientes
- Quando um cliente se conecta, ele é adicionado à lista de clientes.

- Um gerador de mensagens (message_generator) é criado para enviar mensagens ao cliente.
#### Recebimento e Retransmissão de Mensagens
- O servidor recebe mensagens do cliente e as retransmite para todos os outros clientes conectados.

- As mensagens são armazenadas em uma lista específica para cada cliente e enviadas através do gerador de mensagens.

### Cliente (client.py)
#### Inicialização
- O cliente se conecta ao servidor e inicia duas threads:

  - Uma para receber mensagens do servidor.

  - Outra para enviar mensagens digitadas pelo usuário.
#### Recepção de Mensagens
- A função receive_messages fica em loop, recebendo mensagens do servidor e exibindo-as no terminal.
#### Envio de Mensagens

- A função send_messages fica em loop, capturando mensagens digitadas pelo usuário e enviando-as ao servidor.
    
## Como Executar

### Pré-requisitos
- Python 3.x instalado.
- Biblioteca grpcio e grpcio-tools instaladas. Para instalá-las, execute:
```bash
pip install grpcio grpcio-tools
```

### Passos
1. Clone o repositório:
```bash
  git clone https://github.com/seu-usuario/nome-do-repositorio.git
cd nome-do-repositorio
```
2. Execute o servidor:

```bash
  python server.py
```

3. Execute os clientes:

Em terminais separados, execute usuários diferentes que irão interagir entre si no chat:
```bash
  python client.py
```
- Digite o nome do usuário quando solicitado.

- Comece a enviar e receber mensagens.

## Exemplo de Uso

### 1. Servidor
```bash
  $ python server.py
Servidor rodando na porta 50051...
```

### 2. Cliente 1
```bash
  $ python client.py
Digite seu nome: Amanda
[Cid] Olá, Amanda!
```

### 3. Cliente 2
```bash
$ python client.py
Digite seu nome: Cid
[Amanda] Olá, Cid!
```

### 4. Interação
- Quando Amanda digitar uma mensagem, Cid a receberá, e vice-versa.

- As mensagens são exibidas no formato [Usuário] *Mensagem*.
