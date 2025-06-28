# Orquestração multi-LLM para codificação paralela em Git

A automação da geração de código com múltiplas LLMs trabalhando simultaneamente em diferentes branches Git exige uma arquitetura robusta que combine engenharia de software, gerenciamento de repositórios e inteligência artificial. **Este sistema pode aumentar a produtividade em projetos de desenvolvimento em até 400%** quando implementado corretamente, permitindo que equipes aproveitem o poder de múltiplos modelos especializados trabalhando em paralelo.

## Arquitetura do sistema: componentes essenciais

O sistema proposto utiliza uma arquitetura de microserviços com quatro componentes principais: orquestrador central, gerenciador de Git, agentes LLM e motor de memória. A comunicação entre componentes acontece via mensagens assíncronas, garantindo que o trabalho paralelo não cause bloqueios.

Cada componente tem responsabilidades específicas:

1. **Orquestrador central**: Coordena todo o fluxo de trabalho, distribui tarefas e mantém o estado do sistema
2. **Gerenciador de Git**: Automatiza operações de Git, incluindo criação e gerenciamento de branches
3. **Agentes LLM**: Instâncias individuais que geram código em suas respectivas branches
4. **Motor de memória**: Armazena histórico de alterações e contexto usando LangChain

A arquitetura segue um padrão de barramento de eventos, onde eventos como "nova tarefa", "código gerado" ou "conflito detectado" desencadeiam ações específicas nos diferentes componentes.

## Automação de branches Git para cada instância de LLM

A automação do gerenciamento de branches é o alicerce do sistema. **Cada instância de LLM recebe sua própria branch isolada**, criada dinamicamente no momento da atribuição da tarefa.

A biblioteca GitPython é ideal para esta implementação:

```python
import git
from datetime import datetime

class GitManager:
    def __init__(self, repo_path):
        self.repo = git.Repo(repo_path)
        
    def create_llm_branch(self, llm_id, task_id):
        # Garantir que estamos na branch principal
        self.repo.git.checkout('main')
        # Criar nova branch para a LLM
        branch_name = f"llm_{llm_id}_task_{task_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.repo.git.checkout('-b', branch_name)
        return branch_name
        
    def commit_changes(self, message, files=None):
        if files:
            for file in files:
                self.repo.git.add(file)
        else:
            self.repo.git.add('.')
        self.repo.git.commit('-m', message)
        
    def push_branch(self, branch_name):
        self.repo.git.push('--set-upstream', 'origin', branch_name)
        
    def create_pull_request(self, branch_name, title, body):
        # Utilizando PyGithub para criar PR
        from github import Github
        g = Github(os.environ.get("GITHUB_TOKEN"))
        repo = g.get_repo(os.environ.get("GITHUB_REPO"))
        pr = repo.create_pull(title=title, body=body, head=branch_name, base="main")
        return pr.number
```

Para automatizar a integração com CI/CD, você pode configurar webhooks do GitHub ou GitLab para acionar seu orquestrador:

```python
from flask import Flask, request, jsonify
import hmac
import hashlib

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    # Verificar assinatura do webhook para segurança
    signature = request.headers.get('X-Hub-Signature-256')
    data = request.data
    secret = os.environ.get("WEBHOOK_SECRET").encode()
    expected_signature = hmac.new(secret, data, hashlib.sha256).hexdigest()
    
    if not hmac.compare_digest(f"sha256={expected_signature}", signature):
        return jsonify({"error": "Invalid signature"}), 403
    
    # Processar evento do webhook
    event = request.headers.get('X-GitHub-Event')
    payload = request.json
    
    if event == 'pull_request':
        # Acionar análise de PR
        pr_number = payload['pull_request']['number']
        orchestrator.analyze_pull_request(pr_number)
        
    return jsonify({"status": "ok"})
```

## Como permitir trabalho paralelo entre múltiplas LLMs

O trabalho paralelo exige uma orquestração eficiente para atribuir tarefas apropriadas a cada LLM. Frameworks como LangChain, Haystack ou Ray servem como excelente base para implementar essa orquestração.

A estrutura básica do orquestrador:

