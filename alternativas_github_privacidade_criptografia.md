# Alternativas blindadas ao GitHub: onde seu código fica realmente privado

Em um mundo onde a privacidade de dados se torna cada vez mais crítica, encontrar alternativas ao GitHub que priorizem segurança não é apenas uma preferência, mas uma necessidade para muitos desenvolvedores. Esta análise identifica as melhores opções disponíveis atualmente, tanto self-hosted quanto hospedadas por terceiros, com foco específico em recursos de criptografia e proteção de privacidade.

## O que você precisa saber primeiro

As melhores alternativas ao GitHub para privacidade são uma combinação de soluções self-hosted como Forgejo e GitLab CE, ou plataformas hospedadas como SourceHut e Codeberg. Para máxima segurança, ferramentas como git-remote-gcrypt podem criptografar completamente seu repositório antes mesmo de enviá-lo para qualquer servidor. A opção ideal depende do seu nível de expertise técnica e recursos disponíveis para manutenção da infraestrutura. Nenhuma plataforma Git popular oferece criptografia completa em repouso nativamente, tornando ferramentas adicionais de criptografia essenciais para proteção máxima.

A migração para plataformas alternativas ao GitHub tem crescido devido a preocupações com privacidade, especialmente após a aquisição do GitHub pela Microsoft em 2018 e a crescente integração com ferramentas de IA que analisam código. Desenvolvedores preocupados com privacidade buscam alternativas que ofereçam maior controle sobre seus dados e transparência nas políticas de uso.

## Soluções self-hosted: máximo controle sobre seus dados

As soluções self-hosted oferecem o maior nível de controle sobre seus dados, já que todo o repositório permanece em sua própria infraestrutura.

### Forgejo: o defensor da privacidade

O **Forgejo** se destaca como a melhor opção para usuários focados em privacidade. Este fork do Gitea é gerenciado pela organização sem fins lucrativos Codeberg e.V., com governança transparente e orientada pela comunidade.

**Por que escolher:**
- Recursos completos de segurança com SECRET_KEY para dados sensíveis
- Extremamente leve (funciona até em Raspberry Pi)
- Equipe dedicada à segurança para responder a vulnerabilidades
- Compatível com GPG para verificação de assinaturas
- Compromisso explícito com privacidade como valor central
- Trabalho ativo para implementar federação via ActivityPub
- **Gerenciado por uma organização sem fins lucrativos**, reduzindo riscos comerciais

**Considerações:**
- Fork mais recente (desde 2022), menos histórico que outras opções
- Mesmo núcleo de limitações que o Gitea para criptografia de dados em repouso
- Base de usuários menor que GitLab e Gitea

### GitLab Community Edition: poderoso mas pesado

O GitLab CE oferece o conjunto mais completo de recursos de segurança entre as opções self-hosted, embora exija mais recursos.

**Por que escolher:**
- **Recursos de segurança extensos** incluindo hardening de instância
- Suporte para configurações criptografadas para recursos sensíveis
- Sistema granular de permissões em múltiplos níveis
- Conformidade com regulamentações como GDPR e HIPAA
- Possibilidade de operar em ambiente completamente isolado
- Logs detalhados de auditoria

**Considerações:**
- Consome significativamente mais recursos (mínimo 4GB RAM recomendado)
- Arquitetura mais complexa para instalação e manutenção
- Criptografia limitada para dados em repouso

### Gitea: simples e eficiente

Para quem busca simplicidade e baixo consumo de recursos, o Gitea é uma excelente opção.

**Por que escolher:**
- **Incrivelmente leve** (menos de 100MB de instalação)
- Suporte para 2FA, LDAP, e múltiplas opções de autenticação
- Verificação de commits assinados com GPG
- Fácil implementação com HTTPS/SSL e certificados Let's Encrypt
- Interface intuitiva e amigável

**Considerações:**
- Menos recursos avançados que o GitLab CE
- Mesmo modelo de limitações que o Forgejo para criptografia

### OneDev: alternativa focada em usabilidade

O OneDev é uma plataforma Git self-hosted com uma abordagem mais integrada.

**Por que escolher:**
- Interface moderna com busca inteligente de código
- Recursos de segurança incluindo 2FA e verificação GPG
- Sistema autocontido com poucas dependências externas
- Gerenciamento de segredos para pipelines

**Considerações:**
- Histórico de vulnerabilidades significativas no passado
- Comunidade menor para identificação de problemas de segurança
- Documentação menos extensa sobre hardening de segurança

## Plataformas hospedadas: quando você não quer manter infraestrutura

Para quem prefere não gerenciar sua própria infraestrutura, existem opções hospedadas que ainda oferecem bons recursos de privacidade.

### SourceHut: minimalismo com máxima privacidade

O **SourceHut** (sr.ht) se destaca como a opção hospedada mais focada em privacidade.

**Por que escolher:**
- **Design minimalista sem JavaScript** (exceto para pagamentos)
- Hospedado em hardware privado na Holanda (não usa nuvem pública)
- Política radical de coleta mínima de dados
- Sem rastreamento de usuários ou telemetria
- **Não compartilha dados com terceiros**
- Modelo transparente baseado em assinaturas, sem monetização de dados

**Considerações:**
- Interface menos refinada que concorrentes
- Ainda em fase Alpha
- Preço aproximado de $2-5 por mês

### Codeberg: governança ética na Europa

O Codeberg é uma alternativa sem fins lucrativos baseada na Europa, usando Forgejo como software.

