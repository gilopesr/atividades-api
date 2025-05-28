# Sistema de Controle de Atividades :orange_book:

## Descrição

Este é uma API RESTful focada no gerenciamento de Atividades. Desenvolvida com Flask, esta API oferece funcionalidades completas de Criação, Leitura, Atualização e Exclusão (CRUD) para dados relacionados a atividades, garantindo a persistência em um banco de dados relacional.

## Funcionalidades

Gerenciamento de Atividades: 

Capacidade de criar, visualizar, atualizar e excluir registros de atividades.

Persistência de Dados: Armazenamento seguro de informações em um banco de dados relacional.

Estrutura Modular: Organização do código com Blueprints para facilitar a manutenção e escalabilidade.

 ## 🔧 Tecnologias Utilizadas

  * Python
  * Flask
  * Flask-RESTx
  * SQLAlchemy (ORM)
  * Swagger
  * Docker
  * Docker Compose

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

## Execução

1.  **Inicialize o banco de dados:**

    ```bash
    with app.app_context():
    db.create_all()
    ```

  **Execute a API:**
Você pode executar a API diretamente ou usando Docker Compose.

2. Executando com Docker Compose (Recomendado)
Certifique-se de ter os arquivos Dockerfile e docker-compose.yml na raiz do seu projeto.

    ```bash
    docker-compose up --build
    ```

    Ou, se você estiver usando o arquivo principal para executar a aplicação:

    ```bash
    python app.py
    ```

 ## Acesse a documentação:

    * A API estará disponível em `http://localhost:5003/atividades` (ou na porta e host configurados).
  
 ## Endpoints da API:
   
   * A API expõe os seguintes endpoints específicos para o gerenciamento de Atividades:

   Atividades (/atividades)
* GET /atividades: Lista todas as atividades.
* GET /atividades/<id>: Obtém uma atividade específica por ID.
* POST /atividades: Cria uma nova atividade. 
* PUT /atividades/<id>: Atualiza uma atividade existente por ID. 
* DELETE /atividades/<id>: Exclui uma atividade por ID.

(Nota: Os endpoints acima são exemplos baseados em uma estrutura CRUD típica. Consulte o código-fonte em controllers/atividade_controller.py para os endpoints exatos e seus parâmetros.)
  


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
    
## Configuração

A aplicação é configurada através da classe `Config` no arquivo `config.py`. As seguintes opções estão disponíveis:

* `DEBUG`: Ativa/desativa o modo de depuração do Flask.
* `SQLALCHEMY_DATABASE_URI`: URI de conexão do banco de dados.
* `SQLALCHEMY_TRACK_MODIFICATIONS`: Ativa/desativa o rastreamento de modificações do SQLAlchemy.
* `HOST`: Endereço IP em que o servidor irá rodar.
* `PORT`: Porta em que o servidor irá rodar.

## Licença

[MIT License](https://opensource.org/licenses/MIT)