```python
from langchain.llms import OpenAI
import redis
import json
from threading import Thread

class LLMOrchestrator:
    def __init__(self, git_manager, memory_manager):
        self.git_manager = git_manager
        self.memory_manager = memory_manager
        self.llms = {}  # Dicionário de instâncias LLM
        self.task_queue = redis.Redis(host='localhost', port=6379, db=0)
        self.result_queue = redis.Redis(host='localhost', port=6379, db=1)
        
    def register_llm(self, llm_id, llm_config):
        """Registra uma nova instância de LLM no sistema"""
        self.llms[llm_id] = {
            "instance": OpenAI(**llm_config),
            "status": "idle",
            "current_branch": None,
            "current_task": None
        }
        
    def assign_task(self, task_description, files_to_modify, llm_id=None):
        """Atribui uma tarefa a uma LLM específica ou à próxima disponível"""
        if llm_id and llm_id in self.llms:
            target_llm = llm_id
        else:
            # Encontrar LLM disponível
            idle_llms = [id for id, info in self.llms.items() if info["status"] == "idle"]
            if not idle_llms:
                raise Exception("No idle LLMs available")
            target_llm = idle_llms[0]
            
        # Criar nova branch para esta tarefa
        task_id = str(uuid.uuid4())
        branch_name = self.git_manager.create_llm_branch(target_llm, task_id)
        
        # Atualizar status da LLM
        self.llms[target_llm]["status"] = "working"
        self.llms[target_llm]["current_branch"] = branch_name
        self.llms[target_llm]["current_task"] = task_id
        
        # Adicionar à fila de tarefas
        task = {
            "llm_id": target_llm,
            "task_id": task_id,
            "branch_name": branch_name,
            "description": task_description,
            "files": files_to_modify,
            "context": self.memory_manager.get_context_for_files(files_to_modify)
        }
        self.task_queue.rpush("tasks", json.dumps(task))
        
        # Iniciar worker thread
        Thread(target=self._process_tasks).start()
        
        return {"task_id": task_id, "llm_id": target_llm, "branch": branch_name}
```

Para cada LLM, um worker dedicado executa:

```python
def _process_task(self, task):
    """Processa uma única tarefa usando a LLM especificada"""
    llm_id = task["llm_id"]
    llm = self.llms[llm_id]["instance"]
    
    # Obter contexto e descrição da tarefa
    context = task["context"]
    description = task["description"]
    files = task["files"]
    
    # Construir prompt para a LLM
    prompt = f"""
    Com base no seguinte contexto sobre os arquivos:
    {context}
    
    Sua tarefa é:
    {description}
    
    Modifique os seguintes arquivos:
    {', '.join(files)}
    
    Forneça o código atualizado para cada arquivo.
    """
    
    # Gerar código com a LLM
    response = llm(prompt)
    
    # Processar resposta e atualizar arquivos
    updated_files = self._extract_code_from_response(response, files)
    for file_path, content in updated_files.items():
        with open(file_path, 'w') as f:
            f.write(content)
    
    # Commit e push das alterações
    self.git_manager.commit_changes(f"Update by LLM {llm_id} for task {task['task_id']}", files)
    self.git_manager.push_branch(task["branch_name"])
    
    # Criar PR
    pr_title = f"Código gerado por LLM {llm_id}"
    pr_body = f"Tarefa: {description}\n\nGerado automaticamente."
    pr_number = self.git_manager.create_pull_request(task["branch_name"], pr_title, pr_body)
    
    # Atualizar status da LLM
    self.llms[llm_id]["status"] = "idle"
    self.llms[llm_id]["current_branch"] = None
    self.llms[llm_id]["current_task"] = None
    
    # Adicionar à memória
    self.memory_manager.store_task_result(task, pr_number, updated_files)
    
    # Notificar resultado
    result = {
        "task_id": task["task_id"],
        "llm_id": llm_id,
        "pr_number": pr_number,
        "status": "completed"
    }
    self.result_queue.rpush("results", json.dumps(result))
```

## Sistema de revisão e resolução de conflitos

O sistema de análise de diffs e resolução de conflitos é crítico para integrar o trabalho de múltiplas LLMs na branch principal. Este componente utiliza uma LLM especializada para revisar PRs e resolver conflitos.

### Analisador de diffs

