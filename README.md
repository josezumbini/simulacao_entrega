# Simulação de Rede de Entregas 🚚📦

Este projeto implementa uma **simulação concorrente de entrega de encomendas**, utilizando **threads** em Python. O sistema simula a interação entre veículos, pontos de redistribuição e pacotes, representando o transporte de encomendas de um ponto de origem até um ponto de destino. Foi desenvolvido para a disciplina de **Sistemas Operacionais** e aborda conceitos fundamentais de concorrência, como **threads**, **semaforos** e **variáveis de trava**.

---

## 📜 Problema Proposto

1. Criar uma rede de entrega onde:
   - Pacotes possuem um **ponto de origem** e um **ponto de destino**.
   - Veículos são responsáveis por transportar os pacotes entre os pontos.
   - Pontos de redistribuição funcionam como hubs para armazenamento temporário dos pacotes.
2. A simulação deveria utilizar **threads** para representar os veículos e pacotes, e a sincronização deveria ser garantida com **semaforos** e **variáveis de trava**.
3. O sistema deveria:
   - Registrar todos os eventos relevantes (carregamento, descarregamento, movimentação, etc.).
   - Notificar o usuário sobre estados importantes, como quando uma fila em um ponto de redistribuição está vazia ou quando um veículo finaliza todas as entregas.
   - Encerrar a simulação apenas quando todas as encomendas fossem entregues.

---

## 🛠️ Como Executar

1. **Requisitos**:
   - Python 3.8 ou superior.

2. **Executando o Código**:
   - Clone este repositório:
     ```bash
     git clone <url-do-repositorio>
     cd <nome-do-repositorio>
     ```
   - Execute o script no terminal:
     ```bash
     python simulacao_entregas.py
     ```
   - Insira os parâmetros solicitados no terminal:
     ```
     Digite o número de pontos de redistribuição (S): 3
     Digite o número de veículos (C): 2
     Digite o número de encomendas (P): 5
     Digite a capacidade máxima de cada veículo (A): 3
     ```

3. **Saída**:
   - O estado inicial do sistema será exibido.
   - A simulação gerará eventos em tempo real, como movimentação de veículos, carregamento/descarregamento de pacotes e notificações importantes.

---

## 🧵 Conceitos de Threads e Concorrência

Threads permitem a execução simultânea de múltiplas tarefas dentro de um único programa. No contexto deste projeto:
- Cada **veículo** e **pacote** é representado como uma **thread**.
- **Veículos** se movem entre os pontos e interagem com as filas de pacotes.
- **Pacotes** têm origem e destino, e são processados pelos veículos.

### Por que usar Threads?
- Para simular o comportamento assíncrono e paralelo dos veículos em tempo real.
- Para lidar com múltiplas tarefas concorrentes, como a movimentação de veículos e o processamento das filas de pacotes.

---

## 🚦 Uso de Semáforos no Projeto

Semáforos são usados para **controlar o acesso a recursos compartilhados** por múltiplas threads. Neste projeto:
- Cada ponto de redistribuição possui um semáforo para gerenciar o acesso à fila de pacotes, garantindo que apenas um veículo interaja com a fila do ponto ao mesmo tempo.

---

## 🔒 Uso de Variáveis de Trava no Projeto

Variáveis de trava (Locks) são utilizadas para **proteger seções críticas**, garantindo que apenas uma thread execute determinado trecho de código por vez. Neste projeto:
- Uma trava protege a variável que rastreia quantas encomendas ainda não foram entregues, garantindo que a contagem seja atualizada de forma segura.
- Outras travas protegem as filas de pacotes nos pontos de redistribuição, evitando problemas de acesso simultâneo.

---

## 🔍 Funcionamento Geral do Sistema

1. **Estado Inicial**:
   - Os pontos, veículos e pacotes são configurados de acordo com os parâmetros fornecidos.
   - O estado inicial do sistema é exibido.

2. **Simulação**:
   - Cada veículo (thread) se move entre os pontos, interage com as filas e processa os pacotes.
   - Eventos importantes, como carregamento/descarregamento de pacotes e fila vazia, são registrados.

3. **Finalização**:
   - A simulação termina quando todas as encomendas foram entregues.
   - Logs de eventos são exibidos em tempo real no terminal.
