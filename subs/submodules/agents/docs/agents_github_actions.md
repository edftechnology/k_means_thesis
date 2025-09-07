# agents.md

## Missão do Agente
Você é responsável por manter, criar e atualizar workflows no GitHub Actions, garantindo automação confiável de testes, builds e deploys. Todas as alterações devem ser validadas antes de integrar na branch principal.

O agente deve:
- Garantir que workflows sigam boas práticas e padrões definidos.
- Manter os workflows eficientes e sem jobs redundantes.
- Testar alterações em branches de desenvolvimento antes de aplicar na principal.
- Garantir compatibilidade com todas as versões e sistemas suportados.

---

## Procedimento de Exploração do Repositório

### Listar workflows existentes
```bash
ls -1 .github/workflows
```

### Validar sintaxe de todos os workflows
```bash
act -n
```
> É necessário ter o `act` instalado para executar workflows localmente.

### Verificar logs de execução de workflows no GitHub
1. Acesse o repositório no GitHub.
2. Vá até **Actions**.
3. Abra o workflow desejado para inspecionar logs.

### Buscar jobs e steps repetidos
```bash
grep -R "run:" .github/workflows
```

### Testar workflows localmente
```bash
act
```

---

## Padrões de Workflow

- Nome dos workflows em inglês, descritivos e concisos.
- Nome dos jobs deve seguir padrão `snake_case` ou `kebab-case`.
- Reutilizar actions já testadas antes de adicionar novas.
- Utilizar caching (`actions/cache`) sempre que possível para otimizar execução.
- Sempre definir `on:` de forma restritiva para evitar execuções desnecessárias.

---

## Fluxo de Trabalho Recomendado

1. Criar branch para alterar workflows:
```bash
git checkout -b ci/update_workflows
```

2. Editar arquivos em `.github/workflows/`.

3. Validar localmente:
```bash
act -n
```

4. Commitar alterações:
```bash
git add .github/workflows
git commit -m "[CI] Atualiza workflows"
```

5. Abrir Pull Request para revisão.

---

## Segurança
- Evitar usar segredos diretamente no código.
- Utilizar `secrets.GITHUB_TOKEN` ou segredos configurados no repositório.
- Revisar permissões mínimas necessárias (`permissions:`) para cada workflow.
- Não usar `pull_request_target` sem validação extra de segurança.

---

## Checklist Antes do Commit
- [x] Workflows validados localmente com `act`
- [x] Sintaxe YAML validada
- [x] Jobs otimizados e sem redundância
- [x] Segredos e permissões revisados
- [x] Logs de execução revisados
- [x] Documentação dos workflows atualizada

---

## Referências
- GitHub Actions Documentation: https://docs.github.com/actions  
- Awesome Actions: https://github.com/sdras/awesome-actions  
- ACT (local runner): https://github.com/nektos/act  