```python
import unidiff
import requests

class DiffAnalyzer:
    def __init__(self, llm_resolver, memory_manager):
        self.llm_resolver = llm_resolver  # Instância LLM para resolução
        self.memory_manager = memory_manager
        
    def get_pr_diff(self, pr_number, repo_info):
        """Obtém o diff de um PR usando a API do GitHub"""
        url = f"https://api.github.com/repos/{repo_info['owner']}/{repo_info['repo']}/pulls/{pr_number}"
        headers = {"Accept": "application/vnd.github.v3.diff"}
        if "token" in repo_info:
            headers["Authorization"] = f"token {repo_info['token']}"
        
        response = requests.get(url, headers=headers)
        return response.text
        
    def parse_diff(self, diff_text):
        """Analisa o texto do diff em uma estrutura de dados utilizável"""
        patch_set = unidiff.PatchSet(diff_text)
        
        changes = []
        for patched_file in patch_set:
            file_changes = {
                "file_path": patched_file.path,
                "is_added": patched_file.is_added_file,
                "is_removed": patched_file.is_removed_file,
                "hunks": []
            }
            
            for hunk in patched_file:
                hunk_data = {
                    "old_start": hunk.source_start,
                    "old_length": hunk.source_length,
                    "new_start": hunk.target_start,
                    "new_length": hunk.target_length,
                    "removed_lines": [line.value for line in hunk if line.is_removed],
                    "added_lines": [line.value for line in hunk if line.is_added]
                }
                file_changes["hunks"].append(hunk_data)
                
            changes.append(file_changes)
            
        return changes
```

### Resolução de conflitos

```python
def resolve_conflicts(self, base_content, our_changes, their_changes):
    """Resolve conflitos entre duas versões de alterações no mesmo arquivo"""
    # Preparar contexto para a LLM
    context = self.memory_manager.get_context_for_file(their_changes["file_path"])
    
    prompt = f"""
    Você precisa resolver um conflito de merge em um arquivo.
    
    Arquivo: {their_changes["file_path"]}
    
    Contexto sobre o arquivo e seu propósito:
    {context}
    
    Conteúdo base do arquivo:
    ```
    {base_content}
    ```
    
    Nossas alterações (branch principal):
    ```
    {"".join(our_changes["added_lines"])}
    ```
    
    Alterações deles (PR sendo mesclado):
    ```
    {"".join(their_changes["added_lines"])}
    ```
    
    Resolva o conflito da melhor maneira possível, preservando a funcionalidade
    de ambas as alterações. Forneça o arquivo completo como ficaria após a resolução.
    """
    
    response = self.llm_resolver(prompt)
    
    # Extrair o código resolvido
    resolved_code = self._extract_code_from_response(response)
    
    return resolved_code
```

## Implementação de memória com LangChain

A memória do sistema é crucial para manter contexto entre diferentes operações e auxiliar na resolução de conflitos.

