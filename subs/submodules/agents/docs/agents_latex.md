# AGENTS.md

## Missão do Agente
Você é responsável por manter e evoluir este projeto LaTeX, garantindo consistência de formatação, organização dos arquivos e compatibilidade com as diretrizes estabelecidas. Todas as alterações devem preservar a estrutura do documento e evitar erros de compilação.

O agente deve:
- Mapear a estrutura do projeto antes de alterações.
- Compreender o estilo e padrão adotado (pacotes, comandos, macros).
- Garantir que a compilação final ocorra sem erros ou warnings desnecessários.
- Manter organização de arquivos e referências bibliográficas.

---

## Procedimento de Exploração Inteligente

### Mapear estrutura de diretórios
```bash
tree -L 3 --dirsfirst
```

### Localizar arquivos principais e de configuração
```bash
ls *.tex *.sty *.cls *.bib
```

### Detectar pacotes utilizados
```bash
grep -R "\usepackage" *.tex
```

### Detectar comandos e macros definidos
```bash
grep -R "\newcommand" *.tex
grep -R "\renewcommand" *.tex
grep -R "\DeclareMathOperator" *.tex
```

### Localizar figuras e tabelas
```bash
grep -R "\begin{figure}" *.tex
grep -R "\begin{table}" *.tex
```

### Verificar presença de referências bibliográficas
```bash
grep -R "\cite{" *.tex
grep -R "@article" *.bib
```

### Compilar documento (XeLaTeX recomendado para UTF-8)
```bash
latexmk -xelatex main.tex
```

### Limpar arquivos temporários
```bash
latexmk -c
```

---

## Padrões de Código LaTeX
- Utilizar codificação UTF-8.
- Seguir padrão de nomenclatura de arquivos em minúsculas e com underscore (`_`).
- Centralizar definições de macros e comandos em um único arquivo (`macros.tex`).
- Pacotes essenciais devem ser carregados no preâmbulo principal (`main.tex` ou equivalente).
- Evitar redefinir comandos padrão sem justificativa.

---

## Estrutura Recomendada
```
project/
│── main.tex            # Arquivo principal
│── preamble.tex        # Pacotes e configurações globais
│── macros.tex          # Definições de comandos
│── chapters/           # Capítulos do documento
│── figures/            # Imagens
│── tables/             # Tabelas
│── references.bib      # Bibliografia
```

---

## Testes e Validação
- Compilar com `latexmk` para garantir consistência.
- Evitar warnings como "Overfull hbox" e "Undefined references".
- Conferir sumário, listas de figuras e tabelas após cada modificação.
- Garantir que todas as referências `\ref{}` e `\cite{}` possuam destino válido.

---

## Fluxo de Trabalho (Git)
- Criar branch:
  ```bash
  git checkout -b feature/nome
  ```
- Commits:
  ```
  [Tipo] Descrição curta
  ```
- Antes do PR:
  - Compilar e verificar documento final.
  - Garantir que não há arquivos temporários no commit.

---

## Segurança
- Não incluir arquivos PDF compilados no repositório, exceto se especificado.
- Adicionar arquivos temporários e de build ao `.gitignore`:
  ```
  *.aux
  *.log
  *.toc
  *.out
  *.fls
  *.fdb_latexmk
  *.synctex.gz
  ```

---

## Checklist Antes do Commit
- [x] Compilação sem erros
- [x] Nenhum warning relevante
- [x] Sumário e listas atualizados
- [x] Referências válidas
- [x] Estrutura de arquivos organizada

---

## Referências
- LATEX Project: https://www.latex-project.org/  
- Overleaf LaTeX Guides: https://www.overleaf.com/learn  
