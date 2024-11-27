import threading
import queue
import time
import random

# Variáveis globais e travas
encomendas_pendentes = 0
trava_encomendas = threading.Lock()

# Lista de logs do sistema
trava_log = threading.Lock()
eventos_log = []


class Pacote(threading.Thread):
    def __init__(self, id_pacote, origem, destino):
        super().__init__()
        self.id_pacote = id_pacote
        self.origem = origem
        self.destino = destino
        self.registros = []

    def registrar_evento(self, evento, exibir=True):
        """Registra um evento no histórico do pacote."""
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        log = f"{timestamp} - Pacote {self.id_pacote}: {evento}"
        self.registros.append(log)
        registrar_evento(log, exibir=exibir)

    def salvar_registros(self):
        """Salva o histórico do pacote em um arquivo."""
        with open(f"pacote_{self.id_pacote}.txt", "w") as arquivo:
            arquivo.write("\n".join(self.registros))

    def run(self):
        self.registrar_evento(f"Criado no Ponto {self.origem.id_ponto} com destino ao Ponto {self.destino.id_ponto}.", exibir=False)


class PontoRedistribuicao:
    def __init__(self, id_ponto):
        self.id_ponto = id_ponto
        self.fila_pacotes = queue.Queue()
        self.semaforo_acesso = threading.Semaphore(1)
        self.trava_fila = threading.Lock()

    def __repr__(self):
        return f"PontoRedistribuicao(id={self.id_ponto})"


class Veiculo(threading.Thread):
    def __init__(self, id_veiculo, pontos_redistribuicao, capacidade_maxima):
        super().__init__()
        self.id_veiculo = id_veiculo
        self.pontos_redistribuicao = pontos_redistribuicao
        self.ponto_atual = random.choice(pontos_redistribuicao)
        self.capacidade_maxima = capacidade_maxima
        self.pacotes_transportados = []
        self.trava_pacotes = threading.Lock()

    def run(self):
        global encomendas_pendentes
        while True:
            with trava_encomendas:
                if encomendas_pendentes == 0 and not self.pacotes_transportados:
                    registrar_evento(f"### Veículo {self.id_veiculo} finalizou todas as entregas! ###")
                    break

            self.mover_para_proximo_ponto()
            self.interagir_com_ponto()
            self.descarregar_pacotes()
            time.sleep(1)  # Simulação do tempo entre ações

    def mover_para_proximo_ponto(self):
        """Movimenta o veículo para o próximo ponto."""
        indice_atual = self.pontos_redistribuicao.index(self.ponto_atual)
        proximo_indice = (indice_atual + 1) % len(self.pontos_redistribuicao)
        self.ponto_atual = self.pontos_redistribuicao[proximo_indice]
        registrar_evento(f"Veículo {self.id_veiculo} moveu-se para o Ponto {self.ponto_atual.id_ponto}.")

    def interagir_com_ponto(self):
        """Carrega pacotes do ponto de redistribuição."""
        ponto = self.ponto_atual
        with ponto.semaforo_acesso:
            with ponto.trava_fila:
                if ponto.fila_pacotes.empty():
                    registrar_evento(f"### Ponto {ponto.id_ponto} está com a fila vazia ###")
                while not ponto.fila_pacotes.empty() and len(self.pacotes_transportados) < self.capacidade_maxima:
                    pacote = ponto.fila_pacotes.get()
                    with self.trava_pacotes:
                        self.pacotes_transportados.append(pacote)
                    pacote.registrar_evento(f"Carregado no Veículo {self.id_veiculo} no Ponto {ponto.id_ponto}.")

    def descarregar_pacotes(self):
        """Descarrega pacotes no ponto de destino."""
        global encomendas_pendentes
        for pacote in self.pacotes_transportados[:]:
            if pacote.destino == self.ponto_atual:
                with self.trava_pacotes:
                    self.pacotes_transportados.remove(pacote)
                pacote.registrar_evento(f"Descarregado no Ponto {self.ponto_atual.id_ponto} pelo Veículo {self.id_veiculo}.")
                pacote.salvar_registros()
                with trava_encomendas:
                    encomendas_pendentes -= 1


