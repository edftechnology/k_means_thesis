#!/usr/bin/env python
# coding: utf-8

# # Como instalar o `AGENTS.md` no `Linux Ubuntu`
# 
# ## Resumo
# 
# Este documento apresenta os passos necessários para obter o arquivo `AGENTS.md` no `Linux Ubuntu`.
# 
# ## _Abstract_
# 
# _This document shows the steps required to obtain the `AGENTS.md` file on `Linux Ubuntu`._
# 
# ## Descrição
# 
# ### `AGENTS.md`
# 
# O `AGENTS.md` é um arquivo de documentação que reúne diretrizes para agentes que interagem com repositórios Git.
# 
# ## 1. Instalar o `AGENTS.md` no `Linux Ubuntu`
# 
# Para instalar o `AGENTS.md`, siga os passos abaixo:
# 
# 1. Abra o `Terminal Emulator`. Você pode fazer isso pressionando: `Ctrl + Alt + T`
# 
# 2. Certifique-se de que seu sistema esteja limpo e atualizado.
# 
#     2.1 Limpar o `cache` do gerenciador de pacotes `apt`. Especificamente, ele remove todos os arquivos de pacotes (`.deb`) baixados pelo `apt` e armazenados em `/var/cache/apt/archives/`. Digite o seguinte comando:
#     ```bash
#     sudo apt clean
#     ```
# 
#     2.2 Remover pacotes `.deb` antigos ou duplicados do `cache` local. É útil para liberar espaço, pois remove apenas os pacotes que não podem mais ser baixados (ou seja, versões antigas de pacotes que foram atualizados). Digite o seguinte comando:
#     ```bash
#     sudo apt autoclean
#     ```
# 
#     2.3 Remover pacotes que foram automaticamente instalados para satisfazer as dependências de outros pacotes e que não são mais necessários. Digite o seguinte comando:
#     ```bash
#     sudo apt autoremove -y
#     ```
# 
#     2.4 Buscar as atualizações disponíveis para os pacotes que estão instalados em seu sistema. Digite o seguinte comando e pressione `Enter`:
#     ```bash
#     sudo apt update
#     ```
# 
#     2.5 **Corrigir pacotes quebrados**: Isso atualizará a lista de pacotes disponíveis e tentará corrigir pacotes quebrados ou com dependências ausentes:
#     ```bash
#     sudo apt --fix-broken install
#     ```
# 
#     2.6 Limpar o `cache` do gerenciador de pacotes `apt` novamente:
#     ```bash
#     sudo apt clean
#     ```
# 
#     2.7 Para ver a lista de pacotes a serem atualizados, digite o seguinte comando e pressione `Enter`:
#     ```bash
#     sudo apt list --upgradable
#     ```
# 
#     2.8 Realmente atualizar os pacotes instalados para as suas versões mais recentes, com base na última vez que você executou `sudo apt update`. Digite o seguinte comando e pressione `Enter`:
#     ```bash
#     sudo apt full-upgrade -y
#     ```
# 
# 3. Baixe o `AGENTS.md` e verifique seu conteúdo:
#     ```bash
#     curl -O https://exemplo.com/AGENTS.md
#     cat AGENTS.md
#     ```
# 
# ## 2. Abrir o arquivo `AGENTS.md`
# 
# Você pode abrir o `AGENTS.md` com um editor de texto, por exemplo:
# ```bash
# nano AGENTS.md
# ```
# Esse comando abre a interface do editor carregando o arquivo `AGENTS.md`.
# 
# ## 3. Usar uma variável de terminal para definir o arquivo
# 
# Também é possível definir o caminho em uma variável antes de abrir o `AGENTS.md`:
# ```bash
# file_path="AGENTS.md"
# cat "$file_path"
# ```
# 
# ## Referências
# 
# [1] OPENAI. ***OpenAI Codex Overview***. Disponível em: <https://platform.openai.com/docs/codex/overview>. Acessado em: 14/08/2025 17:44.
# 
