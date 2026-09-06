import json
from datetime import datetime
from pathlib import Path
import os

from .logs import Logger


class InterromperLoop(Exception):
    """
    Classe de erro para interrupção do fluxo de while por dentro de uma segunda função.
    Essa classe funciona apenas para chamada do fim do código.
    """

    pass


class NCAS:
    """
    Classe do Núcleo Cognitivo da Aurora Siger. Esse núcleo serve para ativarmos nossos logs, e nossas análises.
    Aqui podemos cadastrar alertas e erros, consultar alertas e visualizar as nossas opções do json.
    Vamos também gerar algumas análises dos alertas e gerar os prompts para jogarmos na IA e recebermos os resultados.
    Além disso, temos também a opção de finalizarmos o sistema.
    """

    def __init__(self):
        # self.running = True

        # # Diretório raiz do projeto:
        # # fase-5/
        self.base_dir = Path(__file__).resolve().parent.parent

        # # Caminhos dos arquivos
        self.json_path = self.base_dir / "dados" / "dados_colonia.json"

        # # Criação dos diretórios necessários
        self.json_path.parent.mkdir(parents=True, exist_ok=True)

        self.message_menu = """
==================================================
     Núcleo Cognitivo da Aurora Siger
==================================================

Escolha uma opção:

1 - Cadastrar alerta
2 - Consultar alertas
3 - Visualizar JSON
4 - Analisar alerta
5 - Visualizar prompts
6 - Sair
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

        print("\n")
        print("===================================")
        print("Núcleo Cognitivo da Aurora Siger")
        print("===================================")
        print(f'{"Inicializando Núcleo":-^35}')
        print("===================================")

    # =========================================================
    # MÉTODOS AUXILIARES
    # =========================================================

    def pausar(self):
        input("\nPressione ENTER para continuar...")

    def _carregar_dados(self):
        """
        Carrega os dados do JSON.

        Caso o arquivo não exista ou esteja vazio, retorna
        uma estrutura inicial válida.
        """

        if not os.path.exists(self.json_path):
            self.logger.warning(
                "Arquivo JSON não encontrado. Criando estrutura inicial."
            )

            return {"ocorrencias": []}

        try:
            with open(self.json_path, "r", encoding="utf-8") as arquivo:
                dados = json.load(arquivo)

            if not isinstance(dados, dict):
                raise ValueError("O JSON deve conter um objeto.")

            if "ocorrencias" not in dados:
                dados["ocorrencias"] = []

            return dados

        except json.JSONDecodeError:
            self.logger.error("Arquivo JSON inválido.")
            print("Erro: o arquivo JSON está inválido.")

            return {"ocorrencias": []}

        except OSError as erro:
            self.logger.error(
                f"Erro ao carregar JSON: {erro}"
            )
            print("Erro ao carregar os dados.")

            return {"ocorrencias": []}

    def _salvar_dados(self, dados):
        """
        Salva os dados no arquivo JSON.
        """

        try:
            self.json_path.parent.mkdir(
                parents=True,
                exist_ok=True
            )

            with self.json_path.open("w", encoding="utf-8") as arquivo:
                json.dump(
                    dados,
                    arquivo,
                    ensure_ascii=False,
                    indent=4
                )

            self.logger.info("Dados salvos no JSON.")

        except OSError as erro:
            self.logger.error(
                f"Erro ao salvar JSON: {erro}"
            )

            print("Erro ao salvar os dados.")

    def _registrar_txt(self, ocorrencia):
        """
        Adiciona uma ocorrência ao histórico TXT.
        """

        try:

            registro = (
                f"[{ocorrencia['data']}] "
                f"ID: {ocorrencia['id']} | "
                f"Módulo: {ocorrencia['modulo']} | "
                f"Tipo: {ocorrencia['tipo']} | "
                f"Prioridade: {ocorrencia['prioridade']} | "
                f"Status: {ocorrencia['status']}\n"
                f"Mensagem: {ocorrencia['mensagem']}\n"
                f"{'-' * 80}\n"
            )

            self.logger.info(
                f"Ocorrência {ocorrencia['id']} registrada no TXT."
            )

        except OSError as erro:
            self.logger.error(
                f"Erro ao registrar TXT: {erro}"
            )

            print("Erro ao registrar o histórico.")

    def _ler_txt(self):
        """
        Lê e exibe o histórico textual.
        """

        if not os.path.exists(self.logger.get_path):
            print("Nenhum registro TXT encontrado.")
            return

        try:
            with open(self.logger.get_path, "r", encoding="utf-8") as arquivo:
                conteudo = arquivo.read()

            if not conteudo.strip():
                print("O arquivo de registros está vazio.")
                return

            print("\n========== REGISTROS TXT ==========\n")
            print(conteudo)
            print("\n======== FIM DOS REGISTROS ========\n")

        except OSError as erro:
            self.logger.error(
                f"Erro ao ler TXT: {erro}"
            )

            print("Erro ao ler os registros.")

    def _proximo_id(self, ocorrencias):
        """
        Gera o próximo ID disponível.
        """

        if not ocorrencias:
            return 1

        return max(
            ocorrencia.get("id", 0)
            for ocorrencia in ocorrencias
        ) + 1

    def _solicitar_texto(self, mensagem):
        """
        Solicita um texto obrigatório.
        """

        while True:
            valor = input(mensagem).strip()

            if valor:
                return valor

            print("O campo não pode ficar vazio.")
            self.logger.warning(
                "Usuário informou um campo vazio."
            )

    def _solicitar_opcao(self, mensagem, opcoes):
        """
        Solicita uma opção pertencente a uma lista válida.
        """

        while True:
            valor = input(mensagem).strip().lower()

            if valor in opcoes:
                return valor

            print(
                f"Opção inválida. Escolha entre: "
                f"{', '.join(opcoes)}"
            )

            self.logger.warning(
                f"Opção inválida informada: {valor}"
            )

    def _exibir_ocorrencia(self, ocorrencia):
        """
        Exibe uma ocorrência de forma organizada.
        """

        print("\n" + "=" * 60)
        print(f"ID:         {ocorrencia['id']}")
        print(f"Módulo:     {ocorrencia['modulo']}")
        print(f"Tipo:       {ocorrencia['tipo']}")
        print(f"Prioridade: {ocorrencia['prioridade']}")
        print(f"Data:       {ocorrencia['data']}")
        print(f"Status:     {ocorrencia['status']}")
        print(f"Mensagem:   {ocorrencia['mensagem']}")
        print("=" * 60)

    # =========================================================
    # LOOP PRINCIPAL
    # =========================================================

    def run(self):
        """
        Executa o menu principal do sistema.
        """

        try:
            while True:
                print(self.message_menu)

                valor = input("Digite sua opção: ").strip()

                try:
                    opcao = int(valor)

                except ValueError:
                    self.logger.error(
                        f"Input inválido: {valor}"
                    )

                    print(
                        "\nValor inválido. "
                        "Digite um número entre 1 e 7."
                    )

                    self.pausar()
                    continue

                self.logger.info(f"Usuário escolheu opção {opcao}")
                acao = self._dict_actions.get(opcao)

                if acao is None:
                    self.logger.warning(
                        f"Opção inexistente: {opcao}"
                    )

                    print(
                        "\nOpção inválida. "
                        "Digite um número entre 1 e 7."
                    )

                    self.pausar()
                    continue

                try:
                    acao()

                except InterromperLoop:
                    raise

                except Exception as erro:
                    self.logger.error(
                        f"Erro inesperado na execução: {erro}"
                    )

                    print(
                        "\nOcorreu um erro inesperado. "
                        "Consulte os logs."
                    )

                    self.pausar()

        except InterromperLoop:
            print("\nSistema encerrado.")

    # =========================================================
    # CADASTRO
    # =========================================================

    def cadastro_alertas(self):
        """
        Cadastra uma nova ocorrência no JSON e no TXT.
        """

        self.logger.info("Iniciando cadastro de alerta.")

        print("\n========== CADASTRO DE ALERTA ==========\n")

        dados = self._carregar_dados()
        ocorrencias = dados["ocorrencias"]

        ocorrencia = {
            "id": self._proximo_id(ocorrencias),
            "modulo": self._solicitar_texto(
                "Módulo: "
            ),
            "tipo": self._solicitar_texto(
                "Tipo da ocorrência: "
            ),
            "prioridade": self._solicitar_opcao(
                "Prioridade [baixa/media/alta/critica]: ",
                ["baixa", "media", "alta", "critica"]
            ),
            "data": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            "status": "Aberta",
            "mensagem": self._solicitar_texto(
                "Mensagem: "
            ),
        }

        ocorrencias.append(ocorrencia)

        self._salvar_dados(dados)
        self._registrar_txt(ocorrencia)

        self.logger.info(
            f"Alerta {ocorrencia['id']} cadastrado."
        )

        print("\nAlerta cadastrado com sucesso.")
        self._exibir_ocorrencia(ocorrencia)

        self.pausar()

    # =========================================================
    # CONSULTA
    # =========================================================

    def consulta_alertas(self):
        """
        Consulta ocorrências cadastradas.
        """

        self.logger.info("Iniciando consulta de alertas.")

        print("\n========== CONSULTA DE ALERTAS ==========\n")

        dados = self._carregar_dados()
        ocorrencias = dados["ocorrencias"]

        if not ocorrencias:
            print("Nenhuma ocorrência cadastrada.")
            self.pausar()
            return

        print("1 - Exibir todas")
        print("2 - Buscar por módulo")
        print("3 - Buscar por prioridade")
        print("4 - Buscar por status")
        print("5 - Exibir registros TXT")

        opcao = input("\nDigite sua opção: ").strip()

        if opcao == "1":
            resultados = ocorrencias

        elif opcao == "2":
            modulo = self._solicitar_texto(
                f"Módulos disponíveis:\n{'\n'.join({item['modulo'] for item in dados['ocorrencias']})}\nDigite o módulo entre os acima:"
            ).lower()

            resultados = [
                ocorrencia
                for ocorrencia in ocorrencias
                if ocorrencia["modulo"].lower() == modulo
            ]

        elif opcao == "3":
            prioridade = self._solicitar_opcao(
                "Prioridade [baixa/media/alta/critica]: ",
                ["baixa", "media", "alta", "critica"]
            )

            resultados = [
                ocorrencia
                for ocorrencia in ocorrencias
                if ocorrencia["prioridade"] == prioridade
            ]

        elif opcao == "4":
            status = self._solicitar_texto(
                "Digite o status: "
            ).lower()

            resultados = [
                ocorrencia
                for ocorrencia in ocorrencias
                if ocorrencia["status"].lower() == status
            ]

        elif opcao == "5":
            self._ler_txt()
            self.pausar()
            return

        else:
            self.logger.warning(
                f"Opção de consulta inválida: {opcao}"
            )

            print("Opção inválida.")
            self.pausar()
            return

        if not resultados:
            print("\nNenhuma ocorrência encontrada.")

        else:
            print(
                f"\nForam encontradas "
                f"{len(resultados)} ocorrência(s)."
            )

            for ocorrencia in resultados:
                self._exibir_ocorrencia(ocorrencia)

        self.pausar()

    # =========================================================
    # VISUALIZAÇÃO DO JSON
    # =========================================================

    def visualiza_json(self):
        """
        Exibe o conteúdo completo do JSON.
        """

        self.logger.info("Visualizando JSON.")

        dados = self._carregar_dados()

        print("\n========== DADOS DO JSON ==========\n")

        print(
            json.dumps(
                dados,
                ensure_ascii=False,
                indent=4
            )
        )

        self.pausar()

    # =========================================================
    # REGRA LÓGICA
    # =========================================================

    def validar_regra_logica(self, usuario_autorizado, modulo_ativo):
        """
        Regra:

            A = U AND M

        A consulta só é permitida quando:
        - o usuário está autorizado;
        - o módulo está ativo.

        Retorna True ou False.
        """

        autorizacao = usuario_autorizado and modulo_ativo

        self.logger.info(
            f"Validação lógica executada: "
            f"usuario_autorizado={usuario_autorizado}, "
            f"modulo_ativo={modulo_ativo}, "
            f"resultado={autorizacao}"
        )

        return autorizacao

    def _solicitar_booleano(self, mensagem):
        """
        Solicita uma resposta booleana.
        """

        while True:
            valor = input(mensagem).strip().lower()

            if valor in ["s", "sim", "1", "true"]:
                return True

            if valor in ["n", "nao", "não", "0", "false"]:
                return False

            print("Digite sim ou não.")

    # =========================================================
    # ANÁLISE
    # =========================================================

    def analise_alerta(self):
        """
        Analisa uma ocorrência e simula uma recomendação
        de um assistente inteligente.
        """

        self.logger.info("Iniciando análise de alerta.")

        print("\n========== ANÁLISE DE ALERTA ==========\n")

        dados = self._carregar_dados()
        ocorrencias = dados["ocorrencias"]

        if not ocorrencias:
            print("Nenhuma ocorrência cadastrada.")
            self.pausar()
            return

        try:
            identificador = int(
                input("Digite o ID da ocorrência: ")
            )

        except ValueError:
            self.logger.error(
                "ID inválido informado na análise."
            )

            print("ID inválido.")
            self.pausar()
            return

        ocorrencia = next(
            (
                item
                for item in ocorrencias
                if item["id"] == identificador
            ),
            None
        )

        if ocorrencia is None:
            self.logger.warning(
                f"Ocorrência não encontrada: {identificador}"
            )

            print("Ocorrência não encontrada.")
            self.pausar()
            return

        self._exibir_ocorrencia(ocorrencia)

        print("\n========== VALIDAÇÃO LÓGICA ==========\n")

        usuario_autorizado = self._solicitar_booleano(
            "Usuário autorizado? [s/n]: "
        )

        modulo_ativo = self._solicitar_booleano(
            "Módulo ativo? [s/n]: "
        )

        consulta_permitida = self.validar_regra_logica(
            usuario_autorizado,
            modulo_ativo
        )

        print(
            f"\nConsulta permitida: "
            f"{'SIM' if consulta_permitida else 'NÃO'}"
        )

        print("\n========== RESPOSTA SIMULADA ==========\n")

        resposta = self._gerar_resposta_simulada(ocorrencia)

        print(
            json.dumps(
                resposta,
                ensure_ascii=False,
                indent=4
            )
        )

        self.logger.info(
            f"Análise concluída para ocorrência {identificador}."
        )

        self.pausar()

    def _gerar_resposta_simulada(self, ocorrencia):
        """
        Simula uma resposta estruturada de uma IA.
        """

        prioridade = ocorrencia["prioridade"]

        if prioridade == "critica":
            acao = "Acionar imediatamente a equipe de manutenção"
            risco = "Alto risco operacional"

        elif prioridade == "alta":
            acao = "Priorizar análise da equipe responsável"
            risco = "Possível impacto em módulos dependentes"

        elif prioridade == "media":
            acao = "Programar avaliação técnica"
            risco = "Impacto operacional moderado"

        else:
            acao = "Registrar e acompanhar a ocorrência"
            risco = "Baixo impacto operacional"

        return {
            "ocorrencia_id": ocorrencia["id"],
            "modulo": ocorrencia["modulo"],
            "prioridade": prioridade,
            "acao_recomendada": acao,
            "risco": risco,
            "resposta_gerada_por": "Simulação local de assistente inteligente"
        }

    # =========================================================
    # PROMPTS
    # =========================================================

    def visualizar_prompts(self):
        """
        Exibe os prompts utilizados na simulação.
        """

        self.logger.info("Visualizando prompts.")

        print("\n========== PROMPTS UTILIZADOS ==========\n")

        print("----- ZERO-SHOT -----")

        print(
            """
