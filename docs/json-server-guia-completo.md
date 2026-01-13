# json-server: Guia Completo para Documentação

Uma REST API fake completa com zero codificação em menos de 30 segundos — essa é a promessa do json-server, uma das ferramentas de mocking mais populares do ecossistema JavaScript com **75.5K estrelas no GitHub** e aproximadamente **300K downloads semanais no npm**. Criado por typicode (mesmo autor do husky e lowdb), o json-server transforma qualquer arquivo JSON em uma API RESTful funcional, tornando-se essencial para desenvolvimento frontend, prototipagem rápida e demonstrações.

A ferramenta opera em dois branches principais: a versão estável **v0.17.4** (amplamente utilizada e documentada) e a versão beta **v1.0.0-beta.3** (com breaking changes significativos e licença Fair Source). Desenvolvedores devem escolher conscientemente qual versão usar, pois as diferenças são substanciais.

---

## O que é o json-server e por que existe

O json-server foi criado para resolver um problema comum: desenvolvedores frontend precisam consumir APIs REST durante o desenvolvimento, mas frequentemente o backend ainda não está pronto ou é trabalhoso mockar dados manualmente. A ferramenta gera automaticamente endpoints REST completos a partir de um simples arquivo JSON, suportando todas as operações CRUD (Create, Read, Update, Delete).

O funcionamento é direto: você cria um arquivo `db.json` com a estrutura de dados desejada, executa `json-server --watch db.json`, e instantaneamente tem uma API funcional em `http://localhost:3000` com endpoints para cada recurso. Alterações via POST, PUT, PATCH e DELETE são automaticamente persistidas no arquivo JSON usando lowdb como engine de banco de dados.

**Casos de uso ideais:**
- Prototipagem rápida de aplicações frontend
- Desenvolvimento paralelo frontend/backend antes da API real estar disponível
- Demonstrações e provas de conceito
- Testes manuais de componentes de UI
- Aprendizado de conceitos REST API
- Workshops e tutoriais de programação

---

## Instalação e configuração inicial

### Instalação global (v0.x estável)

```bash
npm install -g json-server@0.17.4   # NPM
yarn global add json-server@0.17.4  # Yarn
pnpm add -g json-server@0.17.4      # PNPM
```

### Instalação como dependência de desenvolvimento

```bash
npm install json-server@0.17.4 --save-dev
```

### Instalação v1.x (Beta)

```bash
npm install json-server   # Instala a versão mais recente (1.0.0-beta.3)
```

> ⚠️ **Importante:** A versão beta (v1.x) possui breaking changes significativos. Para projetos existentes, recomenda-se manter a v0.17.4.

### Estrutura básica do db.json

```json
{
  "posts": [
    { "id": 1, "title": "json-server", "author": "typicode" },
    { "id": 2, "title": "Hello World", "author": "dev" }
  ],
  "comments": [
    { "id": 1, "body": "Um comentário", "postId": 1 }
  ],
  "profile": {
    "name": "typicode"
  }
}
```

### Iniciando o servidor

```bash
json-server --watch db.json
```

O servidor inicia em `http://localhost:3000` exibindo todos os recursos disponíveis.

---

## Rotas e endpoints gerados automaticamente

