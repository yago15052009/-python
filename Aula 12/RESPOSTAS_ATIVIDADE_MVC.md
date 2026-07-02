# Atividade Aula 12 — StreamFlix Flask MVC
**Disciplina:** Python / Flask  
**Profª:** Janaína Duarte  
**Projeto:** flask/Aula12/

---

## Bloco A — Model (perguntas 1 a 10)

**1. Em qual pasta ficam as classes que representam tabelas do banco SQLite? Cite o caminho.**

As classes ficam na pasta `models/`. Cada arquivo define uma tabela: `models/filme_favorito.py` e `models/historico_busca.py`.

---

**2. Qual é o nome do arquivo de banco criado quando o app roda? Em qual arquivo Python essa configuração está?**

O banco se chama `streamflix.db`. A configuração está em `app.py`:
```python
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(pasta, "streamflix.db")
```
O arquivo é criado automaticamente quando `db.create_all()` é chamado dentro do `with app.app_context()`.

---

**3. Quais classes Model existem no projeto? Em quais arquivos cada uma está?**

- `ModeloBase` → `models/base.py`
- `FilmeFavorito` → `models/filme_favorito.py`
- `HistoricoBusca` → `models/historico_busca.py`

A instância `db` do SQLAlchemy é criada em `models/__init__.py`.

---

**4. De qual superclasse FilmeFavorito e HistoricoBusca herdam? O que elas ganham automaticamente (cite 3 campos)?**

Arquivo: `models/base.py`  
Ambas herdam de `ModeloBase`. Por essa herança, ganham automaticamente:
- `id` — chave primária inteira, gerada automaticamente
- `data_criacao` — data/hora de quando o registro foi criado
- `data_atualizacao` — data/hora da última modificação do registro

---

**5. Qual é o `__tablename__` da tabela de favoritos? Por que usamos `__tablename__`?**

Arquivo: `models/filme_favorito.py`  
O `__tablename__` é `"filmes_favoritos"`. Usamos esse atributo para definir explicitamente o nome da tabela no banco. Sem ele, o SQLAlchemy usaria o nome da classe em minúsculas (`filmefavorito`), que é menos legível. Com `__tablename__` controlamos exatamente como a tabela aparece no SQLite.

---

**6. Qual coluna guarda o id do filme vindo da API TMDB? Ela tem alguma restrição especial?**

Arquivo: `models/filme_favorito.py`  
A coluna é `tmdb_id`. Ela tem duas restrições:
- `nullable=False` — não pode ser vazia
- `unique=True` — não pode ter dois favoritos com o mesmo filme da API

Isso impede que o mesmo filme seja salvo duas vezes nos favoritos.

---

**7. O que o método `@classmethod adicionar` faz passo a passo? O que acontece se o filme já existir?**

Arquivo: `models/filme_favorito.py`  
Passo a passo:
1. Chama `buscar_por_tmdb(tmdb_id)` para verificar se o filme já está salvo
2. Se já existir, retorna `None` imediatamente (não salva duplicata)
3. Se não existir, cria um novo objeto `FilmeFavorito` com os dados recebidos
4. Adiciona à sessão com `db.session.add(fav)`
5. Confirma no banco com `db.session.commit()`
6. Retorna o objeto criado

Se o filme já existir nos favoritos, o método retorna `None` e não faz nada.

---

**8. Onde está o método que lista as últimas 8 buscas? Qual é o nome da classe e do método?**

Arquivo: `models/historico_busca.py`  
Classe: `HistoricoBusca`  
Método: `ultimas(cls, limite=8)`  
Ele ordena os registros pela `data_criacao` de forma decrescente e limita ao número passado como parâmetro (padrão 8).

---

**9. O model grava dados da API TMDB inteira ou só alguns campos espelhados? Cite 4 campos salvos em FilmeFavorito.**

Arquivo: `models/filme_favorito.py`  
O model salva apenas alguns campos espelhados, não todos os dados da API. Os 4 campos salvos são:
- `tmdb_id` — id do filme na API TMDB
- `titulo` — nome do filme
- `nota` — avaliação média
- `ano` — ano de lançamento

---

**10. Em `models/__init__.py`, o que é exportado além de `db`? Por que o controller importa `from models import FilmeFavorito`?**

Arquivo: `models/__init__.py`  
Além de `db`, são exportados: `ModeloBase`, `FilmeFavorito` e `HistoricoBusca` (declarados em `__all__`).  
O controller usa `from models import FilmeFavorito` porque o `__init__.py` centraliza tudo da pasta `models/` em um único ponto de entrada. Assim o controller não precisa saber em qual arquivo interno cada classe está — basta importar do pacote `models`.

---

## Bloco B — Controller (perguntas 11 a 20)

**11. Quantos Blueprints existem? Cite o nome de cada um e o `url_prefix`.**

Arquivo: `controllers/__init__.py`  
Existem 3 Blueprints:
- `dashboard_bp` — sem `url_prefix` (responde na raiz `/`)
- `filmes_bp` — `url_prefix="/filmes"`
- `favoritos_bp` — `url_prefix="/favoritos"`

