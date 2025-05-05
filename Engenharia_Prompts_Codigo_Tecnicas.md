# Engenharia de prompts para código: técnicas que funcionam

Este guia apresenta as melhores técnicas para construir prompts eficazes para agentes de LLM como Cursor IDE, VSCode Copilot, Windsurf e Claude Code. O foco está em como criar instruções que evitem problemas comuns: código que quebra, bugs inesperados, funções que fogem do escopo solicitado e código desnecessariamente extenso.

## Princípios fundamentais para prompts de código eficazes

As ferramentas de LLM para desenvolvimento de código transformaram a programação, mas seu uso eficaz depende diretamente da qualidade dos prompts. Pesquisas recentes e experiências de desenvolvedores revelam que prompts bem estruturados podem melhorar a precisão do código gerado em até 57% no LLaMA e 67% no GPT-4.

**Quatro princípios essenciais se destacam em todas as ferramentas:**

1. **Contexto detalhado**: Forneça informações específicas sobre o projeto, requisitos e limitações técnicas.
2. **Decomposição de problemas**: Divida tarefas complexas em subtarefas menores e mais gerenciáveis.
3. **Pensamento estruturado**: Instrua o LLM a raciocinar passo a passo antes de programar.
4. **Verificação integrada**: Solicite explicitamente a validação do código gerado.

Analisando práticas recomendadas oficialmente, artigos técnicos e experiências compartilhadas por desenvolvedores, compilamos as técnicas mais eficazes para cada aspecto crítico do desenvolvimento.

## Técnicas para evitar código quebrado

### 1. Program-Aided Language Models (PAL)

Esta técnica utiliza o LLM para raciocinar sobre o problema através de código intermediário, mas delega a execução a um interpretador externo.

**Template de prompt:**
```
Vou fornecer um problema para resolver. Gere um código Python para solucioná-lo:
1. Defina claramente as variáveis de entrada
2. Implemente a solução passo a passo com comentários explicativos
3. Adicione uma função principal que retorne o resultado final
4. Certifique-se de que o código seja executável

Problema: [descrição do problema]
```

**Por que funciona:** Estudos mostram um aumento de até 15% na precisão em tarefas complexas comparado a métodos tradicionais, pois separa a geração da execução.

### 2. Structured Chain-of-Thought (SCoT)

Esta técnica estrutura o raciocínio do LLM em torno de elementos fundamentais de programação.

**Template de prompt:**
```
Para resolver este problema, considere as estruturas de programação necessárias:
1. Quais sequências de passos precisamos seguir?
2. Quais estruturas condicionais (if/else) são necessárias?
3. Quais loops (for/while) seriam úteis?

Após esta análise, escreva o código completo.

Problema: [problema aqui]
```

**Por que funciona:** O SCoT prompting superou o Chain-of-Thought tradicional em até 13,79% em benchmarks como HumanEval, estruturando o pensamento em torno de elementos fundamentais de programação.

### 3. Simulação de execução integrada

**Template de prompt:**
```
Crie um código em [linguagem] para [tarefa]. 
Após gerar o código, simule sua execução passo a passo com exemplos de entrada e identifique possíveis falhas. 
Considere especialmente casos como: [listar casos problemáticos típicos].
Corrija quaisquer problemas antes de fornecer a versão final.
```

## Técnicas para minimizar bugs

### 1. Test-Driven Development (TDD) com LLMs

**Template de prompt:**
```
Aqui estão testes unitários para uma função que você deve implementar:

```python
def test_funcao():
    assert funcao_alvo(5) == 120
    assert funcao_alvo(0) == 1
    assert funcao_alvo(-1) == None
```

Implemente a função_alvo para que passe em todos os testes.
Garanta que o código seja robusto e trate casos extremos adequadamente.
```

**Por que funciona:** Começar com testes força o LLM a considerar os requisitos exatos e casos de borda antes de implementar.

### 2. Chain-of-Thought com identificação de bugs

**Template de prompt:**
```
Pense passo a passo para resolver esta tarefa de programação:
1. Descreva o que pretende fazer
2. Escreva o código correspondente
3. Identifique possíveis bugs nesta parte
4. Refine o código para evitar esses problemas

Tarefa: [descrição da tarefa]
```

**Por que funciona:** Esta técnica induz o LLM a adotar uma abordagem crítica, analisando potenciais problemas em cada etapa.

### 3. Abordagem de auto-crítica

**Template de prompt:**
```
Escreva um código para [tarefa].
Depois, atue como um revisor de código experiente e critique seu próprio código. Identifique:
1. Bugs potenciais
2. Casos extremos não tratados
3. Problemas de desempenho 
4. Problemas de legibilidade

Em seguida, refatore o código para corrigir todos os problemas identificados.
```

## Técnicas para manter escopo preciso

### 1. Especificação detalhada de requisitos

**Template de prompt:**
```
Escreva um código em [linguagem] que implemente exatamente a seguinte funcionalidade:

[Descrição detalhada da tarefa]

Requisitos específicos:
- Entrada: [detalhes da entrada]
- Saída: [detalhes da saída]
- Restrições: [restrições específicas]
- Comportamento com erros: [como lidar com erros]
- Funcionalidades que NÃO devem ser implementadas: [o que não fazer]

Mantenha o código focado apenas nesses requisitos, sem adicionar funcionalidades extras.
```

