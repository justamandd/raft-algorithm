## Descrição do Projeto e do Algoritmo Implementado
Este projeto simula um algoritmo de consenso distribuído inspirado no Raft. O Raft é um algoritmo amplamente utilizado em sistemas distribuídos para garantir a consistência e coordenar as decisões entre os nós (ou instâncias) de um cluster. O código implementa a dinâmica de eleição de líder e replicação de valores entre nós, com a capacidade de simular falhas e recuperação de nós.

**Objetivos do projeto:**

- Simular o processo de eleição de líder em um cluster de nós.
- Implementar a replicação de valores do líder para os nós seguidores.
- Gerenciar falhas de nós e permitir sua recuperação.
- Fornecer logs detalhados sobre o estado de cada nó, incluindo o seu termo, valor e estado de falha.


## Instruções Detalhadas para Configurar o Ambiente e Executar o Código
1. Pré-requisitos:
    - Python 3.x instalado no seu sistema.
    - Bibliotecas: threading, time, e random (já incluídas no Python padrão).


2. Passos para execução:
    - Faça o download ou copie o código fornecido.
    - Abra um terminal ou prompt de comando.
    - Navegue até o diretório onde o arquivo está salvo.
    - Execute o arquivo main.py utilizando o Python com o comando:

``` bash
  python main.py
```


- O sistema começará a simular o funcionamento do algoritmo Raft, exibindo os logs sobre o estado dos nós a cada iteração.


## Explicação de Cada Fase do Algoritmo no Contexto da Implementação
1. Inicialização dos Nós:

    - Quando o programa é executado, um cluster de nós é criado. Cada nó é instanciado com um ID, um estado inicial de "follower", e um valor que é usado para replicação. O termo de cada nó é inicialmente 0.
    - Cada nó é responsável por iniciar seu processo de execução em uma thread separada, o que permite que o algoritmo seja executado de forma assíncrona para simular a concorrência entre os nós.

2. Estado de Follower (Seguidor):

    - Quando um nó está no estado de follower, ele aguarda um "heartbeat" (um sinal do líder) ou um tempo limite para mudar para o estado de candidato se não receber comunicação do líder dentro de um tempo aleatório (definido como election_timeout).
    - Se um nó não recebe votos ou sinais de coração (heartbeat) por um tempo aleatório (entre 2 e 3 segundos), ele entra em eleição.

3. Estado de Candidate (Candidato):

    - Quando o nó se torna um candidato, ele aumenta seu termo e envia solicitações de voto para todos os outros nós no cluster.
    - O nó precisa de votos da maioria para ser eleito líder. Caso seja eleito, ele muda para o estado de líder e começa a enviar heartbeats aos outros nós para mantê-los como seguidores.

3. Estado de Leader (Líder):

    - O nó que for eleito líder começa a propagar seu valor para os outros nós seguidores e aumenta o valor periodicamente.
    - O líder envia heartbeats a cada 1 segundo para os seguidores para garantir que permaneçam sincronizados e para impedir que ocorram novas eleições.

4. Falhas e Recuperação de Nós:

    - Em momentos aleatórios (20% de chance), um nó pode falhar e entrar em um estado de falha.
    - Quando um nó falha, ele não participa de mais ações até ser recuperado.
    - Se um nó falhado for recuperado, ele volta ao estado de follower e sincroniza seu valor com o líder.

## Descrição de Possíveis Falhas Simuladas e Como o Sistema Responde a Elas

1. Falha de um Nó:

    - Quando um nó falha (em uma chance de 20% durante a execução), ele deixa de responder a solicitações e mensagens de outros nós, como a eleição de líder e a replicação de valores.
    - O nó falhado não pode participar da eleição e não pode replicar ou atualizar seu valor até que seja recuperado.

2. Recuperação de um Nó:

    - Após a falha, o nó pode ser recuperado. A recuperação é feita aleatoriamente (com 20% de chance), e o nó volta ao estado de follower.
    - Ao ser recuperado, o nó sincroniza seu valor e termo com o líder atual para garantir a consistência de dados no sistema distribuído.

3. Liderança Perdida Durante Falhas:

    - Se o líder falhar, o sistema automaticamente realiza uma nova eleição. Isso pode resultar em um novo líder sendo eleito entre os nós restantes.
    - O novo líder começa a enviar heartbeats e a replicar valores, mantendo a consistência no cluster.