---

**12. Em qual arquivo está a rota `/filmes/populares`? Qual é o nome da função Python?**

Arquivo: `controllers/filmes_controller.py`  
A função se chama `populares()`, decorada com `@filmes_bp.route("/populares")`. Como o Blueprint tem prefixo `/filmes`, a URL completa fica `/filmes/populares`.

---

**13. O que a função `populares()` faz antes de chamar `render_template`? Cite duas chamadas.**

Arquivo: `controllers/filmes_controller.py`  
Antes de renderizar o template, a função faz duas chamadas:
1. `api.filmes_populares()` — busca a lista de filmes populares no serviço TMDB
2. `FilmeFavorito.listar()` — consulta o banco local para saber quais filmes já estão nos favoritos, montando o conjunto `ids_fav`

---

**14. Quando o usuário busca um filme, qual controller registra o termo no banco? Qual model é usado?**

Arquivo: `controllers/filmes_controller.py`  
A função `buscar()` do `filmes_bp` é responsável. Após obter os resultados da API, ela chama:
```python
HistoricoBusca.registrar(termo, len(filmes))
```
O model usado é `HistoricoBusca` (`models/historico_busca.py`). Isso acontece somente se `termo` não estiver vazio.

---

**15. Qual método HTTP é exigido para adicionar favorito? Qual a URL completa de exemplo para o filme id 550?**

Arquivo: `controllers/favoritos_controller.py`  
O método exigido é **POST**, conforme `methods=["POST"]` na rota. A URL completa seria:
```
POST /favoritos/adicionar/550
```
Não funciona com GET — se tentar acessar pelo navegador diretamente, retorna erro 405 (Method Not Allowed).

---

**16. Na rota `detalhe(filme_id)`, o que acontece se `api.detalhe(filme_id)` retornar `None`?**

Arquivo: `controllers/filmes_controller.py`  
Se `api.detalhe(filme_id)` retornar `None`, o controller faz um redirect:
```python
if not filme:
    return redirect(url_for("filmes.populares"))
```
O usuário é redirecionado automaticamente para a página de filmes populares, sem ver nenhuma mensagem de erro.

---

**17. Onde os Blueprints são registrados no Flask? Cite o arquivo e o comando usado (3 registros).**

Arquivo: `app.py`  
Os três Blueprints são registrados dentro da função `criar_app()`:
```python
app.register_blueprint(dashboard_bp)
app.register_blueprint(filmes_bp)
app.register_blueprint(favoritos_bp)
```

---

**18. Qual controller cuida da página inicial `/`? Quais variáveis ele envia para o template `index.html`?**

Arquivo: `controllers/dashboard_controller.py`  
A função `index()` do `dashboard_bp` cuida da rota `/`. As variáveis enviadas para o template são:
- `populares` — primeiros 6 filmes populares
- `melhores` — primeiros 6 melhores avaliados
- `total_favoritos` — quantidade de favoritos salvos
- `historico` — últimas 5 buscas
- `modo_demo` — se está rodando sem chave da API

---

**19. A pasta `services/tmdb_api.py` é Model, Controller ou View? Justifique.**

Arquivo: `services/tmdb_api.py`  
É um **Service** (camada de serviço), não se encaixa exatamente em nenhuma das três camadas MVC. Ela é chamada pelos Controllers (ex: `filmes_controller.py` instancia `TmdbApi()`) para buscar dados externos via HTTP. Não representa uma tabela do banco (não é Model), não exibe nada (não é View) e não define rotas (não é Controller). Ela isola toda a lógica de comunicação com a API TMDB.

---

**20. De onde vem o termo digitado quando o usuário usa o formulário da home? É `request.form` ou `request.args`? Explique a diferença.**

Arquivo: `controllers/filmes_controller.py`  
Quando o usuário vem da home (`index.html`), o formulário usa `method="GET"`, então o termo chega pela URL como query string (ex: `/filmes/buscar?q=batman`). Por isso o controller lê com `request.args.get("q")`.

A diferença é: `request.args` lê parâmetros da URL (query string, método GET), enquanto `request.form` lê dados enviados no corpo da requisição (método POST). Nesse projeto, o formulário da home usa GET, então a resposta correta é **`request.args`**.

---

## Bloco C — View (perguntas 21 a 30)

**21. Onde ficam os templates HTML? Qual o caminho completo da pasta?**

Configurado em `app.py` com `template_folder="views/templates"`.  
Caminho completo: `views/templates/`  
Os arquivos ficam organizados em subpastas: `views/templates/filmes/` e `views/templates/favoritos/`.

---

**22. Qual template é a "base" de todas as páginas? Como os outros templates usam esse layout?**

Arquivo: `views/templates/layout.html`  
É o template base com menu e estrutura HTML completa. Os outros templates o utilizam com:
```jinja
{% extends "layout.html" %}
```
E preenchem o conteúdo dentro de blocos como `{% block conteudo %}...{% endblock %}`.

