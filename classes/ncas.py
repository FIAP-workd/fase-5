from classes import Logger

class InterromperLoop(Exception):
    pass


class NCAS:

    def __init__(self):
        self.running = True
        self.message_menu = """
        Bem vinto ao Núcleo cognitivo da Aurora Singer.
        Escolha uma opção do que deseja fazer:
        1 - Cadastrar alerta.
        2 - Consultar alertas.
        3 - Visualizar JSON.
        4 - Analisar Alerta.
        5 - Visualizar Prompts.
        6 - Sair.
        """
        self._dict_actions = {
            1: self.cadastro_alertas,
            2: self.consulta_alertas,
            3: self.visualiza_json,
            4: self.analise_alerta,
            5: self.visualizar_prompts,
            6: self.quit
        }

        self.logger = Logger()
        self.logger.info("Ativação do sistema.")
        print("\n\n")
        print("===================================")
        print("Núcleo cognitivo  da  Aurora  Siger")
        print("===================================")
        print(f"{"Inicializando Núcleo":-^35}")
        print("===================================")
    

    def run(self):
        try:
            while self.running:
                
                print(self.message_menu)
                value = input("Digite sua opção: ")
                self.logger.info(f"Usuário informou um valor {value}")
                try:
                    value = int(value)
                    if value > 6:
                        raise ValueError
                except ValueError:
                    print("Valor inválido. Digite um número entre 1 e 6.")

                finally:
                    self._dict_actions.get(value)()
                    input()


        except InterromperLoop:
            pass



    def quit(self):
        raise InterromperLoop
    

    def cadastro_alertas(self):
        print("cadastro")

    def consulta_alertas(self):
        print("consulta")

    def visualiza_json(self):
        print("visualiza")

    def analise_alerta(self):
        print("analise")

    def visualizar_prompts(self):
        print("visualiza_prompt")