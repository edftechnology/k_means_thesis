# agents.md

## Missão do Agente
Você é responsável por manter a integridade do histórico do repositório Git, garantindo commits claros, branches organizadas e fluxo de trabalho consistente. Todas as alterações devem seguir as boas práticas de versionamento e integração contínua.

O agente deve:
- Manter histórico limpo e legível.
- Seguir convenções de nomenclatura de branches e commits.
- Garantir que o código passe por testes antes de ser integrado.
- Resolver conflitos de forma segura e documentada.

---

## Procedimento de Exploração do Repositório

### Verificar estado atual
```bash
git status
```

### Listar branches
```bash
git branch -a
```

### Ver histórico recente
```bash
git log --oneline --graph --decorate -n 20
```

### Ver mudanças não commitadas
```bash
git diff
```

### Ver commits não enviados ao remoto
```bash
git log origin/main..HEAD --oneline
```

---

## Fluxo de Trabalho Recomendado

### Criar nova branch
```bash
git checkout -b feature/nome_funcionalidade
```

### Adicionar alterações
```bash
git add arquivo1.py arquivo2.py
```

### Commit com mensagem padronizada
```bash
git commit -m "[Tipo] Descrição breve"
```
Tipos comuns: `Feat`, `Fix`, `Refactor`, `Docs`, `Test`, `Chore`.

### Atualizar branch local
```bash
git pull origin main --rebase
```

### Enviar branch para remoto
```bash
git push origin feature/nome_funcionalidade
```

---

## Boas Práticas

- Pequenos commits, cada um com uma mudança lógica única.
- Mensagens de commit descritivas e no imperativo.
- Evitar commits diretos na branch `main` ou `master`.
- Sempre atualizar a branch antes de criar PR.

---

## Resolução de Conflitos
- Usar `git status` para identificar arquivos em conflito.
- Editar arquivos e resolver conflitos manualmente.
- Após resolver:
  ```bash
  git add arquivo_conflito.txt
  git rebase --continue
  ```
- Testar o projeto após a resolução.

---

## Limpeza e Organização
- Remover branches locais já mescladas:
  ```bash
  git branch --merged | grep -v "main" | xargs git branch -d
  ```
- Limpar branches remotas obsoletas:
  ```bash
  git fetch --prune
  ```

---

## Checklist Antes do Commit
- [x] Testes executados e aprovados
- [x] Código revisado e formatado
- [x] Nenhum arquivo temporário ou sensível adicionado
- [x] Mensagem de commit clara

---

## Referências
- Pro Git Book: https://git-scm.com/book  
- Git Documentation: https://git-scm.com/doc  
