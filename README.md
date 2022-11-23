# Script para continuação das mentorias _Python na Web_

# O que foi feito até agora:


[Link para o código da parte 2](https://github.com/tryber/sd-019-a-live-lectures/tree/mentoria/cs/python-na-web/parte-2)


Iniciar o momento com a revisão da proposta do momento _Python na Web_, mostrando a API que é consumida no projeto _Star Wars Planet Search_ que foi construída em _Django_, é importante ressaltar a estrutura da API mostrando o que se é esperado da requisição e que vamos construir uma estrutura similar utiliando o _FASTAPI_, além disso, é importante fazer a revisão do código que já foi preparado até o momento.

```shell
swapi
├── db.py
├── main.py
└── model.py

tests
└── test_db_populate.py
```
----

O arquivo ```model.py``` contém a estrutura do básica da tabela _Planet_, na qual a classe representa a tabela que é criada no banco e seus atributos são as colunas dessa mesma tabela. Para cada um dos atributos da classe são definidas seuas características específicas, como tipagem, valores _default_, comprimento máximo (_max length_), opcionalidade, chave primária ou não, entre outras coisas que ainda não foram utilizadas no código.

----

No arquivo ```db.py``` são importadas as definições feitas no arquivo ```model.py``` e é feita toda a configuração para utilização do banco de dados _sqlite_. São definidos o nome do arquivo do banco e também sua url de conexão. Ainda, é criado o motor que lida com todas as operações do banco, e são passados parâmetros que verificam se tais operações são realizadas por uma mesma _thread_ e que ecoam o log das operações no terminal para que se possa acompanhar o que foi realizado pelo motor.

Além disso, nesse mesmo arquivo são definidas 3 funções importantes para o funcionamento da API. A primeira delas é a que, quando invocada, faz a criação do banco e de suas tabelas. A segunda é a função que popula o banco de dados a partir de um arquivo _JSON_ que se encontra dentro da pasta ```data``` na raíz do projeto, nesse arquivo constam 60 planetas que são lidos e inseridos no banco através da invocação da função.

```shell
data
└── planets.json
```

Por fim, a última função definida nesse arquivo é a função que faz a invocação da função descrita anteriormente. A intenção dessa função é invocar simultaneamente todas as funções que forem definidas nesse projeto que tem a intenção de popular tabelas do banco de dados, isto é, caso sejam criadas novas tabelas que também serão populadas, esta última função deverá invocar todas as outras funções que lidam com a inserção de dados nas tabelas.

----

Para testar a função que popula a tabela foi escrito um teste no arquivo ```test_db_populate.py```. Para sua execução são criadas duas _fixtures_ que serão utilizadas neste teste, a primeira delas representa a estrutura de um banco de dados em memória que será utilizado para realizar os testes, já a segunda representa um _mock_ que contém dois planetas que serão inseridos no banco através da função que será testada. Por fim, o teste verifica se a quantidade de planetas no banco em memória é igual a quantidade de planetas no _mock_, demonstrando o funcionamento correto da função.

----

O último dos arquivos que deve ser revisado é o ```main.py```, nele são construídas funções que atuam diretamente no funcionamento da API. A primeira delas, ```on_startup()```, é que é executada assim que a aplicação é iniciada, ela verificará a existência do arquivo do banco, e de acordo com o resultado, fará ou não o povoamento das tabelas.

A segunda função ```create_response()``` é uma função auxiliar que nos ajudará a escrever a resposta da requisição de acordo com o formato que desejamos. É válido mostrar novamente a resposta da ```SWAPI``` original escrita em _Django_.

Por fim, é escrita a função que implementa a rota ```GET``` que lista todos os planetas, essa rota funciona através da execução da _query_ _"select"_ usando a classe _Planet_. Ainda, vale lembrar que toda aplicação ```FASTAPI``` implementa uma rota ```/docs``` que cria uma documentação ```SWAGGER``` automaticamente baseado nos schemas que foram criados também automaticamente pelo código.

Para ter um momento de melhor qualidade, abra dois terminais, execute os testes em um deles e no outro deixe a aplicação rodando, para isso, use o comando:

```shell
uvicorn swapi.main:app --reload
```

----

## Início da parte 3:

Para começar a mentoria faremos a adição de algumas dependências ao arquivo ```dev-requirements.txt```. Serão adicionadas duas novas linhas: ```pytest-cov``` e ```requests```. Essas linhas são adicionadas para que possamos testar com melhor qualidade as funções que estamos escrevendo.

Inicialmente, vamos mostrar o comando que é usado para rodar os testes com a nova dependência instalada e ler o relatório que é colocado no terminal, neste relatório é possível visualizar as linhas que estão e não estão sendo testadas.

```shell
python3 -m pytest --cov-report term-missing --cov=swapi tests/
```

Será observado que o arquivo ```main.py``` não está sendo testado, por essa razão, o primeiro ponto a ser implementado aqui será o teste da rota que foi criada, embora que, para escrever esse teste, será necessária uma refatoração do código, isso porque, para os testes, será utilizado um banco em memória mockado.

A refatoração consiste em implementar uma função ```get_session()```dentro do arquivo ```main.py``` que retorna a própria sessão recebendo como parâmetro uma engine. Isso irá nos permitir mockar essa sessão, podendo assim, encaminhar as ações do teste para uma sessão mockada que serão direcionadas ao banco que está em memória e não o banco da aplicação de fato. Essa refatoração fará com que a função ```list_planets``` na abertura do contexto da sessão. Veja só:

```python
def get_session():
    return Session(engine)


@app.get("/api/planets/", tags=["planets"])
async def list_planets():
    with get_session() as session:
        planets = session.exec(select(Planet)).all()

        return create_response(planets)
```

Feito isso, podemos começar a escrever nosso teste em um novo arquivo, como vamos testar o arquivo ```main.py```, podemos nomear o arquivo de teste como ```test_main.py```. Por enquanto, escreveremos duas funções neste arquivo, a primeira é aquela que retorna a sessão mockada que direciona para o arquivo do banco em memória, a segunda é a função do teste em si. Além disso, é importante fazer as devidas importações e apresentar o ```TestClient``` que o ```FASTAPI``` traz para realizar os testes da aplicação. O código fica assim:

```python
from sqlmodel import create_engine, Session, SQLModel
from sqlmodel.pool import StaticPool
from unittest.mock import patch
from swapi.main import app
from fastapi.testclient import TestClient
from swapi.db import populate_all_tables

client = TestClient(app)

def get_session_override():

    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    session = Session(engine)
    populate_all_tables(session)

    return session


def test_get_planets_route():

    with patch("swapi.main.get_session", get_session_override):

        res = client.get("/api/planets/")
        assert res.status_code == 200
        data = res.json()
        assert data["count"] == 60
```

Isso já fará com que a nossa cobertura de testes aumente consideravalmente, ainda faltaram alguns trechos de código de serem testados, mas sem grandes preocupações quanto a isso. Agora, iremos escrever nossa primeira rota ```POST```que faz a criação de um planeta, no entanto, agora, começaremos pelo teste. No mesmo arquivo anterior, escreveremos uma nova função que usará de uma nova fixture que representa o mock de um planeta a ser inserido. O resultado final desse teste fica assim:

```python
import pytest

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
    with patch("swapi.main.get_session", get_session_override):

        res = client.post("/api/planets/", json=single_planet_mock)
        assert res.status_code == 201
        data = res.json()
        assert data["id"] == 61
```

Logo em seguida podemos implementar a rota de fato, a diante, será realizada alguma refatoração nesse arquivo para adequadar o modelo, mas por enquanto o arquivo fica assim:

```python
@app.post("/api/planets/",  tags=["planets"], status_code=201)
async def create_planet(planet: Planet):
    with get_session() as session:    
        session.add(planet)
        session.commit()
        session.refresh(planet)
        return planet
```

Agora, é importante criar a motivação que nos levará para a refatoração, para isso, na rota da documentação da API, iremos testar a a rota criada. Veremos que no corpo da requisição é passado um ```ìd```, mas que se enviarmos a requisição sem esse campo, funciona normalmente. Faremos então uma refatoração nos nossos modelos que, em seguida, implicará em uma refatoração na rota ```POST```. Veja:

```python
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship

class PlanetBase(SQLModel):
    name: str = Field(max_length=100)
    rotation_period: str = Field(max_length=50)
    orbital_period: str = Field(max_length=50)
    diameter: str = Field(max_length=50)
    climate: str = Field(max_length=50)
    gravity: str = Field(max_length=50)
    terrain: str = Field(max_length=50)
    surface_water: str = Field(max_length=50)
    population: str = Field(max_length=50)

class Planet(PlanetBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

class PlanetCreate(PlanetBase):
    pass

class PlanetRead(PlanetBase):
    id: int
```
----
```python
from swapi.model import Planet, PlanetCreate, PlanetRead

@app.post("/api/planets/",  tags=["planets"], status_code=201)
async def create_planet(planet: PlanetCreate):
    with get_session() as session:    
        db_planet = Planet.from_orm(planet)
        session.add(db_planet)
        session.commit()
        session.refresh(db_planet)
        return db_planet
```

Após a modificação dos modelos, é interessante recriar o banco que é utilizado pela aplicação, para isso, apague o arquivo ```database.sqlite```e reinicialize a aplicação do ```FASTAPI```usando o comando:

```shell
uvicorn swapi.main:app --reload
```

A próxima rota a ser implementada é a rota de busca por planeta, ela pode receber dois ```query params``` caso nenhum tenha sido passado a rota retorna todos os planetas, mas caso eles tenham sido passados é feita uma busca dentro do banco de dados para retornar apenas os planetas que satisfaçam os valores dos parâmetros. Dessa vez, não começaremos pelo teste em razão de desconhecer o número de planetas que satisfazem determinadas condições, sendo assim, podemos implementar a nova rota e mostrar seu funcionamento através da rota ```/docs```. Define-se um query param no FASTAPI quando há parâmetros na função que não estão descritos na rota, além disso, podemos fazer com que tais parâmetros sejam opcionais caso coloquemos um valor padrão ```None``` para eles. O código fica assim:

```python
@app.get("/api/planets/search", tags=["planets"])
async def search_planets(name: str = None, gravity: str = None):
    with get_session() as session:
        if name and not gravity:
            planets = session.exec(select(Planet).where(Planet.name == name)).all()
        elif not name and gravity:
            planets = session.exec(select(Planet).where(Planet.gravity == gravity)).all()
        elif name and gravity:
            planets = session.exec(select(Planet).where(Planet.name == name).where(Planet.gravity == gravity)).all()
        else:
            planets = session.exec(select(Planet)).all()
    
        return create_response(planets)
```

# Fim da parte 3 
---

# Início da parte 4

[Link para o código para o início da parte 4](https://github.com/tryber/sd-019-a-live-lectures/blob/mentoria/cs/python-na-web/parte-3/swapi/main.py)

Vale revisar as rotas que foram criadas no arquivo ```main.py```e rodar os testes com o relatório de cobertura.

```shell
python3 -m pytest --cov-report term-missing --cov=swapi tests/
```

Uma vez que a rota está criada, podemos fazer alguns testes manuais antes de escrever o teste, para isso, use a rota ```/docs```. Mostre a rota funcionando caso nenhum parâmetro seja passado, caso apenas ```name```seja passado, caso apenas ```gravity```seja passado e caso ambos os parâmetros sejam passados. Com os valores obtidos dessa inspeção manual podemos escrever quatro novas funções de testes no nosso arquivo ```test_main.py```. Veja só:

```python
def test_planet_search_route_with_no_query():

    with patch("swapi.main.get_session", get_session_override):

        res = client.get("/api/planets/search/")
        assert res.status_code == 200
        data = res.json()
        assert data["count"] == 60

def test_planet_search_route_with_name_only():

    with patch("swapi.main.get_session", get_session_override):

        res = client.get("/api/planets/search?name=Hoth")
        assert res.status_code == 200
        data = res.json()
        assert data["count"] == 1

def test_planet_search_route_with_gravity_only():

    with patch("swapi.main.get_session", get_session_override):

        res = client.get("/api/planets/search?gravity=unknown")
        assert res.status_code == 200
        data = res.json()
        assert data["count"] == 15

def test_planet_search_route_with_name_and_gravity():

    with patch("swapi.main.get_session", get_session_override):

        res = client.get("/api/planets/search?name=Hoth&gravity=unknown")
        assert res.status_code == 200
        data = res.json()
        assert data["count"] == 0
```

A última rota que escreveremos relacionada aos planetas é a rota que retorna o planeta desejado de acordo com o seu ``ìd```, aqui, podemos começar escrevendo o teste por se tratar de um teste mais simples. Veja só:

```python
def test_get_planet_by_id_route():
    with patch("swapi.main.get_session", get_session_override):

        res = client.get("/api/planets/1")
        assert res.status_code == 200
        data = res.json()
        assert data["id"] == 1
```

Por fim, escrevemos então a rota referente à esse teste, em seguida, podemos novamente abrir a rota ```/docs``` para que sejam feitos testes manuais, é possível acessar a própria rota no navegador também. Definimos um ```path param``` ao colocá-lo, ao mesmo tempo, como parâmetro da função e também na rota desejada, esse parâmetro assume o valor daquilo que é passado na rota. O código para a nova rota fica assim:

```python
@app.get("/api/planets/{id}", tags=["planets"], response_model=PlanetRead)
async def list_planet_by_id(id: int):
    with get_session() as session:
        planet = session.exec(select(Planet).where(Planet.id == id)).one()

        return planet
```

Trabalharemos agora implementando um novo modelo, o modelo ```People```, vale novamente entrar na API original que estamos embasando para mostrar quais os atributos que novo modelo possui, além disso, mostrar que há um relacionamento entro o modelo ```Planet``` e o modelo ```People```. Já o escreveremos esse novo modelo no formato em que estamos trabalhando e, além disso, iremos acrescentar uma linha no modelo base dos planetas para fazer o relacionamento que existe entre esses modelos. O código fica assim:

```python
class PlanetBase(SQLModel):
    name: str = Field(max_length=100)
    rotation_period: str = Field(max_length=50)
    orbital_period: str = Field(max_length=50)
    diameter: str = Field(max_length=50)
    climate: str = Field(max_length=50)
    gravity: str = Field(max_length=50)
    terrain: str = Field(max_length=50)
    surface_water: str = Field(max_length=50)
    population: str = Field(max_length=50)
    residents: List["People"] = Relationship(back_populates="homeworld")

class PeopleBase(SQLModel):
    name: str = Field(max_length=100)
    height: str = Field(max_length=50)
    mass: str = Field(max_length=50)
    hair_color: str = Field(max_length=50)
    skin_color: str = Field(max_length=50)
    eye_color: str = Field(max_length=50)
    birth_year: str = Field(max_length=50)
    gender: str = Field(max_length=50)
    planet_id: int = Field(default=None, foreign_key="planet.id")
    homeworld: Planet = Relationship(back_populates="residents")


class People(PeopleBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    

class PeopleCreate(PeopleBase):
    pass


class PeopleRead(PeopleBase):
    id: int

```

Uma vez que criamos o modelo, vamos adicionar alguns dados à essa tabela provenientes do arquivo ```people.json``` que foi previamente preparado para popular a tabela ```People```, aqui, faremos um processo similar ao que já estava sendo realizado com a tabela ```Planet```, assim, no arquivo ```db.py```vamos criar uma nova função ```populate_table_people()``` e adicioná-la a função ```populate_all_tables()```, ao fazer isso, apagando o banco e reinicializando a aplicação, teremos um banco que possui duas tabelas e que ambas tem dados populados. O código implementado fica assim:

```python
from .model import Planet, People

def populate_all_tables(session):
    populate_table_planets(session)
    populate_table_people(session)


def populate_table_people(session):
    with open("data/people.json") as file:
        people = json.load(file)

    for each_person in people:
        person = People(
            id=each_person["id"],
            name=each_person["name"],
            height=each_person["height"],
            mass=each_person["mass"],
            hair_color=each_person["hair_color"],
            skin_color=each_person["skin_color"],
            eye_color=each_person["eye_color"],
            birth_year=each_person["birth_year"],
            gender=each_person["gender"],
            planet_id=each_person["planet_id"],
        )

        session.add(person)
        session.commit()
```

O próximo passo então é criar o teste que verifica se a função que popula o banco está devidamente implementada, isso também será feito de maneira similar ao que já foi implementado para a tabela ```Planet```. O código adicional implementado no arquivo ```test_db_populate.py```fica assim:

```python
from swapi.db import populate_table_planets, populate_table_people
from swapi.model import Planet, People

@pytest.fixture
def fake_people_data():
    return [
        {
            "id": 1,
            "name": "Luke Skywalker",
            "height": "172",
            "mass": "77",
            "hair_color": "blond",
            "skin_color": "fair",
            "eye_color": "blue",
            "birth_year": "19BBY",
            "gender": "male",
            "planet_id": "1",
        },
        {
            "id": 2,
            "name": "C-3PO",
            "height": "167",
            "mass": "75",
            "hair_color": "n/a",
            "skin_color": "gold",
            "eye_color": "yellow",
            "birth_year": "112BBY",
            "gender": "n/a",
            "planet_id": "1",
        },
    ]


def test_populate_table_people(engine, fake_people_data):
    with (
        patch("builtins.open", mock_open(read_data=json.dumps(fake_people_data))),
        Session(engine) as session,
    ):
        populate_table_people(session)

        people = session.exec(select(People)).all()

        assert len(people) == len(fake_people_data)

```

Uma vez que fizemos isso, podemos começar a escrever os testes e rotas relacionados à essa tabela. Serão três rotas bem similares ao que produzimos anteriormente para a tabela ```Planet```, assim, podemos começar pela implementação dos testes sem prejuízo algum. As três rotas que iremos escrever são: ```Listagem de todas as pessoas, criação de uma nova pessoa, listagem de uma pessoa por id```. Lembre-se que para o teste de criação de uma nova pessoa será necessário criar uma pessoa mockada cujo JSON será passado no corpo da requisição.O código dos testes para as rotas mencionadas fica assim:

```python
@pytest.fixture
def single_people_mock():
    return {
            "name": "Not Luke",
            "height": "170",
            "mass": "72",
            "hair_color": "dark",
            "skin_color": "fair",
            "eye_color": "green",
            "birth_year": "19BBY",
            "gender": "male",
            "planet_id": "1",
            }

def test_get_people_route():

    with patch("swapi.main.get_session", get_session_override):
        res = client.get("/api/people/")
        assert res.status_code == 200
        data = res.json()
        assert data["count"] == 83


def test_post_people_route(single_people_mock):
    with patch("swapi.main.get_session", get_session_override):
        res = client.post("/api/people/", json=single_people_mock)
        assert res.status_code == 201
        data = res.json()
        assert data["id"] == 84


def test_get_people_by_id_route():
    with patch("swapi.main.get_session", get_session_override):
        res = client.get("/api/people/1")
        assert res.status_code == 200
        data = res.json()
        assert data["id"] == 1
```

Após a implementação desses testes, podemos criar as rotas à que se referem, o código para ela fica assim:

```python
from swapi.model import Planet, PlanetCreate, PlanetRead, People, PeopleCreate, PeopleRead

@app.get("/api/people/",  tags=["people"])
async def list_people():
    with get_session() as session:
        people = session.exec(select(People)).all()

        return create_response(people)


@app.post("/api/people/",  tags=["people"], status_code=201)
async def create_people(people: PeopleCreate):
    with get_session() as session:
        db_people = People.from_orm(people)
        session.add(db_people)
        session.commit()
        session.refresh(db_people)
        return db_people


@app.get("/api/people/{id}", tags=["people"], response_model=PeopleRead)
async def list_people_by_id(id: int):
    with get_session() as session:
        people = session.exec(select(People).where(People.id == id)).one()

        return people
```

Após a implementação é interessante mais uma vez acessar a documentação gerada pelo ```FASTAPI```para mostrar a separação que fizemos utilizando as tags, toda a documentação bem elaborada, os modelos de validação que foram criados, etc.

O próximo passo agora é utilizar essa aplicação no lugar da API original, mostrando que podemos criar nossas próprias APIs e consumí-las, por exemplo, em um front-end REACT. Para começar a fazer isso, antes, é necessário adiconar algumas linhas de código no arquivo ```main.py``` isso para que a aplicação permita que sejam feitas requisições do navegador, especificamente de determinada porta, na qual roda a nossa aplicação REACT.

```python
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```


Feito isso, é necessário ter também o repositório do projeto clonado na máquina [link](https://github.com/tryber/sd-014-a-project-starwars-planets-search) e acessar a branch de uma pessoa estudante que concluiu o projeto, recomenda-se aqui a branch ```jonathan-f-silva-starwars-planets-search```. O comando para chegar a essa branch é:

```shell
git checkout jonathan-f-silva-starwars-planets-search
```

Dentro do repositório do projeto é necessário fazer a instalação prévia dos requerimentos, através do seguinte comando:

```shell
npm install
```

Feito isso, podemos ver a aplicação funcionando com a API original através do comando:

```shell
npm start
```

A aplicação abrirá no navegador usando a porta 3000. Para consumir da API que acabamos de construir, é necessário acessar o arquivo que faz à requisição para a API, o caminho para esse arquivo (```SWPlanetsAPI.js```), dentro da branch mencionada, é o seguinte:

```shell
src/services
└── SWPlanetsAPI.js
```

Para consumir da API local que deve estar rodando em um terminal na sua máquina, basta alterar a url na primeira linha para ```http://127.0.0.1:8000/api/planets/```. A linha inteira  fica assim:

```javascript
const SW_PLANETS_API_URL = 'http://127.0.0.1:8000/api/planets/';
```

Com isso, você verá que a aplicação react já começará a consumir da API local, e é possível verificar esse fato manualmente, caso você faça a inserção de um novo planeta usando o POST dos planetas através da rota ```/docs```da API que construímos e logo em seguida que verifique se esse planeta que você inseriu aparece dentro da aplicação REACT.