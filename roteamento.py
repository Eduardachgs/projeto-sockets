class Roteamento():
    def __init__(self):
        # Tabela de roteamento indicando qual o próximo PC para onde a mensagem deve ser enviada
        self.tabela = {
            (1, 3): 2,
            (1, 4): 2,
            (1, 5): 6,
            (1, 6): 6,
            (1, 2): 2,
            (2, 4): 3,
            (2, 5): 3,
            (2, 6): 1,
            (2, 3): 3, 
            (2, 1): 1,
            (3, 5): 4,
            (3, 6): 1,
            (3, 1): 2,
            (3, 2): 2,
            (3, 4): 4,
            (4, 2): 3,
            (4, 6): 5,
            (4, 1): 3,
            (4, 5): 5,
            (4, 3): 3,
            (5, 6): 6,
            (5, 4): 4,
            (5, 3): 4,
            (5, 2): 4,
            (5, 1): 6,
            (6, 3): 1,
            (6, 2): 1,
            (6, 4): 5,
            (6, 5): 5,
            (6, 1): 1
        }

    def enviar_mensagens(self, pc_origem, pc_destino):
        rota = self.tabela[pc_origem, pc_destino]
        return rota
