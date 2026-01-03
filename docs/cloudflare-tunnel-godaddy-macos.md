# Tutorial completo: Cloudflare Tunnel com domínio GoDaddy no macOS

Expor uma API FastAPI local para a internet 24/7 nunca foi tão simples. Este tutorial cobre **dois cenários práticos**: usar um subdomínio enquanto mantém sites Vercel funcionando, ou dedicar um domínio inteiro para suas APIs via Cloudflare Tunnel. A configuração leva cerca de 20 minutos e sobrevive a reboots automaticamente.

**Importante**: O Cloudflare Tunnel na camada gratuita **requer migrar os nameservers para o Cloudflare**. A opção de "DNS parcial" (CNAME setup) exige plano Business ($200+/mês), tornando a migração completa a escolha prática para desenvolvedores.

---

## Instalação do cloudflared no macOS

O cloudflared está disponível no Homebrew core, sem necessidade de taps adicionais. A instalação é direta:

```bash
# Instalar via Homebrew
brew install cloudflared

# Verificar instalação
cloudflared --version
# Saída esperada: cloudflared version 2025.x.x
```

O binário é instalado em `/opt/homebrew/bin/cloudflared` (Apple Silicon) ou `/usr/local/bin/cloudflared` (Intel). A versão atual estável é **2025.11.1**.

---

## Cenário A: Subdomínio para API com Vercel no domínio principal

Este cenário mantém `www.meusite.com` na Vercel enquanto `api.meusite.com` aponta para seu localhost via Cloudflare Tunnel.

### Passo 1: Adicionar domínio ao Cloudflare