**Por que funciona:** Definir limites claros do que deve e não deve ser implementado ajuda o LLM a manter o escopo preciso.

### 2. Decomposição funcional

**Template de prompt:**
```
Para implementar [tarefa principal], decomponha-a em funções menores e específicas:

1. Identifique todas as suboperações necessárias
2. Para cada suboperação, defina: nome, entradas, saídas e propósito
3. Implemente cada função com propósito único
4. Combine as funções para compor a solução completa

Limite cada função a uma única responsabilidade e mantenha o escopo preciso.
```

**Por que funciona:** A decomposição funcional incentiva a criação de funções modulares com propósito bem definido.

### 3. Contrato de interface explícito

**Template de prompt:**
```
Defina um contrato de interface para uma função que [faz algo]:

1. Nome da função: [nome]
2. Parâmetros: [lista de parâmetros com tipos]
3. Valor de retorno: [tipo e descrição]
4. Exceções possíveis: [lista de exceções]
5. Pré-condições: [condições necessárias antes da função]
6. Pós-condições: [garantias após a execução]

Agora implemente essa função seguindo EXATAMENTE esse contrato.
```

## Técnicas para evitar código excessivo

### 1. Restrições de estilo e concisão

**Template de prompt:**
```
Escreva um código [linguagem] para [tarefa] seguindo estas diretrizes:

1. Priorize concisão e legibilidade
2. Use construções idiomáticas da linguagem
3. Elimine código redundante 
4. Limite comentários apenas para explicações não óbvias
5. Utilize no máximo [X] linhas de código

O código deve ser completo e funcional, mas sem verbosidade desnecessária.
```

### 2. Refatoração para concisão

**Template de prompt:**
```
Primeiro, escreva um código funcional para [tarefa].

Em seguida, refatore o código aplicando estas técnicas de simplificação:
1. Remova redundâncias
2. Substitua estruturas verbosas por equivalentes mais concisas
3. Utilize recursos idiomáticos da linguagem 
4. Mantenha apenas variáveis essenciais
5. Simplifique estruturas de controle

Compare as duas versões e explique as melhorias.
```

### 3. Solução one-liner (quando apropriado)

**Template de prompt:**
```
Para a tarefa de [descrição], forneça:

1. Uma implementação em uma única linha de código (one-liner) se possível
2. Uma explicação detalhada de como essa solução concisa funciona
3. Uma avaliação de quando esta abordagem é apropriada versus quando expandir

Use construções idiomáticas de [linguagem] para maximizar concisão sem sacrificar legibilidade.
```

## Técnicas específicas por ferramenta

### Cursor IDE

O Cursor IDE integra modelos de linguagem ao VS Code, oferecendo assistência contextual ao desenvolvedor.

**Práticas recomendadas:**

1. **Arquivos .cursorrules**: Crie arquivos com regras específicas para o projeto que guiam o comportamento do LLM.
   ```
   // Exemplo de .cursorrules
   Você é um especialista em React e TypeScript.
   Siga sempre os princípios SOLID.
   Prefira hooks sobre classes.
   Mantenha o código limpo e bem tipado.
   ```

2. **Modo YOLO com cautela**: Configure adequadamente para verificações automáticas, mas com allow/deny lists para segurança.

3. **Fluxo de trabalho em etapas**: Especialmente eficaz para tarefas complexas:
   ```
   Escreva uma função que converte markdown para HTML
   Primeiro escreva testes, depois o código, execute os testes e atualize o código até os testes passarem
   ```

4. **Uso de Command-K**: Selecione código e use Command-K para modificações específicas, e Command-I para discussões sobre partes selecionadas.

### GitHub Copilot

**Práticas recomendadas:**

1. **Contexto em comentários estruturados**:
   ```javascript
   /**
    * Função para validar endereços de e-mail
    * Requisitos:
    * - Verificar formato user@domain.tld
    * - Rejeitar caracteres especiais inválidos
    * - Retornar booleano
    * - Tratar casos extremos (null, string vazia)
    * 
    * Exemplos:
    * isValidEmail("user@example.com") // true
    * isValidEmail("invalid-email") // false
    */
   ```

2. **Neighboring tabs**: Mantenha arquivos relacionados abertos para que o Copilot entenda melhor o contexto do projeto.

3. **Configurações personalizadas**: Use o arquivo `.github/copilot-instructions.md` para definir regras globais para o projeto.

4. **Participantes de chat**: Em VSCode, utilize os comandos `@workspace` e `@vscode` para especificar o contexto da pergunta.

### Windsurf (anteriormente Codeium)

**Práticas recomendadas:**

1. **@-menções específicas**: Referencie arquivos ou funções específicas:
   ```
   // Ruim
   Refatore rawDataTransform.
   
   // Bom
   Refatore @func:rawDataTransform transformando o while loop em um for loop
   e usando a mesma estrutura de saída de @func:otherDataTransformer
   ```

