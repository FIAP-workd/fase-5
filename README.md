# Núcleo Cognitivo da Aurora Siger (NCAS)

Aplicação de terminal em Python para registrar e acompanhar ocorrências de uma colônia espacial fictícia. O sistema centraliza o cadastro e a consulta de alertas, aplica uma regra simples de autorização durante a análise e produz recomendações locais simuladas conforme a prioridade da ocorrência.

## Funcionalidades

- **Cadastrar alerta:** cria uma ocorrência com ID sequencial, módulo, tipo, prioridade, data, status e mensagem.
- **Consultar alertas:** lista todas as ocorrências ou filtra por módulo, prioridade ou status.
- **Visualizar JSON:** mostra o conteúdo integral da base de dados no terminal.
- **Analisar alerta:** verifica se o usuário está autorizado e se o módulo está ativo; em seguida, gera uma recomendação simulada com o risco associado à prioridade.
- **Visualizar prompts:** exibe exemplos de engenharia de prompt *zero-shot*, *few-shot* e saída estruturada.
- **Registrar eventos técnicos:** grava ativações, escolhas de menu, validações e erros no arquivo de log administrativo.

## Requisitos

- Python **3.12** ou superior.
- Nenhuma dependência externa: o projeto utiliza apenas a biblioteca padrão do Python.

## Como executar

No diretório raiz do projeto, execute:

```bash
python codigo_fonte.py
```

O programa apresentará o menu abaixo:

```text
1 - Cadastrar alerta
2 - Consultar alertas
3 - Visualizar JSON
4 - Analisar alerta
5 - Visualizar prompts
6 - Sair
```

Preencha os campos solicitados pelo terminal. Os valores aceitos para prioridade são `baixa`, `media`, `alta` e `critica`; entradas vazias ou prioridades fora dessa lista são solicitadas novamente.

## Fluxo de análise

Ao selecionar **Analisar alerta**, informe o ID de uma ocorrência existente e responda às perguntas de autorização e atividade do módulo. A consulta é considerada permitida somente quando ambas as respostas forem positivas:

```text
consulta_permitida = usuario_autorizado and modulo_ativo
```
Esse valor veio pela lei de De Morgan.

Não gostaríamos de analisar se o usuário não estivesse autorizado nem se o modulo estivesse ativo. Dessa forma gostaríamos de ter $A' + B'$, e pela lei de De Morgan, podemos simplificar a estrutura fazendo apenas $(A.B)'$ (Primeira lei de __*De Morgan*__)


Independentemente do resultado dessa validação, a aplicação apresenta uma resposta simulada para a ocorrência. A recomendação é definida localmente pela prioridade:

| Prioridade | Ação recomendada | Risco |
| --- | --- | --- |
| `baixa` | Registrar e acompanhar a ocorrência | Baixo impacto operacional |
| `media` | Programar avaliação técnica | Impacto operacional moderado |
| `alta` | Priorizar análise da equipe responsável | Possível impacto em módulos dependentes |
| `critica` | Ativar contingência e acionar manutenção imediatamente | Alto risco operacional |

> A resposta é uma simulação local; o projeto não faz chamadas para serviços de IA nem integrações externas.

## Dados e logs

- As ocorrências são persistidas em [`dados/dados_colonia.json`](dados/dados_colonia.json), no formato JSON, sob a chave `ocorrencias`.
- Os eventos de operação são registrados pelo componente `Logger` em `.logs/registros_colonia.txt`.
- A opção **Exibir registros TXT**, disponível no menu de consulta, apresenta o conteúdo do arquivo de log configurado quando ele existe.

Para limpar o log administrativo manualmente, descomente a chamada abaixo em [`codigo_fonte.py`](codigo_fonte.py) e execute novamente o programa:

```python
nucleo.zerar_logs()
```

O procedimento pede confirmação antes de apagar o conteúdo do arquivo.

## Estrutura do projeto

```text
.
├── codigo_fonte.py              # Ponto de entrada da aplicação
├── classes/
│   ├── ncas.py                  # Menu, cadastro, consulta e análise de alertas
│   └── logs.py                  # Registro de logs administrativos
├── dados/
│   └── dados_colonia.json       # Base de ocorrências
└── .logs/
    └── registros_colonia.txt    # Histórico de logs disponível no repositório
```

## Formato de uma ocorrência

Cada item de `ocorrencias` possui esta estrutura:

```json
{
    "id": 1,
    "modulo": "Habitação",
    "tipo": "Alerta",
    "prioridade": "media",
    "data": "2026-09-06 18:29:17",
    "status": "Aberta",
    "mensagem": "Erro de carregamento."
}
```

## Limitações conhecidas

- O campo `status` é criado como `Aberta`; esta versão não oferece uma opção de menu para alterá-lo.
- Os prompts e as recomendações são conteúdos demonstrativos, impressos localmente no terminal.
- O histórico textual de ocorrências é preparado pelo fluxo de cadastro, mas esta versão não o adiciona ao arquivo; o arquivo de log contém os eventos administrativos da aplicação.
