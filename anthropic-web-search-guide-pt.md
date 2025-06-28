# Ferramenta de Busca na Web da Anthropic: Sua Conexão Definitiva com a Web em Tempo Real

## Resumo Executivo

A Ferramenta de Busca na Web da Anthropic revoluciona as capacidades do Claude ao fornecer acesso direto ao conteúdo da web em tempo real. Lançada em maio de 2025, esse recurso permite que o Claude pesquise na internet, analise resultados e incorpore informações atuais em suas respostas com citações precisas. Esta documentação abrangente detalha todos os aspectos da ferramenta - desde implementação básica até padrões de uso avançados, considerações de segurança e otimização de desempenho.

A Ferramenta de Busca na Web custa $10 por 1.000 pesquisas mais custos padrão de tokens e está disponível para Claude 3.7 Sonnet, Claude 3.5 Sonnet e Claude 3.5 Haiku. Oferece filtragem robusta de domínios, capacidades de busca localizada e integração perfeita de citações, permitindo aos desenvolvedores criar aplicações sofisticadas que combinam o raciocínio do Claude com informações atualizadas de toda a web.

## Índice

1. [Visão Geral](#1-visão-geral)
2. [Recursos e Funcionalidades](#2-recursos-e-funcionalidades)
3. [Documentação da API](#3-documentação-da-api)
4. [Casos de Uso e Cenários](#4-casos-de-uso-e-cenários)
5. [Opções de Configuração](#5-opções-de-configuração)
6. [Métodos de Integração](#6-métodos-de-integração)
7. [Tratamento de Erros](#7-tratamento-de-erros)
8. [Comparação com Outras Ferramentas](#8-comparação-com-outras-ferramentas)
9. [Preços e Limitações](#9-preços-e-limitações)
10. [Exemplos de Código](#10-exemplos-de-código)
11. [Padrões de Uso Avançados](#11-padrões-de-uso-avançados)
12. [Considerações de Segurança](#12-considerações-de-segurança)
13. [Otimização de Desempenho](#13-otimização-de-desempenho)
14. [Exemplos de Implementação no Mundo Real](#14-exemplos-de-implementação-no-mundo-real)
15. [Referências e Recursos](#15-referências-e-recursos)

## 1. Visão Geral

### 1.1 O que é a Ferramenta de Busca na Web?

A Ferramenta de Busca na Web da Anthropic é um recurso do lado do servidor que permite ao Claude acesso direto ao conteúdo da web em tempo real. Isso permite que o Claude pesquise na internet, recupere informações atuais além de seu limite de conhecimento, analise resultados e incorpore essas informações em suas respostas com citações apropriadas.

### 1.2 Propósito Principal

Os principais propósitos da Ferramenta de Busca na Web são:

- Aumentar o conhecimento abrangente do Claude com dados atuais do mundo real
- Permitir que o Claude forneça insights atualizados sobre tópicos em rápida evolução
- Permitir que o Claude funcione como um agente de pesquisa que pode encontrar, analisar e sintetizar informações de toda a web
- Fornecer informações verificáveis através de citações automáticas de fontes

### 1.3 Visão Geral da Arquitetura

A Ferramenta de Busca na Web segue este fluxo arquitetural:

1. **Processo de Decisão**: Quando o Claude recebe uma solicitação que se beneficiaria de informações atualizadas, ele usa suas capacidades de raciocínio para determinar se a busca na web ajudaria a fornecer uma resposta mais precisa.

2. **Geração de Consulta**: Se pesquisar na web for benéfico, o Claude gera uma consulta de pesquisa direcionada.

3. **Execução de Consulta**: A API executa a pesquisa e fornece os resultados ao Claude.

4. **Análise de Resultados**: O Claude analisa os resultados da pesquisa em busca de informações relevantes.

5. **Pesquisa Progressiva**: O Claude pode conduzir múltiplas pesquisas sequenciais, usando resultados anteriores para informar consultas subsequentes.

6. **Formulação de Resposta**: O Claude fornece uma resposta abrangente com citações do material fonte.

7. **Integração de Citações**: Cada resposta com fonte web inclui citações, permitindo aos usuários verificar informações diretamente.

### 1.4 Como a Busca na Web difere do Claude Básico

Ao contrário das interações padrão do Claude, o Claude com Busca na Web ativada pode:

- Acessar e referenciar informações atuais além de seu limite de treinamento
- Conduzir pesquisas através de múltiplas consultas sequenciais em uma única conversa
- Verificar informações de fontes originais
- Fornecer citações para declarações factuais
- Acessar informações especializadas ou de nicho não cobertas em seus dados de treinamento

## 2. Recursos e Funcionalidades

### 2.1 Recursos Principais

#### 2.1.1 Comportamento de Busca Agêntica

O Claude pode conduzir múltiplas pesquisas progressivas dentro de uma única solicitação, usando resultados anteriores para informar consultas subsequentes. Isso permite pesquisas mais abrangentes e exploração mais profunda de tópicos.

#### 2.1.2 Citação Automática

O Claude cita automaticamente fontes dos resultados de pesquisa, aumentando a transparência e verificabilidade. As citações incluem a URL da fonte, título e o texto específico sendo referenciado.

#### 2.1.3 Controle de Domínio

- **Listas de Domínios Permitidos**: Especifique quais domínios o Claude pode pesquisar, garantindo que os resultados venham apenas de fontes aprovadas
- **Listas de Domínios Bloqueados**: Impeça o Claude de acessar determinados domínios que podem conter conteúdo sensível, competitivo ou inapropriado

#### 2.1.4 Busca Localizada

Os resultados da pesquisa podem ser adaptados com base na localização do usuário para informações regionalmente relevantes. Os desenvolvedores podem especificar parâmetros de cidade, região, país e fuso horário.

#### 2.1.5 Suporte a Streaming

Com streaming habilitado, você recebe eventos de pesquisa como parte do stream, mostrando o processo de pesquisa em tempo real. Isso inclui a decisão do Claude de pesquisar, a consulta sendo usada e os resultados sendo analisados.

### 2.2 Funcionalidade Adicional

#### 2.2.1 Integração com Cache de Prompts

A busca na web funciona com cache de prompts para conversas multi-turno mais eficientes. Isso permite reutilizar conteúdo através de solicitações enquanto mantém acesso às capacidades de busca na web.

#### 2.2.2 Tratamento de Erros

A ferramenta fornece respostas adequadas de erro (ex: quando os usos máximos são excedidos) e comportamento de fallback, permitindo que aplicações lidem graciosamente com limitações ou problemas.

#### 2.2.3 Suporte a Conversas Multi-turno

Os resultados de busca na web e citações podem ser mantidos através de múltiplos turnos de conversa, permitindo perguntas de acompanhamento e exploração mais profunda de tópicos.

## 3. Documentação da API

### 3.1 Endpoint

```
POST https://api.anthropic.com/v1/messages
```

### 3.2 Autenticação

Todas as solicitações para a API da Anthropic requerem autenticação usando uma chave API.

```
x-api-key: SUA_CHAVE_API
```

Cabeçalhos obrigatórios:
```
anthropic-version: 2023-06-01
content-type: application/json
```

### 3.3 Schema da Ferramenta de Busca na Web

A Ferramenta de Busca na Web é especificada no array `tools` de uma solicitação da API Messages:

```json
{
  "type": "web_search_20250305",
  "name": "web_search",
  "max_uses": 5,
  "allowed_domains": ["example.com", "dominionconfiavel.org"],
  "blocked_domains": ["fonteduvidosa.com"],
  "user_location": {
    "type": "approximate",
    "city": "São Paulo",
    "region": "São Paulo",
    "country": "BR",
    "timezone": "America/Sao_Paulo"
  }
}
```

### 3.4 Parâmetros

| Parâmetro | Tipo | Obrigatório | Descrição |
|-----------|------|-------------|-----------|
| `type` | string | Sim | Deve ser `web_search_20250305` |
| `name` | string | Sim | Deve ser `web_search` |
| `max_uses` | integer | Não | Limita o número de pesquisas realizadas em uma única solicitação. O padrão varia por modelo. |
| `allowed_domains` | array de strings | Não | Inclui apenas resultados desses domínios |
| `blocked_domains` | array de strings | Não | Nunca inclui resultados desses domínios |
| `user_location` | object | Não | Localiza os resultados da pesquisa com base na localização do usuário |

#### 3.4.1 Restrições de Parâmetros

- Você pode usar ou `allowed_domains` OU `blocked_domains`, mas não ambos na mesma solicitação.
- O parâmetro `max_uses` deve ser um número inteiro positivo.
- `user_location` requer as seguintes propriedades:
  - `type`: Atualmente suporta apenas "approximate"
  - `city`: Nome da cidade
  - `region`: Nome da região/estado
  - `country`: Código de país ISO
  - `timezone`: String de fuso horário IANA (ex: "America/Sao_Paulo")

### 3.5 Formato de Solicitação

Exemplo de solicitação completa:

```json
{
  "model": "claude-3-7-sonnet-20250219",
  "max_tokens": 1024,
  "messages": [
    {
      "role": "user",
      "content": "Quais são os últimos desenvolvimentos em computação quântica?"
    }
  ],
  "tools": [
    {
      "type": "web_search_20250305",
      "name": "web_search",
      "max_uses": 5,
      "blocked_domains": ["fonteduvidosa.com"],
      "user_location": {
        "type": "approximate",
        "city": "São Paulo",
        "region": "São Paulo",
        "country": "BR",
        "timezone": "America/Sao_Paulo"
      }
    }
  ]
}
```

### 3.6 Formato de Resposta

A resposta da Ferramenta de Busca na Web segue um formato específico com múltiplos componentes:

1. Decisão do Claude de pesquisar
2. A consulta de pesquisa usada
3. Resultados da pesquisa
4. Resposta final do Claude com citações

Exemplo de resposta:

```json
{
  "role": "assistant",
  "content": [
    {
      "type": "text",
      "text": "Vou pesquisar os desenvolvimentos recentes em computação quântica."
    },
    {
      "type": "server_tool_use",
      "id": "srvtoolu_01WYG3ziw53XMcoyKL4XcZmE",
      "name": "web_search",
      "input": {
        "query": "avanços computação quântica 2025"
      }
    },
    {
      "type": "web_search_tool_result",
      "tool_use_id": "srvtoolu_01WYG3ziw53XMcoyKL4XcZmE",
      "content": [
        {
          "type": "web_search_result",
          "url": "https://exemplo.com/noticias-computacao-quantica",
          "title": "Avanços em Computação Quântica em 2025",
          "encrypted_content": "EqgfCioIARgBIiQ3YTAwMjY1Mi1mZjM5LTQ1NGUtODgxNC1kNjNjNTk1ZWI3Y...",
          "page_age": "30 de abril de 2025"
        }
      ]
    },
    {
      "type": "text",
      "text": "Com base nos resultados da pesquisa, houve vários desenvolvimentos importantes em computação quântica em 2025. Pesquisadores do MIT alcançaram um novo recorde de tempo de coerência quântica, mantendo qubits em estado de superposição por mais de 10 minutos.",
      "citations": [
        {
          "type": "web_search_result_location",
          "url": "https://exemplo.com/noticias-computacao-quantica",
          "title": "Avanços em Computação Quântica em 2025",
          "encrypted_index": "Eo8BCioIAhgBIiQyYjQ0OWJmZi1lNm..",
          "cited_text": "Pesquisadores do MIT alcançaram um novo recorde de tempo de coerência quântica, mantendo qubits em estado de superposição por mais de 10 minutos, um marco crítico para aplicações práticas de computação quântica."
        }
      ]
    }
  ],
  "id": "msg_a930390d3a",
  "usage": {
    "input_tokens": 6039,
    "output_tokens": 931,
    "server_tool_use": {
      "web_search_requests": 1
    }
  },
  "stop_reason": "end_turn"
}
```

### 3.7 Componentes de Resposta

| Componente | Tipo | Descrição |
|-----------|------|-------------|
| `text` | string | Respostas textuais do Claude |
| `server_tool_use` | object | Detalhes da consulta de pesquisa do Claude |
| `web_search_tool_result` | object | Os resultados da pesquisa retornados |
| `citations` | array | Citações de fontes para informações usadas |
| `encrypted_index` | string | Conteúdo criptografado que deve ser passado de volta em conversas multi-turno para citações |
| `usage` | object | Uso de tokens e contagem de solicitações de pesquisa |

### 3.8 Resposta em Streaming

Quando o streaming está habilitado, você receberá eventos de pesquisa como parte do stream:

```
event: message_start
data: {"type": "message_start", "message": {"id": "msg_abc123", "type": "message"}}

event: content_block_start
data: {"type": "content_block_start", "index": 0, "content_block": {"type": "text", "text": ""}}

// Decisão do Claude de pesquisar
event: content_block_start
data: {"type": "content_block_start", "index": 1, "content_block": {"type": "server_tool_use", "id": "srvtoolu_xyz789", "name": "web_search"}}

// Consulta de pesquisa em stream
event: content_block_delta
data: {"type": "content_block_delta", "index": 1, "delta": {"type": "input_json_delta", "value": "{\"query\":\"avanços computação quântica 2025\"}"}}

// Pausa enquanto a pesquisa é executada

// Resultados da pesquisa em stream
event: content_block_start
data: {"type": "content_block_start", "index": 2, "content_block": {"type": "web_search_tool_result", "tool_use_id": "srvtoolu_xyz789", "content": [{"type": "web_search_result", "title": "Avanços em Computação Quântica em 2025", "url": "https://exemplo.com"}]}}
```

## 4. Casos de Uso e Cenários

### 4.1 Serviços Financeiros

- **Análise de Mercado**: Construa agentes de IA que analisem preços de ações em tempo real, tendências de mercado e indicadores econômicos
- **Conformidade Regulatória**: Mantenha-se atualizado com regulamentações financeiras e requisitos de conformidade
- **Pesquisa de Investimentos**: Compile informações atuais sobre empresas, setores e condições de mercado
- **Análise de Resultados**: Pesquise e analise relatórios trimestrais e notícias financeiras

### 4.2 Pesquisa Jurídica

- **Atualizações de Jurisprudência**: Acesse decisões judiciais recentes, precedentes e desenvolvimentos legais
- **Acompanhamento Regulatório**: Monitore mudanças em leis e estruturas regulatórias
- **Verificação de Conformidade**: Garanta que conselhos reflitam os requisitos legais mais atuais
- **Verificação de Citações**: Verifique e atualize citações legais com informações atuais

### 4.3 Ferramentas para Desenvolvedores

- **Documentação de APIs**: Acesse a documentação mais recente de APIs para linguagens de programação e frameworks
- **Solução de Problemas**: Encontre soluções atuais para mensagens de erro e problemas técnicos
- **Atualizações Tecnológicas**: Mantenha-se informado sobre os últimos lançamentos, patches e recursos
- **Exemplos de Código**: Descubra exemplos de implementação para novas tecnologias

### 4.4 Produtividade e Pesquisa

- **Inteligência de Mercado**: Incorpore os últimos relatórios empresariais, inteligência competitiva ou pesquisa do setor
- **Pesquisa Acadêmica**: Construa propostas de financiamento mais sólidas e revisões de literatura pesquisando em fontes primárias
- **Síntese de Informações**: Combine informações de múltiplas fontes em relatórios abrangentes
- **Verificação de Fatos**: Verifique alegações contra fontes de informação atuais

### 4.5 Aplicações para Consumidores

- **Pesquisa de Produtos**: Ajude compradores a comparar recursos, preços e avaliações de produtos
- **Planejamento de Viagens**: Acesse informações atuais sobre destinos, acomodações e requisitos de viagem
- **Resumo de Notícias**: Compile e analise notícias de múltiplas fontes sobre tópicos específicos
- **Informações de Saúde**: Pesquise recomendações de saúde atuais e informações médicas

## 5. Opções de Configuração

### 5.1 Parâmetro Max Uses

O parâmetro `max_uses` limita o número de pesquisas que o Claude pode realizar em uma única solicitação:

```json
{
  "type": "web_search_20250305",
  "name": "web_search",
  "max_uses": 5
}
```

- Valores maiores permitem pesquisas mais abrangentes, mas aumentam os custos
- Valores menores limitam custos, mas podem restringir a capacidade do Claude de explorar tópicos completamente
- Se o Claude tentar mais pesquisas do que o permitido, você receberá um erro `max_uses_exceeded`

### 5.2 Controle de Domínio

#### 5.2.1 Domínios Permitidos

Restrinja o Claude a pesquisar apenas domínios específicos:

```json
{
  "type": "web_search_20250305",
  "name": "web_search",
  "allowed_domains": ["exemplo.com", "dominionconfiavel.org"]
}
```

Casos de uso:
- Garantir que informações venham apenas de fontes confiáveis
- Limitar pesquisas a veículos de notícias específicos ou periódicos acadêmicos
- Restringir pesquisas aos domínios da própria organização

#### 5.2.2 Domínios Bloqueados

Impeça o Claude de pesquisar domínios específicos:

```json
{
  "type": "web_search_20250305",
  "name": "web_search",
  "blocked_domains": ["fonteduvidosa.com"]
}
```

Casos de uso:
- Bloquear fontes conhecidamente problemáticas ou de baixa qualidade
- Impedir acesso a informações de concorrentes
- Bloquear sites com conteúdo inapropriado

**Nota**: Você pode usar `allowed_domains` OU `blocked_domains`, mas não ambos na mesma solicitação.

### 5.3 Localização do Usuário

Localize os resultados da pesquisa com base na localização do usuário:

```json
{
  "type": "web_search_20250305",
  "name": "web_search",
  "user_location": {
    "type": "approximate",
    "city": "São Paulo",
    "region": "São Paulo",
    "country": "BR",
    "timezone": "America/Sao_Paulo"
  }
}
```

Casos de uso:
- Fornecer resultados de pesquisa regionalmente relevantes
- Acessar informações específicas de localização (ex: regulamentações locais)
- Obter informações apropriadas para fuso horário

### 5.4 Controles Administrativos

Administradores de organizações podem:
- Habilitar ou desabilitar a busca na web no nível organizacional
- Configurar listas de domínios permitidos e bloqueados
- Gerenciar configurações de busca na web através da interface do Console

## 6. Métodos de Integração

### 6.1 Integração com API

#### 6.1.1 Chamadas Diretas da API

```json
{
  "model": "claude-3-7-sonnet-20250219",
  "max_tokens": 1024,
  "tools": [
    {
      "type": "web_search_20250305",
      "name": "web_search",
      "max_uses": 5,
      "allowed_domains": ["exemplo.com", "dominionconfiavel.org"],
      "blocked_domains": ["fonteduvidosa.com"],
      "user_location": {
        "type": "approximate",
        "city": "São Paulo",
        "region": "São Paulo",
        "country": "BR",
        "timezone": "America/Sao_Paulo"
      }
    }
  ],
  "messages": [
    {"role": "user", "content": "Quais são os últimos desenvolvimentos em computação quântica?"}
  ]
}
```

#### 6.1.2 Usando SDKs

A Anthropic fornece SDKs para:
- Python
- TypeScript/JavaScript
- Java
- Ruby
- Go (suporte beta)

### 6.2 Padrões Arquiteturais

#### 6.2.1 Padrão Baseado em Agente

Implemente o Claude como um agente que pode decidir autonomamente quando pesquisar na web:
- Permita que o Claude determine quando pesquisas na web são necessárias
- Habilite capacidades de múltiplas pesquisas progressivas onde cada pesquisa se baseia em resultados anteriores
- Defina limites apropriados de `max_uses` para controlar a profundidade da pesquisa

#### 6.2.2 Padrão Proxy

Implemente um serviço proxy que gerencie solicitações de busca na web:
- Centralize logging e monitoramento de busca na web
- Adicione lógica personalizada de filtragem de domínio
- Implemente limitação de taxa e controles de custo
- Adicione camadas de cache para informações frequentemente solicitadas

#### 6.2.3 Padrão de Streaming

Use respostas em streaming para melhorar a experiência do usuário:
- Implemente ouvintes de evento para eventos `server_tool_use` para mostrar atividade de pesquisa
- Exiba conteúdo incremental conforme chega
- Implemente fallbacks se as pesquisas demorarem muito

### 6.3 Integração com Plataformas Populares

A Ferramenta de Busca na Web também pode ser integrada através de plataformas de IA existentes:
- Amazon Bedrock (para modelos Claude)
- Google Cloud Vertex AI
- Zapier para integrações sem código
- Plataforma Poe da Quora

## 7. Tratamento de Erros

### 7.1 Erros da Ferramenta de Busca na Web

Se o Claude tentar mais pesquisas do que o permitido por `max_uses`, a resposta incluirá um erro:

```json
{
  "type": "web_search_tool_result",
  "tool_use_id": "servertoolu_a93jad",
  "content": {
    "type": "web_search_tool_result_error",
    "error_code": "max_uses_exceeded"
  }
}
```

### 7.2 Erros da API

A API usa códigos de status HTTP padrão para erros:

| Código de Status | Tipo de Erro | Descrição |
|------------------|--------------|------------|
| 400 | `invalid_request_error` | Formato ou conteúdo de solicitação inválido |
| 401 | `authentication_error` | Problema com chave API |
| 403 | `permission_error` | Chave API não tem permissão |
| 404 | `not_found_error` | Recurso não encontrado |
| 413 | `request_too_large` | Solicitação excede tamanho máximo |
| 429 | `rate_limit_error` | Limite de taxa excedido |
| 500 | `api_error` | Erro inesperado do servidor |
| 529 | `overloaded_error` | API temporariamente sobrecarregada |

Respostas de erro seguem este formato:

```json
{
  "type": "error",
  "error": {
    "type": "not_found_error",
    "message": "O recurso solicitado não pôde ser encontrado."
  }
}
```

### 7.3 Implementação de Tratamento de Erros

```javascript
try {
  const response = await anthropic.messages.create({
    model: "claude-3-7-sonnet-20250219",
    max_tokens: 1024,
    tools: [{
      type: "web_search_20250305",
      name: "web_search",
      max_uses: 5
    }],
    messages: [
      { role: "user", content: "Quais são os últimos desenvolvimentos em computação quântica?" }
    ]
  });
  
  // Processar resposta bem-sucedida
} catch (error) {
  if (error.status === 429) {
    // Tratar limitação de taxa com backoff exponencial
    const retryAfter = error.headers['retry-after'] || 1;
    await new Promise(resolve => setTimeout(resolve, retryAfter * 1000));
    // Tentar novamente a solicitação
  } else if (error.type === 'web_search_tool_result_error') {
    // Tratar erros específicos de busca na web
    if (error.error_code === 'max_uses_exceeded') {
      // Tratar limite de pesquisa excedido
    }
  } else {
    // Tratar outros erros
  }
}
```

### 7.4 Estratégias Recomendadas de Tratamento de Erros

| Código de Erro | Descrição | Tratamento Recomendado |
|----------------|-----------|------------------------|
| `too_many_requests` | Limite de taxa excedido | Implementar backoff exponencial e tentar novamente |
| `invalid_input` | Parâmetro de consulta de pesquisa inválido | Registrar erro, validar entradas antes de enviar |
| `max_uses_exceeded` | Usos máximos da ferramenta de busca na web excedidos | Fornecer feedback claro ao usuário, oferecer continuar com resultados limitados |
| `query_too_long` | Consulta excede comprimento máximo | Implementar validação de comprimento de consulta no cliente |
| `unavailable` | Erro interno ocorreu | Degradar graciosamente para funcionalidade sem busca na web |

## 8. Comparação com Outras Ferramentas

### 8.1 Capacidades de Navegação da OpenAI

| Recurso | Ferramenta de Busca na Web da Anthropic | Navegação da OpenAI |
|---------|----------------------------------------|---------------------|
| **Preços** | $10 por 1.000 pesquisas + custos de tokens | Incluído nos custos de assinatura/API sem taxas adicionais por pesquisa |
| **Recência** | Informações da web em tempo real | Informações da web em tempo real |
| **Citação de Fontes** | Citações inline com links de fonte | Citações inline com links de fonte |
| **Implementação** | Baseada em API com configuração mínima | Navegação disponível através de API e interface ChatGPT |
| **Controle do Usuário** | Controle direto de consulta limitado | Usuários podem solicitar diretamente ações de navegação |
| **Segurança de Conteúdo** | Adesão aos princípios de IA Constitucional da Anthropic | Filtragem e moderação de conteúdo da OpenAI |
| **Integração** | Principalmente via API, com Claude decidindo quando pesquisar | Disponível através de API e UI com mais controle direto |
| **Recursos Avançados** | Filtragem de domínio | Pode seguir links e navegar além dos resultados de pesquisa iniciais |

### 8.2 Ofertas de API de Busca do Google

| Recurso | Ferramenta de Busca na Web da Anthropic | API de Motor de Busca Programável do Google |
|---------|----------------------------------------|----------------------------------------------|
| **Preços** | $10 por 1.000 pesquisas + custos de tokens | $5 por 1.000 consultas (até 10.000 por dia) |
| **Tier Gratuito** | Sem tier gratuito | 100 pesquisas gratuitas por dia |
| **Controle** | Limitado - Claude decide consultas de pesquisa | Controle total sobre consultas e parâmetros |
| **Formato de Resultados** | Processado e sintetizado pelo Claude | Resultados JSON brutos requerendo processamento adicional |
| **Complexidade de Integração** | Simples - integrado ao Claude | Requer mais trabalho de desenvolvimento |
| **Recursos de Busca Avançada** | Limitado - apenas busca básica | Mais operadores e filtros de busca avançados |
| **Personalização de Domínio** | Listas de permitidos/bloqueados | Pode criar motores de busca personalizados para domínios específicos |
| **Apresentação de Resultados** | Formato conversacional com citações | Dados brutos requerendo desenvolvimento de UI |
| **Limites de Uso** | Baseado nos limites de taxa da Anthropic | Até 10.000 consultas por dia padrão |

### 8.3 API de Busca do Bing

| Recurso | Ferramenta de Busca na Web da Anthropic | API de Busca do Bing |
|---------|----------------------------------------|----------------------|
| **Preços** | $10 por 1.000 pesquisas + custos de tokens | Preços em camadas: S1 (~$25/1.000), S2 (~$15/1.000), S3 (~$6/1.000) |
| **Estrutura** | Preços fixos simples | Sistema de camadas complexo (S1-S9) com capacidades diferentes |
| **Tipos de Resultado** | Limitado ao que o Claude usa | Tipos de resultado ricos dependendo da camada (web, imagens, vídeos, notícias) |
| **Acesso a Dados** | Processado através do Claude | Acesso direto a dados de pesquisa brutos |
| **Controle** | Limitado - Claude controla consultas | Controle total sobre parâmetros de pesquisa |
| **Análises** | Análises integradas limitadas | Complemento de estatísticas disponível |
| **Integração de API** | API única para todas as capacidades | APIs múltiplas baseadas no tipo de conteúdo |
| **Restrições de Domínio** | Listas de permitidos/bloqueados | Instâncias de busca personalizadas para domínios específicos |
| **Processamento de Resultados** | Síntese automática pelo Claude | Requer processamento personalizado |

### 8.4 Serper.dev e APIs de Busca Especializadas

| Recurso | Ferramenta de Busca na Web da Anthropic | Serper.dev |
|---------|----------------------------------------|------------|
| **Preços** | $10 por 1.000 pesquisas | $0,30 por 1.000 consultas (significativamente mais barato) |
| **Foco** | Resultados sintetizados por IA | Dados de pesquisa brutos |
| **Implementação** | IA decide quando pesquisar | Desenvolvedor tem controle total |
| **Velocidade** | Depende do processamento do Claude | Tempos de resposta de 1-2 segundos |
| **Tipos de Resultado** | O que o Claude escolhe incluir | Web, imagens, vídeos, notícias, mapas personalizáveis |
| **Formato de Resultados** | Linguagem natural com citações | JSON estruturado |
| **Complexidade de Integração** | Simples - integrado ao Claude | Requer integração personalizada |
| **Tier Gratuito** | Nenhum | 2.500 consultas gratuitas |

### 8.5 Resumo da Posição Competitiva

A Ferramenta de Busca na Web da Anthropic oferece várias vantagens únicas:

- **Integração Perfeita**: Totalmente integrada ao Claude, requerendo esforço mínimo do desenvolvedor
- **Síntese de Alta Qualidade**: Excele em sintetizar informações de múltiplas fontes
- **Transparência de Fontes**: Todos os resultados de busca na web incluem citações, melhorando a credibilidade
- **Controle de Domínio**: Organizações podem manter controle através de configurações administrativas
- **Preços Simples**: Modelo de preços direto
- **Capacidades de Múltiplas Pesquisas**: Pode realizar múltiplas pesquisas sequenciais em um único turno de conversa

Principais desvantagens comparadas às alternativas:

- **Custo**: Mais caro que APIs de busca direta
- **Controle Limitado**: Desenvolvedores têm controle limitado sobre quando as pesquisas ocorrem
- **Limitações de Busca**: Sem operadores de busca avançados ou tipos de busca especializados

## 9. Preços e Limitações

### 9.1 Estrutura de Preços

- **Custo base**: $10 por 1.000 buscas na web
- **Custos adicionais**: Custos padrão por token para modelos Claude se aplicam para tokens de entrada e saída
- **Cálculo de tokens**: Resultados de busca na web recuperados ao longo de uma conversa são contados como tokens de entrada
- **Estrutura de cobrança**: Cada busca na web conta como um uso, independentemente do número de resultados retornados
- **Buscas com falha**: Se ocorrer um erro durante a busca na web, a busca não será cobrada

### 9.2 Modelos que Suportam Busca na Web

A Ferramenta de Busca na Web está disponível na API da Anthropic para:
- Claude 3.7 Sonnet
- Claude 3.5 Sonnet
- Claude 3.5 Haiku

### 9.3 Limites de Uso

- **Máximo de pesquisas por solicitação**: Configurável via parâmetro `max_uses`
- **Pesquisas sequenciais**: O Claude pode conduzir múltiplas pesquisas sequenciais em um único turno de conversa
- **Throttling de solicitações**: Sujeito aos limites de taxa padrão da API Anthropic baseados no tier de uso
- **Disponibilidade do serviço**: Atualmente disponível para usuários pagos da API Claude globalmente

### 9.4 Limitações Técnicas

- **Sem controle direto de consulta**: Desenvolvedores não podem especificar diretamente consultas de pesquisa
- **Motor de busca caixa-preta**: Transparência limitada na tecnologia de busca subjacente
- **Configurabilidade limitada**: Apenas opções básicas de configuração
- **Requisitos de citação**: Citações estão sempre habilitadas, não podem ser desabilitadas
- **Impacto na janela de contexto**: Resultados de pesquisa consomem tokens da janela de contexto

### 9.5 Limitações de Conteúdo

- **Restrições de domínio**: Organizações podem restringir quais domínios o Claude pode pesquisar
- **Filtragem de conteúdo**: Sujeito às políticas de conteúdo padrão da Anthropic
- **Controles administrativos**: Busca na web pode ser habilitada/desabilitada no nível organizacional
- **Frescor dos resultados**: Resultados dependem do frescor do índice de busca

### 9.6 Disponibilidade Regional

- **Versão API**: Disponível para desenvolvedores globalmente
- **Personalização de localização**: Suporta o parâmetro `user_location` para localizar resultados de pesquisa

## 10. Exemplos de Código

### 10.1 Python

```python
import os
import anthropic

# Inicializar cliente com chave API
client = anthropic.Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY"),
)

# Criar uma mensagem com busca na web habilitada
response = client.messages.create(
    model="claude-3-7-sonnet-20250219",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Quais são os últimos desenvolvimentos em computação quântica?"}
    ],
    tools=[
        {
            "type": "web_search_20250305",
            "name": "web_search",
            "max_uses": 5,
            "blocked_domains": ["fonteduvidosa.com"],
            "user_location": {
                "type": "approximate",
                "city": "São Paulo",
                "region": "São Paulo",
                "country": "BR",
                "timezone": "America/Sao_Paulo"
            }
        }
    ]
)

# Processar resposta
for content_block in response.content:
    if content_block.type == "text":
        print(f"Resposta do Claude: {content_block.text}")
        if hasattr(content_block, "citations") and content_block.citations:
            for citation in content_block.citations:
                print(f"Fonte: {citation.url}")
                print(f"Texto citado: {citation.cited_text}")
    elif content_block.type == "server_tool_use":
        print(f"Consulta de pesquisa: {content_block.input.query}")
```

### 10.2 JavaScript/Node.js

```javascript
const { Anthropic } = require('@anthropic-ai/sdk');

// Inicializar cliente com chave API
const anthropic = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY,
});

async function buscarComClaude() {
  try {
    const response = await anthropic.messages.create({
      model: "claude-3-7-sonnet-20250219",
      max_tokens: 1024,
      messages: [
        { role: "user", content: "Quais são os últimos desenvolvimentos em computação quântica?" }
      ],
      tools: [
        {
          type: "web_search_20250305",
          name: "web_search",
          max_uses: 5,
          blocked_domains: ["fonteduvidosa.com"],
          user_location: {
            type: "approximate",
            city: "São Paulo",
            region: "São Paulo",
            country: "BR",
            timezone: "America/Sao_Paulo"
          }
        }
      ]
    });

    // Processar resposta
    response.content.forEach(block => {
      if (block.type === "text") {
        console.log(`Resposta do Claude: ${block.text}`);
        if (block.citations) {
          block.citations.forEach(citation => {
            console.log(`Fonte: ${citation.url}`);
            console.log(`Texto citado: ${citation.cited_text}`);
          });
        }
      } else if (block.type === "server_tool_use") {
        console.log(`Consulta de pesquisa: ${block.input.query}`);
      }
    });
  } catch (error) {
    console.error('Erro:', error);
  }
}

buscarComClaude();
```

### 10.3 Ruby

```ruby
require 'anthropic'

# Inicializar cliente com chave API
client = Anthropic::Client.new(
  access_token: ENV['ANTHROPIC_API_KEY'],
  log_errors: true
)

# Criar uma mensagem com busca na web habilitada
response = client.messages.create(
  model: "claude-3-7-sonnet-20250219",
  max_tokens: 1024,
  messages: [
    { role: "user", content: "Quais são os últimos desenvolvimentos em computação quântica?" }
  ],
  tools: [
    {
      type: "web_search_20250305",
      name: "web_search",
      max_uses: 5,
      blocked_domains: ["fonteduvidosa.com"],
      user_location: {
        type: "approximate",
        city: "São Paulo",
        region: "São Paulo",
        country: "BR",
        timezone: "America/Sao_Paulo"
      }
    }
  ]
)

# Processar resposta
response.content.each do |block|
  if block.type == "text"
    puts "Resposta do Claude: #{block.text}"
    if block.respond_to?(:citations) && block.citations
      block.citations.each do |citation|
        puts "Fonte: #{citation.url}"
        puts "Texto citado: #{citation.cited_text}"
      end
    end
  elsif block.type == "server_tool_use"
    puts "Consulta de pesquisa: #{block.input.query}"
  end
end
```

### 10.4 cURL

```bash
curl https://api.anthropic.com/v1/messages \
  --header "x-api-key: $ANTHROPIC_API_KEY" \
  --header "anthropic-version: 2023-06-01" \
  --header "content-type: application/json" \
  --data '{
    "model": "claude-3-7-sonnet-20250219",
    "max_tokens": 1024,
    "messages": [
      {
        "role": "user",
        "content": "Quais são os últimos desenvolvimentos em computação quântica?"
      }
    ],
    "tools": [
      {
        "type": "web_search_20250305",
        "name": "web_search",
        "max_uses": 5,
        "blocked_domains": ["fonteduvidosa.com"],
        "user_location": {
          "type": "approximate",
          "city": "São Paulo",
          "region": "São Paulo",
          "country": "BR",
          "timezone": "America/Sao_Paulo"
        }
      }
    ]
  }'
```

### 10.5 Python com Streaming

```python
import os
import anthropic
import json

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

with client.messages.stream(
    model="claude-3-7-sonnet-20250219",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Quais são os últimos desenvolvimentos em computação quântica?"}
    ],
    tools=[
        {
            "type": "web_search_20250305",
            "name": "web_search",
            "max_uses": 5
        }
    ]
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
    
    # Processar mensagem completa no final
    message = stream.get_final_message()
    
    for block in message.content:
        if block.type == "server_tool_use":
            print(f"\nConsulta de pesquisa: {block.input['query']}")
        elif block.type == "web_search_tool_result":
            print(f"\nResultados da pesquisa: {len(block.content)} itens")
            for result in block.content:
                if hasattr(result, "url"):
                    print(f"- {result.title}: {result.url}")
```

## 11. Padrões de Uso Avançados

### 11.1 Busca Multi-hop

Implementar busca multi-hop permite que o Claude siga um caminho de pesquisa:

```javascript
// Configurar max_uses mais alto para permitir pesquisa multi-hop
const response = await anthropic.messages.create({
  model: "claude-3-7-sonnet-20250219",
  tools: [{ 
    type: "web_search_20250305", 
    name: "web_search", 
    max_uses: 10 
  }],
  messages: [
    { 
      role: "user", 
      content: "Pesquise o impacto das últimas políticas de mudanças climáticas sobre investimentos em energia renovável. Conduza uma pesquisa completa examinando múltiplas fontes." 
    }
  ]
});
```

Isso permite que o Claude conduza uma série de pesquisas, com cada pesquisa se baseando em descobertas anteriores.

### 11.2 Implementação de Cache de Prompts

```json
{
  "model": "claude-3-7-sonnet-20250219",
  "system": [
    {
      "type": "text",
      "text": "Você é um assistente de pesquisa que ajuda usuários a encontrar informações atuais.",
      "cache_control": {
        "type": "ephemeral"
      }
    }
  ],
  "tools": [
    {
      "type": "web_search_20250305",
      "name": "web_search",
      "max_uses": 5
    }
  ],
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Quais são os últimos desenvolvimentos em computação quântica?"
        }
      ]
    }
  ]
}
```

Isso permite conversas multi-turno mais eficientes ao cachear conteúdo entre solicitações.

### 11.3 Integração com Outras Ferramentas

Você pode combinar busca na web com outras ferramentas para funcionalidade aprimorada:
- Integrar com bancos de dados vetoriais para busca híbrida
- Combinar com processamento de arquivos para contextualização de documentos
- Emparelhar com chamadas de função para saídas acionáveis

Exemplo de combinação com outras ferramentas:

```python
response = client.messages.create(
    model="claude-3-7-sonnet-20250219",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Analise as últimas tendências de mercado para energia renovável e forneça um resumo."}
    ],
    tools=[
        {
            "type": "web_search_20250305",
            "name": "web_search",
            "max_uses": 5
        },
        {
            "type": "function",
            "function": {
                "name": "gerar_relatorio",
                "description": "Gerar um relatório formatado com as informações analisadas",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "titulo": {"type": "string"},
                        "secoes": {"type": "array", "items": {"type": "string"}},
                        "dados": {"type": "object"},
                        "resumo": {"type": "string"}
                    },
                    "required": ["titulo", "secoes", "resumo"]
                }
            }
        }
    ]
)
```

### 11.4 Configuração de Busca Especializada

Configure busca para setores específicos:

#### Saúde

```json
{
  "type": "web_search_20250305",
  "name": "web_search",
  "max_uses": 8,
  "allowed_domains": [
    "nih.gov", 
    "who.int", 
    "mayoclinic.org", 
    "medlineplus.gov", 
    "nejm.org", 
    "jamanetwork.com"
  ]
}
```

#### Educação

```json
{
  "type": "web_search_20250305",
  "name": "web_search",
  "max_uses": 8,
  "allowed_domains": [
    "ed.gov", 
    "harvard.edu", 
    "mit.edu", 
    "stanford.edu", 
    "scholar.google.com", 
    "jstor.org"
  ]
}
```

#### Governo

```json
{
  "type": "web_search_20250305",
  "name": "web_search",
  "max_uses": 8,
  "allowed_domains": [
    "gov.br", 
    "camara.leg.br", 
    "senado.leg.br", 
    "planalto.gov.br", 
    "justica.gov.br",
    "fazenda.gov.br"
  ]
}
```

### 11.5 Lidando com Casos Extremos

#### Resultados Insuficientes ou Ausentes

Quando pesquisas retornam poucos resultados:
- Implementar estratégias de fallback (ampliar termos de pesquisa)
- Fornecer feedback claro ao usuário sobre limitações de pesquisa
- Usar conhecimento base do Claude quando resultados web não estão disponíveis

```javascript
// Monitorar resultados de pesquisa vazios
client.on('web_search_results', (results) => {
  if (results.length === 0) {
    // Executar pesquisa de fallback com termos mais amplos
    executarPesquisaFallback();
  }
});
```

#### Lidando com Tópicos Controversos

Para tópicos sensíveis ou controversos:
- Implementar filtragem adicional de conteúdo
- Fornecer fontes equilibradas de múltiplas perspectivas
- Usar restrições adicionais de domínio
- Adicionar avisos sobre precisão das informações

#### Inconsistências nos Resultados de Pesquisa

Quando informações contraditórias aparecem:
- Implementar pontuação de credibilidade de fontes
- Priorizar recência para informações sensíveis ao tempo
- Solicitar que o Claude aborde contradições explicitamente
- Considerar revisão humana para informações críticas

## 12. Considerações de Segurança

### 12.1 Autenticação e Autorização

#### Segurança de Chaves API
- **Armazenamento Seguro**: Nunca armazene chaves API em repositórios públicos, código do lado cliente ou armazenamento não criptografado
- **Variáveis de Ambiente**: Use variáveis de ambiente para injetar chaves API de forma segura em aplicações
- **Gerenciamento de Segredos**: Utilize serviços de gerenciamento de segredos de provedores de nuvem para armazenamento de chaves API
- **Rotação de Chaves**: Implemente um cronograma regular para rotação de chaves API
- **Controle de Acesso**: Restrinja o acesso à chave API apenas aos serviços e pessoal que absolutamente necessitam
- **Monitoramento**: Implemente monitoramento para padrões suspeitos de uso da API

#### Controles de Acesso de Usuário
- **Hierarquias de Permissão**: Estabeleça controles de acesso em várias camadas para capacidades de busca na web
- **Acesso Baseado em Papel**: Implemente controle de acesso baseado em papel (RBAC)
- **Log de Auditoria**: Mantenha logs abrangentes do uso de busca na web

### 12.2 Manipulação e Privacidade de Dados

#### Proteção de Dados
- **Minimização de Dados**: Passe apenas dados necessários para a API
- **Criptografia**: Garanta que todos os dados sejam criptografados em trânsito usando TLS
- **Informações Sensíveis**: Evite enviar informações pessoalmente identificáveis (PII) em consultas
- **Políticas de Retenção**: Implemente políticas claras de retenção de dados

#### Dados de Localização do Usuário
- **Use com Consideração Cuidadosa**: Forneça dados de localização do usuário apenas quando necessário
- **Transparência**: Informe usuários quando sua localização aproximada pode ser usada
- **Anonimização**: Use apenas a granularidade mínima de localização necessária

### 12.3 Proteção Contra Vulnerabilidades Comuns

#### Prevenção de Injeção de Prompts
- **Validação de Entrada**: Valide e sanitize todas as entradas do usuário
- **Filtragem de Solicitações**: Implemente filtros para identificar e bloquear entradas potencialmente prejudiciais
- **Detecção de Padrões**: Use correspondência de padrões para detectar tentativas de injeção de prompt
- **Limites de Contexto**: Mantenha limites claros entre instruções do sistema e entradas do usuário

#### Filtragem de Domínio
- **Listas de Permitidos**: Implemente listas de domínios permitidos para restringir pesquisas a sites confiáveis
- **Listas de Bloqueados**: Use listas de domínios bloqueados para prevenir acesso a sites prejudiciais
- **Validação de Domínio**: Valide a estrutura do domínio para prevenir tentativas de manipulação

### 12.4 Considerações de Conformidade

#### Conformidade com GDPR
- **Base Legal**: Garanta uma base legal para processamento de dados pessoais
- **Minimização de Dados**: Colete e processe apenas a quantidade mínima de dados necessária
- **Transparência**: Informe usuários quando seus dados podem ser usados para buscas na web
- **Direitos de Acesso**: Implemente mecanismos permitindo que usuários acessem, corrijam ou excluam seus dados

#### Conformidade com CCPA
- **Avisos de Privacidade**: Atualize avisos de privacidade para refletir funcionalidade de busca na web
- **Mecanismos de Opt-Out**: Forneça opções claras para usuários optarem por não participar
- **Inventários de Dados**: Mantenha inventários de categorias de dados coletados

#### Regulamentações Específicas do Setor
- **Saúde (HIPAA)**: Evite passar informações de saúde protegidas (PHI) em consultas de busca na web
- **Serviços Financeiros**: Considere regulamentações adicionais para dados financeiros
- **Proteção Infantil**: Implemente salvaguardas extras se serviços podem ser usados por crianças

### 12.5 Lidando com Consultas de Pesquisa Sensíveis

- **Filtros de Pré-processamento**: Implemente filtros para identificar e bloquear conteúdo de consulta potencialmente prejudicial
- **Triagem de Respostas**: Filtre respostas para conteúdo sensível ou inapropriado
- **Categorias de Uso**: Classifique diferentes tipos de pesquisas e aplique controles de segurança apropriados

### 12.6 Exemplo de Implementação de Segurança

```javascript
// Exemplo: Recuperação de dados financeiros com medidas de segurança
const response = await anthropic.messages.create({
  model: "claude-3-7-sonnet-20250219",
  max_tokens: 1024,
  tools: [{
    type: "web_search_20250305",
    name: "web_search",
    max_uses: 10,
    allowed_domains: [
      "sec.gov", 
      "investor-relations.company.com",
      "finance.trusted-news-source.com"
    ]
  }],
  system: [{
    type: "text",
    text: "Você é um assistente de análise financeira. Forneça apenas informações factuais sobre empresas públicas com citações.",
    cache_control: { type: "ephemeral" }
  }],
  messages: [
    { role: "user", content: "Quais são os últimos resultados trimestrais da Tesla?" }
  ]
});
```

## 13. Otimização de Desempenho

### 13.1 Minimizando Latência

#### Design Eficiente de Consultas
- **Consultas Estruturadas**: Projete consultas claras e específicas para gerar resultados mais relevantes mais rapidamente
- **Comprimento de Consulta**: Mantenha consultas concisas, mas informativas, para otimizar a eficiência da pesquisa
- **Precisão de Contexto**: Forneça apenas o contexto necessário para reduzir a sobrecarga de processamento

#### Paralelização
- **Processamento em Lote**: Use a API de processamento em lote para múltiplas solicitações de pesquisa relacionadas
- **Solicitações Assíncronas**: Implemente processamento assíncrono para operações não bloqueantes
- **Pipeline de Solicitações**: Construa pipelines de solicitação para processar múltiplas pesquisas eficientemente

#### Otimização do Lado Cliente
- **Pool de Conexões**: Mantenha conexões persistentes para reduzir a sobrecarga de handshake
- **Compressão de Solicitações**: Comprima solicitações para reduzir o tempo de transmissão de rede
- **Manuseio Eficiente de JSON**: Otimize serialização/deserialização de JSON

### 13.2 Estratégias de Cache

#### Cache de Prompts
- **Implementação**: Habilite cache de prompts adicionando pontos de quebra `cache_control`
- **Otimização**: Coloque conteúdo estático no início dos prompts para cache ideal
- **Cache Multi-turno**: Defina pontos de quebra de cache após o último resultado de busca na web

Exemplo com cache de prompts:
```json
{
  "messages": [
    {"role": "user", "content": "Pesquise avanços em computação quântica"},
    {"role": "assistant", "content": [
      {"type": "web_search_tool_result", "tool_use_id": "123", "content": {...}},
      {"type": "text", "text": "Aqui estão os últimos avanços...", "cache_control": {"type": "cache_breakpoint"}}
    ]},
    {"role": "user", "content": "Conte-me mais sobre esses avanços quânticos"}
  ]
}
```

#### Cache de Respostas
- **Cache do Lado Cliente**: Cache respostas para perguntas frequentemente feitas
- **Invalidação de Cache**: Implemente estratégias de invalidação de cache baseadas em TTL
- **Cache de Resposta Parcial**: Cache partes estáveis das respostas enquanto atualiza elementos voláteis

### 13.3 Limitação de Taxa e Throttling

#### Entendendo Limites de Taxa
A Anthropic aplica limites de taxa no nível organizacional:
- Solicitações por minuto (RPM)
- Tokens de entrada por minuto (ITPM)
- Tokens de saída por minuto (OTPM)

#### Gerenciamento Efetivo de Limites de Taxa
- **Algoritmo Token Bucket**: Implemente limitação de taxa token bucket do lado cliente
- **Throttling Adaptativo**: Ajuste dinamicamente as taxas de solicitação com base nos cabeçalhos de resposta
- **Estratégias de Backoff**: Implemente backoff exponencial para lidar com exceções de limite de taxa
- **Priorização de Solicitações**: Priorize solicitações críticas ao se aproximar dos limites de taxa

#### Exemplo de Implementação

```javascript
class LimitadorDeRate {
  constructor(maxRequestsPorMinuto) {
    this.maxRequestsPorMinuto = maxRequestsPorMinuto;
    this.tokensDisponiveis = maxRequestsPorMinuto;
    this.ultimoRefreshTimestamp = Date.now();
    this.taxaDeRefresh = maxRequestsPorMinuto / (60 * 1000); // tokens por milissegundo
  }

  async obterToken() {
    this.recarregar();
    
    if (this.tokensDisponiveis >= 1) {
      this.tokensDisponiveis -= 1;
      return true;
    }
    
    // Calcular tempo de espera
    const tempoEspera = (1 / this.taxaDeRefresh) * 1000;
    await new Promise(resolve => setTimeout(resolve, tempoEspera));
    
    return this.obterToken(); // Tentar novamente após espera
  }
  
  recarregar() {
    const agora = Date.now();
    const tempoDecorrido = agora - this.ultimoRefreshTimestamp;
    const tokensParaAdicionar = tempoDecorrido * this.taxaDeRefresh;
    
    this.tokensDisponiveis = Math.min(
      this.maxRequestsPorMinuto,
      this.tokensDisponiveis + tokensParaAdicionar
    );
    
    this.ultimoRefreshTimestamp = agora;
  }
}

// Uso
const limitadorDeRate = new LimitadorDeRate(60); // 60 solicitações por minuto

async function fazerSolicitacao() {
  await limitadorDeRate.obterToken();
  // Agora fazer a chamada real da API
  return anthropic.messages.create({...});
}
```

### 13.4 Otimização de Recursos

#### Otimização de Tokens
- **Engenharia de Prompts**: Elabore prompts eficientes para minimizar o uso de tokens
- **Janelas de Contexto**: Implemente janelas de contexto deslizantes para conversas longas
- **Uso Eficiente de Ferramentas**: Habilite uso eficiente de ferramentas com cabeçalhos apropriados

#### Considerações de Arquitetura do Sistema
- **Design Stateless**: Projete componentes stateless para permitir escalonamento horizontal
- **Balanceamento de Carga**: Distribua solicitações através de múltiplas instâncias ou regiões
- **Computação Serverless**: Considere arquiteturas serverless para escalonamento elástico

#### Otimização de Custos
- **Análises de Uso**: Implemente rastreamento detalhado de uso para identificar oportunidades de otimização
- **Planejamento de Uso em Camadas**: Planeje camadas de uso baseadas em volumes antecipados de pesquisa
- **Alocação de Custos**: Implemente marcação de alocação de custos para faturamento preciso

### 13.5 Benchmarks de Desempenho

#### Benchmarks de Tempo de Resposta
- **Tempo de Resposta Médio**: 500ms-2s para consultas básicas (excluindo tempo de execução de busca na web)
- **Sobrecarga de Busca na Web**: Adicional de 1-3s para operações de busca na web
- **Processamento em Lote**: Espere melhoria de eficiência de 20-30% para operações em lote

#### Expectativas de Throughput
- **Consultas Por Segundo (QPS)**: Planeje para 1-10 QPS por instância de aplicação
- **Concorrência**: Projete para 10-100 usuários concorrentes por implantação
- **Fator de Escalonamento**: Escalonamento linear até os limites de taxa organizacionais

## 14. Exemplos de Implementação no Mundo Real

### 14.1 Implementação em Serviços Financeiros

**Agente de Análise de Portfólio:**

```javascript
const response = await anthropic.messages.create({
  model: "claude-3-7-sonnet-20250219",
  max_tokens: 2048,
  tools: [{
    type: "web_search_20250305",
    name: "web_search",
    max_uses: 10,
    allowed_domains: [
      "sec.gov",
      "bloomberg.com",
      "wsj.com",
      "finance.yahoo.com",
      "ft.com",
      "investor.company-name.com"
    ]
  }],
  system: "Você é um assistente de análise financeira que ajuda investidores a tomar decisões informadas. Ao analisar empresas, sempre cite suas fontes e inclua métricas financeiras relevantes.",
  messages: [{
    role: "user",
    content: "Analise o desempenho trimestral mais recente da Tesla, Apple e Microsoft. Compare seu crescimento de receita, margens de lucro e perspectivas futuras. O que os analistas estão dizendo sobre o desempenho de suas ações no próximo trimestre?"
  }]
});
```

### 14.2 Aplicação de Pesquisa Jurídica

```javascript
const response = await anthropic.messages.create({
  model: "claude-3-7-sonnet-20250219",
  max_tokens: 2048,
  tools: [{
    type: "web_search_20250305",
    name: "web_search",
    max_uses: 15,
    allowed_domains: [
      "law.cornell.edu",
      "supremecourt.gov",
      "courtlistener.com",
      "justice.gov",
      "findlaw.com",
      "lexisnexis.com",
      "westlaw.com"
    ],
    user_location: {
      type: "approximate",
      country: "BR",
      region: "São Paulo"
    }
  }],
  system: "Você é um assistente de pesquisa jurídica. Forneça informações legais atuais com citações precisas de estatutos, regulamentos e jurisprudência. Sempre inclua a jurisdição, tribunal e data para citações de casos.",
  messages: [{
    role: "user",
    content: "Pesquise decisões recentes do Supremo Tribunal Federal relacionadas ao direito digital, particularmente focando em casos dos últimos 2 anos. Forneça um resumo das principais decisões e suas implicações."
  }]
});
```

### 14.3 Ferramenta de Suporte para Desenvolvedores

```javascript
const response = await anthropic.messages.create({
  model: "claude-3-7-sonnet-20250219",
  max_tokens: 1024,
  tools: [{
    type: "web_search_20250305",
    name: "web_search",
    max_uses: 8,
    allowed_domains: [
      "github.com",
      "stackoverflow.com",
      "docs.python.org",
      "developer.mozilla.org",
      "reactjs.org",
      "nodejs.org",
      "aws.amazon.com"
    ]
  }],
  system: "Você é um assistente de desenvolvedor que ajuda a resolver problemas de programação e fornece informações atualizadas sobre linguagens de programação, frameworks e bibliotecas. Sempre inclua exemplos de código e cite suas fontes.",
  messages: [{
    role: "user",
    content: "Estou recebendo este erro com React 18: 'Warning: ReactDOM.render is no longer supported in React 18'. Como atualizo meu código para usar a nova abordagem? Mostre-me exemplos de código tanto para o método antigo quanto para o novo."
  }]
});
```

### 14.4 Assistente de Planejamento de Viagens

```javascript
const response = await anthropic.messages.create({
  model: "claude-3-7-sonnet-20250219",
  max_tokens: 2048,
  tools: [{
    type: "web_search_20250305",
    name: "web_search",
    max_uses: 12,
    allowed_domains: [
      "travel.state.gov",
      "cdc.gov",
      "tripadvisor.com",
      "lonelyplanet.com",
      "booking.com",
      "kayak.com"
    ],
    user_location: {
      type: "approximate",
      city: "São Paulo",
      region: "São Paulo",
      country: "BR",
      timezone: "America/Sao_Paulo"
    }
  }],
  system: "Você é um assistente de planejamento de viagens que fornece informações atuais sobre destinos, acomodações, atrações e requisitos de viagem. Sempre inclua detalhes importantes como requisitos de visto, avisos de saúde e considerações sazonais.",
  messages: [{
    role: "user",
    content: "Estou planejando uma viagem ao Japão em outubro de 2025. Quais são os requisitos de entrada atuais para cidadãos brasileiros? Que cidades devo visitar? Onde devo me hospedar em Tóquio? Quais são as melhores coisas para fazer em Kyoto?"
  }]
});
```

### 14.5 Serviço de Informações de Saúde

```javascript
const response = await anthropic.messages.create({
  model: "claude-3-7-sonnet-20250219",
  max_tokens: 2048,
  tools: [{
    type: "web_search_20250305",
    name: "web_search",
    max_uses: 10,
    allowed_domains: [
      "nih.gov",
      "cdc.gov",
      "who.int",
      "mayoclinic.org",
      "medlineplus.gov",
      "nejm.org",
      "jamanetwork.com"
    ]
  }],
  system: "Você é um assistente de informações de saúde que fornece informações baseadas em evidências sobre condições médicas, tratamentos e cuidados preventivos. Sempre cite fontes médicas autoritárias e inclua avisos sobre consultar profissionais de saúde para aconselhamento médico pessoal.",
  messages: [{
    role: "user",
    content: "Quais são as diretrizes mais recentes para o gerenciamento do diabetes tipo 2? Que mudanças no estilo de vida, medicamentos e abordagens de monitoramento são atualmente recomendadas pelas principais organizações de saúde?"
  }]
});
```

## 15. Referências e Recursos

### 15.1 Documentação Oficial

- [Documentação da Ferramenta de Busca na Web da Anthropic](https://docs.anthropic.com/en/docs/build-with-claude/tool-use/web-search-tool)
- [Referência da API da Anthropic](https://docs.anthropic.com/claude/reference/messages_post)
- [Guia de Uso de Ferramentas do Claude](https://docs.anthropic.com/claude/docs/tool-use)
- [Documentação do Console da Anthropic](https://console.anthropic.com/docs/)

### 15.2 Especificações da API

- [Referência da API Messages](https://docs.anthropic.com/claude/reference/messages_post)
- [Referência da API Streaming](https://docs.anthropic.com/claude/reference/messages-streaming)
- [Referência de Tipos](https://docs.anthropic.com/claude/reference/types)
- [Documentação de Limites de Taxa](https://docs.anthropic.com/claude/docs/rate-limits)

### 15.3 Documentação dos SDKs

- [Documentação do SDK Python](https://github.com/anthropics/anthropic-sdk-python)
- [Documentação do SDK JavaScript/TypeScript](https://github.com/anthropics/anthropic-sdk-typescript)
- [Documentação do SDK Ruby](https://github.com/anthropics/anthropic-sdk-ruby)
- [Documentação do SDK Java](https://github.com/anthropics/anthropic-sdk-java)
- [Documentação do SDK Go](https://github.com/anthropics/anthropic-sdk-go)

### 15.4 Posts do Blog e Anúncios

- [Anúncio da Ferramenta de Busca na Web](https://www.anthropic.com/news/web-search-api)
- [Notas de Lançamento do Claude 3.7 Sonnet](https://www.anthropic.com/news/claude-3-7-sonnet)
- [Visão Geral do Uso de Ferramentas](https://www.anthropic.com/news/tool-use-with-claude)

### 15.5 Tutoriais e Guias

- [Começando com Busca na Web](https://docs.anthropic.com/claude/docs/getting-started-with-web-search)
- [Técnicas Avançadas de Busca na Web](https://docs.anthropic.com/claude/docs/advanced-web-search)
- [Melhores Práticas de Filtragem de Domínio](https://docs.anthropic.com/claude/docs/domain-filtering)
- [Diretrizes de Segurança para Busca na Web](https://docs.anthropic.com/claude/docs/security-guidelines)

### 15.6 Recursos da Comunidade

- [Fórum de Desenvolvedores da Anthropic](https://www.anthropic.com/developers)
- [Repositório de Exemplos no GitHub](https://github.com/anthropics/anthropic-cookbook)
- [Tag Anthropic no Stack Overflow](https://stackoverflow.com/questions/tagged/anthropic)

### 15.7 Ferramentas e Serviços Relacionados

- [Guia de Engenharia de Prompts da Anthropic](https://docs.anthropic.com/claude/docs/prompt-engineering)
- [Visão Geral dos Modelos Claude](https://docs.anthropic.com/claude/docs/models-overview)
- [Status da Plataforma Anthropic](https://status.anthropic.com/)

---

Esta documentação abrangente fornece uma referência completa para a Ferramenta de Busca na Web da Anthropic, cobrindo todos os aspectos desde implementação básica até padrões de uso avançados, considerações de segurança e otimização de desempenho. Seja você um desenvolvedor implementando as capacidades de busca na web do Claude pela primeira vez ou um usuário experiente procurando otimizar sua implementação, este guia oferece as informações detalhadas que você precisa para ter sucesso.