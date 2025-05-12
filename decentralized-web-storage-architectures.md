# Introdução

Criar um site verdadeiramente **incontrolável** exige arquiteturas descentralizadas tanto para o armazenamento do conteúdo quanto para o sistema de nomes. Tecnologias como IPFS, Arweave, Sia/Skynet, Storj etc. removem o ponto único de falha: cada nó que baixa um conteúdo o armazena em cache e o compartilha com outros, formando uma rede peer-to-peer **sem servidor central único**. Isso garante que mesmo se alguns nós forem derrubados, outros continuam servindo o site. De forma semelhante, domínios baseados em blockchain (ENS, Handshake, Unstoppable Domains, etc.) tornam o nome do site imune a intervenções de registradores ou governos. No entanto, é preciso combinar essas tecnologias para atingir anonimato e acessibilidade na web comum. Este relatório detalha as opções técnicas (IPFS, Arweave, Skynet, contratos blockchain, DNS descentralizada etc.), suas vantagens e limitações, e recomendações práticas para manter o site atualizado, seguro, resistente a ataques e proteger a identidade do autor.

## Armazenamento Descentralizado de Conteúdo

**IPFS (InterPlanetary File System):** é um sistema de arquivos ponto-a-ponto distribuído por blocos de dados. Cada nó que baixa um arquivo o **copia em cache** e passa a compartilhar com outros, de modo que “quanto mais um arquivo é baixado, mais cópias existem e, portanto, mais disponível ele se torna”. Isso elimina pontos únicos de falha: se um nó sair da rede, outros irmãos ainda conterão o conteúdo, aumentando a **resiliência** do site. Na prática, ao hospedar o site no IPFS, não se liga o domínio a um único servidor, mas sim a um *CID* (identificador de conteúdo). A desvantagem é que, sozinho, o IPFS não garante anonimato (você acaba expondo IP e ID de nó) e dados não são mantidos indefinidamente se não houver nós fixos. Para permanência, costuma-se usar serviços de pinning (como Pinata ou serviços de Filecoin) que **pagam para manter** os arquivos no IPFS. Atualizar conteúdo no IPFS exige publicar um novo CID (ou usar IPNS/ENS para apontar para o hash atualizado).

**Arweave:** é um blockchain de “armazenamento permanente” (“permaweb”). Sua promessa é “armazenar dados permanentemente”: paga-se uma única vez para manter o arquivo disponível **para sempre**, nas máquinas da rede Arweave. Como descrito, “Arweave garante que, uma vez armazenados, os dados permanecem acessíveis para sempre”. Isso torna o site imutável e imune a apagões de longo prazo. A desvantagem é que cada atualização requer uma nova transação (o conteúdo antigo permanece lá e o novo é um arquivo adicional), e o custo inicial pode ser elevado. Arweave é acessível pela web tradicional via gateways (ex. `arweave.net/<txid>`), mas depende desses gateways funcionarem.

**Sia/Skynet:** são redes de armazenamento descentralizado pagas. No Sia, você aluga espaço em hosts (paga mensalidades); o **Skynet** é uma camada para hospedagem de sites dentro do Sia. Diferente do IPFS, “tudo é hospedado em servidores pagos, e usa roteamento direto ao invés de DHT, resultando em latência muito melhor”. O Skynet inclui o SkyDB para atualizações rápidas (\~200ms) e é totalmente acessível via HTTP (qualquer pessoa pode rodar um portal Skynet que serve conteúdo via web). Isso facilita o acesso comum sem precisar de plugins. Porém, como exige pagamento contínuo, sua durabilidade depende de contratos ativos.

**Outros (Filecoin, Storj, BitTorrent, Freenet, etc):** Plataformas como Filecoin ou Storj também oferecem armazenamento descentralizado (pagando nós para manter dados), mas geralmente requerem gateways/IPFS para acesso web. O BitTorrent só distribui arquivos como torrent (sem interface web). O Freenet fornece anonimato extremo, mas funciona isolado da internet comum (não atende ao requisito de acesso pela web tradicional) e é mais voltado para compartilhamento anônimo entre usuários.

