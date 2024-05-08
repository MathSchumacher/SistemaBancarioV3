import datetime
from abc import ABC, abstractmethod, abstractproperty

# Classe abstrata para transações
class Transacao(ABC):
    @abstractproperty
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass

# Classe Saque (herda de Transação)
class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        if conta.saldo < self._valor:
            print("Saldo insuficiente para realizar o saque.")
            return False
        conta.saldo -= self._valor
        conta.historico.adicionar_transacao(f"Saque de R$ {self._valor:.2f}")
        print(f"Saque de R$ {self._valor:.2f} realizado com sucesso!")
        return True

# Classe Depósito (herda de Transação)
class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        conta.saldo += self._valor
        conta.historico.adicionar_transacao(f"Depósito de R$ {self._valor:.2f}")
        print(f"Depósito de R$ {self._valor:.2f} realizado com sucesso!")
        return True

# Classe Histórico
class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(transacao)

# Classe Conta
class Conta:
    def __init__(self, numero, cliente):
        self._numero = numero
        self._cliente = cliente
        self._saldo = 0.0
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self._saldo

    @saldo.setter
    def saldo(self, valor):
        self._saldo = valor

    @property
    def numero(self):
        return self._numero

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        pass  # Será implementado na subclasse

    def depositar(self, valor):
        pass  # Será implementado na subclasse

# Classe ContaCorrente (herda de Conta)
class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques
        self._numero_saques = 0

    def sacar(self, valor):
        if self._numero_saques >= self._limite_saques:
            print("Limite diário de saques atingido.")
            return False
        
        if valor > self._limite:
            print("Valor do saque excede o limite diário permitido.")
            return False
        
        saque = Saque(valor)
        if saque.registrar(self):
            self._numero_saques += 1
            return True
        return False

    def depositar(self, valor):
        deposito = Deposito(valor)
        deposito.registrar(self)

    def __str__(self):
        return f"Conta Corrente [Número: {self._numero}, Cliente: {self._cliente.nome}, Saldo: R$ {self._saldo:.2f}]"

# Classe Cliente
class Cliente:
    def __init__(self, endereco):
        self._endereco = endereco
        self._contas = []

    def realizar_transacao(self, conta, transacao):
        return transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self._contas.append(conta)

# Classe PessoaFisica (herda de Cliente)
class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self._nome = nome
        self._data_nascimento = data_nascimento
        self._cpf = cpf

    @property
    def nome(self):
        return self._nome

    @property
    def cpf(self):
        return self._cpf

    def __str__(self):
        return f"{self._nome} [CPF: {self._cpf}]"

# Variáveis globais para armazenar dados em memória
clientes = []
contas = []
conta_ativa = None

# Função para cadastrar um cliente pessoa física
def cadastrar_cliente():
    print("Cadastrar Cliente Pessoa Física")
    nome = input("Nome: ")
    data_nascimento = input("Data de nascimento (DD/MM/AAAA): ")
    cpf = input("CPF: ")
    endereco = input("Endereço: ")

    # Verifica se o CPF já existe
    for cliente in clientes:
        if cliente.cpf == cpf:
            print("Erro: Cliente com este CPF já cadastrado.")
            return

    # Cria um novo cliente
    cliente = PessoaFisica(nome, data_nascimento, cpf, endereco)
    clientes.append(cliente)
    print("Cliente cadastrado com sucesso!")

# Função para criar uma conta corrente
def criar_conta_corrente():
    print("Criar Conta Corrente")
    cpf = input("CPF do cliente: ")

    # Verifica se o CPF está cadastrado
    cliente_encontrado = None
    for cliente in clientes:
        if cliente.cpf == cpf:
            cliente_encontrado = cliente
            break

    if not cliente_encontrado:
        print("Cliente não encontrado.")
        return

    numero_conta = len(contas) + 1
    conta = ContaCorrente(numero_conta, cliente_encontrado)

    # Adiciona a conta à lista de contas
    contas.append(conta)
    cliente_encontrado.adicionar_conta(conta)
    print(f"Conta corrente criada com sucesso! Número da conta: {conta.numero}")

# Função para ativar uma conta corrente
def ativar_conta_corrente():
    global conta_ativa
    print("Ativar Conta Corrente")
    numero_conta = int(input("Número da conta: "))
    cpf = input("CPF do cliente: ")

    conta_encontrada = None
    for conta in contas:
        if conta.numero == numero_conta and conta.cliente.cpf == cpf:
            conta_encontrada = conta
            break

    if not conta_encontrada:
        print("Conta não encontrada ou dados incorretos.")
        return

    conta_ativa = conta_encontrada
    print("Conta corrente ativada com sucesso!")

# Função para realizar um depósito
def depositar():
    if conta_ativa is None:
        print("Não há conta ativa no momento, por favor ative uma conta.")
        return

    valor = float(input("Informe o valor do depósito: "))
    deposito = Deposito(valor)

    if deposito.registrar(conta_ativa):
        print(f"Depósito de R$ {valor:.2f} realizado com sucesso!")
    else:
        print("Depósito não realizado.")

# Função para realizar um saque
def sacar():
    if conta_ativa is None:
        print("Não há conta ativa no momento, por favor ative uma conta.")
        return

    valor = float(input("Informe o valor do saque: "))
    saque = Saque(valor)

    if saque.registrar(conta_ativa):
        print(f"Saque de R$ {valor:.2f} realizado com sucesso!")
    else:
        print("Saque não realizado.")

# Função para exibir o extrato
def exibir_extrato():
    if conta_ativa is None:
        print("Não há conta ativa no momento, por favor ative uma conta.")
        return

    print("\n======= EXTRATO =======")
    for transacao in conta_ativa.historico.transacoes:
        print(transacao)
    print(f"\nSaldo atual: R$ {conta_ativa.saldo:.2f}")
    print("=======================\n")

# Menu do programa
def menu_principal():
    menu = """
    [a] Ativar Conta Corrente
    [c] Cadastrar Cliente Pessoa Física
    [r] Criar Conta Corrente
    [d] Depositar
    [s] Sacar
    [e] Exibir Extrato
    [x] Sair

    Escolha uma opção: """

    while True:
        opcao = input(menu)

        if opcao == "c":
            cadastrar_cliente()

        elif opcao == "r":
            criar_conta_corrente()

        elif opcao == "a":
            ativar_conta_corrente()

        elif opcao == "d":
            depositar()

        elif opcao == "s":
            sacar()

        elif opcao == "e":
            exibir_extrato()

        elif opcao == "x":
            print("Saindo...")
            break

        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    menu_principal()