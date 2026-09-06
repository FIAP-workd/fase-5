from datetime import datetime
from pathlib import Path


class Logger:


    def __init__(self):
        base_dir = Path(__file__).resolve().parent.parent
        self.__path_log = base_dir / ".logs" / "registros_colonia.txt"


    def open_doc_log(self):

        caminho_arquivo = self.get_path

        caminho_arquivo.parent.mkdir(parents=True, exist_ok=True)

        f = caminho_arquivo.open(mode="a", encoding="utf-8")
        
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
        caminho_arquivo.parent.mkdir(parents=True, exist_ok=True)

        with caminho_arquivo.open("w", encoding="utf-8") as f:
            pass

    @property
    def get_path(self):
        return self.__path_log
