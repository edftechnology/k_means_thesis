# agents.md

## Missão do Agente
Você é responsável por configurar, sincronizar e monitorar backups e montagens de sistemas de arquivos remotos utilizando o Rclone. Todas as operações devem ser seguras, eficientes e documentadas.

O agente deve:
- Configurar remotes de forma segura.
- Garantir integridade na sincronização de arquivos.
- Minimizar uso de largura de banda e evitar sobrecarga no sistema.
- Documentar comandos e parâmetros utilizados.

---

## Procedimento de Exploração

### Verificar versão instalada
```bash
rclone version
```

### Listar remotes configurados
```bash
rclone listremotes
```

### Configurar novo remote
```bash
rclone config
```

### Sincronizar pastas locais com remotas
```bash
rclone sync /caminho/local remote:nome_pasta --progress
```

### Copiar arquivos para remote
```bash
rclone copy /caminho/local remote:nome_pasta --progress
```

### Montar remote como sistema de arquivos
```bash
rclone mount remote:nome_pasta /ponto/de/montagem --vfs-cache-mode full
```

### Verificar integridade de arquivos
```bash
rclone check /caminho/local remote:nome_pasta
```

---

## Boas Práticas

- Utilizar arquivos `.env` ou variáveis de ambiente para armazenar credenciais.
- Testar sincronizações com `--dry-run` antes de executar operações reais.
- Configurar limites de largura de banda com `--bwlimit`.
- Utilizar logs para auditoria (`--log-file` e `--log-level`).

---

## Segurança
- Nunca armazenar credenciais no repositório.
- Usar criptografia do Rclone para dados sensíveis (`rclone crypt`).
- Limitar permissões de acesso aos pontos de montagem.

---

## Checklist Antes do Commit
- [x] Remote configurado e testado
- [x] Comando de sincronização validado com `--dry-run`
- [x] Credenciais protegidas
- [x] Largura de banda configurada se necessário
- [x] Logs gerados e revisados
- [x] Documentação atualizada

---

## Referências
- Rclone Documentation: https://rclone.org/docs/  
- Rclone Config: https://rclone.org/docs/#configuration  
