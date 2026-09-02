Coloque aqui a gravação da FRASE CURTA de teste (a mesma que o
generate_speech.py pede pra IA gerar), uma por condição, com o
MESMO nome de arquivo (sem extensão) usado em samples/.

Formato: qualquer um destes é aceito, sem conversão manual: wav, mp3,
m4a, ogg, oga, flac. A extensão pode ser diferente da usada em
samples/ para a mesma condição, o que importa é o nome do arquivo
(sem extensão) ser idêntico.

Frase exata a gravar em cada condição:
"This is a voice cloning test to evaluate how the quality of the
original recording affects the generated result."

Exemplo: se em samples/ você tem phone_home_open.m4a (o parágrafo
longo usado pra clonar), aqui em reference/ deve existir
phone_home_open.m4a ou phone_home_open.wav (qualquer formato aceito),
contendo só essa frase curta gravada na mesma condição física.

Isso existe pra comparação justa: o analyze.py compara esse arquivo
(original, frase curta) com o áudio que a IA gerou (mesma frase
curta), em vez de comparar com o parágrafo longo de clonagem, que
tem texto diferente e invalidaria a comparação.
