from datetime import datetime
import os


class Logger:


    def __init__(self):
        self.__path_log = r".logs\registros_colonia.txt"


    def open_doc_log(self):

        caminho_arquivo = self.get_path

        parent_dir = os.path.dirname(caminho_arquivo)

        if not os.path.exists(parent_dir):
            os.makedirs(parent_dir)

        f = open(caminho_arquivo, mode="a")
        
        return f
    

    def logar(self, f, type_erro, message):
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        msg_log = f"[{now}] | {type_erro} | {message}\n"
        
        f.write(msg_log)

        return msg_log
    

    def info(self, message: str):
        
        arquivo = self.open_doc_log()

        log = self.logar(arquivo, 'INFO', message)

        arquivo.close()

        # print(log)


    def warning(self, message: str):
        
        arquivo = self.open_doc_log()

        log = self.logar(arquivo, 'WARNING', message)

        arquivo.close()

        # print(log)

    
    def error(self, message: str):
        
        arquivo = self.open_doc_log()

        log = self.logar(arquivo, 'ERROR', message)

        arquivo.close()

        # print(log)


    def zerar_log(self):
        caminho_arquivo = self.get_path
        parent_dir = os.path.dirname(caminho_arquivo)

        os.makedirs(parent_dir, exist_ok=True)

        with open(caminho_arquivo, "w") as f:
            pass

    @property
    def get_path(self):
        return self.__path_log