Acesse [dash.cloudflare.com](https://dash.cloudflare.com) e clique em **"Add a Site"**. Digite seu domínio (ex: `meusite.com`) e selecione o plano **Free**. O Cloudflare importará automaticamente seus registros DNS existentes — **revise-os cuidadosamente** antes de prosseguir, especialmente registros MX para email.

### Passo 2: Migrar nameservers do GoDaddy para Cloudflare

Após adicionar o site, o Cloudflare mostrará dois nameservers atribuídos (ex: `anna.ns.cloudflare.com` e `bob.ns.cloudflare.com`).

**No GoDaddy:**

1. Acesse [dcc.godaddy.com/control/portfolio](https://dcc.godaddy.com/control/portfolio)
2. Selecione seu domínio → **DNS** → **Nameservers**
3. Escolha **"I'll use my own nameservers"**
4. Remova os nameservers existentes do GoDaddy
5. Adicione os dois nameservers do Cloudflare exatamente como mostrados
6. Clique **Save** e complete a verificação 2FA se solicitado

**Propagação**: Tipicamente **1-4 horas**, podendo levar até 48 horas em casos raros. Verifique o status com:

```bash
dig ns meusite.com @1.1.1.1
```

Quando os nameservers Cloudflare aparecerem, seu domínio mostrará status **"Active"** no dashboard.

### Passo 3: Configurar DNS para coexistência Vercel + Tunnel

No dashboard Cloudflare, vá em **DNS → Records** e configure:

| Type | Name | Content | Proxy Status |
|------|------|---------|--------------|
| A | `@` | `76.76.21.21` | **DNS only** (nuvem cinza) |
| CNAME | `www` | `cname.vercel-dns.com` | **DNS only** (nuvem cinza) |
| CNAME | `api` | `<UUID>.cfargotunnel.com` | **Proxied** (nuvem laranja) |

**Crítico**: Registros Vercel devem usar **nuvem cinza (DNS only)** para:
- Permitir que a Vercel emita certificados Let's Encrypt
- Evitar loops de redirecionamento HTTPS
- Manter o cache e CDN nativos da Vercel

Se você precisar usar proxy (nuvem laranja) para registros Vercel, configure **SSL/TLS → Overview → Full (strict)**.

### Passo 4: Autenticar cloudflared

```bash
cloudflared tunnel login
```

Isso abre o navegador para autenticação. Após login, um arquivo `cert.pem` é salvo em `~/.cloudflared/`. Este certificado permite gerenciar túneis para suas zonas no Cloudflare.

### Passo 5: Criar Named Tunnel

```bash
cloudflared tunnel create api-tunnel
```

Saída esperada:
```
Tunnel credentials written to /Users/seuuser/.cloudflared/<UUID>.json
Created tunnel api-tunnel with id <UUID>
```

**Anote o UUID** — você precisará dele para o config.yml.

### Passo 6: Criar arquivo config.yml

Crie o arquivo `~/.cloudflared/config.yml`:

```yaml
tunnel: <UUID-DO-TUNNEL>
credentials-file: /Users/seuuser/.cloudflared/<UUID-DO-TUNNEL>.json

ingress:
  - hostname: api.meusite.com
    service: http://localhost:8000
  - service: http_status:404
```

**Regras de ingress**: São avaliadas de cima para baixo. A primeira que corresponder é usada. A última regra **deve ser um catch-all** sem hostname (retorna 404 para qualquer coisa não mapeada).

### Passo 7: Criar registro DNS automaticamente

```bash
cloudflared tunnel route dns api-tunnel api.meusite.com
```

Isso cria o registro CNAME apontando para `<UUID>.cfargotunnel.com` automaticamente.

### Passo 8: Testar manualmente

```bash
# Inicie sua API FastAPI
uvicorn main:app --port 8000

# Em outro terminal, rode o tunnel
cloudflared tunnel run api-tunnel
```

Acesse `https://api.meusite.com` — deve responder com sua API local.

---

## Cenário B: Domínio dedicado para APIs

Para um domínio exclusivo (ex: `minhasapis.dev`), o processo é mais simples pois não há necessidade de configurar coexistência com Vercel.

### Passos 1-5: Idênticos ao Cenário A

Adicione o domínio ao Cloudflare, migre nameservers, autentique e crie o tunnel.

### Configuração multi-serviço no mesmo tunnel

Para múltiplas APIs em subdomínios diferentes, use um único tunnel com múltiplas regras de ingress:

```yaml
tunnel: <UUID>
credentials-file: /Users/seuuser/.cloudflared/<UUID>.json

ingress:
  # FastAPI principal
  - hostname: api.minhasapis.dev
    service: http://localhost:8000
    
  # Serviço de autenticação
  - hostname: auth.minhasapis.dev
    service: http://localhost:8001
    
  # Aplicação de staging
  - hostname: staging.minhasapis.dev
    service: http://localhost:3000
    
  # Wildcard para qualquer outro subdomínio
  - hostname: "*.minhasapis.dev"
    service: http://localhost:8080
    
  # Catch-all obrigatório
  - service: http_status:404
```

Crie os registros DNS para cada hostname:

```bash
cloudflared tunnel route dns api-tunnel api.minhasapis.dev
cloudflared tunnel route dns api-tunnel auth.minhasapis.dev
cloudflared tunnel route dns api-tunnel staging.minhasapis.dev
cloudflared tunnel route dns api-tunnel "*.minhasapis.dev"
```

---

## Configurando cloudflared como serviço 24/7

Para que o tunnel sobreviva a reboots e rode continuamente, configure-o como Launch Daemon no macOS.

### Preparar configuração para modo daemon

O serviço em modo root espera arquivos em `/etc/cloudflared/`:

```bash
# Criar diretório de configuração do sistema
sudo mkdir -p /etc/cloudflared

# Copiar configuração e credenciais
sudo cp ~/.cloudflared/config.yml /etc/cloudflared/
sudo cp ~/.cloudflared/<UUID>.json /etc/cloudflared/

# Ajustar caminho das credenciais no config
sudo nano /etc/cloudflared/config.yml
```

Atualize o `credentials-file` para o caminho do sistema:

```yaml
tunnel: <UUID>
credentials-file: /etc/cloudflared/<UUID>.json

ingress:
  - hostname: api.meusite.com
    service: http://localhost:8000
  - service: http_status:404
```

### Instalar e iniciar serviço

```bash
# Instalar como Launch Daemon (roda no boot)
sudo cloudflared service install

# Iniciar imediatamente
sudo launchctl start com.cloudflare.cloudflared
```

O plist é criado em `/Library/LaunchDaemons/com.cloudflare.cloudflared.plist` com `RunAtLoad: true` e `KeepAlive` configurado para reiniciar em caso de crash.

### Comandos de gerenciamento do serviço

```bash
# Verificar status (mostra PID se rodando)
sudo launchctl list com.cloudflare.cloudflared

# Parar serviço
sudo launchctl stop com.cloudflare.cloudflared

# Reiniciar após mudanças no config
sudo launchctl stop com.cloudflare.cloudflared
sudo launchctl start com.cloudflare.cloudflared

# Ver logs em tempo real
tail -f /Library/Logs/com.cloudflare.cloudflared.err.log

# Desinstalar serviço
sudo cloudflared service uninstall
```

### Verificar funcionamento após reboot

```bash
# Checar processo rodando
ps aux | grep cloudflared

# Testar endpoint
curl -I https://api.meusite.com

# Ver status no dashboard
# Zero Trust → Networks → Tunnels → status deve ser "Healthy"
```

---

## Troubleshooting comum

### DNS não propaga após mudar nameservers

**Sintoma**: Domínio ainda mostra "Pending" no Cloudflare após várias horas.

**Soluções**:
- Verifique se DNSSEC está **desabilitado** no GoDaddy antes de migrar
- Confirme que **ambos** os nameservers foram adicionados corretamente
- Use `whois meusite.com | grep -i nameserver` para verificar
- Aguarde até 48 horas para propagação completa

### ERR_TOO_MANY_REDIRECTS com Vercel

**Causa**: SSL/TLS configurado como "Flexible" com proxy habilitado.

**Solução**: No Cloudflare, vá em **SSL/TLS → Overview** e mude para **Full** ou **Full (strict)**.

### Tunnel não conecta: "failed to connect to origin"

**Verificações**:
1. Sua API local está rodando? (`curl localhost:8000`)
2. O hostname no config.yml corresponde ao registro DNS?
3. Credenciais corretas no caminho especificado?

```bash
# Validar configuração
cloudflared tunnel ingress validate

# Testar qual regra corresponde
cloudflared tunnel ingress rule https://api.meusite.com
```

### Serviço não inicia após reboot

**Verificações**:

```bash
# Arquivo plist existe?
ls -la /Library/LaunchDaemons/com.cloudflare.cloudflared.plist

# Config existe em /etc/cloudflared/?
ls -la /etc/cloudflared/

# Ver erro específico
tail -50 /Library/Logs/com.cloudflare.cloudflared.err.log
```

**Problema comum**: O plist pode não incluir `tunnel run`. Edite-o:

```bash
sudo nano /Library/LaunchDaemons/com.cloudflare.cloudflared.plist
```

Confirme que `ProgramArguments` contém:
```xml
<array>
    <string>/opt/homebrew/bin/cloudflared</string>
    <string>tunnel</string>
    <string>run</string>
</array>
```

### Certificado SSL não emite na Vercel

**Causa**: Proxy (nuvem laranja) habilitado bloqueia challenge HTTP-01.

**Soluções**:
1. **Preferida**: Use nuvem cinza para registros Vercel
2. **Alternativa**: Desabilite proxy temporariamente, deixe Vercel emitir cert, reabilite
3. Na Vercel, use verificação via TXT record (Settings → Domains → Verify)

---

## Referência rápida de comandos

| Ação | Comando |
|------|---------|
| Instalar | `brew install cloudflared` |
| Autenticar | `cloudflared tunnel login` |
| Criar tunnel | `cloudflared tunnel create <nome>` |
| Listar tunnels | `cloudflared tunnel list` |
| Criar DNS | `cloudflared tunnel route dns <nome> <hostname>` |
| Rodar manual | `cloudflared tunnel run <nome>` |
| Validar config | `cloudflared tunnel ingress validate` |
| Instalar serviço | `sudo cloudflared service install` |
| Ver logs | `tail -f /Library/Logs/com.cloudflare.cloudflared.err.log` |
| Status serviço | `sudo launchctl list com.cloudflare.cloudflared` |

---

## Conclusão

A combinação Cloudflare Tunnel + domínio GoDaddy oferece uma forma gratuita e robusta de expor serviços locais. Para desenvolvedores com sites na Vercel, a chave é usar **nuvem cinza para registros Vercel** e **nuvem laranja apenas para o tunnel**. O serviço launchd garante operação 24/7 sem intervenção manual após reboots.

Para ambientes de produção futuros, considere adicionar **Cloudflare Access** para autenticação em suas APIs — configurável diretamente no dashboard Zero Trust sem mudanças no código.