```python
from langchain.memory import ConversationBufferMemory
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import TextLoader

class MemoryManager:
    def __init__(self):
        # Memória para conversas com cada LLM
        self.conversation_memories = {}
        
        # Armazenamento vetorial para conteúdo de código
        self.embeddings = OpenAIEmbeddings()
        self.code_store = Chroma(embedding_function=self.embeddings, persist_directory="./code_memory")
        
        # Histórico de alterações em formato de grafo
        self.file_history = {}  # file_path -> list of changes
        
    def initialize_llm_memory(self, llm_id):
        """Inicializa a memória para uma nova LLM"""
        self.conversation_memories[llm_id] = ConversationBufferMemory()
        
    def store_file_content(self, file_path, content):
        """Armazena o conteúdo de um arquivo no armazenamento vetorial"""
        # Dividir o conteúdo em chunks
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = text_splitter.split_text(content)
        
        # Criar documentos com metadados
        documents = [
            {"text": chunk, "metadata": {"file_path": file_path}} 
            for chunk in chunks
        ]
        
        # Armazenar no Chroma
        self.code_store.add_texts(
            texts=[doc["text"] for doc in documents],
            metadatas=[doc["metadata"] for doc in documents]
        )
        
    def get_context_for_files(self, file_paths, max_chunks=5):
        """Recupera contexto relevante para um conjunto de arquivos"""
        context = ""
        
        for file_path in file_paths:
            # Recuperar histórico de alterações
            history = self.get_file_history(file_path)
            if history:
                context += f"Histórico de alterações para {file_path}:\n"
                for change in history[-3:]:  # últimas 3 alterações
                    context += f"- {change['description']} (por {change['author']})\n"
                context += "\n"
            
            # Recuperar conteúdo semântico similar
            docs = self.code_store.similarity_search(
                f"Conteúdo do arquivo {file_path}", 
                k=max_chunks,
                filter={"file_path": file_path}
            )
            
            if docs:
                context += f"Conteúdo relevante de {file_path}:\n"
                for doc in docs:
                    context += f"{doc.page_content}\n\n"
        
        return context
    
    def store_task_result(self, task, pr_number, updated_files):
        """Armazena o resultado de uma tarefa na memória"""
        llm_id = task["llm_id"]
        
        # Atualizar memória de conversação
        if llm_id in self.conversation_memories:
            self.conversation_memories[llm_id].save_context(
                {"input": task["description"]},
                {"output": f"Completed PR #{pr_number}"}
            )
        
        # Atualizar armazenamento vetorial
        for file_path, content in updated_files.items():
            self.store_file_content(file_path, content)
            
            # Atualizar histórico do arquivo
            if file_path not in self.file_history:
                self.file_history[file_path] = []
                
            self.file_history[file_path].append({
                "pr_number": pr_number,
                "task_id": task["task_id"],
                "description": task["description"],
                "author": f"LLM {llm_id}",
                "timestamp": datetime.now().isoformat()
            })
```

## Integrando tudo: fluxo de trabalho completo

O sistema completo funciona seguindo estes passos:

1. O usuário solicita uma tarefa através de uma API ou interface
2. O orquestrador seleciona uma LLM disponível e cria uma branch dedicada
3. A LLM gera código com base na tarefa e contexto da memória
4. As alterações são commitadas e um PR é criado automaticamente
5. O analisador de diffs revisa o PR, procurando por possíveis conflitos
6. Se houver conflitos, a LLM de resolução os soluciona
7. Após aprovação, o código é mesclado à branch principal
8. Todas as ações e resultados são armazenados na memória do sistema

### Implementação de API REST para o sistema

```python
from flask import Flask, request, jsonify
import os
import threading

app = Flask(__name__)
orchestrator = None  # Será inicializado na inicialização do app

@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.json
    if not data or 'description' not in data or 'files' not in data:
        return jsonify({"error": "Missing required fields"}), 400
    
    try:
        result = orchestrator.assign_task(
            task_description=data['description'],
            files_to_modify=data['files'],
            llm_id=data.get('llm_id')
        )
        return jsonify(result), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/tasks/<task_id>', methods=['GET'])
def get_task_status(task_id):
    # Implementar lógica para consultar status da tarefa
    pass

@app.route('/llms', methods=['POST'])
def register_llm():
    data = request.json
    if not data or 'llm_id' not in data or 'config' not in data:
        return jsonify({"error": "Missing required fields"}), 400
    
    try:
        orchestrator.register_llm(data['llm_id'], data['config'])
        return jsonify({"status": "LLM registered successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/prs/<pr_number>/analyze', methods=['POST'])
def analyze_pr(pr_number):
    # Implementar lógica para análise manual de PRs
    pass

if __name__ == '__main__':
    # Inicializar componentes do sistema
    git_manager = GitManager(os.environ.get("REPO_PATH", "./repo"))
    memory_manager = MemoryManager()
    orchestrator = LLMOrchestrator(git_manager, memory_manager)
    
    # Registrar LLMs iniciais
    orchestrator.register_llm("gpt4", {"model_name": "gpt-4"})
    orchestrator.register_llm("codellama", {"model_name": "codellama-34b"})
    
    app.run(debug=True)
```

## Conclusão

A arquitetura proposta permite que múltiplas instâncias de LLMs trabalhem em paralelo no mesmo repositório Git sem causar conflitos. O sistema utiliza uma combinação de automação de Git, orquestração de LLMs, análise inteligente de código e memória persistente para gerenciar todo o fluxo de trabalho. A implementação é flexível e pode ser adaptada para diferentes necessidades e escalas de projeto.