2. **Verificações em tempo real**: O Cascade (interface do Windsurf) detecta e corrige erros de lint automaticamente.

3. **Uso do sistema de Chat**: Para tarefas complexas que exigem menções a blocos de código específicos, prefira Chat em vez de Command.

### Claude Code (Anthropic)

**Práticas recomendadas:**

1. **Tags XML para estruturação**:
   ```
   <task>
   Criar uma API REST em Python usando FastAPI com as seguintes funcionalidades:
   - Listar usuários
   - Buscar por ID
   - Criar novo usuário
   - Atualizar existente
   - Excluir usuário
   </task>
   
   <context>
   Estou usando Python 3.12 e FastAPI 0.110.0.
   </context>
   ```

2. **Fluxo de "pensar e planejar"**:
   1. Pedir para pesquisar e entender o código
   2. Pedir para planejar uma solução
   3. Pedir para implementar
   4. Pedir para verificar e validar

3. **Comandos personalizados**: Armazene templates em `.claude/commands/` para workflows repetitivos.

4. **Palavras-chave de pensamento estendido**: Termos como "think", "think hard", "ultrathink" dão ao Claude mais tempo para avaliar alternativas.

## Exemplos práticos por situação

### Para projetos complexos (evitar código quebrado)

```
Quero desenvolver um sistema de autenticação seguro usando OAuth2.
Antes de escrever o código:

1. Analise os componentes necessários e suas relações
2. Determine quais estruturas condicionais serão necessárias
3. Identifique potenciais pontos de falha

Após essa análise, implemente o código seguindo estas especificações:
- Entrada: Credenciais do usuário via formulário web
- Saída: Token JWT após autenticação bem-sucedida
- Restrições: Usar apenas bibliotecas padrão e OAuth2
- Tratamento de erros: Mensagens claras e logs detalhados
- NÃO implementar: Cadastro de usuários ou recuperação de senha

Divida a implementação em módulos bem definidos e inclua testes para casos críticos.
```

### Para garantir qualidade (minimizar bugs)

```
Implemente uma função que valida e sanitiza entradas de formulário.

Escreva primeiro os testes unitários para os seguintes casos:
- Entradas válidas de diferentes tipos (texto, email, número)
- Entradas com caracteres especiais potencialmente perigosos
- Entradas nulas ou vazias
- Entradas muito longas ou muito curtas

Depois implemente a função para passar em todos os testes.
Após implementar, simule a execução com cada caso de teste e verifique seu comportamento.
Refine o código para garantir robustez contra todos os casos problemáticos.
```

### Para manter foco (evitar fuga de escopo)

```
Crie uma função que converte valores monetários entre diferentes moedas.

Defina claramente sua interface:
- Nome: currencyConverter
- Parâmetros: amount (número), fromCurrency (string), toCurrency (string)
- Retorno: Objeto com valor convertido e taxa utilizada
- Exceções: Para moedas não suportadas ou valores inválidos

O conversor deve suportar apenas USD, EUR, BRL e JPY.
NÃO implemente: histórico de taxas, interface gráfica, armazenamento.

Decomponha em funções menores com responsabilidade única:
- Função para validar entradas
- Função para obter taxa de conversão
- Função principal que utiliza as anteriores
```

### Para código conciso (evitar verbosidade)

```
Implemente um utilitário para manipulação de strings com estas funções:
- Capitalizar primeira letra de cada palavra
- Remover espaços extras
- Truncar com ellipsis

Siga estas diretrizes:
1. Use recursos idiomáticos de JavaScript (ou sua linguagem)
2. Elimine redundâncias
3. Limite cada função a no máximo 5 linhas
4. Use nomes descritivos e concisos

Após implementar, refatore para maximizar concisão:
- Combine operações quando apropriado
- Use métodos de array funcionais
- Simplifique condicionais com operadores ternários

Compare a versão original e a refatorada.
```

## Conclusão: princípios e práticas emergentes

Após analisar documentações oficiais, artigos técnicos e experiências da comunidade, identificamos padrões comuns que transcendem ferramentas específicas:

1. **Especificidade vence generalidade**: Prompts detalhados e focados produzem resultados superiores comparados a instruções vagas.

2. **Pensamento antes de código**: Solicitar que o LLM raciocine sobre o problema antes de programar reduz significativamente a taxa de erros.

3. **Verificação incorporada**: Integrar validação e testes como parte do prompt melhora a qualidade do código gerado.

4. **Decomposição de problemas**: Dividir tarefas complexas em componentes menores é consistentemente eficaz para todas as ferramentas.

5. **Contexto é rei**: Fornecer contexto adequado, seja através de arquivos relacionados, exemplos ou descrições detalhadas, é crucial para resultados precisos.

A engenharia de prompts para código evolui rapidamente, mas estes princípios fundamentais permanecem constantes. Adaptar as técnicas específicas para cada ferramenta, combinadas com estes princípios gerais, permitirá aos desenvolvedores maximizar o potencial das ferramentas de IA para programação, produzindo código mais robusto, correto, focado e conciso.