def registrar_evento(evento, exibir=True):
    """Registra eventos no log global e opcionalmente exibe no terminal."""
    with trava_log:
        eventos_log.append(evento)  # Sempre adiciona ao log
        if exibir:  # Exibe no terminal apenas se exibir=True
            print(evento)

def exibir_estado_inicial(pontos, veiculos, pacotes):
    """Exibe o estado inicial do sistema antes de iniciar a simulação."""
    print("\n=== Estado Inicial do Sistema ===\n")
    
    print("Pontos de Redistribuição:")
    for ponto in pontos:
        print(f"  - Ponto {ponto.id_ponto}: {ponto.fila_pacotes.qsize()} pacotes na fila")
        if not ponto.fila_pacotes.empty():
            print("    Pacotes na fila:")
            with ponto.trava_fila:
                for pacote in list(ponto.fila_pacotes.queue):
                    print(f"      Pacote {pacote.id_pacote}: destino Ponto {pacote.destino.id_ponto}")
    
    print("\nVeículos:")
    for veiculo in veiculos:
        print(f"  - Veículo {veiculo.id_veiculo}: posição inicial no Ponto {veiculo.ponto_atual.id_ponto}, capacidade máxima {veiculo.capacidade_maxima} pacotes")
    
    print("\nTotal de Encomendas Criadas:")
    for pacote in pacotes:
        print(f"  - Pacote {pacote.id_pacote}: origem Ponto {pacote.origem.id_ponto}, destino Ponto {pacote.destino.id_ponto}")
    
    print("\n=================================\n")
    time.sleep(5)  # Pausa para que o usuário veja o estado inicial


def executar_teste_simulacao(num_pontos, num_veiculos, num_pacotes, capacidade_veiculo):
    global encomendas_pendentes
    encomendas_pendentes = num_pacotes

    pontos_teste = [PontoRedistribuicao(i) for i in range(num_pontos)]
    veiculos_teste = [Veiculo(i, pontos_teste, capacidade_veiculo) for i in range(num_veiculos)]
    pacotes_teste = []

    # Criar pacotes com origem e destino diferentes
    for i in range(num_pacotes):
        origem, destino = random.sample(pontos_teste, 2)
        pacote = Pacote(i, origem, destino)
        origem.fila_pacotes.put(pacote)
        pacotes_teste.append(pacote)

    # Exibir estado inicial do sistema
    exibir_estado_inicial(pontos_teste, veiculos_teste, pacotes_teste)

    # Inicia as threads dos pacotes
    for pacote in pacotes_teste:
        pacote.start()

    # Inicia as threads dos veículos
    for veiculo in veiculos_teste:
        veiculo.start()

    # Aguarda todas as threads finalizarem
    for veiculo in veiculos_teste:
        veiculo.join()
    for pacote in pacotes_teste:
        pacote.join()

    registrar_evento("=== Simulação Finalizada ===")


def solicitar_parametros():
    """Solicita os parâmetros de entrada ao usuário."""
    while True:
        try:
            s = int(input("Digite o número de pontos de redistribuição (S): "))
            c = int(input("Digite o número de veículos (C): "))
            p = int(input("Digite o número de encomendas (P): "))
            a = int(input("Digite a capacidade máxima de cada veículo (A): "))
            return s, c, p, a
        except ValueError:
            print("Entrada inválida. Tente novamente.")


def executar_simulacao():
    """Executa a simulação com base nos parâmetros fornecidos pelo usuário."""
    print("\n=== Simulação de Rede de Entregas ===")
    s, c, p, a = solicitar_parametros()
    executar_teste_simulacao(num_pontos=s, num_veiculos=c, num_pacotes=p, capacidade_veiculo=a)


if __name__ == "__main__":
    executar_simulacao()
