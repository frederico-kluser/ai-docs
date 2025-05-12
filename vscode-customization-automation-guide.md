# Guia Definitivo de Customização e Automação do VSCode

Este guia abrangente mostra como personalizar e automatizar praticamente todos os aspectos do VSCode, permitindo que você transforme o editor de acordo com suas necessidades específicas.

## Índice

1. [Personalização Básica](#personalização-básica)
2. [Comandos Personalizados](#comandos-personalizados)
3. [Automação com Tarefas](#automação-com-tarefas)
4. [Criando Extensões](#criando-extensões)
5. [Modificando a Interface](#modificando-a-interface)
6. [Integração com Ferramentas Externas](#integração-com-ferramentas-externas)
7. [Projetos Avançados](#projetos-avançados)

## Personalização Básica

### Arquivos de Configuração Principais

O VSCode utiliza principalmente três arquivos JSON para personalização:

1. **settings.json**: Configura o comportamento do editor
2. **keybindings.json**: Define atalhos de teclado
3. **tasks.json**: Configura tarefas automatizadas

Para acessar estes arquivos:
- **settings.json**: `Ctrl+,` (ou `Cmd+,` no Mac) e clique no ícone `{}` no canto superior direito
- **keybindings.json**: `Ctrl+K Ctrl+S` (ou `Cmd+K Cmd+S` no Mac) e clique no ícone `{}` no canto superior direito
- **tasks.json**: Deve ser criado em uma pasta `.vscode` na raiz do seu projeto

### Exemplos Práticos de settings.json

```json
{
  "editor.fontFamily": "JetBrains Mono, Fira Code, Consolas, monospace",
  "editor.fontSize": 14,
  "editor.formatOnSave": true,
  "editor.minimap.enabled": false,
  "workbench.colorTheme": "GitHub Dark",
  "workbench.startupEditor": "none",
  "workbench.editor.enablePreview": false,
  "workbench.sideBar.location": "right",
  "terminal.integrated.defaultProfile.windows": "PowerShell",
  "files.autoSave": "afterDelay",
  "files.autoSaveDelay": 1000,
  "explorer.compactFolders": false
}
```

### Modificando Atalhos de Teclado

Para criar atalhos personalizados no keybindings.json:

```json
[
  {
    "key": "ctrl+alt+s",
    "command": "workbench.action.files.saveAll"
  },
  {
    "key": "ctrl+`",
    "command": "workbench.action.terminal.toggleTerminal"
  },
  {
    "key": "alt+z",
    "command": "editor.action.formatDocument"
  },
  {
    "key": "ctrl+shift+r",
    "command": "workbench.action.tasks.runTask",
    "args": "Minha Tarefa Personalizada"
  }
]
```

### Configurações Por Workspace e Por Linguagem

Para configurações específicas por linguagem:

```json
"[javascript]": {
  "editor.tabSize": 2,
  "editor.defaultFormatter": "esbenp.prettier-vscode"
},
"[python]": {
  "editor.tabSize": 4,
  "editor.rulers": [88],
  "editor.defaultFormatter": "ms-python.python"
}
```

Para configurações por workspace, crie um arquivo `.vscode/settings.json` no diretório do projeto.

## Comandos Personalizados

### O Que São Comandos no VSCode?

Os comandos são a espinha dorsal do VSCode - cada ação que você realiza no editor é um comando. Eles são identificados por strings como `workbench.action.files.save` e podem ser:

1. Comandos internos do VSCode
2. Comandos de extensões instaladas
3. Comandos personalizados criados por você

### Como Encontrar Comandos Disponíveis

1. Abra a Paleta de Comandos com `Ctrl+Shift+P` (ou `Cmd+Shift+P` no Mac)
2. Digite `?` para ver categorias de comandos
3. Para ver todos os comandos e seus identificadores: 
   - Execute o comando `Developer: Generate Keyboard Shortcuts From Default`
   - Isso criará um arquivo com todos os comandos e atalhos padrão

### Criando Comandos Personalizados via Extensão

Para criar seus próprios comandos, você precisará desenvolver uma extensão. Vamos ver um exemplo passo a passo:

1. **Instale as ferramentas necessárias**:
   ```bash
   npm install -g yo generator-code
   ```

2. **Crie uma estrutura básica de extensão**:
   ```bash
   yo code
   ```
   Selecione "New Extension (TypeScript)" quando perguntado.

3. **Crie um comando simples** modificando o arquivo `src/extension.ts`:

   ```typescript
   import * as vscode from 'vscode';
   
   export function activate(context: vscode.ExtensionContext) {
     // Comando simples que mostra a data e hora atual
     let disposable = vscode.commands.registerCommand('meuComando.dataHora', () => {
       const dataHora = new Date().toLocaleString();
       vscode.window.showInformationMessage(`Data e hora atual: ${dataHora}`);
     });
     
     context.subscriptions.push(disposable);
     
     // Comando que insere um cabeçalho de comentário
     let headerCmd = vscode.commands.registerCommand('meuComando.inserirCabecalho', () => {
       const editor = vscode.window.activeTextEditor;
       if (editor) {
         const dataHora = new Date().toLocaleString();
         editor.edit(editBuilder => {
           editBuilder.insert(new vscode.Position(0, 0), 
           `/*
            * Arquivo: ${editor.document.fileName.split('/').pop()}
            * Criado em: ${dataHora}
            * Autor: Seu Nome
            * Descrição: 
            */\n\n`);
         });
       }
     });
     
     context.subscriptions.push(headerCmd);
   }
   ```

4. **Registre o comando no `package.json`**:

   ```json
   "contributes": {
     "commands": [
       {
         "command": "meuComando.dataHora",
         "title": "Meu Comando: Mostrar Data e Hora"
       },
       {
         "command": "meuComando.inserirCabecalho",
         "title": "Meu Comando: Inserir Cabeçalho de Arquivo"
       }
     ],
     "keybindings": [
       {
         "command": "meuComando.inserirCabecalho",
         "key": "ctrl+alt+h",
         "when": "editorFocus"
       }
     ]
   }
   ```

5. **Teste a extensão** pressionando F5 no VSCode.

### Comandos Complexos com Argumentos

Você pode criar comandos que aceitam argumentos:

```typescript
// Comando para formatar texto
let formatCmd = vscode.commands.registerCommand('meuComando.formatarTexto', async (options) => {
  // Se não receber opcões, pergunte ao usuário
  if (!options) {
    const formatOption = await vscode.window.showQuickPick(['MAIÚSCULAS', 'minúsculas', 'Capitalizar Palavras'], {
      placeHolder: 'Selecione o tipo de formatação'
    });
    
    if (!formatOption) return; // Usuário cancelou
    
    options = { formatType: formatOption };
  }
  
  const editor = vscode.window.activeTextEditor;
  if (!editor) return;
  
  const selection = editor.selection;
  const text = editor.document.getText(selection);
  
  let newText;
  switch (options.formatType) {
    case 'MAIÚSCULAS':
      newText = text.toUpperCase();
      break;
    case 'minúsculas':
      newText = text.toLowerCase();
      break;
    case 'Capitalizar Palavras':
      newText = text.split(' ')
        .map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
        .join(' ');
      break;
    default:
      newText = text;
  }
  
  editor.edit(editBuilder => {
    editBuilder.replace(selection, newText);
  });
});

context.subscriptions.push(formatCmd);
```

### Executando Comandos Programaticamente

Dentro de suas extensões, você pode executar qualquer comando disponível no VSCode:

```typescript
// Executa formatação de documento
vscode.commands.executeCommand('editor.action.formatDocument');

// Abre um arquivo
const uri = vscode.Uri.file('/caminho/para/arquivo.txt');
vscode.commands.executeCommand('vscode.open', uri);

// Executa uma tarefa específica
vscode.commands.executeCommand('workbench.action.tasks.runTask', 'Tarefa Específica');

// Chama um comando com argumentos e obtém o resultado
const resultado = await vscode.commands.executeCommand('meuComando.formatarTexto', {
  formatType: 'MAIÚSCULAS'
});
```

## Automação com Tarefas

### Configurando Tarefas Básicas

O arquivo `tasks.json` permite automatizar tarefas de compilação, testes e qualquer outro processo em linha de comando:

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Compilar Projeto",
      "type": "shell",
      "command": "gcc",
      "args": ["-g", "main.c", "-o", "main"],
      "group": {
        "kind": "build",
        "isDefault": true
      }
    },
    {
      "label": "Executar Testes",
      "type": "shell",
      "command": "npm",
      "args": ["test"],
      "presentation": {
        "reveal": "always",
        "panel": "new"
      }
    },
    {
      "label": "Limpar Diretório",
      "type": "shell",
      "command": "rm -rf build/* && mkdir -p build",
      "windows": {
        "command": "if exist build rmdir /s /q build && mkdir build"
      }
    }
  ]
}
```

### Tarefas com Dependências

Você pode criar tarefas que dependem de outras:

```json
{
  "label": "Build e Deploy",
  "dependsOn": ["Compilar Projeto", "Executar Testes"],
  "dependsOrder": "sequence"
}
```

### Tarefas de Background

Crie tarefas que executam continuamente em segundo plano:

```json
{
  "label": "Servidor de Desenvolvimento",
  "type": "shell",
  "command": "npm run dev",
  "isBackground": true,
  "problemMatcher": {
    "owner": "custom",
    "pattern": {
      "regexp": "^.*Error.*$",
      "file": 1,
      "location": 2,
      "message": 3
    },
    "background": {
      "activeOnStart": true,
      "beginsPattern": "Starting development server",
      "endsPattern": "Development server started"
    }
  }
}
```

### Automatização Avançada com Scripts Externos

Você pode chamar scripts externos em suas tarefas para automações mais complexas:

```json
{
  "label": "Deploy Completo",
  "type": "shell",
  "command": "${workspaceFolder}/scripts/deploy.sh",
  "args": ["--env", "production"],
  "windows": {
    "command": "${workspaceFolder}\\scripts\\deploy.bat",
    "args": ["--env", "production"]
  }
}
```

## Criando Extensões

### Estrutura Básica de uma Extensão

Uma extensão do VSCode possui a seguinte estrutura de arquivos:

```
minha-extensao/
  ├── .vscode/            # Configurações para depuração da extensão
  ├── src/
  │   └── extension.ts    # Código principal da extensão
  ├── package.json        # Manifesto da extensão
  ├── tsconfig.json       # Configuração do TypeScript
  └── README.md           # Documentação
```

### Exemplo de uma Extensão Completa

Vamos criar uma extensão que adiciona funcionalidades para trabalhar com arquivos markdown:

```typescript
// src/extension.ts
import * as vscode from 'vscode';
import * as path from 'path';
import * as fs from 'fs';

export function activate(context: vscode.ExtensionContext) {
  
  // Comando para inserir um título de seção
  let insertSectionCmd = vscode.commands.registerCommand('markdownHelper.insertSection', async () => {
    const editor = vscode.window.activeTextEditor;
    if (!editor) return;
    
    const sectionTitle = await vscode.window.showInputBox({
      prompt: 'Digite o título da seção'
    });
    
    if (!sectionTitle) return;
    
    // Gera o título em markdown e o id de âncora
    const anchor = sectionTitle.toLowerCase().replace(/\s+/g, '-').replace(/[^\w-]/g, '');
    const markdownHeader = `\n\n## ${sectionTitle} {#${anchor}}\n\n`;
    
    editor.edit(editBuilder => {
      editBuilder.insert(editor.selection.active, markdownHeader);
    });
  });
  
  // Comando para gerar sumário
  let generateTocCmd = vscode.commands.registerCommand('markdownHelper.generateToc', () => {
    const editor = vscode.window.activeTextEditor;
    if (!editor || editor.document.languageId !== 'markdown') return;
    
    const text = editor.document.getText();
    let toc = "# Sumário\n\n";
    
    // Expressão regular para encontrar cabeçalhos markdown
    const headerRegex = /^(#{2,4})\s+(.+?)(?:\s+\{#([a-z0-9-]+)\})?$/gm;
    let match;
    
    while ((match = headerRegex.exec(text)) !== null) {
      const level = match[1].length - 1; // Número de # menos 1
      const title = match[2];
      const anchor = match[3] || title.toLowerCase().replace(/\s+/g, '-').replace(/[^\w-]/g, '');
      
      // Adiciona indentação baseada no nível
      const indent = '  '.repeat(level - 1);
      toc += `${indent}- [${title}](#${anchor})\n`;
    }
    
    toc += "\n---\n\n";
    
    // Insere o sumário no início do documento
    editor.edit(editBuilder => {
      editBuilder.insert(new vscode.Position(0, 0), toc);
    });
  });
  
  // Comando para exportar para HTML
  let exportHtmlCmd = vscode.commands.registerCommand('markdownHelper.exportHtml', async () => {
    const editor = vscode.window.activeTextEditor;
    if (!editor || editor.document.languageId !== 'markdown') return;
    
    const markdown = editor.document.getText();
    
    // Aqui você usaria uma biblioteca como marked ou markdown-it para converter
    // para HTML. Para este exemplo, vamos simular o resultado:
    const html = `<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Documento Exportado</title>
  <style>
    body { font-family: system-ui, -apple-system, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
    code { background-color: #f0f0f0; padding: 2px 4px; border-radius: 3px; }
    pre { background-color: #f5f5f5; padding: 10px; border-radius: 5px; overflow-x: auto; }
  </style>
</head>
<body>
  <!-- Aqui entraria o HTML convertido do markdown -->
  ${markdown.replace(/\n/g, '<br>')}
</body>
</html>`;
    
    // Obtém o caminho do documento atual
    const currentFile = editor.document.fileName;
    const htmlFile = currentFile.replace(/\.md$/i, '.html');
    
    // Escreve o arquivo HTML
    fs.writeFileSync(htmlFile, html);
    
    vscode.window.showInformationMessage(`Documento exportado para ${path.basename(htmlFile)}`);
  });
  
  context.subscriptions.push(insertSectionCmd, generateTocCmd, exportHtmlCmd);
  
  // Cria um painel de visualização personalizado
  let previewCmd = vscode.commands.registerCommand('markdownHelper.openPreview', () => {
    const editor = vscode.window.activeTextEditor;
    if (!editor || editor.document.languageId !== 'markdown') return;
    
    // Cria um webview panel
    const panel = vscode.window.createWebviewPanel(
      'markdownPreview',
      'Visualização Personalizada',
      vscode.ViewColumn.Beside,
      {
        enableScripts: true,
        retainContextWhenHidden: true
      }
    );
    
    // Função para atualizar o conteúdo
    function updateContent() {
      if (editor) {
        const markdown = editor.document.getText();
        // Aqui você converteria markdown para HTML
        panel.webview.html = `<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <style>
    body { font-family: system-ui, -apple-system, sans-serif; padding: 20px; }
  </style>
</head>
<body>
  <div id="content">
    ${markdown.replace(/\n/g, '<br>')}
  </div>
</body>
</html>`;
      }
    }
    
    // Atualiza o conteúdo inicialmente
    updateContent();
    
    // Registra para eventos de mudança no documento
    const changeDocumentSubscription = vscode.workspace.onDidChangeTextDocument(e => {
      if (e.document.uri.toString() === editor.document.uri.toString()) {
        updateContent();
      }
    });
    
    // Limpa quando o painel for fechado
    panel.onDidDispose(() => {
      changeDocumentSubscription.dispose();
    });
  });
  
  context.subscriptions.push(previewCmd);
}
```

### Definindo o Manifesto da Extensão

O arquivo `package.json` é crucial para definir as capacidades da sua extensão:

```json
{
  "name": "markdown-helper",
  "displayName": "Assistente Markdown",
  "description": "Ferramentas avançadas para trabalhar com Markdown",
  "version": "1.0.0",
  "engines": {
    "vscode": "^1.60.0"
  },
  "categories": [
    "Other"
  ],
  "activationEvents": [
    "onLanguage:markdown"
  ],
  "main": "./out/extension.js",
  "contributes": {
    "commands": [
      {
        "command": "markdownHelper.insertSection",
        "title": "Markdown: Inserir Seção"
      },
      {
        "command": "markdownHelper.generateToc",
        "title": "Markdown: Gerar Sumário"
      },
      {
        "command": "markdownHelper.exportHtml",
        "title": "Markdown: Exportar para HTML"
      },
      {
        "command": "markdownHelper.openPreview",
        "title": "Markdown: Abrir Visualização Personalizada"
      }
    ],
    "menus": {
      "editor/context": [
        {
          "when": "editorLangId == markdown",
          "command": "markdownHelper.insertSection",
          "group": "markdownHelper"
        },
        {
          "when": "editorLangId == markdown",
          "command": "markdownHelper.generateToc",
          "group": "markdownHelper"
        },
        {
          "when": "editorLangId == markdown",
          "command": "markdownHelper.exportHtml",
          "group": "markdownHelper"
        }
      ]
    },
    "keybindings": [
      {
        "command": "markdownHelper.insertSection",
        "key": "ctrl+alt+s",
        "mac": "cmd+alt+s",
        "when": "editorLangId == markdown"
      },
      {
        "command": "markdownHelper.generateToc",
        "key": "ctrl+alt+t",
        "mac": "cmd+alt+t",
        "when": "editorLangId == markdown"
      }
    ],
    "configuration": {
      "title": "Assistente Markdown",
      "properties": {
        "markdownHelper.defaultHeaderLevel": {
          "type": "number",
          "default": 2,
          "description": "Nível padrão de cabeçalho ao inserir seções"
        },
        "markdownHelper.includeIntroduction": {
          "type": "boolean",
          "default": true,
          "description": "Incluir uma seção de introdução ao gerar sumário"
        }
      }
    }
  },
  "scripts": {
    "vscode:prepublish": "npm run compile",
    "compile": "tsc -p ./",
    "watch": "tsc -watch -p ./",
    "pretest": "npm run compile && npm run lint",
    "lint": "eslint src --ext ts",
    "test": "node ./out/test/runTest.js"
  },
  "devDependencies": {
    "@types/vscode": "^1.60.0",
    "@types/node": "16.x",
    "@typescript-eslint/eslint-plugin": "^5.30.0",
    "@typescript-eslint/parser": "^5.30.0",
    "eslint": "^8.13.0",
    "typescript": "^4.7.2"
  }
}
```

### Desenvolvendo a Extensão

1. **Inicie com o teste local**:
   - Pressione F5 no VSCode para abrir uma nova janela com a extensão ativada
   - Teste seus comandos através da paleta de comandos ou atalhos
   
2. **Depure problemas**:
   - Use os console.log que aparecerão no console de depuração
   - Defina pontos de interrupção no código

3. **Publique sua extensão**:
   - Instale a ferramenta VSCE:
     ```bash
     npm install -g vsce
     ```
   - Crie um pacote:
     ```bash
     vsce package
     ```
   - Este comando gerará um arquivo .vsix que pode ser instalado ou publicado

## Modificando a Interface

### Temas Personalizados

Crie seu próprio tema de cores modificando o settings.json:

```json
"workbench.colorCustomizations": {
  "editor.background": "#1E1E1E",
  "editor.foreground": "#D4D4D4",
  "titleBar.activeBackground": "#3C3C3C",
  "activityBar.background": "#333333",
  "sideBar.background": "#252526",
  "statusBar.background": "#007ACC",
  "statusBar.foreground": "#FFFFFF"
}
```

Para criar um tema completo, desenvolva uma extensão de tema.

### Ícones Personalizados

Para modificar ícones de arquivos e pastas:

```json
"workbench.iconTheme": "material-icon-theme",
"material-icon-theme.folders.associations": {
  "infra": "app",
  "entities": "class",
  "schemas": "database",
  "typeorm": "database",
  "repositories": "mappings",
  "implementations": "core",
  "dtos": "typescript",
  "fakes": "mock",
  "websockets": "pipe",
  "protos": "pipe",
  "grpc": "pipe"
},
"material-icon-theme.files.associations": {
  "*.service.ts": "nest-service",
  "*.repository.ts": "database",
  "*.controller.ts": "nest-controller"
}
```

### Snippets Personalizados

Crie snippets no arquivo `~/.config/Code/User/snippets/javascript.json` (Linux/Mac) ou `%APPDATA%\Code\User\snippets\javascript.json` (Windows):

```json
{
  "Console Log": {
    "prefix": "cl",
    "body": [
      "console.log('$1:', $1);"
    ],
    "description": "Log output to console"
  },
  "React Component": {
    "prefix": "rfc",
    "body": [
      "import React from 'react';",
      "",
      "function ${1:ComponentName}(${2:props}) {",
      "  return (",
      "    <div>",
      "      $0",
      "    </div>",
      "  );",
      "}",
      "",
      "export default $1;"
    ],
    "description": "React Functional Component"
  },
  "Try Catch": {
    "prefix": "tc",
    "body": [
      "try {",
      "  $1",
      "} catch (error) {",
      "  console.error('Erro:', error);",
      "  $2",
      "}"
    ],
    "description": "Try-catch block"
  }
}
```

### Layout Personalizado

Modifique o layout do VSCode com estas configurações:

```json
"workbench.editor.showTabs": true,
"workbench.editor.enablePreview": false,
"workbench.sideBar.location": "right",
"workbench.activityBar.visible": true,
"workbench.statusBar.visible": true,
"editor.minimap.enabled": false,
"workbench.editor.tabSizing": "shrink",
"window.zoomLevel": 1
```

## Integração com Ferramentas Externas

### Integrando com Git e Controle de Versão

Configure o Git no VSCode:

```json
"git.enableSmartCommit": true,
"git.confirmSync": false,
"git.autofetch": true,
"git.fetchOnPull": true,
"diffEditor.ignoreTrimWhitespace": false,
"editor.formatOnSave": true,
"editor.formatOnSaveMode": "file"
```

Para criar comandos personalizados de Git:

```typescript
let gitBlameCmd = vscode.commands.registerCommand('meuGit.blame', async () => {
  const editor = vscode.window.activeTextEditor;
  if (!editor) return;
  
  const filePath = editor.document.uri.fsPath;
  const lineNumber = editor.selection.active.line + 1;
  
  // Execute git blame para a linha atual
  const terminal = vscode.window.createTerminal('Git Blame');
  terminal.show();
  terminal.sendText(`git blame -L ${lineNumber},${lineNumber} ${filePath}`);
});

context.subscriptions.push(gitBlameCmd);
```

### Executando Ferramentas de Linha de Comando

Crie uma extensão que integra com o Docker:

```typescript
let dockerStatusCmd = vscode.commands.registerCommand('docker.status', async () => {
  // Cria um terminal para executar comandos Docker
  const terminal = vscode.window.createTerminal('Docker Status');
  terminal.show();
  terminal.sendText('docker ps');
});

// Comando para iniciar um contêiner
let dockerStartCmd = vscode.commands.registerCommand('docker.start', async () => {
  // Obter a lista de containers Docker
  const result = await executeCommand('docker ps -a --format "{{.Names}}"');
  const containers = result.stdout.trim().split('\n');
  
  // Mostrar a lista para seleção
  const selectedContainer = await vscode.window.showQuickPick(containers, {
    placeHolder: 'Selecione um contêiner para iniciar'
  });
  
  if (selectedContainer) {
    const terminal = vscode.window.createTerminal('Docker');
    terminal.show();
    terminal.sendText(`docker start ${selectedContainer}`);
  }
});

// Função auxiliar para executar comandos e obter saída
function executeCommand(command) {
  return new Promise((resolve, reject) => {
    const cp = require('child_process');
    cp.exec(command, (error, stdout, stderr) => {
      if (error) {
        reject({ error, stderr });
      } else {
        resolve({ stdout, stderr });
      }
    });
  });
}

context.subscriptions.push(dockerStatusCmd, dockerStartCmd);
```

### Automação Usando APIs Externas

Crie uma extensão que integra com APIs REST:

```typescript
let checkWeatherCmd = vscode.commands.registerCommand('ferramentas.verificarClima', async () => {
  const cidade = await vscode.window.showInputBox({
    prompt: 'Digite a cidade para verificar o clima'
  });
  
  if (!cidade) return;
  
  // Mostrar status de carregamento
  const statusBarItem = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left);
  statusBarItem.text = `$(sync~spin) Consultando clima para ${cidade}...`;
  statusBarItem.show();
  
  try {
    // Usando node-fetch (você precisaria adicionar como dependência)
    const fetch = require('node-fetch');
    const response = await fetch(`https://api.openweathermap.org/data/2.5/weather?q=${cidade}&appid=SUA_API_KEY&units=metric`);
    const data = await response.json();
    
    if (data.cod === 200) {
      const temp = data.main.temp;
      const descricao = data.weather[0].description;
      
      vscode.window.showInformationMessage(`Clima em ${cidade}: ${temp}°C, ${descricao}`);
    } else {
      vscode.window.showErrorMessage(`Não foi possível obter o clima para ${cidade}: ${data.message}`);
    }
  } catch (error) {
    vscode.window.showErrorMessage(`Erro ao consultar API: ${error.message}`);
  } finally {
    statusBarItem.dispose();
  }
});

context.subscriptions.push(checkWeatherCmd);
```

## Projetos Avançados

### Assistente de Código Inteligente

Crie uma extensão que sugere melhorias no código:

```typescript
let suggestImprovementCmd = vscode.commands.registerCommand('codeAssistant.suggestImprovement', async () => {
  const editor = vscode.window.activeTextEditor;
  if (!editor) return;
  
  const selection = editor.selection;
  const text = editor.document.getText(selection);
  
  if (!text) {
    vscode.window.showInformationMessage('Por favor, selecione algum código para analisar.');
    return;
  }
  
  // Analise o código (este é um exemplo simples)
  const improvements = [];
  
  // Verifica variáveis não utilizadas (exemplo simples)
  const varDeclaration = /let|var|const\s+(\w+)\s*=/g;
  const declaredVars = [];
  let match;
  
  while ((match = varDeclaration.exec(text)) !== null) {
    declaredVars.push(match[1]);
  }
  
  // Verifica uso das variáveis
  for (const varName of declaredVars) {
    const regex = new RegExp(`\\b${varName}\\b`, 'g');
    // Conta ocorrências (menos a declaração)
    let count = 0;
    while (regex.exec(text) !== null) count++;
    
    if (count <= 1) {
      improvements.push(`A variável "${varName}" parece não ser utilizada.`);
    }
  }
  
  // Sugestões de estilo
  if (text.includes('==') && !text.includes('===')) {
    improvements.push('Considere usar === ao invés de == para comparações mais seguras.');
  }
  
  if (text.includes('var ')) {
    improvements.push('Considere usar let ou const ao invés de var para melhor escopo de variáveis.');
  }
  
  // Mostra resultados
  if (improvements.length > 0) {
    const panel = vscode.window.createWebviewPanel(
      'codeImprovement',
      'Sugestões de Melhorias',
      vscode.ViewColumn.Beside,
      {}
    );
    
    panel.webview.html = `
      <!DOCTYPE html>
      <html>
        <head>
          <style>
            body { font-family: system-ui, -apple-system, sans-serif; padding: 20px; }
            .improvement { margin-bottom: 15px; padding: 10px; background: #f0f0f0; border-left: 4px solid #007acc; }
          </style>
        </head>
        <body>
          <h2>Sugestões de Melhorias</h2>
          ${improvements.map(imp => `<div class="improvement">${imp}</div>`).join('')}
        </body>
      </html>
    `;
  } else {
    vscode.window.showInformationMessage('Não foram encontradas sugestões de melhoria.');
  }
});

context.subscriptions.push(suggestImprovementCmd);
```

### Sincronização com Serviços em Nuvem

Crie uma extensão que sincroniza com um serviço em nuvem:

```typescript
// Simplificado para ilustração
let syncCloudCmd = vscode.commands.registerCommand('cloud.sync', async () => {
  const workspacePath = vscode.workspace.rootPath;
  if (!workspacePath) {
    vscode.window.showErrorMessage('Nenhum workspace aberto para sincronizar.');
    return;
  }
  
  // Mostrar progresso
  vscode.window.withProgress({
    location: vscode.ProgressLocation.Notification,
    title: "Sincronizando com a nuvem",
    cancellable: true
  }, async (progress, token) => {
    progress.report({ increment: 0 });
    
    // Simula autenticação
    progress.report({ increment: 10, message: "Autenticando..." });
    await delay(1000);
    
    // Simula upload
    progress.report({ increment: 30, message: "Enviando arquivos..." });
    await delay(2000);
    
    // Simula conclusão
    progress.report({ increment: 60, message: "Finalizando..." });
    await delay(1000);
    
    vscode.window.showInformationMessage('Sincronização concluída com sucesso!');
    return true;
  });
});

function delay(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

context.subscriptions.push(syncCloudCmd);
```

### Sistema de Gerenciamento de Projetos

Crie uma extensão mais complexa com armazenamento de dados:

```typescript
// Implementação simplificada - um sistema real seria mais complexo
class TaskManager {
  private context: vscode.ExtensionContext;
  private tasks: any[] = [];
  
  constructor(context: vscode.ExtensionContext) {
    this.context = context;
    this.loadTasks();
  }
  
  private loadTasks() {
    this.tasks = this.context.globalState.get('projectTasks', []);
  }
  
  private saveTasks() {
    this.context.globalState.update('projectTasks', this.tasks);
  }
  
  public async addTask() {
    const taskName = await vscode.window.showInputBox({
      prompt: 'Digite o nome da tarefa'
    });
    
    if (!taskName) return;
    
    const priority = await vscode.window.showQuickPick(['Alta', 'Média', 'Baixa'], {
      placeHolder: 'Selecione a prioridade'
    });
    
    this.tasks.push({
      id: Date.now(),
      name: taskName,
      priority: priority || 'Média',
      completed: false,
      created: new Date().toISOString()
    });
    
    this.saveTasks();
    this.showTaskList();
  }
  
  public async completeTask() {
    if (this.tasks.length === 0) {
      vscode.window.showInformationMessage('Não há tarefas para concluir.');
      return;
    }
    
    const taskItems = this.tasks
      .filter(t => !t.completed)
      .map(t => ({
        label: t.name,
        description: t.priority,
        task: t
      }));
    
    if (taskItems.length === 0) {
      vscode.window.showInformationMessage('Todas as tarefas já foram concluídas.');
      return;
    }
    
    const selectedItem = await vscode.window.showQuickPick(taskItems, {
      placeHolder: 'Selecione a tarefa para concluir'
    });
    
    if (selectedItem) {
      const task = this.tasks.find(t => t.id === selectedItem.task.id);
      if (task) {
        task.completed = true;
        task.completedAt = new Date().toISOString();
        this.saveTasks();
        this.showTaskList();
      }
    }
  }
  
  public showTaskList() {
    const panel = vscode.window.createWebviewPanel(
      'taskList',
      'Gerenciador de Tarefas',
      vscode.ViewColumn.One,
      {}
    );
    
    const pendingTasks = this.tasks.filter(t => !t.completed);
    const completedTasks = this.tasks.filter(t => t.completed);
    
    panel.webview.html = `
      <!DOCTYPE html>
      <html>
        <head>
          <style>
            body { font-family: system-ui, -apple-system, sans-serif; padding: 20px; }
            .task { margin-bottom: 10px; padding: 10px; border-radius: 4px; }
            .task.high { background-color: #ffe0e0; }
            .task.medium { background-color: #e0f0ff; }
            .task.low { background-color: #e0ffe0; }
            .completed { text-decoration: line-through; opacity: 0.7; }
          </style>
        </head>
        <body>
          <h2>Tarefas Pendentes (${pendingTasks.length})</h2>
          ${pendingTasks.map(t => `
            <div class="task ${t.priority.toLowerCase()}">
              <strong>${t.name}</strong> - ${t.priority}
              <div><small>Criada em: ${new Date(t.created).toLocaleString()}</small></div>
            </div>
          `).join('') || '<p>Não há tarefas pendentes.</p>'}
          
          <h2>Tarefas Concluídas (${completedTasks.length})</h2>
          ${completedTasks.map(t => `
            <div class="task ${t.priority.toLowerCase()} completed">
              <strong>${t.name}</strong> - ${t.priority}
              <div><small>Concluída em: ${new Date(t.completedAt).toLocaleString()}</small></div>
            </div>
          `).join('') || '<p>Não há tarefas concluídas.</p>'}
        </body>
      </html>
    `;
  }
}

// No método activate
export function activate(context: vscode.ExtensionContext) {
  const taskManager = new TaskManager(context);
  
  let addTaskCmd = vscode.commands.registerCommand('projectManager.addTask', () => {
    taskManager.addTask();
  });
  
  let completeTaskCmd = vscode.commands.registerCommand('projectManager.completeTask', () => {
    taskManager.completeTask();
  });
  
  let showTasksCmd = vscode.commands.registerCommand('projectManager.showTasks', () => {
    taskManager.showTaskList();
  });
  
  context.subscriptions.push(addTaskCmd, completeTaskCmd, showTasksCmd);
}
```

## O Que É Possível vs. O Que Não É Possível

### O Que É Possível Fazer no VSCode

1. **Personalização da Interface**:
   - Modificar completamente cores, temas e ícones
   - Reorganizar painéis, barras laterais e editores
   - Ocultar ou mostrar elementos específicos da interface
   - Personalizar fontes, tamanhos e espacamentos

2. **Automação de Tarefas**:
   - Criar tarefas para compilação, testes e implantação
   - Configurar tarefas em execução contínua (watch)
   - Encadear múltiplas tarefas em sequência
   - Executar scripts externos (bash, PowerShell, etc.)

3. **Extensões e Comandos**:
   - Criar comandos personalizados com funcionalidades específicas
   - Estender o editor com novas funcionalidades via API
   - Adicionar novos painéis, visualizações e menus contextuais
   - Integrar com ferramentas e serviços externos

4. **Editores Personalizados**:
   - Criar editores personalizados para tipos de arquivo específicos
   - Implementar visualizações personalizadas (webviews)
   - Criar validadores e formatadores de código
   - Adicionar diagnósticos e realce de sintaxe personalizados

5. **Automação via Extensões**:
   - Processar e modificar arquivos programaticamente
   - Integrar com APIs externas e serviços web
   - Automatizar fluxos de trabalho completos
   - Comunicar-se com outras ferramentas de desenvolvimento

### O Que Não É Possível Fazer no VSCode

1. **Limitações da Interface**:
   - Não é possível modificar o DOM da interface diretamente para personalização
   - Não é possível alterar a estrutura básica da janela do VSCode
   - Não é possível substituir componentes internos centrais do VSCode
   - Não é possível injetar CSS diretamente na interface (apenas via extensões específicas)

2. **Limitações de Performance**:
   - Não é possível acessar diretamente o processo principal do VSCode
   - Não é possível contornar o sandbox de extensões para operações não seguras
   - Não é possível executar tarefas de CPU intensivas no thread principal
   - Extensões lentas podem impactar negativamente a performance do editor

3. **Limitações de Extensões**:
   - Não é possível substituir ou modificar comandos internos do VSCode
   - Não é possível ter comportamentos que violem as diretrizes de UX do VSCode
   - Não é possível compartilhar estado diretamente entre extensões diferentes
   - Extensões não podem acessar dados de outras extensões sem APIs específicas

4. **Limitações de Segurança**:
   - Não é possível executar código arbitrário no contexto do VSCode sem permissão
   - Não é possível acessar o sistema de arquivos fora dos escopos permitidos
   - Não é possível contornar as políticas de segurança do VSCode
   - Não é possível ler ou modificar configurações críticas do editor

5. **Limitações de API**:
   - Nem todas as funcionalidades internas do VSCode são expostas na API
   - Alguns recursos podem estar disponíveis apenas em versões de Insider
   - APIs propostas podem mudar ou serem removidas antes de se tornarem estáveis
   - Algumas APIs têm limitações no ambiente web do VSCode vs. versão desktop

## Dicas e Truques

1. **Combinando Múltiplas Personalizações**:
   - Use a extensão "Settings Sync" para manter suas configurações sincronizadas entre máquinas
   - Crie diferentes perfis para diferentes tipos de trabalho

2. **Otimizando o Desempenho**:
   - Desative extensões que você não usa com frequência
   - Use a configuração `"editor.largeFileOptimizations": true`
   - Ajuste `"files.watcherExclude"` para ignorar pastas grandes como `node_modules`

3. **Melhores Práticas para Extensões**:
   - Mantenha suas extensões pequenas e focadas
   - Use o sistema de eventos do VSCode para evitar processamento desnecessário
   - Teste extensivamente com diferentes tipos de arquivos e configurações

4. **Compartilhando suas Customizações**:
   - Publique suas extensões no Marketplace do VSCode
   - Compartilhe snippets e configurações com sua equipe
   - Crie repositórios no GitHub para suas configurações

---

Este guia apresenta apenas uma fração do que é possível fazer para personalizar e automatizar o VSCode. Quanto mais você explorar, mais possibilidades descobrirá para tornar o editor perfeito para seu fluxo de trabalho.