Para cada **array** no arquivo JSON, o json-server cria um conjunto completo de endpoints RESTful:

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/posts` | Lista todos os posts |
| GET | `/posts/1` | Retorna post com id 1 |
| POST | `/posts` | Cria um novo post |
| PUT | `/posts/1` | Substitui post com id 1 |
| PATCH | `/posts/1` | Atualiza parcialmente post com id 1 |
| DELETE | `/posts/1` | Remove post com id 1 |

Para **objetos singleton** (como `profile`), apenas GET e PUT são gerados:

```bash
GET /profile
PUT /profile
PATCH /profile
```

### Persistência de dados

Todas as operações de escrita (POST, PUT, PATCH, DELETE) são **automaticamente salvas** no arquivo `db.json`. O header `Content-Type: application/json` é obrigatório para operações de escrita; caso contrário, a requisição retorna 2XX mas sem modificar os dados.

**Comportamento do ID:**
- IDs são imutáveis em PUT/PATCH (valores no body são ignorados)
- Em POST, o ID é respeitado apenas se não existir
- IDs são gerados automaticamente se não fornecidos

---

## Recursos de consulta e filtros

### Filtros por igualdade

```bash
GET /posts?title=json-server
GET /posts?author=typicode&title=Hello
```

### Operadores de comparação (v1.x)

| Sufixo | Operador | Exemplo |
|--------|----------|---------|
| `_gt` | > (maior que) | `GET /posts?views_gt=100` |
| `_gte` | >= (maior ou igual) | `GET /posts?views_gte=100` |
| `_lt` | < (menor que) | `GET /posts?views_lt=500` |
| `_lte` | <= (menor ou igual) | `GET /posts?views_lte=500` |
| `_ne` | != (diferente) | `GET /posts?status_ne=draft` |

**Combinação de filtros:**
```bash
GET /posts?views_gte=100&views_lt=500   # 100 <= views < 500
```

### Busca full-text e parcial

```bash
GET /posts?q=javascript          # Busca em todos os campos
GET /posts?title_like=server     # Busca parcial (v0.x)
```

### Paginação

**v0.x (versão estável):**
```bash
GET /posts?_page=2&_limit=10
```

**v1.x (versão beta):**
```bash
GET /posts?_page=2&_per_page=10   # _per_page substitui _limit
```

**Slice/Range:**
```bash
GET /posts?_start=10&_end=20      # Registros 10 até 20
GET /posts?_start=10&_limit=10    # 10 registros a partir do índice 10
```

### Ordenação

**v0.x:**
```bash
GET /posts?_sort=views&_order=desc
GET /posts?_sort=author,title&_order=desc,asc   # Múltiplos campos
```

**v1.x (sintaxe simplificada):**
```bash
GET /posts?_sort=id,-views        # id ASC, views DESC (prefixo - para DESC)
```

---

## Relacionamentos entre recursos

O json-server suporta relacionamentos através de convenções de nomenclatura.

### Estrutura de dados relacionados

```json
{
  "posts": [{ "id": 1, "title": "Post 1", "authorId": 1 }],
  "comments": [{ "id": 1, "text": "Comentário", "postId": 1 }],
  "authors": [{ "id": 1, "name": "John" }]
}
```

### Expandir referências (_expand)

```bash
GET /posts/1?_expand=author
# Retorna post com objeto author completo embutido
```

### Incluir recursos filhos (_embed)

```bash
GET /posts?_embed=comments
# Retorna posts com array de comments relacionados
```

### Rotas aninhadas

```bash
GET /posts/1/comments             # Todos os comentários do post 1
```

### Configuração de Foreign Key (uso programático)

```javascript
jsonServer.router('db.json', { foreignKeySuffix: '_id' })
```

### Delete com dependentes (v1.x)

```bash
DELETE /posts/1?_dependent=comments   # Remove post E seus comentários
```

---

## Middlewares e customizações

### Criando middleware personalizado

```javascript
// middleware.js
module.exports = (req, res, next) => {
  res.header('X-Custom-Header', 'Value')
  
  // Adicionar timestamp automaticamente em criações
  if (req.method === 'POST') {
    req.body.createdAt = Date.now()
  }
  
  next()
}
```

**Via CLI:**
```bash
json-server --watch db.json --middlewares middleware.js
```

### Middleware de autenticação

```javascript
server.use((req, res, next) => {
  if (isAuthorized(req)) {
    next()
  } else {
    res.status(401).send('Unauthorized')
  }
})
```

### Middleware de delay (simular latência)

```javascript
server.use((req, res, next) => {
  setTimeout(next, 2000)  // 2 segundos de delay
})
```

### Rotas customizadas (routes.json) - apenas v0.x

```json
{
  "/api/*": "/$1",
  "/api/v1/posts/:id": "/posts/:id",
  "/posts/:category": "/posts?category=:category",
  "/articles?id=:id": "/posts/:id"
}
```

```bash
json-server db.json --routes routes.json
```

**Exemplos de mapeamento:**
```
/api/posts       → /posts
/api/posts/1     → /posts/1
/posts/javascript → /posts?category=javascript
```

> ⚠️ **v1.x:** A opção `--routes` foi **removida**. Requer uso programático.

---

## Uso programático (como módulo Node.js)

### Exemplo completo

```javascript
const jsonServer = require('json-server')
const path = require('path')

