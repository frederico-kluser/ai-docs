# Soluções open source para controlar o Terminal do macOS via iPhone

Existem diversas abordagens para expor o terminal do macOS a partir do iPhone de forma segura e direta. As principais soluções baseiam-se em SSH (acesso remoto seguro) e/ou terminais web. A tabela abaixo resume as características das opções mais relevantes:

| Nome do Projeto            | Plataforma                           | Tipo de Conexão                 | Segurança                                 | Fac. de Uso | Open Source | Observações                                                                                                                                                |
| -------------------------- | ------------------------------------ | ------------------------------- | ----------------------------------------- | ----------- | ----------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **OpenSSH (Remote Login)** | macOS (servidor SSH) + iOS (cliente) | SSH/TCP (porta 22)              | Criptografado (SSH)                       | Média       | Sim         | SSH nativo do macOS. Usa app SSH no iPhone (e.g. Blink, Termius). P2P via rede local ou Internet (com port forwarding ou VPN). Suporta chaves públicas.    |
| **Mosh (Mobile Shell)**    | macOS + iOS                          | SSH/TCP + UDP (≈60001)          | Criptografado via SSH (somente handshake) | Média       | Sim         | Substituto do SSH que permanece estável em redes instáveis. Usa hand‑shake SSH para autenticação, depois UDP dinâmico. Bom para roaming e conexões móveis. |
| **ttyd (Web Terminal)**    | macOS (servidor) + iOS (browser)     | HTTP/WebSocket (p.ex. ws)       | Opcionalmente TLS/SSL                     | Média       | Sim         | Compartilha o shell via navegador web. Fácil de instalar (brew install ttyd). Suporta autenticação básica e TLS.                                           |
| **Shell In A Box**         | macOS (servidor) + iOS (browser)     | HTTP/WebSocket                  | Opcionalmente TLS/SSL                     | Média-Baixa | Sim         | Servidor web que expõe o CLI a um terminal em navegador. Não requer plugins (funciona em Safari). Permite SSL e customização de comandos.                  |
| **WireGuard (VPN)**        | macOS + iOS                          | VPN Ponto-a-ponto (IP Tunelado) | Altíssima (criptografia moderna)          | Média-Alta  | Sim         | VPN leve cross-platform (inclui macOS/iOS). Cria rede virtual segura onde SSH funciona como se estivesse na LAN. Evita expor porta 22 diretamente.         |

* **OpenSSH (Remote Login)**: o macOS inclui um servidor OpenSSH (“Remote Login”). No iPhone basta um cliente SSH (por exemplo Blink Shell, Termius, Prompt, etc.). Funciona em LAN/Wi-Fi ou via internet (necessita redirecionar porta no roteador ou usar VPN). Suporta autenticação por senha ou, preferencialmente, por chaves pública/privada. É a solução mais direta e segura (criptografia SSH padrão).
* **Mosh (Mobile Shell)**: é um shell interativo sobre SSH projetado para conexões móveis. Usa SSH para fazer login e, em seguida, comunica-se por UDP em uma porta aleatória (≈60001). Isso permite manter a sessão ativa mesmo com IPs e redes variáveis. No iPhone, clientes como Blink Shell suportam Mosh. A vantagem é resistência a latência e interrupções, mas requer abrir UDP no firewall.
* **Terminais Web (ttyd, Shell In A Box, etc.)**: ferramentas como *ttyd* ou *Shell In A Box* executam um servidor HTTP que expõe o shell via navegador web. Basta abrir um endereço IP\:porta no Safari do iPhone. Elas suportam HTTPS (TLS) e autenticacão básica, mas devem ser configuradas com cuidado (uso de certificados, firewall) por questões de segurança.
* **WireGuard VPN + SSH**: WireGuard é um VPN moderno, de código aberto, que estabelece um túnel P2P criptografado. Instalando-o no Mac e iPhone, cria-se uma rede virtual segura entre eles (mesmo sobre internet). Dentro dessa rede, basta usar SSH normalmente. Isso evita ter que abrir portas públicas no roteador e adiciona uma camada extra de segurança.

Cada solução acima é open source (servidor macOS) e atende ao requisito de conexão direta segura.

## Roadmap de Implementação

A seguir detalhamos um passo a passo prático para configurar a solução recomendada (**OpenSSH + WireGuard**), seguido de variações opcionais:

1. **Habilitar Remote Login (SSH) no Mac:** No macOS Monterey ou superior, vá em **Sistema → Compartilhamento** e marque **Remote Login**. Isso inicia o servidor OpenSSH. Observe o endereço mostrado (ex: `ssh usuário@hostname.local`).

   * Como alternativa via Terminal: `sudo systemsetup -setremotelogin on`.
   * Verifique `ifconfig` ou **Preferências de Rede** para obter o IP local (ex: 192.168.x.x).

2. **Configurar chaves SSH (recomendado):** No iPhone, use o app SSH (p.ex. Blink ou Termius) para gerar um par de chaves pública/privada. Copie a chave pública para o Mac: abra o Terminal no Mac e edite `~/.ssh/authorized_keys`, adicionando a chave do iPhone. Ajuste permissão: `chmod 600 ~/.ssh/authorized_keys`. Com isso, o login será feito por chave em vez de senha (mais seguro).

3. **Conexão via Rede Local (Wi-Fi):** Certifique-se de que o iPhone esteja na mesma rede Wi-Fi do Mac. No app SSH, crie um novo host usando o IP local do Mac e porta 22. Teste a conexão; você deve ver o prompt do terminal do Mac e poder executar comandos remotamente.

