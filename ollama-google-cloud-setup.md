# Modelos Falcon-180B (sem censura) e LLaMA 4 no Google Cloud (GPU A100)

Para executar modelos LLM tão grandes como o Falcon-180B ou LLaMA 4 com baixa latência, recomenda-se usar instâncias **A2 Ultra** no Compute Engine, que oferecem GPUs NVIDIA A100 de 80 GB. Por exemplo, o tipo de máquina `a2-ultragpu-2g` dispõe de **2 GPUs A100-80GB**, 24 vCPUs e 340 GB de RAM. Essas VMs vêm com SSD local incluso (750 GB no caso do `2g`) e devem ser criadas em zonas que suportem A100, como `us-central1-c` (Iowa) ou `us-east4-c` (Virgínia). Por exemplo:

```sh
gcloud compute instances create vm-falcon-180b \
  --machine-type=a2-ultragpu-2g \
  --accelerator=type=nvidia-a100-80gb,count=2 \
  --image-family=ubuntu-22-04 --image-project=ubuntu-os-cloud \
  --maintenance-policy=TERMINATE \
  --zone=us-central1-c \
  --boot-disk-size=1000GB
```

Use um disco de boot grande (≥ 40 GB) para instalar drivers e modelos. Para **LLaMA 4 Scout** (109B, 17B ativos), que requer \~96 GB de RAM em quantização 4-bit, bastaria uma VM `a2-ultragpu-1g` (1 GPU A100-80GB, 170 GB RAM) ou `a2-ultragpu-2g` para performance extra. Por exemplo:

```sh
gcloud compute instances create vm-llama4 \
  --machine-type=a2-ultragpu-1g \
  --accelerator=type=nvidia-a100-80gb,count=1 \
  --image-family=ubuntu-22-04 --image-project=ubuntu-os-cloud \
  --maintenance-policy=TERMINATE \
  --zone=us-central1-c \
  --boot-disk-size=500GB
```

## Configurando o Ubuntu e drivers

Após criar a VM, conecte-se via SSH e atualize o sistema:

```sh
sudo apt-get update && sudo apt-get upgrade -y
```

Instale os drivers NVIDIA para acessar a GPU. Por exemplo, para Ubuntu 22.04:

```sh
sudo apt-get install -y nvidia-driver-535
```

Isso instalará o NVIDIA CUDA Toolkit e o driver compatível. Reinicie a VM e verifique com `nvidia-smi` que a GPU A100 foi reconhecida. Instale também ferramentas úteis:

```sh
sudo apt-get install -y build-essential git python3-pip
```

## Instalando e configurando o Ollama

O **Ollama** fornece uma interface CLI para rodar modelos locais. Instale-o com o comando único oficial:

```sh
curl -fsSL https://ollama.com/install.sh | sh
```

Isso baixa o binário e configura o ambiente. Depois, confirme a instalação:

```sh
ollama version
```

e inicie o daemon (`ollama daemon`) se necessário. Você pode listar modelos disponíveis via `ollama list` e consultar `ollama help` para comandos.

## Baixando e executando os modelos no Ollama

Com o Ollama instalado, faça o **download** do Falcon-180B e do LLaMA 4 (Scout) usando o comando `ollama pull`. Por exemplo:

```sh
ollama pull falcon:180b
ollama pull llama4:scout
```

Isso baixa as versões quantizadas dos modelos da biblioteca oficial. Observe que o Falcon-180B requer \~192 GB de memória total, portanto o ambiente multi-GPU é necessário. Para **rodar** o modelo em modo chat/completion, use:

```sh
ollama run falcon:180b "Olá! Como você pode me ajudar hoje?"
ollama run llama4:scout
```

No segundo caso, você entrará em um prompt interativo do LLaMA 4 (Scount). O Ollama cuida de distribuir as cargas na GPU. (Você também pode usar `ollama run llama4:maverick` se quiser testar a versão maior, mas ela é muito pesada.)

## Interface Web (Open WebUI) *opcional*

Para uma interface de chat amigável, você pode instalar o **Open WebUI** com suporte integrado ao Ollama via Docker. Primeiro, instale o Docker:

```sh
sudo apt-get install -y docker.io
sudo usermod -aG docker $USER
```

Em seguida, rode o container oficial com Ollama embutido:

```sh
docker run -d -p 3000:8080 --gpus=all \
  -v ollama:/root/.ollama \
  -v open-webui:/app/backend/data \
  --name open-webui --restart always \
  ghcr.io/open-webui/open-webui:ollama
```

Isso publica a interface web na porta 3000. Em seguida, abra o firewall da GCP para permitir acesso externo (por exemplo, `gcloud compute firewall-rules create open-webui --allow tcp:3000`). Acesse `http://<EXTERNAL_IP>:3000` no navegador para conversar com o modelo pelo WebUI.

## Integração com LangChain para RAG (Python)

Para implementar RAG (Retrieval-Augmented Generation), você pode usar a biblioteca LangChain com o Ollama como provedor LLM. Exemplo mínimo em Python:

```python
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_chroma import Chroma
from langchain.chains import RetrievalQA

# Carrega embeddings de texto (via Ollama Embeddings)
embeddings = OllamaEmbeddings(model="nomic-embed-text")
# Suponha que 'documents' seja uma lista de strings/documentos para indexar
vectorstore = Chroma.from_documents(documents, embedding=embeddings)

# Carrega o modelo Falcon-180B (pode usar 'llama4:scout' analogamente)
model = ChatOllama(model="falcon:180b", temperature=0)

# Cria chain RAG de recuperação + resposta
qa_chain = RetrievalQA.from_chain_type(llm=model, chain_type="stuff", retriever=vectorstore.as_retriever())
resposta = qa_chain.run("Quem descobriu o Brasil?")
print(resposta)
```

Nesse código, usamos `OllamaEmbeddings` para converter textos em vetores e `ChatOllama` para gerar respostas. O LangChain cuidará da passagem do prompt ao Ollama e agregação da resposta.

## Boas práticas de segurança e uso de recursos

* **Firewall e acessos**: abra apenas as portas necessárias (SSH e, opcionalmente, porta do WebUI). Use chaves SSH seguras e evite senhas simples.
* **Atualizações**: mantenha o Ubuntu e drivers atualizados (`sudo apt-get update && sudo apt-get upgrade`) para corrigir vulnerabilidades.
* **Usuários/Serviços**: execute serviços apenas com privilégios mínimos. Considere usar service accounts específicas se integrar APIs externas.
* **Recursos**: monitore o uso de GPU e memória. Use alertas ou dashboards do GCP para custos. Para economizar, pode-se usar VMs *preemptible* (spot) se o trabalho suportar interrupções.
* **Disco**: como recomendado, use discos de boot grandes (≥ 40 GB) e SSD locais para modelos. Remova snapshots/desanexe discos não usados para não pagar por armazenamento ocioso.
* **Segurança do modelo**: evite expor o Ollama API indiscriminadamente; configure `token`. Defina limites de taxa no WebUI e não permita usuários não autorizados (RBAC).

Seguindo essas práticas, você garante que os modelos rodem de forma eficiente e segura no GCP.

**Fontes:** Documentação do Ollama e LangChain, além de guias da Google Cloud para GPUs e fontes técnicas sobre LLaMA 4.