const server = jsonServer.create()
const router = jsonServer.router(path.join(__dirname, 'db.json'))
const middlewares = jsonServer.defaults({
  static: './public',
  logger: true,
  bodyParser: true,
  noCors: false,
  readOnly: false
})

// Middlewares padrão (CORS, logger, static, etc.)
server.use(middlewares)
server.use(jsonServer.bodyParser)

// Rotas customizadas ANTES do router
server.get('/echo', (req, res) => {
  res.jsonp(req.query)
})

server.post('/login', (req, res) => {
  const { email, password } = req.body
  // Lógica de autenticação fake
  res.jsonp({ token: 'fake-jwt-token' })
})

// Rewriter para prefixo de API
server.use(jsonServer.rewriter({
  '/api/*': '/$1'
}))

// Router principal
server.use(router)

server.listen(3000, () => {
  console.log('JSON Server rodando em http://localhost:3000')
})
```

### Database em memória (sem arquivo)

```javascript
const router = jsonServer.router({
  posts: [{ id: 1, title: 'Hello' }],
  comments: []
})
```

### Integração com Express existente

```javascript
const express = require('express')
const jsonServer = require('json-server')

const app = express()
app.use('/api', jsonServer.router('db.json'))
app.listen(3000)
```

### Acesso direto ao lowdb

```javascript
const router = jsonServer.router('db.json')

// Manipular banco diretamente
router.db.get('posts').push({ id: 99, title: 'Novo' }).write()
```

---

## Geração de dados com Faker.js

### Arquivo de geração dinâmica

```javascript
// generate.js
const { faker } = require('@faker-js/faker')

module.exports = () => {
  const data = { users: [], posts: [] }
  
  for (let i = 1; i <= 100; i++) {
    data.users.push({
      id: i,
      firstName: faker.person.firstName(),
      lastName: faker.person.lastName(),
      email: faker.internet.email(),
      avatar: faker.image.avatar(),
      job: faker.person.jobTitle(),
      company: faker.company.name(),
      createdAt: faker.date.past()
    })
  }
  
  for (let i = 1; i <= 50; i++) {
    data.posts.push({
      id: i,
      title: faker.lorem.sentence(),
      body: faker.lorem.paragraphs(3),
      authorId: faker.number.int({ min: 1, max: 100 }),
      views: faker.number.int({ min: 0, max: 10000 })
    })
  }
  
  return data
}
```

**Uso:**
```bash
json-server generate.js --port 3001
```

### Script de build do database

```javascript
// filldata.js
const { faker } = require('@faker-js/faker')
const fs = require('fs')

const database = { employees: [] }

for (let i = 1; i <= 500; i++) {
  database.employees.push({
    id: i,
    name: faker.person.fullName(),
    email: faker.internet.email(),
    department: faker.commerce.department()
  })
}

fs.writeFileSync('./db.json', JSON.stringify(database, null, 2))
console.log('Database gerado com sucesso!')
```

### package.json scripts

```json
{
  "scripts": {
    "generate": "node filldata.js",
    "api": "json-server --watch db.json --port 3001",
    "api:delay": "json-server --watch db.json --delay 1000",
    "start": "npm run generate && npm run api",
    "dev": "concurrently \"npm run api\" \"npm start\""
  }
}
```

---

## Opções de CLI (v0.x)

```bash
json-server [options] <source>