4. **Acesso Remoto pela Internet (opções):** Como o Mac geralmente está atrás de um roteador NAT, há duas abordagens principais para acesso externo **sem serviços terceiros**:

   * **a. Port Forward + DNS:** Configure o roteador para encaminhar a porta 22 (ou outra porta customizada) para o IP do Mac. Use um serviço de DNS dinâmico (p.ex. DuckDNS, No-IP) para obter um nome que acompanhe seu IP público dinâmico. No iPhone, conecte-se ao `nome.ddns.net` na porta configurada. Em termos de segurança, recomendamos alterar a porta SSH padrão e restringir logins por chave (disabilitar senha).
   * **b. VPN WireGuard:** Instale o WireGuard no Mac (via Homebrew: `brew install wireguard-tools`) e no iPhone (App Store). Gere um par de chaves, crie um *interface* WireGuard no Mac (defina IPs VPN e chaves) e um perfil no iPhone (pode usar QR code). Ative a VPN no iPhone; ele receberá um IP privado (ex: 10.0.0.2) na mesma “LAN” virtual do Mac. Agora basta conectar via SSH usando o IP WireGuard do Mac (ex: 10.0.0.1). Essa abordagem é muito segura (criptografia de ponta a ponta) e dispensa abrir portas na internet.

5. **Segurança adicional:** Independentemente da opção de acesso remoto, é essencial:

   * **Desabilitar senhas SSH:** Em `/etc/ssh/sshd_config`, defina `PasswordAuthentication no` para permitir apenas chaves.
   * **Desativar Root:** Certifique-se que `PermitRootLogin no` esteja configurado. Use uma conta de usuário normal.
   * **Firewall:** Habilite o Firewall do macOS (nas Preferências de Segurança) e permita apenas tráfego SSH ou WireGuard. Você pode restringir por IP se necessário.
   * **Fail2ban/Limitadores:** Opcionalmente instale ferramentas como *fail2ban* para bloquear tentativas de login repetidas mal sucedidas.
   * **Keychain no iOS:** Se o app SSH permitir, armazene a chave privada com senha para maior segurança.

6. **Uso do iPhone:** No cliente SSH do iPhone, após configurar o host (IP/porta, usuário, chave), basta abrir a conexão. Você terá uma tela de terminal interativa para o macOS. Se usar termos web (ttyd/shellinabox), abrir o navegador em `http://IP:porta` e autenticar. Para WireGuard, ative a VPN primeiro.

## Conceitos Técnicos Explicados

* **SSH (Secure Shell):** protocolo de acesso remoto seguro que criptografa toda comunicação. O macOS inclui um servidor OpenSSH; basta habilitar **Remote Login** para ativá-lo. O cliente SSH (iPhone) conecta via TCP (porta 22) ao servidor.
* **Autenticação por chave pública/privada:** em vez de senha, gera-se um par de chaves criptográficas. A chave pública vai no servidor (`~/.ssh/authorized_keys`) e a privada fica no iPhone. Na conexão, o servidor verifica a chave do cliente. Isso elimina riscos de ataques de força bruta por senha.
* **SSH vs Mosh:** Mosh é um substituto de SSH otimizado para mobilidade. Ele começa com uma sessão SSH normal, depois passa a enviar dados pelo protocolo UDP (porta \~60001). Isso permite que a sessão sobreviva a mudanças de IP e a desconexões temporárias. No entanto, Mosh não criptografa o canal UDP após o handshake inicial, confiando na sessão SSH feita. Ainda assim, a autenticação é a mesma do SSH.
* **Tunelamento/Port Forwarding:** significa encaminhar uma porta de rede de um ponto a outro. Ex.: `ssh -R` ou `ssh -L`. No caso do Mac atrás de NAT, o port forward do roteador redireciona conexões externas (porta pública) para a porta 22 interna do Mac. O serviço de DNS dinâmico associa um nome fixo ao IP externo do roteador, permitindo encontrar o Mac na internet.
* **VPN WireGuard:** cria uma rede privada virtual ponto-a-ponto com criptografia moderna. Cada dispositivo (Mac e iPhone) tem um IP virtual, mesmo se estiverem em locais distintos. Ao conectar o iPhone via WireGuard, é como se ele estivesse na mesma LAN do Mac. Pode-se então usar SSH diretamente no IP da VPN. O WireGuard usa algoritmos avançados (Curve25519, ChaCha20, etc.), oferecendo alta segurança e simplicidade de configuração (chaves públicas, similar ao SSH).
* **Rede Local x Internet Pública:** Na rede local (Wi-Fi doméstico), dispositivos têm IPs privados (192.168.x.x). Esses IPs não são visíveis da internet. Para que o iPhone acesse o Mac de fora, precisamos ou fazer port forwarding (com IP público do roteador) ou usar VPN. Ferramentas de DNS dinâmico ou serviços como iCloud+ também podem mapear seu IP dinâmico para um nome fixo, mas são terceirizadas. Nossa solução foca em alternativas auto-hospedadas (VPN ou SSH).

Com essas configurações, é possível controlar o terminal do macOS completamente a partir do iPhone, local ou remotamente, usando somente software open source (servidor macOS e, no caso do iPhone, apps compatíveis). As referências a seguir detalham algumas dessas ferramentas: por exemplo, o *Remote Login* do macOS é baseado em SSH, o *Mosh* oferece conectividade móvel robusta, e ferramentas como *Shell In A Box* ou *ttyd* expõem o shell via navegador web. A VPN WireGuard é destacada por sua simplicidade e criptografia de ponta, tornando-a ideal para acesso P2P seguro.

**Fontes:** Documentação do macOS (SSH/Remote Login), site oficial do Mosh, repositórios de Shell In A Box e ttyd, e site do WireGuard.
