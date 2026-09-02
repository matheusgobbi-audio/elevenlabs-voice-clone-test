# Teste de qualidade de clonagem de voz: como a captação afeta o resultado

## Hipótese
A qualidade técnica da gravação de entrada (ruído de fundo, captação, processamento)
afeta diretamente a fidelidade do clone de voz gerado pela ElevenLabs.

## Metodologia
Gravei o mesmo texto de entrada em 7 condições diferentes de captação, cobrindo
desde uso comum (celular em casa) até estúdio tratado com controle técnico:

**Fase 1, casa, celular:**
- **phone_home_open**: celular, sala de casa, janela aberta (ruído externo presente)
- **phone_home_closed**: celular, sala de casa, janela fechada
- **whatsapp_home_closed**: mesma sala fechada, mas enviado como mensagem de voz do
  WhatsApp (compressão e processamento próprios do app)

**Fase 2, estúdio:**
- **phone_studio**: celular, dentro do estúdio (isola o efeito do dispositivo,
  mantendo o ambiente controlado)
- **studio_clean**: microfone de estúdio, referência limpa, sem vazamento
- **studio_noise**: microfone de estúdio, com ruído de fundo controlado (aspirador
  ou chiado ligado)
- **studio_96_32**: microfone de estúdio, 96kHz/32bit, comparado contra a
  referência limpa para testar se especificação acima do mínimo recomendado
  pela ElevenLabs (22kHz) muda algo perceptível

Cada gravação foi enviada para a API da ElevenLabs (Instant Voice Cloning) para criar
um clone separado. Em seguida, pedi à API para gerar a mesma frase de teste usando
cada clone, isolando a variável de captação como o único fator diferente entre eles.

**Nota sobre formato de upload:** por padrão, todos os arquivos são convertidos para
MP3 320kbps antes do envio, seguindo a recomendação oficial da ElevenLabs (a
documentação deles afirma que WAV não melhora a qualidade do clone e pode causar
problemas no upload). Exceção: `studio_96_32` foi enviado no formato nativo WAV,
sem conversão, deliberadamente, para comparar minha entrega padrão de estúdio
(`studio_clean`, MP3, uso normal) contra uma captura elevada de propósito (WAV,
96kHz/32bit). Ou seja, esse par testa a diferença entre "entrega padrão" e
"captura excepcional" como pacote, compressão e especificação mudando juntas, não
um teste isolado de sample rate/bit depth puro.

**Limitação conhecida:** como `studio_clean` também serve de referência nas
comparações de ambiente e ruído (`phone_studio`, `studio_noise`, que também passam
pela conversão MP3), essas comparações específicas mantêm o formato consistente
entre si, sem essa variável extra.

## Resultados
[Cole aqui os espectrogramas gerados em results/, um por condição, com uma linha de
análise técnica sua para cada um: o que você identifica como engenheiro de áudio]

## Conclusão
[O que você recomendaria a um cliente da ElevenLabs antes de enviar áudio para
clonagem, baseado no que você observou neste teste]

## Como rodar este projeto
Ver INSTRUCOES.md
