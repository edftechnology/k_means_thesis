# agents.md

## Missão do Agente
Você é responsável por configurar, manter e administrar volumes criptografados com LUKS (Linux Unified Key Setup), garantindo segurança e integridade dos dados. Todas as operações devem ser feitas com backups e autorização adequada.

O agente deve:
- Configurar volumes criptografados de forma segura.
- Gerenciar chaves de acesso de maneira protegida.
- Testar montagem e desmontagem antes de liberar para uso.
- Documentar procedimentos e parâmetros utilizados.

---

## Procedimento de Exploração

### Verificar dispositivos disponíveis
```bash
lsblk
```

### Criar volume criptografado
```bash
sudo cryptsetup luksFormat /dev/sdX
```

### Abrir volume criptografado
```bash
sudo cryptsetup luksOpen /dev/sdX nome_volume
```

### Fechar volume criptografado
```bash
sudo cryptsetup luksClose nome_volume
```

### Adicionar nova chave
```bash
sudo cryptsetup luksAddKey /dev/sdX
```

### Remover chave
```bash
sudo cryptsetup luksRemoveKey /dev/sdX
```

### Ver informações do volume
```bash
sudo cryptsetup luksDump /dev/sdX
```

---

## Boas Práticas

- Sempre manter backup seguro das chaves.
- Utilizar senhas fortes e longas.
- Evitar manipular volumes montados em uso crítico.
- Proteger arquivos de chave (`keyfile`) com permissões restritas.

---

## Segurança
- Não armazenar chaves em texto plano.
- Utilizar criptografia de chave (`gpg`, `openssl`) para backups.
- Montar volumes apenas em sistemas confiáveis.

---

## Checklist Antes do Commit
- [x] Volume LUKS configurado e testado
- [x] Backup das chaves realizado
- [x] Permissões de arquivos de chave revisadas
- [x] Senha forte utilizada
- [x] Documentação atualizada
- [x] Procedimentos testados de montagem e desmontagem

---

## Referências
- cryptsetup Documentation: https://gitlab.com/cryptsetup/cryptsetup  
- Arch Wiki LUKS: https://wiki.archlinux.org/title/Dm-crypt/Encrypting_an_entire_system  
