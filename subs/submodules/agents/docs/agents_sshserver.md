# agents.md

## Missão do Agente
Você é responsável por configurar e manter o servidor SSH de forma segura e funcional, garantindo acesso remoto confiável e proteção contra acessos não autorizados.

O agente deve:
- Configurar o serviço SSH conforme boas práticas de segurança.
- Testar conexões após alterações de configuração.
- Monitorar tentativas de acesso e ajustar firewall conforme necessário.
- Documentar alterações e parâmetros aplicados.

---

## Procedimento de Exploração

### Verificar status do SSH
```bash
sudo systemctl status ssh
```

### Editar arquivo de configuração
```bash
sudo nano /etc/ssh/sshd_config
```

### Testar configuração antes de reiniciar
```bash
sudo sshd -t
```

### Reiniciar serviço
```bash
sudo systemctl restart ssh
```

### Conectar a partir de cliente
```bash
ssh usuario@ip_do_servidor
```

### Verificar logs de acesso
```bash
sudo journalctl -u ssh
```

---

## Boas Práticas

- Alterar porta padrão do SSH.
- Desabilitar login como root (`PermitRootLogin no`).
- Utilizar autenticação por chave pública.
- Restringir acesso a IPs autorizados no firewall.
- Habilitar `Fail2Ban` ou equivalente para bloqueio automático.

---

## Segurança
- Usar chaves SSH protegidas por senha.
- Proteger o arquivo `~/.ssh/authorized_keys` com permissões adequadas.
- Monitorar tentativas de login mal sucedidas.

---

## Checklist Antes do Commit
- [x] Porta SSH alterada e registrada
- [x] Login como root desativado
- [x] Autenticação por chave configurada
- [x] Firewall configurado para porta SSH
- [x] Logs verificados
- [x] Documentação atualizada

---

## Referências
- OpenSSH Documentation: https://www.openssh.com/manual.html  
- Arch Wiki SSH: https://wiki.archlinux.org/title/Secure_Shell  
