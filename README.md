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

class Planet(PlanetBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

class PlanetCreate(PlanetBase):
    pass

class PlanetRead(PlanetBase):
    id: int
```
----
```python
@app.post("/api/planets/",  tags=["planets"], status_code=201)
async def create_planet(planet: PlanetCreate):
    with get_session() as session:    
        db_planet = Planet.from_orm(planet)
        session.add(db_planet)
        session.commit()
        session.refresh(db_planet)
        return db_planet
```
