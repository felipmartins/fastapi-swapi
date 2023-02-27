# Mentoria FastAPI - **Python na Web**
# Parte 1 - O Início da Aplicação
## Motivação

Antes mesmo de compartilhar a tela, inicie o momento trazendo o porquê dessa mentoria, em resumo esses pontos são:

* Mostrar um pouco do uso de Python no desenvolvimento web;
* Aprender a construir um projeto do zero em Python;
* Conectar com conteúdos de módulos anteriores (integração com front-end).

Faça o compartilhamento de tela já com o projeto `Star Wars Planet Search` (Front-End -> Seção 9 - Context API e React Hooks) rodando em sua máquina e pergunte a turma se lembram que projeto é esse quais funcionalidades ele implementa.

Em linhas gerais, comente que o projeto consome de uma API de Star Wars (`SWAPI`) que pode ser acessada em um desses links:

* https://swapi-trybe.herokuapp.com/api/planets/
* https://swapi.dev/api/planets

Finalize a motivação da mentoria dizendo para a turma o que almejamos alcançar com a mentoria Python na Web: 

**"Construíremos uma API similar à SWAPI usando Python e faremos a integração com o Front-End do projeto! No final, tudo ainda vai continuar funcionando mas com o Back-End que construímos aqui!"**

---

## Preparando para o Desenvolvimento

Compartilhe o seu VSCode em um diretório contendo apenas o ambiente virtual do Python, ainda sem nenhuma instalação. Nesse momento vale ressaltar com as Pessoas Estudantes que será tomada a primeira decisão em relação à estruturação do projeto: **Como nomear as pastas?**

Comente sobre ser comum nos projetos python termos duas pastas principais, uma contendo os testes e nomeada como `tests` e outra que pode, ou ser nomeada como `src`, ou receber o nome do pacote que iremos construir. Aqui, nomearemos como `swapi`.

O próximo passo agora é a instalação de dependências, explique o porquê da existência de dois arquivos ( `requirements.txt` e `dev-requirements.txt`) crie-os e coloque os pacotes que usaremos aqui. 

- Em produção usaremos o `FastAPI`(`fastapi==0.88.0`) e o SQLModel (`sqlmodel==0.0.8`). 
- Em desenvolvimento usaremos os mesmos da produção além do `flake8`, `black`, `pytest`e `uvicorn`. Esse último, é usado como nosso servidor e que vai se comunicar com o FastAPI.

