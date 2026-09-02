# Como rodar este projeto

## 1. Confirme se tem Python instalado
Abra o aplicativo Terminal (Cmd+Espaço, digite "Terminal") e rode:

    python3 --version

Se aparecer uma versão (ex: Python 3.11), siga para o passo 2.
Se der erro, baixe em https://www.python.org/downloads/ e instale antes de continuar.

## 2. Entre na pasta do projeto
Arraste a pasta do projeto pro Terminal depois de digitar "cd " (com espaço), ou digite
o caminho manualmente:

    cd caminho/para/elevenlabs-voice-clone-test

## 3. Crie um ambiente isolado
Isso evita que as bibliotecas deste projeto bagunçem outras coisas no seu Mac.

    python3 -m venv venv
    source venv/bin/activate

Você vai ver "(venv)" aparecer no início da linha do Terminal quando estiver ativo.
Precisa rodar o "source venv/bin/activate" toda vez que abrir um novo Terminal
pra continuar trabalhando neste projeto.

## 4. Instale as dependências
    pip install -r requirements.txt

Também precisa do ffmpeg instalado no sistema (não é pacote Python,
é usado pelo clone_voice.py para converter os áudios para MP3 antes
do upload, e pelo librosa para ler formatos como m4a e ogg). Se não
tiver, instale com:

    brew install ffmpeg

Se não tiver o Homebrew instalado, baixe em https://brew.sh primeiro.

## 5. Configure sua chave de API
Copie o arquivo de exemplo:

    cp .env.example .env

Abra o arquivo .env num editor de texto (TextEdit serve) e cole sua chave de API,
que fica em elevenlabs.io, no seu perfil, seção "API Keys" (precisa de plano pago
pra Instant Voice Cloning).

Nunca coloque essa chave direto nos scripts, nem suba o arquivo .env pro GitHub.
Ele já está listado no .gitignore pra não subir por acidente.

## 6. Organize seus áudios gravados
Se seus arquivos já seguem uma nomenclatura própria diferente da
esperada pelo projeto, crie uma pasta raw/ na raiz do projeto, coloque
os 14 arquivos originais lá dentro (sem renomear nada), e rode:

    python scripts/setup_from_raw.py

Isso copia os arquivos pra samples/ e reference/ já com os nomes
corretos, baseado no mapeamento definido no topo do script. Confira
a saída no Terminal pra garantir que todos os 14 arquivos foram
reconhecidos, nenhum deve aparecer como "não reconheci o padrão".

Se preferir nomear manualmente, cada condição precisa de DOIS
arquivos, com o mesmo nome (sem extensão), em pastas diferentes.
Qualquer formato comum funciona (wav, mp3, m4a, ogg, oga, flac):

    samples/condition_bad.m4a     (parágrafo longo, usado pra clonar)
    reference/condition_bad.m4a   (frase curta de teste, mesma que a
                                    IA vai gerar, gravada na mesma
                                    condição física)

A frase curta de referência é sempre a mesma:
"This is a voice cloning test to evaluate how the quality of the
original recording affects the generated result."

## 7. Rode os scripts, nesta ordem
    python scripts/clone_voice.py
    python scripts/generate_speech.py
    python scripts/analyze.py

## 8. Confira os resultados
Os áudios gerados pela IA e os gráficos de espectrograma vão aparecer
dentro da pasta results/.

## 9. Preencha o README.md com suas observações
Depois disso, é só seguir os passos de upload pro GitHub que já foram explicados
na conversa (criar repositório público, Add file > Upload files, confirmar
visibilidade pública, copiar o link).
