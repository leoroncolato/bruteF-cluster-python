# Quebra de Hash Distribuída com Dask

## Descrição da Atividade
O objetivo desta atividade é criar uma aplicação de quebra de hash distribuída, permitindo incrementar o número de hosts no processamento e medir o tempo de quebra para diferentes cenários. O sistema visa demonstrar o ganho de eficiência ao escalar horizontalmente uma tarefa de alto custo computacional, como o ataque de força bruta (*brute-force*).

## Tecnologias Utilizadas
* **Python**
* **Dask (`dask.distributed`)**: Framework utilizado para o processamento paralelo e controle do cluster distribuído.
* **Hashlib**: Biblioteca para o cálculo das funções de hash (MD5 e SHA1).
* **Itertools**: Para a geração combinatória (produto cartesiano) das tentativas de senha.

## Arquitetura e Implementação
O sistema opera em uma arquitetura **Master-Worker**, orquestrada pelo Dask:
1.  **Nó Mestre (Scheduler)**: Coordena o cluster, recebe a requisição do cliente e distribui as tarefas.
2.  **Nós Trabalhadores (Workers)**: Executam a força bruta em paralelo.

### Estratégia de Paralelismo
Para paralelizar a quebra da senha, o espaço de busca foi particionado. Em vez de um único laço testar todas as possibilidades, a aplicação delega para o cluster tarefas baseadas no **prefixo da senha** (o primeiro caractere). 
Sendo o alfabeto composto por 62 caracteres (letras minúsculas, maiúsculas e números), o código submete 62 tarefas individuais ao cluster. Cada *worker* pega um caractere e tenta todas as combinações subsequentes. Assim que um *worker* encontra o hash correspondente, o resultado é retornado ao cliente e o restante das tarefas no cluster é cancelado instantaneamente.

## Resultados e Cenário de Teste

Baseado na execução monitorada pelo VS Code e pelo painel de controle do Dask (Dashboard), os seguintes resultados foram obtidos no ambiente configurado:

**Configuração do Cluster no Teste:**
* **Nó Mestre / Cliente:** Conectado via protocolo TCP (ex: `192.168.4.113:8786`).
* **Workers:** 2 máquinas/processos ativas computando simultaneamente (IPs `192.168.4.113` e `192.168.4.25`).
* **Recursos Alocados:** 16 *threads* totais e aproximadamente 23.7 GiB de memória distribuída.

**Métricas da Execução:**
* **Senha alvo:** `leo1` (4 caracteres).
* **Tarefas geradas:** 62 blocos independentes.
* **Tempo de quebra - MD5:** `~7.03 segundos`
* **Tempo de quebra - SHA1:** `~23.35 segundos`

O *Task Stream* do Dask Dashboard evidenciou um processamento fluido, onde as tarefas foram divididas e consumidas pelas diversas threads sem gerar gargalos de memória (*memory use* mantido em níveis muito baixos), provando a viabilidade técnica da solução proposta.