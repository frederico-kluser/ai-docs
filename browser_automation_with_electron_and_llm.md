# Guia Técnico: Automação de Janelas de Navegador com Electron e LLM

Este guia aborda como criar janelas de navegador automatizadas com *Electron, controlá-las de forma simulada (scroll, clique, preenchimento de campos) usando bibliotecas como **Puppeteer* ou *Playwright, e integrá-las a um modelo de linguagem (LLM) via LangChain. Também tratamos de técnicas anti-detecção (user agent, delays, movimentos realistas), extração de elementos interativos do DOM, uso de **OCR (Tesseract.js)* para leitura de textos em imagens, e da interface entre o LLM e o sistema Electron. Incluímos trechos de código, bibliotecas recomendadas e referências à documentação oficial.

## 1. Criando janelas de navegador com Electron

O Electron permite criar aplicações desktop usando tecnologias web. No processo *main*, usa-se a classe BrowserWindow para abrir janelas que carregam conteúdo web. Exemplo básico (em main.js):

js
const { app, BrowserWindow } = require('electron');
app.whenReady().then(() => {
  const win = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      nodeIntegration: false, // desabilita acesso a Node no renderer
      contextIsolation: true
    }
  });
  win.loadURL('https://example.com');
});


Nesse código, a janela abre em 800×600 e carrega o site indicado. O uso de app.whenReady() garante que a API só seja usada após o evento ready do app. A documentação oficial do Electron mostra um exemplo semelhante ([BrowserWindow | Electron](https://electronjs.org/docs/latest/api/browser-window#:~:text=%2F%2F%20In%20the%20main%20process,%3D%20require%28%27electron)):  

> js
> const { BrowserWindow } = require('electron');
> const win = new BrowserWindow({ width: 800, height: 600 });
> win.loadURL('https://github.com');
>   
> * ([BrowserWindow | Electron](https://electronjs.org/docs/latest/api/browser-window#:~:text=%2F%2F%20In%20the%20main%20process,%3D%20require%28%27electron))*

Para evitar “flash” na abertura, pode-se criar a janela com show: false e só mostrá-la após o evento ready-to-show (para exibir com a página já carregada) ([BrowserWindow | Electron](https://electronjs.org/docs/latest/api/browser-window#:~:text=const%20,%7B%20win.show%28%29)). Cada janela criada tem seu próprio webContents, que oferece APIs para executar scripts ou manipular a página.

## 2. Controlando janelas e simulando interações (scroll, clique, preenchimento)

Para automatizar interações do usuário na janela Electron, duas abordagens comuns são:

- *APIs internas do Electron*: usar win.webContents para executar código JavaScript dentro da página (win.webContents.executeJavaScript) ou enviar eventos de input (win.webContents.sendInputEvent).  
- *Bibliotecas de automação*: conectar Puppeteer ou Playwright ao Chromium embutido no Electron.  

A segunda opção é poderosa e reaproveita APIs de alto nível para navegação e interações. Por exemplo, com *Puppeteer* integrado, pode-se fazer algo como: 

js
import pie from 'puppeteer-in-electron';
import puppeteer from 'puppeteer-core';
import { app, BrowserWindow } from 'electron';

async function main() {
  const browser = await pie.connect(app, puppeteer);
  const window = new BrowserWindow();
  await window.loadURL('https://example.com');
  const page = await pie.getPage(browser, window);

  // Exemplos de interações:
  await page.click('button#login');               // clicar em botão
  await page.type('input#user', 'usuario', {delay: 100}); // digitar com atraso
  await page.evaluate(() => window.scrollBy(0, 500));      // rolar a página
}
main();


Nesse código, usamos o pacote *puppeteer-in-electron* para conectar um browser Puppeteer ao Electron ([javascript - How to use puppeteer-core with electron? - Stack Overflow](https://stackoverflow.com/questions/58213258/how-to-use-puppeteer-core-with-electron#:~:text=import%20%7BBrowserWindow%2C%20app%7D%20from%20,core)). Depois obtemos um objeto page que permite usar métodos familiares (click, type, evaluate). Em outro exemplo, usando *Puppeteer-Core* (sem pacote extra), podemos apontar diretamente para o executável do Electron:

js
const puppeteer = require('puppeteer-core');
const electronPath = require('electron');
const path = require('path');

(async () => {
  const browser = await puppeteer.launch({
    executablePath: electronPath,
    args: [
      path.join(__dirname, 'main.js'),  // carrega a aplicação Electron
      '--no-sandbox',
      '--disable-setuid-sandbox'
    ]
  });
  const page = await browser.newPage();
  await page.goto('https://example.com');
  console.log(await page.title());
  await browser.close();
})();


Este exemplo ilustra o lançamento do Electron pelo Puppeteer-Core ([Electron puppeteer-core guide | Restackio](https://www.restack.io/p/puppeteer-answer-electron-puppeteer-core-guide#:~:text=const%20puppeteer%20%3D%20require%28%27puppeteer,path)), onde passamos o script principal do Electron (main.js) nos argumentos ([Electron puppeteer-core guide | Restackio](https://www.restack.io/p/puppeteer-answer-electron-puppeteer-core-guide#:~:text=%28async%20%28%29%20%3D,sandbox%27%20%5D)). É essencial incluir flags como --no-sandbox para compatibilidade ([Electron puppeteer-core guide | Restackio](https://www.restack.io/p/puppeteer-answer-electron-puppeteer-core-guide#:~:text=You%20need%20to%20specify%20the,configure%20Puppeteer%20to%20use%20it)).

O *Playwright* (by Microsoft) oferece funcionalidade semelhante. Exemplo simples em Node.js:

js
const { chromium } = require('playwright'); 
(async () => {
  const browser = await chromium.launch({ headless: false });
  const page = await browser.newPage();
  await page.goto('https://example.com');
  // Exemplo: clicar e preencher
  await page.click('#search');
  await page.fill('#search', 'teste');
  await page.screenshot({ path: 'result.png' });
  await browser.close();
})();


Ambas as bibliotecas fornecem funções como page.click(), page.fill() ou page.locator('seletor').click() ([Page interactions | Puppeteer](https://pptr.dev/guides/page-interactions#:~:text=%2F%2F%20%27button%27%20is%20a%20CSS,click)) ([Page interactions | Puppeteer](https://pptr.dev/guides/page-interactions#:~:text=Filling%20out%20an%20input)), que cuidam de esperar o elemento estar visível e interagível (redesenhando, visibilidade etc.). Por exemplo, no guia do Puppeteer temos:  

> js
> // Clicar num botão
> await page.locator('button').click();
> // Preencher um input
> await page.locator('input').fill('valor');
>   
> * ([Page interactions | Puppeteer](https://pptr.dev/guides/page-interactions#:~:text=%2F%2F%20%27button%27%20is%20a%20CSS,click)) ([Page interactions | Puppeteer](https://pptr.dev/guides/page-interactions#:~:text=Filling%20out%20an%20input))*  

Essas chamadas garantem que o elemento esteja disponível na página antes de atuar. Também é possível simular movimentos de mouse e teclado:  

js
await page.mouse.move(100, 200, { steps: 10 });
await page.mouse.click(100, 200);
await page.keyboard.type('Olá Mundo', { delay: 100 });


emulando comportamento humano. 

## 3. Técnicas para evitar detecção como bot

Sites sofisticados detectam automação analisando padrões típicos de bots. As estratégias principais para *parecer humano* incluem:

- *Modo headful vs headless*: às vezes abrir a janela com GUI (headless: false) pode ajudar, pois o modo headless (sem interface) é facilmente detectado ([How to Use Puppeteer Stealth to Avoid Detection: 6 Tips | Medium](https://medium.com/@datajournal/avoid-detection-with-puppeteer-stealth-febc3d70f319#:~:text=1)). Alterne entre modos quando possível.  
- *User Agent e idiomas: defina um *user agent realista e rotacione-o. Por exemplo:  
  js
  await page.setUserAgent('Mozilla/5.0 (...) Chrome/91.0 Safari/537.36');
    
  Sites checam o user agent para ver inconsistências. Também defina headers padrões (Accept-Language, Referer, etc.) ([How to Use Puppeteer Stealth to Avoid Detection: 6 Tips | Medium](https://medium.com/@datajournal/avoid-detection-with-puppeteer-stealth-febc3d70f319#:~:text=await%20page.setExtraHTTPHeaders%28%7B%20%27Accept,com%27%2C)) e cookies realistas.  
- *Movimentos randômicos e delays*: insira atrasos não determinísticos entre ações e movimentos irregulares do mouse/teclado. Por exemplo:  
  js
  await page.mouse.move(x1, y1, { steps: 15 });
  await page.waitForTimeout(Math.random()*1000 + 500);
  await page.keyboard.type('texto', { delay: 100 });
    
  Isso imita a variação humana no tempo de resposta ([How to Use Puppeteer Stealth to Avoid Detection: 6 Tips | Medium](https://medium.com/@datajournal/avoid-detection-with-puppeteer-stealth-febc3d70f319#:~:text=,can%20help%20mimic%20human%20behavior)).  
- *Uso de proxies*: roteie requisições por diferentes IPs ou proxies residenciais. Evite usar um único IP em várias sessões, pois IPs repetidos levantam suspeitas ([How to Use Puppeteer Stealth to Avoid Detection: 6 Tips | Medium](https://medium.com/@datajournal/avoid-detection-with-puppeteer-stealth-febc3d70f319#:~:text=const%20browser%20%3D%20await%20puppeteer.launch%28,server%3Aport%27%5D)). Por exemplo, inicie o browser com um proxy:  
  js
  const browser = await puppeteer.launch({
    args: ['--proxy-server=http://ipproxy:porta']
  });
    
- *Puppeteer Stealth*: use plugins como puppeteer-extra-plugin-stealth para mascarar variáveis do navegador (navigator.webdriver, plugins, fonts) e evitar fingerprinting.  
- *Solução de CAPTCHAs*: para captchas ou desafios JS, considere serviços de terceiros (2Captcha, Anti-CAPTCHA) ou implemente resoluções básicas. O Puppeteer-extra possui plugins para ajudar nisso (e.g. page.solveRecaptchas()).

Em resumo, essas táticas combinadas — user agent realista ([How to Use Puppeteer Stealth to Avoid Detection: 6 Tips | Medium](https://medium.com/@datajournal/avoid-detection-with-puppeteer-stealth-febc3d70f319#:~:text=Customize%20User%20Agents%3A%20Websites%20often,mimic%20different%20browsers%20and%20devices)), simulação de comportamento ([How to Use Puppeteer Stealth to Avoid Detection: 6 Tips | Medium](https://medium.com/@datajournal/avoid-detection-with-puppeteer-stealth-febc3d70f319#:~:text=,can%20help%20mimic%20human%20behavior)), delays randômicos, headers apropriados ([How to Use Puppeteer Stealth to Avoid Detection: 6 Tips | Medium](https://medium.com/@datajournal/avoid-detection-with-puppeteer-stealth-febc3d70f319#:~:text=await%20page.setExtraHTTPHeaders%28%7B%20%27Accept,com%27%2C)) e rotação de proxies ([How to Use Puppeteer Stealth to Avoid Detection: 6 Tips | Medium](https://medium.com/@datajournal/avoid-detection-with-puppeteer-stealth-febc3d70f319#:~:text=const%20browser%20%3D%20await%20puppeteer.launch%28,server%3Aport%27%5D)) — aumentam a chance de não ser bloqueado.

## 4. Identificação e extração de elementos interativos do DOM

Para que o LLM decida ações, o sistema precisa saber o estado atual da interface web. Use o DOM para listar elementos como botões (<button>), campos (<input>, <textarea>), links (<a>), selects etc. Duas abordagens comuns:

- *Query via JavaScript*: execute código na página para coletar elementos. Exemplo em Puppeteer:  
  js
  const buttons = await page.evaluate(() => {
    return Array.from(document.querySelectorAll('button')).map(b => ({
      text: b.innerText,
      selector: 'button:nth-of-type(' + (Array.from(document.querySelectorAll('button')).indexOf(b)+1) + ')'
    }));
  });
  
  Aqui obtemos texto e posições (apenas como exemplo) de todos os botões. Similarmente, document.querySelectorAll('input, select, textarea, a') lista inputs, menus e links.  
- *APIs da biblioteca*: Puppeteer e Playwright facilitam isso. Com Puppeteer, por exemplo:  
  js
  const links = await page.$$('a');
  for (const link of links) {
    const href = await link.evaluate(node => node.href);
    const text = await link.evaluate(node => node.innerText);
    // ...
  }
    
  Ou usando locators do Playwright:  
  js
  const buttonCount = await page.locator('button').count();
  for (let i = 0; i < buttonCount; i++) {
    await page.locator('button').nth(i).click(); // ou obter propriedades
  }
    

Ao identificar elementos, filtre apenas os *visíveis e habilitados* (Puppeteer/Playwright ajudam com locators que já consideram visibilidade). Use funções como page.waitForSelector() ou locator().click() que aguardam a condição certa. Referências oficiais ensinam a usar page.locator('button').click() e .fill() para textos ([Page interactions | Puppeteer](https://pptr.dev/guides/page-interactions#:~:text=%2F%2F%20%27button%27%20is%20a%20CSS,click)) ([Page interactions | Puppeteer](https://pptr.dev/guides/page-interactions#:~:text=Filling%20out%20an%20input)), garantindo interação segura.

## 5. Uso de OCR (Tesseract.js) para leitura de elementos visuais

Quando textos ou dados relevantes estão *embutidos em imagens* (por exemplo, captcha de texto ou gráficos) e não no DOM, é necessário OCR. O [Tesseract.js](https://tesseract.projectnaptha.com/) é uma biblioteca JavaScript que roda em Node ou browser para reconhecimento de texto ([Tesseract.js | Pure Javascript OCR for 100 Languages!](https://tesseract.projectnaptha.com/#:~:text=script%20detection%2C%20a%20simple%20interface,on%20a%20server%20with%20NodeJS)). 

Primeiro, capture a região da página que contém o texto. Por exemplo, com Puppeteer:  

js
const screenshot = await page.screenshot({ path: 'capcha.png' });
// ou para região específica: await page.screenshot({ clip: {x, y, width, height} });


Em seguida, use o Tesseract.js:

js
const tesseract = require('tesseract.js');
tesseract.recognize('capcha.png', 'por')  // especifica idioma, se conhecido
  .then(result => {
    console.log(result.data.text);
  })
  .catch(err => {
    console.error('Erro OCR:', err);
  });


Esse código (adaptado de guias práticos ([Convert Images to Text in Node.js with Tesseract.js: A Step-by-Step Guide | Medium](https://medium.com/@abhishekchamoli007/convert-images-to-text-in-node-js-with-tesseract-js-a-step-by-step-guide-b4fa5f5ee809#:~:text=%2F%2F%20Import%20the%20Tesseract,js))) reconhece o texto da imagem. A configuração (idioma, engine) pode ser ajustada conforme necessário. O Tesseract suporta mais de 100 idiomas e pode ser usado no próprio Electron (rodando em Node) ([Tesseract.js | Pure Javascript OCR for 100 Languages!](https://tesseract.projectnaptha.com/#:~:text=script%20detection%2C%20a%20simple%20interface,on%20a%20server%20with%20NodeJS)). Use-o para traduzir imagens em texto compreensível pelo LLM.

## 6. Interface entre o LLM e o Electron (via LangChain)

Para que o LLM (modelo de linguagem) controle a automação, é necessário criar uma *ponte* entre o estado da UI e as ações. A ideia é:

1. *Obter estado da interface*: extrair textos, labels e propriedades dos elementos (como no item 4) ou até screenshots. Envie essas informações em prompts para o LLM.
2. *Decisão do LLM*: o LLM, via LangChain.js (ou Python), avalia o contexto e retorna um comando ou uma sequência de ações (ex: “clicar no botão ‘Confirmar’”, “preencher campo de busca com X”).
3. *Execução da ação*: o Electron interpreta o output do LLM e executa a ação correspondente no BrowserWindow usando Puppeteer/Playwright (como page.click, page.type, etc.).

Em LangChain.js, você pode definir “tools” (ferramentas) que o LLM pode usar. Por exemplo, criar uma ferramenta de clique:

js
import { Tool } from 'langchain/tools';
const clickTool = new Tool({
  name: 'click',
  description: 'Clica num elemento dado um seletor CSS',
  func: async ({ selector }) => {
    await page.click(selector);
    return `Clique em ${selector} executado.`;
  }
});


E um LLMChain que usa esta ferramenta junto a ChatOpenAI ([Web Browser Tool | ️ Langchain](https://js.langchain.com/docs/integrations/tools/webbrowser/#:~:text=pnpm%20add%20%40langchain%2Fopenai%20%40langchain%2Fcore)). Por exemplo:

js
import { ChatOpenAI } from '@langchain/openai';
import { AgentExecutor, initializeAgent } from 'langchain/agents';

const model = new ChatOpenAI({ temperature: 0 });
const tools = [clickTool, /* outros tools como readTextTool, fillTool, etc. */];
const executor = await initializeAgent(tools, model, 'zero-shot-react-description');

const result = await executor.call({ input: 'Clique no botão de login' });
console.log(result.output);


Neste fluxo, LangChain trata de chamar o LLM (por ex. ChatGPT) com prompt adequado, e lê a resposta que pode incluir instruções estruturadas (JSON ou texto) para acionar clickTool, fillTool, etc. 

O artigo “Mastering Browser Automation with LangChain Agent and Playwright” demonstra fluxo semelhante em Python ([Mastering Browser Automation with Langchain Agent and Playwright Tools | by Harshal Abhyankar | Medium](https://medium.com/@abhyankarharshal22/mastering-browser-automation-with-langchain-agent-and-playwright-tools-c70f38fddaa6#:~:text=from%20langchain_community,agents%20import%20AgentExecutor%2C%20create_openai_tools_agent)) (usando kit de ferramentas do Playwright). Em JavaScript, o conceito é análogo: configura-se um *Agent* com ferramentas que abstraem ações no navegador. O LLM age como co-piloto, usando as ferramentas para interagir na UI.

Finalmente, use um protocolo de comunicação (por exemplo, ipcMain.handle no Electron) se o LLM rodar em processo separado, ou integre o LangChain.js diretamente no processo principal do Electron, para trocar mensagens ou comandos. O importante é sempre refletir o *estado atual da interface* no prompt (texto da página, opções visíveis, etc.), de modo que o LLM tome decisões baseadas no contexto real da janela.

## 7. Exemplos de arquitetura e código de orquestração

A arquitetura geral pode ser:

- *Electron (Main Process)*: gerencia janelas (BrowserWindow), carrega o conteúdo e expõe uma API interna (via WebContents ou IPC) para executar comandos (clique, scroll, capturas).
- *Controlador de Automação*: roda dentro do Electron (por ex. usando Puppeteer-core) para acionar interações no BrowserWindow conforme instruções.
- *LLM/Agent (LangChain)*: recebe do controlador o estado da UI (texto, listas de elementos, imagem) e retorna a ação a tomar. Pode rodar no mesmo processo ou comunicação por IPC/HTTP.
- *Fluxo: [Estado da UI] → **LLM* → [Ação (click, type, etc)] → *Electron/Puppeteer* executa → atualiza [estado da UI] → (loop).

Exemplo de inicialização combinada (Node.js):

js
// main.js (processo principal do Electron)
const { app, BrowserWindow, ipcMain } = require('electron');
const puppeteer = require('puppeteer-core');
const { initializeAgent } = require('langchain/agents');
const { ChatOpenAI } = require('@langchain/openai');
const { WebBrowser } = require('langchain/tools/webbrowser');

async function createWindow() {
  const win = new BrowserWindow({ width: 1200, height: 800 });
  await win.loadURL('https://example.com');
  
  // Conectar Puppeteer-core ao Chromium do Electron
  const browser = await puppeteer.launch({
    executablePath: require('electron'), 
    args: ['--no-sandbox','--disable-setuid-sandbox']
  });
  const page = await browser.newPage();
  await page.goto('https://example.com');

  // Configurar LangChain Agent com ferramenta de navegador
  const model = new ChatOpenAI({ temperature: 0 });
  const webTool = new WebBrowser(); // ferramenta que faz requisições HTTP e lê HTML
  const agent = await initializeAgent([webTool], model, 'zero-shot-react-description');

  // Exemplo de loop simples
  const pageText = await page.$eval('body', el => el.innerText);
  const response = await agent.call({ input: `Estou vendo o texto:\n${pageText}\nQual ação fazer?` });
  console.log('LLM diz:', response.output);
  // Interpretar resposta e executar, por exemplo:
  if (response.output.includes('clicar')) {
    await page.click('#submit');
  }
}

app.whenReady().then(createWindow);


Neste exemplo ilustrativo, após abrir a janela e navegar, usamos uma ferramenta de navegador genérica (WebBrowser) para o LLM extrair informação. Em casos reais, você criaria tools customizadas para clicar, ler texto de seletores específicos e preencher campos. O LLM (via LangChain) recebe o texto visível e decide (response.output), então o código interpreta isso e chama page.click, page.type, etc.

Para detalhes de scaffolding, veja no guia oficial do Puppeteer-Core como lançar o Electron com Puppeteer ([Electron puppeteer-core guide | Restackio](https://www.restack.io/p/puppeteer-answer-electron-puppeteer-core-guide#:~:text=%28async%20%28%29%20%3D,sandbox%27%20%5D)) e exemplos de código para cada interação. Use bibliotecas atualizadas (@langchain/openai, langchain/agents etc.) conforme a documentação do LangChain.js. Lembre-se de rodar o Electron em modo não headless (headless: false) durante o desenvolvimento e usar slowMo para debugar passo a passo, garantindo que as ações estejam sincronizadas com a interface do usuário.

Este guia, com trechos de código e links à documentação oficial ([BrowserWindow | Electron](https://electronjs.org/docs/latest/api/browser-window#:~:text=%2F%2F%20In%20the%20main%20process,%3D%20require%28%27electron)) ([Page interactions | Puppeteer](https://pptr.dev/guides/page-interactions#:~:text=%2F%2F%20%27button%27%20is%20a%20CSS,click)) ([Electron puppeteer-core guide | Restackio](https://www.restack.io/p/puppeteer-answer-electron-puppeteer-core-guide#:~:text=const%20puppeteer%20%3D%20require%28%27puppeteer,path)), oferece um panorama completo para arquitetar um sistema de automação de navegador “humanizado” usando Electron, Puppeteer/Playwright e LLM via LangChain. 

*Referências:* Documentação oficial do Electron (BrowserWindow) ([BrowserWindow | Electron](https://electronjs.org/docs/latest/api/browser-window#:~:text=%2F%2F%20In%20the%20main%20process,%3D%20require%28%27electron)), Puppeteer/Playwright guides ([Page interactions | Puppeteer](https://pptr.dev/guides/page-interactions#:~:text=%2F%2F%20%27button%27%20is%20a%20CSS,click)) ([The NodeJS Playwright Guide | ScrapeOps](https://scrapeops.io/playwright-web-scraping-playbook/nodejs-playwright-guide/#:~:text=import%20,playwright)), artigos sobre evasão de bot ([How to Use Puppeteer Stealth to Avoid Detection: 6 Tips | Medium](https://medium.com/@datajournal/avoid-detection-with-puppeteer-stealth-febc3d70f319#:~:text=Customize%20User%20Agents%3A%20Websites%20often,mimic%20different%20browsers%20and%20devices)) ([How to Use Puppeteer Stealth to Avoid Detection: 6 Tips | Medium](https://medium.com/@datajournal/avoid-detection-with-puppeteer-stealth-febc3d70f319#:~:text=await%20page.setExtraHTTPHeaders%28%7B%20%27Accept,com%27%2C)), e exemplos de integração Puppeteer+Electron ([Electron puppeteer-core guide | Restackio](https://www.restack.io/p/puppeteer-answer-electron-puppeteer-core-guide#:~:text=%28async%20%28%29%20%3D,sandbox%27%20%5D)) ([javascript - How to use puppeteer-core with electron? - Stack Overflow](https://stackoverflow.com/questions/58213258/how-to-use-puppeteer-core-with-electron#:~:text=import%20%7BBrowserWindow%2C%20app%7D%20from%20,core)), Tesseract.js ([Tesseract.js | Pure Javascript OCR for 100 Languages!](https://tesseract.projectnaptha.com/#:~:text=script%20detection%2C%20a%20simple%20interface,on%20a%20server%20with%20NodeJS)) ([Convert Images to Text in Node.js with Tesseract.js: A Step-by-Step Guide | Medium](https://medium.com/@abhishekchamoli007/convert-images-to-text-in-node-js-with-tesseract-js-a-step-by-step-guide-b4fa5f5ee809#:~:text=%2F%2F%20Import%20the%20Tesseract,js)) e LangChain tools ([Web Browser Tool | ️ Langchain](https://js.langchain.com/docs/integrations/tools/webbrowser/#:~:text=pnpm%20add%20%40langchain%2Fopenai%20%40langchain%2Fcore)).