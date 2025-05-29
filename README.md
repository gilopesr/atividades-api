# Sistema de  Gestão de Atividades e Submissões  :orange_book:

Este é uma API RESTful focada no gerenciamento de Atividades. Desenvolvida com Flask, esta API oferece funcionalidades completas de Criação, Leitura, Atualização e Exclusão (CRUD) para dados relacionados a atividades, garantindo a persistência em um banco de dados relacional.

### Funcionalidades Principais:

* **Criação de Atividades:** Permite incluir o ID da disciplina, o enunciado da atividade e uma lista opcional de respostas de alunos. Cada resposta inclui o ID do aluno, o conteúdo da resposta e a nota. O ID do aluno é validado externamente.

* **Consulta de Atividades:** Fornece uma lista completa de atividades, com todos os seus detalhes e as submissões associadas a cada uma.

* **Buscar Atividade por ID** Consulta os detalhes de uma atividade específica.

* **Atualizar Atividade :** PModifica informações de uma atividade ou suas submissões.
* **Exclusão de Atividade:** Permite Remover uma atividade do sistema.

 ## 🔧 Tecnologias Utilizadas

  * Python
  * Flask
  * Flask-RESTx
  * SQLAlchemy (ORM)
  * Docker
  * Docker Compose


## Estrutura do Projeto

A estrutura do projeto é a seguinte:  📂

    ```
    ├── Atividade/
    |   ├── controllers/
    |   │   ├── __init__.py
    |   │   └── atividade_controller.py
    |   ├── models/
    |   │   ├── __init__.py
    |   │   └── atividade_model.py
    |   ├── config.py
    |   ├── app.py   
    |   ├── dockerfile
    |   ├── requirements.txt
    |   └── docker-compose.yml
    ├── LICENCE
    └── README.md
    ```
    



 ## 🧩 Integração com Microserviços
 
Este serviço opera como parte de um ecossistema de microserviços, interagindo com a API-SchoolSystem:

API-SchoolSystem: Responsável por dados de turmas e professores.

Serviço de Atividades: Gerencia unicamente a lógica de agendamento de atividades.


## Pré-requisitos

* Python 3.x
* pip (gerenciador de pacotes do Python)
* Um banco de dados compatível com SQLAlchemy (SQLite, MySQL, PostgreSQL, etc.)
* Docker
* Docker Compose (geralmente incluído na instalação do Docker Desktop)

## Configuração e Instalação

1.  **Clone o repositório:**

    ```bash
      git clone [https://github.com/gilopesr/atividades-api.git](https://github.com/gilopesr/atividades-api.git)
      cd Atividades
    ```

2.  **Crie um ambiente virtual (recomendado):**

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # No Linux/macOS
    venv\Scripts\activate  # No Windows
    ```

3.  **Instale as dependências:**

    ```bash
    pip install -r requirements.txt
    ```

5.  **Configure as variáveis de ambiente:**

    * Defina a variável `FLASK_APP` para o nome do seu arquivo principal (geralmente `app.py` ou `__init__.py`).

    * Exemplo no Linux/macOS:

        ```bash
        export FLASK_APP=app.py
        ```

    * Exemplo no Windows:

        ```bash
        set FLASK_APP=app.py
        ```


  ## Como Executar a API:
Você pode executar a API diretamente ou usando Docker Compose.

1. Executando com Docker Compose (Recomendado)
Certifique-se de ter os arquivos Dockerfile e docker-compose.yml na raiz do seu projeto.

    ```bash
    docker-compose up --build
    ```

    Ou, se você estiver usando o arquivo principal para executar a aplicação:

    ```bash
    python app.py
    ```

 ## Acesse a documentação:

    * A API estará disponível em `http://localhost:5003/api` 

   
  ## Endpoints da API (Rotas)

A API de Reservas de Salas expõe os seguintes endpoints:

### Atividades (`/api/atividades`)

#### `POST /atividades`

Cria uma nova atividade e opcionalmente suas submissões iniciais.

* **Corpo da Requisição (JSON):**
    ```json
   {
    "id_disciplina": 101,
    "enunciado": "Crie um app de todo em Flask com autenticação de usuário.",
    "respostas": [
        {
            "id_aluno": 1,
            "resposta": "todo_app_v1.py",
            "nota": 9
        },
        {
            "id_aluno": 2,
            "resposta": "todo_app_final.zip",
            "nota": 10
        }
    ]
   }
    ```

* **Respostas:**
    * `201 OK`: Reserva criada com sucesso. Retorna os detalhes da reserva criada.
    * `400 Bad Request`: Dados inválidos (campos faltando, formato incorreto, ID inválido, hora de início >= hora de fim).
    * `400 Bad Request`: Turma ou professor não encontrados/API-SchoolSystem indisponível.
    * `409 Conflict`: Conflito de horário para a sala e período especificados.

#### `GET /atividades`

Lista todas as atividades existentes no sistema.

* **Respostas:**
    * `200 OK`: Retorna uma lista de objetos de atividades.
   

   ---

#### `GET /atividades/<int:id_atividade>`

Obtém os detalhes de uma atividade específica pelo seu ID.

* **Parâmetros de URL:**
    * `id_atividade` (inteiro): O ID único da atividade .
* **Respostas:**
    * `200 OK`: Retorna o objeto da atividade.
    * `404 Not Found`: Atividade não encontrada.

---

#### `PATCH /atividades/<int:id_atividade>`

Permite a atualização parcial de uma atividade. Pode atualizar o enunciado, a disciplina e/ou manipular as submissões (adicionar novas, atualizar existentes ou remover)..

* **Parâmetros de URL:**
    * `id_atividade` (inteiro): O ID único da atividade a ser atualizada.
* **Corpo da Requisição (JSON):**
    ```json
    {
    "id_disciplina": 102,
    "enunciado": "Refatore o app de todo para usar Blueprints e SQLAlchemy."
   }

    ```

* **Respostas:**
    * `200 OK`: { "mensagem": "Atividade atualizada com sucesso" }
    * `400 Bad Request`: { "erro": "Mensagem de erro" }
    * `404 Not Found`: { "erro": "Atividade não encontrada." }
    * `500 Internal Server Error`: { "erro": "Ocorreu um erro ao atualizar a atividade." }

---


#### `DELETE /atividades/<int:id_atividade>`

Deleta uma atividade existente pelo seu ID.

* **Parâmetros de URL:**
    * `id_atividade` (inteiro): O ID único da atividade a ser deletada.
* **Respostas:**
    * `200 OK`: Atividade deletada com sucesso.
    * `404 Not Found`: Atividade não encontrada.

## Configuração

A aplicação é configurada através da classe `Config` no arquivo `config.py`. As seguintes opções estão disponíveis:

* `DEBUG`: Ativa/desativa o modo de depuração do Flask.
* `SQLALCHEMY_DATABASE_URI`: URI de conexão do banco de dados.
* `SQLALCHEMY_TRACK_MODIFICATIONS`: Ativa/desativa o rastreamento de modificações do SQLAlchemy.
* `HOST`: Endereço IP em que o servidor irá rodar.
* `PORT`: Porta em que o servidor irá rodar.

## Licença

[MIT License](https://opensource.org/licenses/MIT)
