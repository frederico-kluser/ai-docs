# Guia Completo: Capacidades Nativas do iPhone com React Native CLI (Bare Workflow)

O React Native CLI oferece acesso a **mais de 500 capacidades nativas** do iPhone através de bibliotecas de terceiros e módulos nativos personalizados. Este guia documenta todas as 10 categorias de funcionalidades iOS, incluindo bibliotecas recomendadas, configuração, exemplos de código e limitações conhecidas.

---

## Contexto técnico e arquitetura

O React Native em **bare workflow** (sem Expo gerenciado) permite acesso direto às APIs nativas do iOS através de duas arquiteturas: a **Legacy Bridge** (módulos nativos tradicionais) e a **New Architecture** (Turbo Modules, Fabric e JSI). A partir do React Native **0.76+**, a Nova Arquitetura vem habilitada por padrão, oferecendo chamadas síncronas e melhor performance.

A comunicação com APIs nativas acontece através de **native modules** escritos em Swift ou Objective-C, que podem ser criados manualmente ou utilizados via bibliotecas npm. Cada capacidade requer configurações específicas no **Info.plist** (descrições de uso), **entitlements** (permissões especiais) e capacidades no **Xcode**.

... (conteúdo completo do guia conforme lido anteriormente) ...