Em resumo, **tabela comparativa** abaixo resume os pontos-chave:

| Rede/Protocolo       | Modelo                  | Pagamento                  | Permanência                    | Atualizações              | Resistência/Censura                                             |
| -------------------- | ----------------------- | -------------------------- | ------------------------------ | ------------------------- | --------------------------------------------------------------- |
| **IPFS**             | P2P de conteúdo (DHT)   | Grátis (opcional Filecoin) | Fraca nativa (depende de pins) | Nova hash (IPNS/ENS)      | Alta: múltiplos nós, **sem ponto único de falha**               |
| **Arweave**          | Blockchain (permaweb)   | Pago único (AR tokens)     | Muito alta (dados permanentes) | Nova transação (imutável) | Extremamente alta (dados imutáveis)                             |
| **Sia/Skynet**       | P2P paga + portals HTTP | Pagamento periódico (SC)   | Alta (sob contrato)            | SkyDB rápido (\~200ms)    | Alta (dados replicados; acesso via portais HTTP)                |
| **Filecoin (+IPFS)** | Blockchain + IPFS       | Pagamento (FIL)            | Média (depende de contratos)   | Via IPNS/ENS + CID        | Alta (mesmo IPFS)                                               |
| **Storj**            | P2P paga + encriptação  | Pagamento (USD/TB)         | Média (contratos)              | Sob demanda               | Alta (rede descentralizada)                                     |
| **BitTorrent**       | P2P (torrent)           | Grátis                     | Baixa (depende de seeders)     | Novo torrent              | Média (bloqueável por domínio/hospedagem de torrent)            |
| **Freenet**          | P2P anonimato           | Grátis                     | Alta (cache distrib.)          | Suporte embutido          | Altíssima (foco em anonimato, mas não acessível pela web comum) |

## Sistema de Nomes Descentralizado

O *endereço* tradicional (ex. `exemplo.com`) também é um ponto vulnerável: registros DNS e registradores podem ser coagidos ou censurados. Solução moderna são domínios baseados em blockchain (**Web3 domains**) ou sistemas DNS-alternativos. Exemplos:

* **ENS (Ethereum Name Service, .eth):** armazena nomes `.eth` em contratos Ethereum. Isso torna os registros “decentralizados, seguros e resistentes à censura”. Você compra um nome (pagando Ether em taxas) e pode apontá-lo para um hash IPFS. Navegadores padrão não suportam `.eth` nativamente, mas há alternativas: e.g., serviços como `*.eth.link` (via Cloudflare) permitem que um domínio ENS seja acessado via HTTP comum (ex.: `meusite.eth` vira `meusite.eth.link`). Assim, *qualquer pessoa* pode visitar um site ENS sem plugin especial. Vantagem: domínio 100% do usuário (NFT), sem renovação anual (só gas). Desvantagem: atualmente pouco “plug-and-play” em navegadores sem bridges.

* **Unstoppable Domains (.crypto, .zil, .coin etc):** domínios NFT em blockchains (Ethereum ou Zilliqa). São comprados uma vez e armazenados na sua wallet. Por rodarem em blockchain público, são “extremamente difíceis de derrubar” ou censurar. Unstoppable integra-se bem a IPFS – basta apontar o domínio para um CID IPFS – e vários navegadores modernos (Brave, Opera) acessam `.crypto` nativamente ou via plugins. Em outras palavras, seu site passa a ser acessível por uma URL Web tradicional sem depender de servidores DNS centrais. A desvantagem é que ainda não são universalmente suportados, exigindo às vezes ferramentas especiais ou gateways.

* **Handshake (HNS):** protocolo que “armazena a propriedade de TLDs no blockchain”, eliminando ICANN. Permite adquirir TLDs (ex.: `meusite/`) via leilão. É “resistente à censura” porque os registros vivem na rede distribuída. O site pode ter um subdomínio (`minhaempresa/`) e diversos gateways habilitam acesso via HTTP, usando resolvers descentralizados. Handshake reforça a ideia de que **não estamos reféns dos domínios convencionais**: “se o domínio vive em namespaces centralizados, seu direito de existir online pertence a outrem, que pode removê-lo com um único comando”.

