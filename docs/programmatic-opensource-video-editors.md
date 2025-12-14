# Editores de vídeo open source com controle programático

A seguir são listados projetos de edição de vídeo open source que permitem automação via código ou API, com detalhes de repositório, funcionalidades, linguagens, APIs, sistemas suportados, comunidade e casos de uso.

## FFmpeg  
| Característica               | Detalhes                                                                                     |
|------------------------------|----------------------------------------------------------------------------------------------|
| *Nome do projeto*          | FFmpeg ([FFmpeg - Wikipedia](https://en.wikipedia.org/wiki/FFmpeg#:~:text=FFmpeg%20is%20a%20free%20and,137%2C%20ITU))                                                                         |
| *Repositório oficial*      | [git.ffmpeg.org/ffmpeg.git](https://git.ffmpeg.org/ffmpeg.git) ([FFmpeg - Wikipedia](https://en.wikipedia.org/wiki/FFmpeg#:~:text=7.1.1,Wikidata%20%2F%203%20March%202025))               |
| *Funcionalidades principais* | Ferramenta de linha de comando para processamento multimídia: transcodificação, corte e concatenação de vídeos, aplicação de filtros e efeitos de vídeo e áudio, mux/demux, streaming etc. Suporta múltiplos formatos e normas padrões ([FFmpeg - Wikipedia](https://en.wikipedia.org/wiki/FFmpeg#:~:text=FFmpeg%20is%20a%20free%20and,137%2C%20ITU)). |
| *Linguagens*               | C, Assembly ([FFmpeg - Wikipedia](https://en.wikipedia.org/wiki/FFmpeg#:~:text=7.1.1,Wikidata%20%2F%203%20March%202025))                                                                   |
| *API/automação*            | Interface CLI (ffmpeg, ffprobe, ffplay) e bibliotecas (libavcodec, libavfilter etc.) para uso em scripts. Pode ser usado em pipelines automatizados ([FFmpeg - Wikipedia](https://en.wikipedia.org/wiki/FFmpeg#:~:text=FFmpeg%20is%20a%20free%20and,137%2C%20ITU)). |
| *SO compatíveis*           | Linux, Windows, macOS ([FFmpeg - Wikipedia](https://en.wikipedia.org/wiki/FFmpeg#:~:text=Operating%20system%20Various%2C%20including%20,computers%20%20%20122Multimedia%20framework)) (código-fonte portátil).                                |
| *Comunidade/manutenção*    | Projetos de lançamento ativo (versão 7.1.1 em mar/2025) ([FFmpeg - Wikipedia](https://en.wikipedia.org/wiki/FFmpeg#:~:text=7.1.1,Wikidata%20%2F%203%20March%202025)); enorme comunidade de desenvolvedores. É parte central de fluxos de edição de vídeo (por exemplo, usado em VLC, YouTube) ([FFmpeg - Wikipedia](https://en.wikipedia.org/wiki/FFmpeg#:~:text=FFmpeg%20is%20part%20of%20the,common%20and%20uncommon%20media%20files)). |
| *Casos de uso típicos*     | Transcodificação em massa, cortes simples por script, pós-processamento automático em servidores de vídeo, automação de edição não-linear básica (remoção de cenas, adição de legendas, normalização de áudio etc.). |

## MLT (Multimedia Framework) / Melt  
| Característica               | Detalhes                                                                                     |
|------------------------------|----------------------------------------------------------------------------------------------|
| *Nome do projeto*          | MLT Framework (e utilitário *melt*)                                                         |
| *Repositório oficial*      | [mltframework/mlt](https://github.com/mltframework/mlt) (GitHub) ([MLT - Home](https://www.mltframework.org/#:~:text=,in%20based%20API))              |
| *Funcionalidades principais* | Framework para edição multimídia não-linear via timeline e XML. Suporta tracks múltiplos, cortes, transições e filtros. O utilitário de linha de comando *melt* permite gerar vídeos a partir de arquivos XML definindo clipes, efeitos, fades, etc. ([MLT - Documentation](https://www.mltframework.org/docs/melt/#:~:text=Melt%20was%20developed%20as%20a,command%20line%20oriented%20video%20editor)) ([MLT - Home](https://www.mltframework.org/#:~:text=,in%20based%20API)).  |
| *Linguagens*               | C++ (núcleo e plugins MLT)                                                                   |
| *API/automação*            | CLI (melt) com ampla variedade de parâmetros (cortes, fades, mixagens, filtros) ([MLT - Documentation](https://www.mltframework.org/docs/melt/#:~:text=Melt%20was%20developed%20as%20a,command%20line%20oriented%20video%20editor)); scripts podem gerar ou manipular arquivos MLT XML. API C/C++ para integração em aplicações personalizadas. |
| *SO compatíveis*           | Linux, Windows, macOS ([MLT - Home](https://www.mltframework.org/#:~:text=,in%20based%20API)) (cross-platform).                                         |
| *Comunidade/manutenção*    | Ativo; teve releases recentes (v7.28.0 em set/2024, v7.30.0 em jan/2025) ([MLT - Home](https://www.mltframework.org/#:~:text=,in%20based%20API)). É usado em outros editores (Kdenlive, Shotcut) e aplicações de broadcast. |
| *Casos de uso típicos*     | Motor de edição em projetos DIY ou broadcast. Permite automação de renderização via script, geração de vídeos por modelo (XML) e integração em pipelines de transmissão. |

## GStreamer  
| Característica               | Detalhes                                                                                     |
|------------------------------|----------------------------------------------------------------------------------------------|
| *Nome do projeto*          | GStreamer                                                                                   |
| *Repositório oficial*      | [gstreamer](https://gitlab.freedesktop.org/gstreamer/gstreamer) (GitLab)                      |
| *Funcionalidades principais* | Framework modular para construção de pipelines de mídia. Suporta desde simples reprodução de áudio/vídeo até processamento complexo (mistura de áudio, edição não-linear, codificação) ([GStreamer: open source multimedia framework](https://gstreamer.freedesktop.org/#:~:text=GStreamer%20is%20a%20library%20for,linear%20editing%29%20processing)). Inclui GStreamer Editing Services para facilitar aplicações de edição de vídeo. |
| *Linguagens*               | C (núcleo), com bindings Python, Rust, etc.                                                  |
| *API/automação*            | Componentes configuráveis via código (C ou scripts Python). Permite montar gráficos de filtros e encoders por software. É usado por aplicações GNOME (p.ex. o editor Pitivi) e sistemas embarcados. |
| *SO compatíveis*           | Linux, Windows, macOS, Android, iOS ([GStreamer: open source multimedia framework](https://gstreamer.freedesktop.org/#:~:text=GStreamer%20is%20a%20library%20for,linear%20editing%29%20processing)).                                         |
| *Comunidade/manutenção*    | Ativa; lançamentos regulares (1.26.1 em abril/2025) ([GStreamer: open source multimedia framework](https://gstreamer.freedesktop.org/#:~:text=GStreamer%20is%20a%20library%20for,linear%20editing%29%20processing)). É padrão em desktops Linux e em muitas aplicações multimídia. |
| *Casos de uso típicos*     | Desenvolvimento de aplicações customizadas de edição/streaming: agregar filtros, transcodificar fluxos em tempo real, montar editores sob medida através de programação. |

## MoviePy  
| Característica               | Detalhes                                                                                     |
|------------------------------|----------------------------------------------------------------------------------------------|
| *Nome do projeto*          | MoviePy                                                                                     |
| *Repositório oficial*      | [Zulko/moviepy](https://github.com/Zulko/moviepy) (GitHub)                                   |
| *Funcionalidades principais* | Biblioteca Python de edição de vídeo: suporta cortes, concatenações, inserção de títulos, composição de clipes em timeline (edição não-linear), efeitos visuais e sonoros personalizados ([GitHub - Zulko/moviepy: Video editing with Python](https://github.com/Zulko/moviepy#:~:text=MoviePy%20,and%20creation%20of%20custom%20effects)). Leitura/escrita de diversos formatos (via FFmpeg). |
| *Linguagens*               | Python (puro)                                                                                |
| *API/automação*            | Totalmente scriptável em Python. Oferece objetos para manipular vídeos (clipes, efeitos, áudio). Ideal para edição programática, por exemplo em pipelines de processamento automático ou geração de conteúdo sob demanda. |
| *SO compatíveis*           | Linux, Windows, macOS (requer Python) ([GitHub - Zulko/moviepy: Video editing with Python](https://github.com/Zulko/moviepy#:~:text=MoviePy%20,and%20creation%20of%20custom%20effects))                                         |
| *Comunidade/manutenção*    | Ativa (lançou versão 2.0 em 2023) ([GitHub - Zulko/moviepy: Video editing with Python](https://github.com/Zulko/moviepy#:~:text=MoviePy%20,and%20creation%20of%20custom%20effects)). Usado por desenvolvedores Python em projetos de edição automatizada. |
| *Casos de uso típicos*     | Gerar vídeos por script, automatizar montagens (ex.: vídeos personalizados, slideshows gerados dinamicamente), pré-processamento de dados de vídeo em pesquisa. |

## Blender (Video Sequence Editor)  
| Característica               | Detalhes                                                                                     |
|------------------------------|----------------------------------------------------------------------------------------------|
| *Nome do projeto*          | Blender (VSE – Video Sequence Editor) ([Blender (software) - Wikipedia](https://en.wikipedia.org/wiki/Blender_(software)#:~:text=Blender%20has%20a%20node,rendering%20video%20with%20the%20VSE))                                          |
| *Repositório oficial*      | [blender/blender](https://git.blender.org/gitweb)                                            |
| *Funcionalidades principais* | Principalmente software 3D, mas inclui um editor de vídeo não-linear (VSE) integrado ([Blender (software) - Wikipedia](https://en.wikipedia.org/wiki/Blender_(software)#:~:text=Blender%20has%20a%20node,rendering%20video%20with%20the%20VSE)). Suporta transições (fade, wipes), efeitos (desfoque, correção de cor, etc.) e camadas de vídeo/áudio. Compositor node-based para pós-produção. |
| *Linguagens*               | C/C++ (núcleo do Blender); extensível via Python (API integrada) ([Blender (software) - Wikipedia](https://en.wikipedia.org/wiki/Blender_(software)#:~:text=Blender%20supports%20Python%20scripting%20for,for%20further%20automation%20and%20development)).              |
| *API/automação*            | API Python completa. É possível controlar toda a edição de vídeo por scripts Python (tanto no GUI quanto no modo batch) ([Blender (software) - Wikipedia](https://en.wikipedia.org/wiki/Blender_(software)#:~:text=Blender%20supports%20Python%20scripting%20for,for%20further%20automation%20and%20development)). Blender pode ser executado headless (sem interface) para renderização programada. |
| *SO compatíveis*           | Windows, macOS, Linux ([Blender (software) - Wikipedia](https://en.wikipedia.org/wiki/Blender_(software)#:~:text=Blender%20has%20a%20node,rendering%20video%20with%20the%20VSE))                                                         |
| *Comunidade/manutenção*    | Muito ativa (grande comunidade open source). Atualizações frequentes.                          |
| *Casos de uso típicos*     | Edição e composição avançada combinada com 3D/2D; automação de cortes/efeitos em pipelines de animação; projetos independentes de vídeo que requerem scripting detalhado. |

## Avidemux  
| Característica               | Detalhes                                                                                     |
|------------------------------|----------------------------------------------------------------------------------------------|
| *Nome do projeto*          | Avidemux ([Avidemux - Main Page](https://avidemux.sourceforge.net/#:~:text=Avidemux%20is%20a%20free%20video,queue%20and%20powerful%20scripting%20capabilities))                                                                       |
| *Repositório oficial*      | [avidemux/avidemux](https://github.com/mean00/avidemux2) (GitHub)                             |
| *Funcionalidades principais* | Editor simples para corte e filtragem de vídeo, codificação/transcodificação. Suporta vários formatos (AVI, MPEG, MP4, etc.) via FFmpeg ([Avidemux - Main Page](https://avidemux.sourceforge.net/#:~:text=Avidemux%20is%20a%20free%20video,queue%20and%20powerful%20scripting%20capabilities)). Aplicação de filtros visuais e de áudio. |
| *Linguagens*               | C++ (interface Qt) ([Avidemux - Wikipedia](https://en.wikipedia.org/wiki/Avidemux#:~:text=as%20,4%2C%20Avidemux%20also%20offers%20a))                                                              |
| *API/automação*            | Suporta scripts em JavaScript/ECMAScript via motor SpiderMonkey. Possui interface de linha de comando para automação de tarefas ([Avidemux - Main Page](https://avidemux.sourceforge.net/#:~:text=compatible%20MPEG%20files%2C%20MP4%20and,queue%20and%20powerful%20scripting%20capabilities)) ([Avidemux - Wikipedia](https://en.wikipedia.org/wiki/Avidemux#:~:text=An%20integral%20and%20important%20part,queue%20system%20is%20also%20available)). É possível gravar projetos e replicar configurações programaticamente. |
| *SO compatíveis*           | Linux, Windows, macOS ([Avidemux - Main Page](https://avidemux.sourceforge.net/#:~:text=Avidemux%20is%20available%20for%20Linux%2C,bug%20reports%20are%20always%20welcome)). Builds não oficiais para BSD.                              |
| *Comunidade/manutenção*    | Projeto maduro (v2.8.x em 2022). Comunidade menor, mas ainda recebendo atualizações e correções. |
| *Casos de uso típicos*     | Tarefas simples de edição (cortes rápidos sem recodificação completa), montagem de trechos, transcodificação em lotes usando script, extração/inserção de faixas de áudio. |

## LosslessCut  
| Característica               | Detalhes                                                                                     |
|------------------------------|----------------------------------------------------------------------------------------------|
| *Nome do projeto*          | LosslessCut ([GitHub - mifi/lossless-cut: The swiss army knife of lossless video/audio editing](https://github.com/mifi/lossless-cut#:~:text=LosslessCut%20aims%20to%20be%20the,does%20all%20the%20grunt%20work))                                                                   |
| *Repositório oficial*      | [mifi/lossless-cut](https://github.com/mifi/lossless-cut) (GitHub)                            |
| *Funcionalidades principais* | GUI simples (Electron) para cortes *lossless*: recortar, unir e reordenar trechos de vídeo/áudio sem reencodificação ([GitHub - mifi/lossless-cut: The swiss army knife of lossless video/audio editing](https://github.com/mifi/lossless-cut#:~:text=LosslessCut%20aims%20to%20be%20the,does%20all%20the%20grunt%20work)). Suporta multi-faixas (vídeo, áudio, legendas). |
| *Linguagens*               | JavaScript/TypeScript (Electron)                                                            |
| *API/automação*            | Suporta opção de linha de comando e expõe uma *API HTTP* experimental (ativa com --http-api) para controlar ações (corte, exportação, etc.) via requisições REST ([lossless-cut/api.md at master · mifi/lossless-cut · GitHub](https://github.com/mifi/lossless-cut/blob/master/api.md#:~:text=HTTP%20API)). |
| *SO compatíveis*           | Windows, macOS, Linux (aplicativo multiplataforma Electron).                                 |
| *Comunidade/manutenção*    | Muito usado (30k⭐ no GitHub), manutenção ativa. Lançamentos frequentes (versão 3.x).         |
| *Casos de uso típicos*     | Corte rápido de cenas (p.ex. para Youtubers ou videomakers) economizando tempo, sem perda de qualidade. Útil para extrair clipes, remover comerciais ou silêncios automaticamente. |

## OpenShot Video Editor  
| Característica               | Detalhes                                                                                     |
|------------------------------|----------------------------------------------------------------------------------------------|
| *Nome do projeto*          | OpenShot ([OpenShot - Wikipedia](https://en.wikipedia.org/wiki/OpenShot#:~:text=OpenShot%20Video%20Editor%20is%20a,8))                                                                     |
| *Repositório oficial*      | [OpenShot/openshot-qt](https://github.com/OpenShot/openshot-qt) (GitHub)                     |
| *Funcionalidades principais* | Editor não-linear com interface gráfica. Suporta múltiplas trilhas, cortes, transições, animações keyframe e efeitos de vídeo ([OpenShot - Wikipedia](https://en.wikipedia.org/wiki/OpenShot#:~:text=OpenShot%20Video%20Editor%20is%20a,8)) (implementados em libopenshot C++). Permite sobrepor texto, áudio, imagens e criar títulos. |
| *Linguagens*               | Python (PyQt) e C++ (libopenshot) ([OpenShot - Wikipedia](https://en.wikipedia.org/wiki/OpenShot#:~:text=Written%20inPython%20%2C%20%2076%2C,Websitewww%20.openshot%20.org)).                                           |
| *API/automação*            | Disponibiliza API Python para automação de projetos ([OpenShot - Wikipedia](https://en.wikipedia.org/wiki/OpenShot#:~:text=OpenShot%20is%20written%20in%20Python,based%20on%20the%20JUCE%20library)) e ainda oferece o *OpenShot Cloud API* (serviço REST) para edição via servidor. Scripts Python podem criar/editar projetos .osp programaticamente. |
| *SO compatíveis*           | Linux, Windows, macOS (e até ChromeOS) ([OpenShot - Wikipedia](https://en.wikipedia.org/wiki/OpenShot#:~:text=Written%20inPython%20%2C%20%2076%2C,Websitewww%20.openshot%20.org))                                      |
| *Comunidade/manutenção*    | Ativo; várias atualizações (v3.3.0 em dez/2024) ([OpenShot - Wikipedia](https://en.wikipedia.org/wiki/OpenShot#:~:text=Stable%20release)). Comunidade moderada de usuários e desenvolvedores. |
| *Casos de uso típicos*     | Ideal para iniciantes e projetos leves. Usado em escolas, para quick edits pessoais e também em prototipagem de vídeos via script (especialmente em nuvem, usando a Cloud API). |

## Flowblade Movie Editor  
| Característica               | Detalhes                                                                                     |
|------------------------------|----------------------------------------------------------------------------------------------|
| *Nome do projeto*          | Flowblade Movie Editor ([GitHub - jliljebl/flowblade: Video Editor for Linux](https://github.com/jliljebl/flowblade#:~:text=Releases))                                                       |
| *Repositório oficial*      | [jliljebl/flowblade](https://github.com/jliljebl/flowblade) (GitHub)                         |
| *Funcionalidades principais* | Editor não-linear para Linux. Suporta diversas faixas de vídeo/áudio, transições (pattern wipes, fusões, etc.) e filtros de imagem/áudio ([GitHub - jliljebl/flowblade: Video Editor for Linux](https://github.com/jliljebl/flowblade#:~:text=Image%20compositing%3A)). Recursos avançados como geradores de mídia (Fluxity), ferramenta de texto, batch rendering, G’MIC integration, etc. |
| *Linguagens*               | Python (GTK/MLT)                                                                            |
| *API/automação*            | *Fluxity*: API de scripting em Python para criar plugins/generators personalizados ([fluxity API documentation](https://jliljebl.github.io/flowblade/webhelp/fluxity.html#:~:text=FLUXITY%20SCRIPTING%20AND%20API)). Permite adicionar geradores dinâmicos (títulos animados, efeitos) ao fluxo de edição. |
| *SO compatíveis*           | Linux (Linux mint, Fedora, Ubuntu etc.).                                                    |
| *Comunidade/manutenção*    | Ativo; release 2.20 em mar/2025 ([GitHub - jliljebl/flowblade: Video Editor for Linux](https://github.com/jliljebl/flowblade#:~:text=Releases)). Comunidade menor, mas desenvolvimento contínuo. |
| *Casos de uso típicos*     | Edição avançada de vídeo em ambiente Linux. Usado por cineastas independentes e entusiastas para projetos que requerem recursos profissionais (transições customizadas, efeitos avançados) sem depender de softwares proprietários. |

### Destaque de uso na indústria e entre desenvolvedores

- *FFmpeg* e *GStreamer* são amplamente usados em aplicações profissionais (VLC, YouTube, etc.) como base de processamento multimídia ([FFmpeg - Wikipedia](https://en.wikipedia.org/wiki/FFmpeg#:~:text=FFmpeg%20is%20part%20of%20the,common%20and%20uncommon%20media%20files)) ([GStreamer: open source multimedia framework](https://gstreamer.freedesktop.org/#:~:text=GStreamer%20is%20a%20library%20for,linear%20editing%29%20processing)).  
- *Blender* (com VSE) é popular em estúdios pequenos/médios de animação e vídeos 3D, graças ao seu poderoso sistema e API Python ([Blender (software) - Wikipedia](https://en.wikipedia.org/wiki/Blender_(software)#:~:text=Blender%20has%20a%20node,rendering%20video%20with%20the%20VSE)).  
- *MoviePy, **LosslessCut* e *OpenShot* têm grande adesão entre desenvolvedores independentes e educadores para automação de edição e projetos didáticos.  
- *Flowblade* e *Avidemux* são apreciados por usuários Linux que buscam ferramentas leves para edição e scripts personalizáveis.  
- Vários projetos acima são usados em soluções corporativas de streaming e edição online (por exemplo, serviços de edição em nuvem usam FFmpeg ou OpenShot Cloud API).  

Cada projeto acima tem documentação e comunidade própria (fóruns, repositórios públicos) para suporte e evolução contínua. Todos são licenciados abertamente (GPL/LGPL/MIT), permitindo uso, modificação e integração em diversas plataformas e cenários.

*Fontes:* Informações extraídas de repositórios oficiais e documentações dos projetos ([FFmpeg - Wikipedia](https://en.wikipedia.org/wiki/FFmpeg#:~:text=7.1.1,Wikidata%20%2F%203%20March%202025)) ([FFmpeg - Wikipedia](https://en.wikipedia.org/wiki/FFmpeg#:~:text=FFmpeg%20is%20a%20free%20and,137%2C%20ITU)) ([MLT - Home](https://www.mltframework.org/#:~:text=,in%20based%20API)) ([MLT - Documentation](https://www.mltframework.org/docs/melt/#:~:text=Melt%20was%20developed%20as%20a,command%20line%20oriented%20video%20editor)) ([GStreamer: open source multimedia framework](https://gstreamer.freedesktop.org/#:~:text=GStreamer%20is%20a%20library%20for,linear%20editing%29%20processing)) ([GitHub - Zulko/moviepy: Video editing with Python](https://github.com/Zulko/moviepy#:~:text=MoviePy%20,and%20creation%20of%20custom%20effects)) ([Avidemux - Main Page](https://avidemux.sourceforge.net/#:~:text=Avidemux%20is%20a%20free%20video,queue%20and%20powerful%20scripting%20capabilities)) ([Avidemux - Wikipedia](https://en.wikipedia.org/wiki/Avidemux#:~:text=Avidemux%20is%20a%20free%20and,maintained%20and%20is%20now%20discontinued)) ([GitHub - mifi/lossless-cut: The swiss army knife of lossless video/audio editing](https://github.com/mifi/lossless-cut#:~:text=LosslessCut%20aims%20to%20be%20the,does%20all%20the%20grunt%20work)) ([lossless-cut/api.md at master · mifi/lossless-cut · GitHub](https://github.com/mifi/lossless-cut/blob/master/api.md#:~:text=HTTP%20API)) ([OpenShot - Wikipedia](https://en.wikipedia.org/wiki/OpenShot#:~:text=Written%20inPython%20%2C%20%2076%2C,Websitewww%20.openshot%20.org)) ([Blender (software) - Wikipedia](https://en.wikipedia.org/wiki/Blender_(software)#:~:text=Blender%20has%20a%20node,rendering%20video%20with%20the%20VSE)) ([fluxity API documentation](https://jliljebl.github.io/flowblade/webhelp/fluxity.html#:~:text=FLUXITY%20SCRIPTING%20AND%20API)) ([GitHub - jliljebl/flowblade: Video Editor for Linux](https://github.com/jliljebl/flowblade#:~:text=Releases)) (citado no texto).