Opções:
  --config, -c       Caminho para arquivo de config    [default: "json-server.json"]
  --port, -p         Porta do servidor                 [default: 3000]
  --host, -H         Host do servidor                  [default: "localhost"]
  --watch, -w        Observar mudanças no arquivo      [boolean]
  --routes, -r       Caminho para arquivo de rotas
  --middlewares, -m  Caminhos para middlewares         [array]
  --static, -s       Diretório de arquivos estáticos
  --read-only, --ro  Permitir apenas GET               [boolean]
  --no-cors, --nc    Desabilitar CORS                  [boolean]
  --no-gzip, --ng    Desabilitar GZIP                  [boolean]
  --snapshots, -S    Diretório de snapshots            [default: "."]
  --delay, -d        Delay nas respostas (ms)
  --id, -i           Propriedade de ID                 [default: "id"]
  --foreignKeySuffix Sufixo de foreign key             [default: "Id"]
  --quiet, -q        Suprimir logs                     [boolean]
```

### Exemplos de uso

```bash
# Servidor básico
json-server db.json

# Watch mode com porta customizada
json-server --watch db.json --port 4000

# Modo somente leitura
json-server --read-only db.json

# Com delay de 2 segundos
json-server --delay 2000 db.json

# Host para Docker/containers
json-server --host 0.0.0.0 db.json

# Múltiplos diretórios estáticos
json-server -s ./public -s ./uploads db.json

# A partir de URL remota
json-server http://example.com/db.json
```

### Snapshot do database

Durante a execução, pressione `s + Enter` para salvar um snapshot:
```
db-1578083664783.json
```

---

## Diferenças entre v0.x e v1.x

A transição da v0.x para v1.x trouxe mudanças significativas que **quebram compatibilidade**:

| Característica | v0.17.4 (Estável) | v1.0.0-beta.3 (Beta) |
|----------------|-------------------|----------------------|
| **Tipo de ID** | Numérico | **String** (sempre) |
| **Paginação** | `_page` + `_limit` | `_page` + `_per_page` |
| **Ordenação** | `_sort=field&_order=asc` | `_sort=field,-field2` |
| **Delay** | `--delay 2000` | **Removido** |
| **Routes file** | `--routes routes.json` | **Removido** |
| **Custom ID** | `--id _id` | **Removido** |
| **Formato** | Apenas JSON | JSON e **JSON5** |
| **Licença** | MIT | **Fair Source** |

### Novas funcionalidades na v1.x

- **Suporte a JSON5** (comentários, trailing commas)
- **Campos aninhados:** `?a.b.c=value`
- **Array fields:** `?arr[0]=value`
- **Operadores simplificados:** `_gt`, `_lt`, `_gte`, `_lte`, `_ne`
- **Delete com dependentes:** `?_dependent=resource`

### Exemplo de migração

```bash
# v0.x
GET /posts?_page=1&_limit=10&_sort=title&_order=desc