* **DNS tradicional (.com/.org):** *não* atende aos requisitos, pois cada domínio está sob controle de registradores e ICANN. Quanto maior a censura estatal, maior a chance de remover um domínio convencional. Ainda assim, pode-se usar um domínio DNS comum apontando para gateways IPFS (via DNSLink) como rota de fallback, mas sem eliminar pontos centralizados.

Em resumo, domínios blockchain proporcionam **anonimato e imutabilidade do registro** (são NFTs em sua carteira, sem informações pessoais vinculadas) e conectam-se a redes descentralizadas. A tabela comparativa a seguir destaca diferenças:

| Sistema de Domínio             | Tipo/Exemplo | Propriedade     | Custo                | Suporte (Browser)          | Resistência              |
| ------------------------------ | ------------ | --------------- | -------------------- | -------------------------- | ------------------------ |
| **DNS Clássico**               | .com, .org   | Central (ICANN) | R\$ (taxas anuais)   | Universais (HTTP)          | Baixa (controle central) |
| **ENS (.eth)**                 | meusite.eth  | Você (Ethereum) | Gas (Ethereum)       | Via `.eth.link` ou plugins | Alta (blockchain)        |
| **Unstoppable (.crypto/.zil)** | site.crypto  | Você (ETH/ZIL)  | 1x (pagamento único) | Brave/Opera, gateways      | Alta (blockchain)        |
| **Handshake (HNS)**            | meudominio/  | Você (HNS)      | Leilões em HNS       | Gateways especiais         | Alta (blockchain)        |
| **Namecoin (.bit)**            | site.bit     | Você (Namecoin) | Taxa fixa (NTX)      | Plugins/Serviços externos  | Alta (blockchain)        |

## Acessibilidade na Web Comum

Para que qualquer usuário da internet possa visitar o site sem software especial, é preciso usar **gateways ou browsers compatíveis**. Exemplos práticos:

* **Gateways IPFS:** qualquer conteúdo IPFS pode ser acessado por URLs como `https://ipfs.io/ipfs/<CID>` ou via Cloudflare (`<CID>.ipfs.cf-ipfs.com`). Domínios personalizados podem apontar para um gateway público (ex.: DNSLink). Isso permite rodar o site no IPFS mas ainda ser aberto em navegadores comuns. O tradeoff é confiar no gateway: se ele sair do ar, use outro. Uma vantagem é a redundância: há vários gateways públicos (Cloudflare, Infura, Dweb.link etc.), dificultando bloqueio geral.

* **Browsers Web3:** navegadores modernos (Brave, Opera, Firefox via extensão) já incorporam resoluções ENS/IPFS. Por exemplo, Brave resolve nativamente endereços ENS e Unstoppable. Assim, `exemplo.crypto` abre diretamente sem gateway externo. Isso amplia o acesso “convencional” ao site descentralizado. Todavia, nem todo usuário tem esses browsers, então manter um fallback via gateway ou DNSLink é aconselhável.