---

**23. Liste os 5 links do menu e o `url_for` de cada um.**

Arquivo: `views/templates/layout.html`

| Link | `url_for` |
|------|-----------|
| Home | `url_for('dashboard.index')` |
| Populares | `url_for('filmes.populares')` |
| Melhores | `url_for('filmes.melhores')` |
| Buscar | `url_for('filmes.buscar')` |
| Favoritos | `url_for('favoritos.listar')` |

---

**24. Qual arquivo HTML exibe a seção "Onde assistir (Brasil)"? De onde vem a variável `streaming`?**

Arquivo: `views/templates/filmes/detalhe.html`  
A variável `streaming` vem do controller `detalhe()` em `controllers/filmes_controller.py`, que chama `api.streaming(filme_id)` e passa o resultado para o template:
```python
streaming, demo = api.streaming(filme_id)
return render_template("filmes/detalhe.html", ..., streaming=streaming, ...)
```
O template acessa `streaming.flatrate`, `streaming.rent` e `streaming.buy`.

---

**25. O arquivo `filmes/_card.html` é uma página inteira ou um pedaço reutilizado? Quem o inclui e com qual tag Jinja?**

Arquivo: `views/templates/filmes/_card.html`  
É um pedaço reutilizável (componente parcial) — representa o card visual de um único filme. É incluído por `index.html`, `filmes/lista.html` e `filmes/buscar.html` com a tag:
```jinja
{% include "filmes/_card.html" %}
```
O underscore no nome (`_card`) é uma convenção para indicar que é um fragmento, não uma página completa.

---

**26. Em `filmes/detalhe.html`, como a View sabe se o filme já está nos favoritos? Qual variável controla o botão?**

Arquivo: `views/templates/filmes/detalhe.html`  
A variável é `favorito`, enviada pelo controller `detalhe()`:
```python
favorito = FilmeFavorito.buscar_por_tmdb(filme_id)
```
Se o filme já estiver salvo, `favorito` é um objeto `FilmeFavorito`. Se não estiver, é `None`. O template usa:
```jinja
{% if favorito %}
  {# botão Remover #}
{% else %}
  {# botão Salvar #}
{% endif %}
```

---

**27. Onde está o CSS do site? Como o `layout.html` carrega esse arquivo?**

Arquivo CSS: `views/static/css/style.css`  
Configurado em `app.py` com `static_folder="views/static"`.  
O `layout.html` carrega com:
```jinja
{{ url_for('static', filename='css/style.css') }}
```
Isso gera a URL correta para o arquivo estático independente de onde o app estiver rodando.

---

**28. Na listagem de favoritos, qual loop Jinja percorre os registros? Cite 3 campos exibidos.**

Arquivo: `views/templates/favoritos/lista.html`  
O loop é:
```jinja
{% for fav in favoritos %}
```
Os 3 campos exibidos na tabela são:
- `fav.titulo` — nome do filme
- `fav.nota` — avaliação
- `fav.ano` — ano de lançamento

(O template também exibe `fav.data_criacao` — data em que foi salvo nos favoritos.)

---

**29. O que significa `{% if modo_demo %}` no layout? Quem disponibiliza essa variável para todos os templates?**

Arquivo: `app.py` (função `inject_globals`) e `views/templates/layout.html`  
O `{% if modo_demo %}` exibe um aviso visual quando o app está rodando sem uma chave TMDB válida (usando os filmes fixos de demonstração).

A variável é disponibilizada para **todos** os templates automaticamente pelo `context_processor` em `app.py`:
```python
@app.context_processor
def inject_globals():
    from services import TmdbApi
    return {"modo_demo": TmdbApi().usando_demo}
```
Com isso, qualquer template pode usar `modo_demo` sem o controller precisar passá-la manualmente.

---

**30. Descreva o fluxo completo quando o aluno clica em "Salvar favorito" no detalhe do filme (View → Controller → Model → redirect).**

Arquivos envolvidos: `views/templates/filmes/detalhe.html` → `controllers/favoritos_controller.py` → `models/filme_favorito.py`

1. **View** (`filmes/detalhe.html`) — o botão "Salvar" está dentro de um `<form method="POST" action="{{ url_for('favoritos.adicionar', tmdb_id=filme.id) }}">`. O form envia campos ocultos com `titulo`, `poster_path`, `nota`, `ano` e `voltar` (URL da página atual)

2. **Controller** (`favoritos_controller.py`, função `adicionar(tmdb_id)`) — recebe o POST, lê os dados do `request.form`, converte `nota` para float e chama `FilmeFavorito.adicionar(...)`

3. **Model** (`models/filme_favorito.py`, método `adicionar`) — verifica se já existe com `buscar_por_tmdb`; se não existir, cria o objeto, salva com `db.session.add()` e confirma com `db.session.commit()`

4. **Redirect** — o controller lê `request.form.get("voltar")` e redireciona de volta para a página de detalhe do filme, onde o botão agora aparece como "Remover" (porque `favorito` não é mais `None`)