Classifique a prioridade da ocorrência abaixo:

"Falha crítica no sistema de oxigênio."

Responda utilizando o formato JSON.
"""
        )

        print("----- FEW-SHOT -----")

        print(
            """
Exemplo 1:
Ocorrência: "Luz de um corredor apagada."
Classificação: Baixa

Exemplo 2:
Ocorrência: "Falha no sistema de oxigênio."
Classificação: Alta

Agora classifique:
Ocorrência: "Oscilação no sistema de energia."
"""
        )

        print("----- STRUCTURED OUTPUT -----")

        print(
            """
{
    "modulo": "Energia",
    "prioridade": "Alta",
    "acao_recomendada": "Acionar equipe de manutenção",
    "risco": "Interrupção de módulos dependentes"
}
"""
        )

        print("----- RESPOSTA SIMULADA -----")

        resposta = {
            "modulo": "Energia",
            "prioridade": "Alta",
            "acao_recomendada": "Acionar equipe de manutenção",
            "risco": "Interrupção de módulos dependentes"
        }

        print(
            json.dumps(
                resposta,
                ensure_ascii=False,
                indent=4
            )
        )

        self.pausar()

    # =========================================================
    # LOGS ADMINISTRATIVOS
    # =========================================================

    def zerar_logs(self):
        """
        Limpa o arquivo de log administrativo.
        Não faz parte do fluxo operacional normal.
        """

        self.logger.warning(
            "Solicitação de limpeza dos logs administrativos."
        )

        confirmacao = input(
            "Deseja realmente zerar os logs? [s/n]: "
        ).strip().lower()

        if confirmacao not in ["s", "sim"]:
            print("Operação cancelada.")
            self.pausar()
            return

        self.logger.zerar_log()

        print("Logs administrativos zerados.")
        self.pausar()

    # =========================================================
    # ENCERRAMENTO
    # =========================================================

    def quit(self):
        """
        Encerra o sistema.
        """

        self.logger.info("Desativando o sistema.")

        # self.running = False

        raise InterromperLoop