**Por que escolher:**
- Sediada na Alemanha, com **forte conformidade às leis de privacidade da UE/GDPR**
- Hardware próprio na Europa
- Sem uso de cookies de terceiros ou rastreamento
- Mantida por doações e trabalho voluntário
- Nenhuma monetização de dados de usuários

**Considerações:**
- Recursos mais limitados que plataformas comerciais
- Infraestrutura mais restrita por ser uma organização sem fins lucrativos

### GitLab.com: equilíbrio entre recursos e privacidade

Para quem precisa de recursos avançados em uma plataforma hospedada, o GitLab.com oferece um bom equilíbrio.

**Por que escolher:**
- Certificações ISO/IEC 27001:2022 e SOC 2 Tipo 2
- Recursos avançados de varredura de segurança de código
- Criptografia em trânsito e em repouso
- Equipe especializada em segurança

**Considerações:**
- Hospedado no Google Cloud Platform
- Recursos de segurança avançados exigem planos pagos mais caros
- Menos controle sobre infraestrutura que soluções self-hosted

### Bitbucket: integração com ecossistema Atlassian

O Bitbucket é uma alternativa voltada para integração com outras ferramentas da Atlassian.

**Por que escolher:**
- Recursos de segurança empresarial como IP whitelisting
- Conformidade com várias certificações de segurança
- Integração perfeita com ferramentas Atlassian

**Considerações:**
- Menos transparente que alternativas open source
- Operada por empresa com sede nos EUA (sujeita às leis americanas)
- Utiliza infraestrutura AWS

## Criptografia do Git: a última linha de defesa

Para máxima segurança, independentemente da plataforma escolhida, considere estas ferramentas de criptografia:

### git-remote-gcrypt: criptografia total do repositório

Esta é a solução mais **robusta para proteger todo o conteúdo** do seu repositório.

**Por que escolher:**
- **Criptografia completa** do repositório Git (conteúdo e metadados)
- Criptografa mensagens de commit, nomes de arquivos e todo o conteúdo
- Compatível com qualquer serviço Git ou até simples armazenamento
- Usa GPG para gerenciamento de chaves
- O serviço de hospedagem nunca vê dados não criptografados

**Considerações:**
- Operação exclusiva por linha de comando
- Cada push é efetivamente um force push, exigindo cuidado
- Exige conhecimento básico de GPG

### git-crypt: criptografia seletiva transparente

Para quem precisa proteger apenas arquivos específicos sensíveis, o git-crypt é ideal.

**Por que escolher:**
- Integração transparente com fluxo de trabalho Git
- Criptografia/descriptografia automática durante commit/checkout
- Permite repositórios mistos (parte pública, parte privada)
- Baseado em AES-256 em modo CTR

**Considerações:**
- Não criptografa nomes de arquivos ou mensagens de commit
- Não oculta padrões de alteração ou tamanhos de arquivos
- Não suporta revogação de acesso a repositórios previamente concedidos

### Keybase Git: simplicidade com segurança

O Keybase Git oferece uma solução integrada com interface amigável.

**Por que escolher:**
- Interface de usuário fácil de usar
- Criptografia ponta-a-ponta integrada ao sistema Keybase
- Criptografia de nomes de repositórios e branches
- Gerenciamento de chaves simplificado

**Considerações:**
- Desenvolvimento incerto após aquisição pelo Zoom em 2020
- Exige uso do aplicativo Keybase
- Sem interface web ou recursos de colaboração avançados

## Comparativo de privacidade e segurança

| Recurso | GitLab CE | Forgejo | SourceHut | git-remote-gcrypt |
|---------|-----------|---------|-----------|-------------------|
| Controle de dados | Completo (self-hosted) | Completo (self-hosted) | **Hospedagem privada na Europa** | Independente da hospedagem |
| Criptografia em repouso | Parcial | Parcial | Parcial | **Completa** |
| Código aberto | Sim | Sim | Sim | Sim |
| Facilidade de uso | Moderada | Alta | Baixa | Muito baixa |
| Recursos de colaboração | Extensos | Bons | Básicos | Depende da plataforma |
| Custo | Gratuito (self-hosted) | Gratuito (self-hosted) | $2-5/mês | Gratuito |

## Como escolher a melhor opção para seu caso

Se você tiver **recursos técnicos para manutenção**, uma solução self-hosted como Forgejo ou GitLab CE oferece o maior controle sobre seus dados. Para **máxima simplicidade**, o Gitea é a melhor opção self-hosted, enquanto o Codeberg é a opção mais amigável entre os serviços hospedados.

Para **privacidade absoluta**, a combinação ideal é usar git-remote-gcrypt com qualquer plataforma de sua escolha, garantindo que seus dados estejam completamente criptografados antes mesmo de deixarem seu computador.

Para **equipes não técnicas** que precisam de segurança, o Keybase Git oferece um bom equilíbrio entre facilidade de uso e proteção, embora seu futuro seja incerto após a aquisição pelo Zoom.

Se você precisar de **conformidade com regulamentações**, o GitLab (self-hosted ou GitLab.com) oferece os recursos mais robustos para empresas, enquanto o SourceHut e Codeberg são preferíveis para projetos de código aberto e desenvolvedores individuais.

## Conclusão

Embora nenhuma plataforma ofereça privacidade perfeita por padrão, existem várias alternativas ao GitHub que priorizam segurança e privacidade. A escolha ideal depende do seu modelo de ameaça específico, recursos disponíveis para manutenção e necessidades de colaboração. Para máxima privacidade, considere combinar uma plataforma que respeite privacidade com ferramentas adicionais de criptografia, especialmente git-remote-gcrypt, que representa a proteção mais completa disponível atualmente para repositórios Git.