# v1.x equivalente
GET /posts?_page=1&_per_page=10&_sort=-title
```

### Recomendação

Para **projetos existentes**, manter v0.17.4 devido à estabilidade e documentação mais completa. Para **novos projetos experimentais**, considerar v1.x com cautela, sabendo que ainda está em beta.

---

## O que json-server NÃO faz — Limitações

### Não é adequado para produção

O json-server foi projetado exclusivamente para **desenvolvimento e testes**. As razões incluem:

- **Sem autenticação/autorização nativas** — qualquer pessoa pode acessar e modificar dados
- **Sem criptografia** — dados são armazenados em texto plano
- **Armazenamento em arquivo JSON** — não escalável, não transacional
- **Performance limitada** — lentidão significativa com milhares de registros
- **Concorrência insegura** — múltiplas escritas simultâneas podem corromper dados
- **CORS aberto por padrão** — qualquer origem pode acessar a API
- **Todo o db.json carregado em memória** — consumo de RAM cresce com os dados
- **Cada escrita reescreve o arquivo inteiro** — I/O intensivo

### Funcionalidades ausentes

- ❌ Validação de schema/dados
- ❌ Queries complexas (JOINs, agregações)
- ❌ Full-text search avançado
- ❌ WebSockets/Real-time nativo
- ❌ GraphQL nativo
- ❌ Batch operations
- ❌ Rate limiting
- ❌ Backup automático
- ❌ Versionamento de API nativo
- ❌ Suporte a SSL (requer proxy reverso)

### Quando NÃO usar json-server

| Cenário | Motivo |
|---------|--------|
| Aplicações em produção | Sem segurança, sem escalabilidade |
| Dados sensíveis | Sem criptografia ou controle de acesso |
| Alta concorrência (>100 req/s) | Arquivo JSON não suporta |
| Datasets >10.000 registros | Performance degradada |
| APIs complexas/não-RESTful | Limitado às convenções REST |
| Requisitos de compliance | Sem GDPR, HIPAA, etc. |

---

## Opiniões da comunidade e feedback

### Avaliações positivas

A comunidade reconhece o json-server como **a referência** para mock APIs rápidas:

> *"JSON Server delivers what it promises and is easy to set up and customize"* — Dev.to

> *"A valuable tool for frontend developers looking to streamline the development process and prototype applications rapidly"* — Desenvolvedores no Dev.to

**Pontos mais elogiados:**
- Setup em segundos com zero configuração
- CRUD completo automático
- CORS habilitado por padrão (resolve problemas comuns)
- Dados persistem automaticamente
- Suporte a rotas customizadas e middlewares

### Críticas e frustrações

Desenvolvedores com necessidades mais avançadas relatam limitações:

> *"At my company we've been using json-server since the beginning... Now we've reached a point where the customization is just not enough without writing a full blown node server with Express."* — Dev.to

**Problemas comuns relatados:**
- Manutenção de arquivos db.json grandes é trabalhosa
- Backends reais frequentemente não seguem convenções REST puras
- Rotas aninhadas complexas exigem workarounds
- CORS issues em GitHub Codespaces
- Breaking changes na v1.x causaram confusão em deployments

### Tendência de migração

Desenvolvedores com necessidades mais sofisticadas estão migrando para **MSW** (Mock Service Worker) ou **MirageJS**, especialmente para:
- Testes automatizados
- APIs GraphQL
- Relacionamentos complexos entre dados

---

## Alternativas e quando usar cada uma

### Tabela comparativa rápida

| Ferramenta | Downloads/semana | Ideal para | Diferencial |
|------------|------------------|------------|-------------|
| **json-server** | ~300K | Prototipagem REST rápida | Simplicidade máxima |
| **MSW** | ~6.7M | Testes + Development | Intercepta requests, suporta GraphQL |
| **MirageJS** | ~265K | SPAs com relacionamentos | ORM in-memory, factories |
| **Mockoon** | ~30K | Teams com GUI | Interface visual, CI/CD |
| **Prism** | — | OpenAPI-first | Gera mocks do spec |
| **WireMock** | ~5M/mês | Enterprise Java | Record/playback, fault injection |

### MSW (Mock Service Worker)

**Quando escolher MSW:**
- Testes de integração que precisam interceptar requests sem mudanças no código
- Suporte a GraphQL, REST e WebSocket na mesma ferramenta
- Reutilização dos mesmos mocks entre browser e Node.js

**Vantagem sobre json-server:** Não requer servidor separado; intercepta requests via Service Worker.

**Desvantagem:** Não persiste dados entre requisições nativamente.

### MirageJS

**Quando escolher MirageJS:**
- SPAs com relacionamentos complexos (belongsTo, hasMany)
- Necessidade de factories e seeds para gerar dados
- Replicar exatamente a forma da API de produção

**Vantagem sobre json-server:** Database in-memory com ORM e serializers customizáveis.

**Desvantagem:** Requests não aparecem no Network tab do DevTools.

### Mockoon

**Quando escolher Mockoon:**
- Times que preferem interface gráfica
- Necessidade de import/export OpenAPI
- CI/CD pipelines que precisam de mocks consistentes

**Vantagem sobre json-server:** GUI visual, response templating, chaos engineering.

### Quando json-server permanece a melhor escolha

- Prototipagem individual em **menos de 1 minuto**
- Demos e provas de conceito rápidas
- Aprendizado de REST APIs
- Workshops e tutoriais
- Desenvolvimento frontend solo sem complexidade

---

## Integrações e configurações avançadas

### Docker

```dockerfile
FROM node:lts-alpine
WORKDIR /app
RUN npm install -g json-server
COPY db.json .
EXPOSE 3000
CMD ["json-server", "--watch", "db.json", "--host", "0.0.0.0"]
```

```yaml
# docker-compose.yml
version: '3.8'
services:
  api:
    image: node:alpine
    working_dir: /app
    volumes:
      - ./server:/app
    ports:
      - "3001:3000"
    command: npx json-server --watch db.json --host 0.0.0.0