* **Proxies descentralizados:** projetos como [Fleek](https://fleek.co) oferecem hospedagem contínua no IPFS com um domínio tradicional (HTTPS) apontando para o CID. Eles cuidam de atualizar IPNS/ENS e TLS para você. Isso facilita o acesso padrão ([https://meusite.com](https://meusite.com)), mas pode reintroduzir pontos centralizados (Fleek, Cloudflare) no fluxo.

Em suma, o site ficará acessível pela internet comum se for publicado em redes P2P (IPFS, Skynet etc.) e o nome no qual é anunciado for resolvido por meio de gateways ou domínios blockchain já adotados pelos browsers ou serviços intermediários.

## Manutenção de Conteúdo e Atualizações

Um site descentralizado geralmente será **estático** (HTML/CSS/JS) por simplicidade. Cada nova versão gera um novo hash (CID, transação Arweave etc.). Para manter o conteúdo atualizado no mesmo endereço amigável, pode-se:

* **IPNS / ENS / DNSLink:** Publicar o novo CID no IPNS (nome IPFS usando chave) ou atualizar o registro ENS/DNSLink do domínio com o novo hash. Ex.: em ENS, você atualiza o campo *Content* para o novo CID; em IPNS, executa `ipfs name publish`. Isso garante que `dominio.eth` ou `site.com` continue apontando para o site atual. Note que atualizar ENS envolve taxas de gás; IPNS é mais lento, mas grátis além do custo de operação do nó IPFS.

* **Automação de implantação:** usar ferramentas CI/CD (GitHub Actions, Fleek, Pinata) para, ao subir código, automaticamente fazer pin do site no IPFS e atualizar IPNS/ENS. Assim, não é preciso fazê-lo manualmente.

* **Redundância de publicação:** espelhar o site em múltiplos sistemas simultaneamente. Por exemplo, armazenar o conteúdo no IPFS *e* em Arweave. Há soluções que fazem “bridge” entre Arweave e IPFS: arquivam em Arweave (permanente) e publicam o mesmo hash no IPFS. Dessa forma, mesmo que um sistema falhe, o outro mantém o site vivo.

* **Segurança do conteúdo:** verificar assinaturas digitais. Seu site pode assinar arquivos estáticos com sua chave GPG, permitindo que quem baixe do IPFS confirme que veio de você. Isso garante integridade, especialmente importante se alguém interceptar atualizações.

## Resiliência e Contra-Ataques

Graças à descentralização, o site naturalmente resiste a vários ataques: **DDoS** em nós individuais não derruba o site inteiro, pois outros nós (inclusive geograficamente distribuídos) o manterão. Para aumentar a resiliência, recomenda-se:

* **Espelhamento ativo:** incentive apoiadores a também rodar nós IPFS (pin servers) do seu site, ou use serviços de hosting descentralizado (ex.: Spheron, Estuary) para ter múltiplos provedores redundantes. Cada espelho extra diminui a chance de blackout.

* **Caminhos alternativos:** disponibilize múltiplas URLs de acesso (diferentes gateways IPFS, link DNS com ENS e sem, domínios blockchain diferentes). Se um caminho for bloqueado (ex.: determinado gateway IP banido), o usuário pode tentar outro.

* **TLS/HTTPS:** mesmo que o conteúdo venha de IPFS ou Skynet, pode-se servir por domínio tradicional com certificado TLS (por exemplo, usando Cloudflare ao resolver o domínio para um gateway IPFS). Isso protege os usuários de ataques de interceptação (Man-in-the-Middle) e melhora a aparência profissional do site.

* **Atualizações frequentes:** atacar um site (ex.: via injeção) é mais difícil quando ele é somente leitura e imutável; ainda assim, use boas práticas de segurança no front-end (nenhuma biblioteca externa não confiável, CSP adequado etc.) para evitar exploração via browser.

* **Censura governamental:** como cada país pode bloquear IPs ou domínios, é útil instruir usuários a mudar DNS para OpenNIC ou usar VPN. Por exemplo, se `.onion` não é permitido, o fallback pode ser um domínio Handshake personalizado ou um serviço de DNS alternativo que resolva ENS.

## Proteção da Identidade do Criador

Garantir anonimato total do criador requer cuidados além da infraestrutura:

* **Servidores anônimos:** se você hospeda o site (por exemplo, nodos IPFS), faça isso via **VPN ou Tor**. É possível até rodar um nó IPFS usando *transporte Tor* (IPFS over Tor), de modo que seu IP real não seja divulgado. O IPFS por si só “vaza bastante informação” (peer ID persistente, IP, DHT, conteúdo em cache), então isolamento em VM/Docker com VPN dedicado é recomendado. Em última análise, se a ameaça for poderosa (governo real), o IPFS atual *não oferece anonimato forte*, e até o dev IPFS admite isso: “o IPFS não fornecerá o anonimato que você deseja... Se você quer ocultar-se de governos, o IPFS atual provavelmente não é suficiente”.

* **Domínios e registro:** use domínios blockchain que não exigem dados pessoais. Por exemplo, ENS e Unstoppable mintam domínios em blockchain sem exigir KYC. A chave privada que você usa para comprar o domínio é a única identificação. Registre contas de email ou serviços relacionados com pseudônimos e pague com criptomoedas (ou gift cards).

* **Publicação indireta:** outra tática é ter um terceiro confiável (ou um serviço automático) que faça o *publish* em IPNS/ENS em seu lugar. Assim, mesmo que rastreiem quem atualiza o conteúdo, não necessariamente chegarão ao criador original.

* **Evitar logs:** tenha cuidado com logs de rede ou DNS em seu provedor de internet. Se possível, faça tudo (publicar no IPFS, atualizar ENS) em rede isolada (ex.: cafés, bibliotecas, usando Tor).

Em resumo, a criptografia e redes P2P facilitam esconder o conteúdo, mas **não garantem anonimato perfeito**. Para máxima segurança do criador, recomenda-se o uso de camadas dedicadas de anonimato (Tor, VPN, I2P) ao interagir com qualquer sistema descentralizado, lembrando que mesmo aí nada é 100% infalível. Por exemplo, o Freenet foi projetado para anonimato mútuo, mas não se encaixa na exigência de “internet comum”. Portanto, a melhor estratégia é combinar privacidade operacional (VPN/Tor, pseudônimos) com infraestrutura descentralizada.

## Comparativo de Tecnologias

**Resumo em tabelas** das principais soluções:

<table>
<thead>
<tr>
<th align="left">Tecnologia / Sistema</th><th align="left">Tipo</th><th align="left">Modelo de Uso</th><th align="left">Permanência</th><th align="left">Atualizações</th><th align="left">Visibilidade Anônima</th>
</tr>
</thead>
<tbody>
<tr><td><b>IPFS</b></td><td>Rede P2P de arquivos (DHT)</td><td>Grátis. Pode-se pagar Filecoin para pin.</td><td>Dados mantidos enquanto houver nós “pinando”</td><td>Através de IPNS/ENS (troca de CID)</td><td>Sem anonimato nativo (revela IP / ID):contentReference[oaicite:31]{index=31}</td></tr>
<tr><td><b>Arweave</b></td><td>Blockchain de armazenamento</td><td>Pago único (AR) para armazenar permanentemente.</td><td>Permanente (“store once, keep forever”):contentReference[oaicite:32]{index=32}</td><td>Nova transação adiciona versão (imuta.)</td><td>Anônimo (só registra TX, mas wallet usada pode ter rastros; recomenda-se mixing)</td></tr>
<tr><td><b>Sia / Skynet</b></td><td>Armazenamento P2P pago</td><td>Pagam-se contratos (SC) por mês.</td><td>Dados mantidos durante contratos ativos</td><td>Skynet SkyDB (rapidez ~200ms):contentReference[oaicite:33]{index=33}</td><td>Revela uso de rede Sia; anonimato moderado</td></tr>
<tr><td><b>Filecoin</b></td><td>Blockchain + IPFS</td><td>Contratos FIL para armazenamento via IPFS.</td><td>Mantido conforme contratos pagos</td><td>Usa IPNS/ENS (como IPFS)</td><td>Sem anonimato nativo (revela transações)</td></tr>
<tr><td><b>Storj</b></td><td>P2P pago + criptografia</td><td>Pagam-se GB/TB armazenados</td><td>Depende de pagamento contínuo</td><td>Substitui arquivo (assinatura HMAC)</td><td>Sem anonimato (plataforma KYC/recursos de recuperação)</td></tr>
<tr><td><b>BitTorrent</b></td><td>P2P torrent</td><td>Grátis</td><td>Depende de seeders online</td><td>Criar novo torrent</td><td>Depende do cliente (IP exposto em DHT)</td></tr>
<tr><td><b>Freenet</b></td><td>P2P anonimato</td><td>Grátis</td><td>Alto (nós mantêm caches)</td><td>Suporte dinâmico interno</td><td>**Muito alto** (desenhado para anonimato):contentReference[oaicite:34]{index=34}</td></tr>
</tbody>
</table>

<table>
<thead>
<tr>
<th align="left">Sistema de Domínio</th><th align="left">Exemplo TLD</th><th align="left">Controle</th><th align="left">Custo</th><th align="left">Acesso (browser)</th><th align="left">Censurabilidade</th>
</tr>
</thead>
<tbody>
<tr><td><b>DNS Tradicional</b></td><td>.com/.net</td><td>ICANN/Registradores</td><td>Renovação anual</td><td>Universal (HTTP)</td><td>Alto risco (centr.</td></tr>
<tr><td><b>ENS (Ethereum)</b></td><td>.eth</td><td>Usuário via blockchain</td><td>Gás Ethereum (compra + tx)</td><td>Via Gateways (.eth.link) ou Brave:contentReference[oaicite:35]{index=35}</td><td>Muito alto (blockchain):contentReference[oaicite:36]{index=36}</td></tr>
<tr><td><b>Unstoppable</b></td><td>.crypto/.zil</td><td>Usuário (NFT em ETH/ZIL)</td><td>Compra única (sem renovação):contentReference[oaicite:37]{index=37}</td><td>Brave/Opera nativo ou gateway</td><td>Muito alto (blockchain):contentReference[oaicite:38]{index=38}</td></tr>
<tr><td><b>Handshake (HNS)</b></td><td>exemplo/ (TLD próprio)</td><td>Usuário (NFT no HNS)</td><td>Leilão HNS (pago em HNS)</td><td>Gateways HNS ou resolução DNS especial</td><td>Muito alto (blockchain):contentReference[oaicite:39]{index=39}</td></tr>
<tr><td><b>Namecoin</b></td><td>.bit</td><td>Usuário (blockchain NC)</td><td>Taxa fixa (Namecoin)</td><td>DNS alternativo / plugin</td><td>Alto (blockchain)</td></tr>
</tbody>
</table>

## Conclusão

A combinação mais eficaz envolve hospedar o site como **conteúdo estático** em uma rede P2P distribuída (por exemplo, IPFS) e vincular o nome do site a um sistema de nomes descentralizado (ENS, Handshake, etc.). Por exemplo: crie seu site em HTML, publique no IPFS (pegando o CID), e aponte um domínio como `site.eth` para esse CID. Use navegadores Web3 ou gateways IPFS para acesso comum. Como destaca a documentação oficial do IPFS, “não há ponto único de falha” ao se usar IPFS, e conectar o domínio em blockchain torna-o “extremamente difícil de derrubar”.

Entretanto, é preciso gerenciar desafios práticos: atualizar o site requer publicar novo hash (IPNS/ENS), proteger o administrador por VPN/Tor, e instruir usuários a usar resoluções adequadas. Com cuidado nessas etapas – conteúdo estático confiável, sistemas de nomes blockchain e hosting redundante – pode-se atingir um site **praticamente imune à censura estatal ou remoção**, acessível pela internet normal e sem traçar o autor. Cada tecnologia tem limitações (custos de blockchain, necessidade de pinning, suporte de navegador, etc.), por isso as implementações ideais geralmente **misturam** ferramentas: por exemplo, armazenar em Arweave *e* IPFS, usar ENS *e* Handshake como alternativas, oferecer gateway e .eth.link simultaneamente. Essa abordagem em camadas garante que o site fique sempre online e que sua origem permaneça oculta, atendendo aos requisitos de atualização contínua, segurança e anonimato.

**Fontes:** Documentação e artigos técnicos sobre IPFS, Arweave, Sia/Skynet, ENS, Handshake e Unstoppable Domains.
