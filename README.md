# Script para continuação das mentorias _Python na Web_

# O que foi feito até agora:

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