```

### Vite Plugin

```javascript
// vite.config.js
import jsonServer from 'vite-plugin-simple-json-server'

export default {
  plugins: [
    jsonServer({
      mockDir: 'mock',
      urlPrefixes: ['/api/'],
      logLevel: 'info'
    })
  ]
}
```

### Autenticação com json-server-auth

```bash
npm install json-server-auth
```

```javascript
const jsonServer = require('json-server')
const auth = require('json-server-auth')

const app = jsonServer.create()
const router = jsonServer.router('db.json')

app.db = router.db
app.use(auth)
app.use(router)
app.listen(3000)
```

### Deploy gratuito (apenas para demos)

**my-json-server.typicode.com:**
1. Crie um repositório GitHub público
2. Adicione um arquivo `db.json` na raiz
3. Acesse: `https://my-json-server.typicode.com/<user>/<repo>`

---

## Dicas e truques avançados

### Suporte a JSON5 (v1.x)

```javascript
// db.json5 — permite comentários e trailing commas
{
  posts: [
    { id: '1', title: 'Post 1' }, // comentário válido!
  ],
}
```

### Watch mode com nodemon

```bash
nodemon --watch db.json --exec "json-server db.json"
```

### Simular erros HTTP

```javascript
server.get('/error', (req, res) => {
  res.status(500).jsonp({ error: 'Internal Server Error' })
})

server.get('/timeout', (req, res) => {
  // Não responde — simula timeout
})
```

### Múltiplos endpoints de erro

```javascript
const errorMiddleware = (req, res, next) => {
  if (req.query._error) {
    return res.status(parseInt(req.query._error)).json({
      error: `Simulated ${req.query._error} error`
    })
  }
  next()
}
```

### Interceptar requests para logging

```javascript
server.use((req, res, next) => {
  console.log(`${new Date().toISOString()} - ${req.method} ${req.url}`)
  next()
})
```

---

## Conclusão

O json-server permanece como a **ferramenta de referência** para criar mock APIs REST com esforço mínimo. Sua proposta de valor — uma API funcional em menos de 30 segundos — é cumprida de forma exemplar para casos de uso apropriados: prototipagem, demos, aprendizado e desenvolvimento frontend isolado.

Contudo, desenvolvedores devem reconhecer claramente suas **limitações**: não é para produção, não escala, não possui segurança nativa, e APIs complexas rapidamente expõem suas fronteiras. Para projetos que crescem além do protótipo inicial, alternativas como MSW (para testes), MirageJS (para relacionamentos complexos) ou uma API real devem ser consideradas.

**Escolha a versão conscientemente:** v0.17.4 para estabilidade e compatibilidade com tutoriais existentes; v1.x apenas para novos projetos experimentais que podem lidar com breaking changes e a licença Fair Source.

O ecossistema de **75.5K estrelas** e comunidade ativa garantem que o json-server continuará sendo uma ferramenta essencial no toolkit de desenvolvedores frontend por muitos anos.