Aqui, é interessante mostrar para as Pessoas Estudantes de onde vem os pacotes Python, por essa razão, abra a página do [PyPI](https://pypi.org) e mostre como procurar por um pacote.

---

<br>

## Construindo uma Rota Genérica

Comece um arquivo `main.py` dentro da pasta do projeto, nesse arquivo implemente uma rota `GET` simples, retornando um dicionário do Python e mostrando que o FastAPI, por debaixo dos panos, o transforma para um JSON e faz o retorno.

```python
from fastapi import FastAPI

app = FastAPI()

@app.get('/')
async def home():
    return {'details': 'Go to /docs for documentation'}
```

Coloque o servidor do uvicorn para funcionar para que as pessoas estudantes possam ver a aplicação funcionando `uvicorn swapi.main:app --reload`.

Acesse a rota que foi criada e em seguida mostre a rota de documentação criada pelo FastAPI.

---

<br>


## Construindo o Modelo

Comente que, apesar de funcionando, ainda não estamos retornando aquilo que queremos, para isso, devemos criar nosso modelo para começar a modelar as tabelas que serão usadas por nossa API. Lembre as Pessoas Estudantes que usaremos o `SQLModel` e que ele será nosso ORM. Retome o conceito de ORM.

Para essa construção, crie um arquivo `model.py` na pasta da aplicação. Nele implementaremos o modelo que desejamos. Vale lembrar que nosso objetivo é construir uma API similar à aquela consumida pelo Front-End do projeto Star Wars Planet Search, assim, nosso modelo será baseado nessa mesma API. Mostre um [retorno esperado](https://swapi.dev/api/planets/1).


```python
from typing import Optional
from sqlmodel import Field, SQLModel


class Planet(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=100)
    rotation_period: str = Field(max_length=40)
    orbital_period: str = Field(max_length=40)
    diameter: str = Field(max_length=40)
    climate: str = Field(max_length=40)
    gravity: str = Field(max_length=40)
    terrain: str = Field(max_length=40)
    surface_water: str = Field(max_length=40)
    population: str = Field(max_length=40)
```

---

<br>


## Estabelecendo a conexão com o Banco

O próximo passo é criar a conexão com o banco para que nosso ORM consiga fazer a criação das devidas tabelas. Nesse projeto iniciaremos o desenvolvimento com um tipo de banco em arquivo `.sqlite`.

Crie então um arquivo `db.py` dentro da pasta do projeto, nesse arquivo será implementado tudo aquilo que se refere à conexão / criação do banco e das tabelas.

```python
from sqlmodel import SQLModel, create_engine

sqlite_file_name = "database.sqlite"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}

engine = create_engine(
    sqlite_url,
    echo=True,
    connect_args=connect_args
)

def create_db_and_tables():
    from . import model  # noqa: F401

    SQLModel.metadata.create_all(engine)
```

Além dessa implementação, é necessário invocar a função `create_db_and_table()` toda vez que a aplicação iniciar sua execução. Para isso, adicionaremos o trecho de código abaixo no arquivo `main.py`

```python
@app.on_event("startup")
def on_startup():
    create_db_and_tables()
```

Isso será suficiente para que, ao iniciar o servidor uvicorn, o banco sqlite seja criado. Você pode usar a extensão do VSCode para visulizar arquivos sqlite e inspecionar a tabela que foi criada. Além disso, você também pode passar pelos logs mostrados no terminal dado que colocamos `echo=True` na engine que foi criada com o banco.

Para finalizar essa etapa, explique o conceito de "sessão" de conexão com o banco de dados, e comente que, toda vez que a API fizer alguma interação com o banco é necessário estabelecer uma sessão para essa ação, assim, implemente a função `get_session()` também no arquivo `main.py`.

```python
def get_session():
    return Session(engine)
```

Também vale comentar que essa definição é muito importante na hora de implementar os testes para a API, dado que podemos mockar uma sessão e garantir a conexão que desejamos para fazer testes, sem afetar assim o banco da nossa aplicação.

---

<br>


## Populando o banco de dados

Para que seja possível o funcionamento do projeto, precisamos que o banco, além de existir, tenha alguns planetas na tabela. Para fazer isso faremos uma inserção manual de planetas na tabela "populando" a tabela.

Para fazer isso, temos um arquivo JSON preparado `planets.json` com os dados à serem inseridos na tabela. A implementação dessa ação será feita em um outro arquivo `db_populate.py`.


```python
import json
from swapi.model import Planet


def populate_table_planet(session):
    with open("data/planets.json") as file:
        planets = json.load(file)

    for each_planet in planets:
        planet = Planet(
            id=each_planet["id"],
            name=each_planet["name"],
            rotation_period=each_planet["rotation_period"],
            orbital_period=each_planet["orbital_period"],
            diameter=each_planet["diameter"],
            climate=each_planet["climate"],
            gravity=each_planet["gravity"],
            terrain=each_planet["terrain"],
            surface_water=each_planet["surface_water"],
            population=each_planet["population"],
        )

        session.add(planet)
        session.commit()
```

Levante a questão para as pessoas estudantes de quando essa função `populate_table_planet` deve ser invocada. Além disso, pergunte o que aconteceria se tentássemos popular o banco mais de uma vez.

Uma vez que essa discussão se encerrar, você pode fazer a implementação das funções que verificam se a tabela está vazia e caso esteja popula a tabela desejada.

```python
def is_table_empty(session, model):
    return session.exec(select(model)).first() is None

def populate_empty_tables(session):
    if is_table_empty(session, Planet):
        populate_table_planet(session)
```

Uma vez implementadas, basta fazer a adição da chamada da função `populate_empty_tables` dentro da função `on_startup()` definida no arquivo `main.py`.

```python
with get_session() as session:
    populate_empty_tables(session)
```

## Criação da rota get_all_planets

Para finalizar a primeira parte da mentoria `Python na Web` devemos criar a rota que retorna todos os planetas presentes na tabela.


```python
@app.get("/api/planets/")
async def get_all_planets():
    with get_session() as session:
        planets = session.exec(select(Planet)).all()

        return planets
```

Mostre o funcionamento da rota na aplicação rodando no uvicorn e também na documentação. Aqui vale mostrar como poderíamos fazer para melhorar a documentação gerada para a aplicação com os parâmetros  `tags` e `response_model` dentro do decorator da rota.


```python
@app.get("/api/planets/", tags=["planets"], response_model=Planet)
async def list_planets():
    with get_session() as session:
        planets = session.exec(select(Planet)).all()

        return planets
```

Por fim, vale retornar à [aplicação original](https://swapi.dev/api/planets) e verificar se o retorno que estamos obtendo da nossa aplicação é EXATAMENTE o mesmo que é obtido da aplicação original.

A última ação desta mentoria é então, construir uma função auxiliar que retorna uma estrutura similar à aquela apresentada na API original. Feito isso, podemos adicionar a função ao retorno da rota criada.

```python
def create_response(result):
    return {
        "count": len(result),
        "next": None,
        "previous": None,
        "results": result,
    }

@app.get("/api/planets/", tags=["planets"], response_model=Planet)
async def list_planets():
    with get_session() as session:
        planets = session.exec(select(Planet)).all()

        return create_response(planets)
```
<br>

# Parte 2 - Testes e Relacionamentos

## Recapitulando

Assista a gravação do primeiro momento Python na Web que aconteceu com a turma, veja se todo o conteúdo previsto para a primeira parte foi executado, então, comece fazendo uma recapitulação sobre o que foi construído até o momento. 

Passe rapidamente pela motivação da mentoria e por cada um dos arquivos que foram implementados. Essa ação de revisão não deve demorar mais de 10 minutos. Coloque a aplicação para rodar e mostre-a em funcionamento, como havia sido feito na parte anterior. Caso tenha faltado algum conteúdo referente à primeira parte da mentoria, comece por esse conteúdo, em seguida continue esse script.

```shell
uvicorn swapi.main:app --reload
```

Finalizada a revisão do que foi construído, você pode trazer para as pessoas estudantes o que será implementado na mentoria de hoje. Os principais tópicos que serão abordados são: **Testes** e **Relacionamentos** no bando de dados.

----

## Iniciando os testes

Para criar o primeiro teste, primeiro será criado o arquivo ```test_db_populate.py``` dentro do diretório de testes. Nesse arquivo começaremos com a criação de duas fixtures: A primeira delas é a ```engine_fixture``` que será a engine que usaremos nos testes que envolvem funções que usam o banco de dados. Essa fixture é uma *engine* que acessa um banco de dados em memória através de uma conexão estática. 

```python
@pytest.fixture(name='engine')
def engine_fixture():
    engine = create_engine(
        "sqlite://",  # Creates in-memory database
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,  # Single static connection pool
    )
    SQLModel.metadata.create_all(engine)

    return engine
```

A segunda fixture são dados de dois planetas dois planetas que usaremos para substituir a leitura do arquivo json que foi utilizado para popular o banco de dados da nossa aplicação. 

```python
@pytest.fixture
def fake_planets_data():
    return [
        {
            "id": 1,
            "name": "Tatooine",
            "rotation_period": "23",
            "orbital_period": "304",
            "diameter": "10465",
            "climate": "arid",
            "gravity": "1 standard",
            "terrain": "desert",
            "surface_water": "1",
            "population": "200000",
        },
        {
            "id": 2,
            "name": "Alderaan",
            "rotation_period": "24",
            "orbital_period": "364",
            "diameter": "12500",
            "climate": "temperate",
            "gravity": "1 standard",
            "terrain": "grasslands, mountains",
            "surface_water": "40",
            "population": "2000000000",
        },
    ]
```

Agora, é possível começar a implementação do teste. A complexidade maior nesse teste está em entender como serão usadas aqui as fixtures acima e a criação do mock que lerá o conteúdo da fixture dos planetas. A asserção que será criada verifica se a quantidade de planetas no banco em memória é igual a quantidade de planetas ao da fixture implementada, demonstrando o funcionamento correto da função ```populate_table_planet```.

```python
def test_populate_table_planet(engine, fake_planets_data):
    fake_data_open = mock_open(
        read_data=json.dumps(fake_planets_data)
    )

    with (
        Session(engine) as session, 
        patch('builtins.open', fake_data_open)
    ):
        populate_table_planet(session)

        planets = session.exec(select(Planet)).all()
        assert len(planets) == len(fake_planets_data)
```

----


## Criando o segundo modelo

Podemos partir para a criação do segundo modelo que nos possibilitará criar um relacionamento entre as tabelas. É importante lembrar que estamos implementando uma API que é similar à uma outra já existente, portanto, assim como fizemos para ```Planet```, temos campos já determinados para o modelo que criaremos: ```Person```. Se desejar, você pode abrir a SWAPI original e mostrar esses campos, uma outra opção é mostrar o json que está na pasta ```data```.

Mostre que a criação do segundo modelo é muito similar ao do primeiro, exceto pela últimas linhas, que se referem à criação da coluna que conterá a chave estrangeira e o relacionamento. Lembre-se também que será necessário adiconar a linha referente ao relacionamento no modelo ```Planet```.


```python
class Planet(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    name: str = Field(max_length=100)
    rotation_period: str = Field(max_length=40)
    orbital_period: str = Field(max_length=40)
    diameter: str = Field(max_length=40)
    climate: str = Field(max_length=40)
    gravity: str = Field(max_length=40)
    terrain: str = Field(max_length=40)
    surface_water: str = Field(max_length=40)
    population: str = Field(max_length=40)

    residents: List["Person"] = Relationship(back_populates="homeworld")


class Person(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    name: str = Field(max_length=100)
    height: str = Field(max_length=50)
    mass: str = Field(max_length=50)
    hair_color: str = Field(max_length=50)
    skin_color: str = Field(max_length=50)
    eye_color: str = Field(max_length=50)
    birth_year: str = Field(max_length=50)
    gender: str = Field(max_length=50)

    planet_id: int = Field(default=None, foreign_key='planet.id')
    homeworld: Planet = Relationship(back_populates="residents")
```

---

## Populando a tabela Person
Volte ao arquivo ```db_populate.py```e implemente a função que será responsável por executar o povoamento da tabela Person. Invista um tempo aqui em explicar o funcionamento do __**__ e como há um ganho de legibilidade ao usar essa prática.

```python
def populate_table_person(session):
    with open("data/people.json") as file:
        people = json.load(file)

    for each_person in people:
        person = Person(**each_person)

        session.add(person)
        session.commit()
```

Lembre-se de acrescentar as linhas de código referente à tabela ```Person```dentro da função ```populate_empty_tables```.

```python
def populate_empty_tables(session):
    if is_table_empty(session, Planet):
        populate_table_planet(session)

    if is_table_empty(session, Person):
        populate_table_person(session)
```
---

## Implementando mais alguns testes

O próximo passo aqui é implementar mais dois testes referentes à API propriamente dita. Para isso, será necessário adicionar mais duas bibliotecas auxiliares aqui usadas pelo FastAPI ao arquivo dev-requirements.txt, instale novamente as dependências para prosseguir.

```python
starlette==0.22.0
httpx
```

O primeiro teste à ser implementado é o teste da rota que já está implementada e que retorna todos os planetas. Para esse primeiro teste é usado mais uma vez um **mock**, mas agora, ao invés de mockarmos apenas a engine, faremos o mock da sessão como um todo. Essa decisão pode ser justificada ao se analisar a estrutura da rota que foi criada e também pelo fato de que nossos testes não deveriam usar o banco de dados da API para fazer os testes em si.

Assim, usando o mock da sessão, testa-se o status code e também a quantidade de planetas dentro do banco em memória. Uma vez que mockamos nossa sessão sabemos quantos planetas deveriam existir lá.

O segundo teste pode ser construído antes mesmo da implementação da rota, aqui, você pode perguntar para as pessoas estudantes como elas fariam para implementar esse teste. Proponha então criar a fixture contendo os dados de um planeta e faça as asserções referentes ao `status_code` e `id` do novo elemento que foi inserido na tabela.


```python
from fastapi.testclient import TestClient
import pytest
from swapi.main import app
from unittest.mock import patch
from swapi.db_populate import populate_empty_tables
from sqlmodel.pool import StaticPool
from sqlmodel import SQLModel, create_engine, Session
from fastapi.testclient import TestClient
from swapi.main import app

client = TestClient(app)


def get_session_mock():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    session = Session(engine)
    populate_empty_tables(session)

    return session


def test_get_planet_route():
    with patch('swapi.main.get_session', get_session_mock):
        response = client.get("/api/planets/")

        assert response.status_code == 200
        data = response.json()

        assert data["count"] == 60


@pytest.fixture
def single_planet_mock():
    return {
        "name": "new_planet",
        "rotation_period": "14",
        "orbital_period": "34",
        "diameter": "1045",
        "climate": "tropic",
        "gravity": "1 standard",
        "terrain": "planains",
        "surface_water": "1",
        "population": "50000",
    }


def test_post_planet_route(single_planet_mock):
    with patch("swapi.main.get_session", get_session_mock):
        response = client.post("/api/planets/", json=single_planet_mock)
        # Check if status code is 201 (created)
        assert response.status_code == 201
        data = response.json()
        # Check if new id is correct (previous data was 1-60)
        assert data["id"] == 61
```
---

## Implementação da rota post

Implemente a nova rota e retome conceitos como a modificação do status_code que é retornado e também a tag de documentação que escolhemos.

```python
@app.post("/api/planets/",  tags=["planets"], status_code=201)
async def create_planet(planet: Planet):
    with get_session() as session:
        session.add(planet)
        session.commit()
        session.refresh(planet)
        return planet
```

Depois da implementação, abra a rota de documentação e mostre todas as rotas que foram criadas, além disso, use esse momento para discutir a presença do campo id dentro da requisição POST que será feita. Discuta com as pessoas estudantes possíveis refatorações nesse modelo.

---