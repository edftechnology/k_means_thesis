# agents.md

## Missão do Agente
Você é responsável por configurar, manter e monitorar o servidor de e-mails Postfix, garantindo funcionamento seguro, estável e conforme as melhores práticas. Todas as alterações devem ser testadas antes de entrar em produção.

O agente deve:
- Configurar o Postfix de acordo com as necessidades do servidor.
- Garantir segurança contra spam e abuso.
- Monitorar filas e desempenho.
- Documentar alterações de configuração.

---

## Procedimento de Exploração

### Verificar versão instalada
```bash
postconf mail_version
```

### Editar configuração principal
```bash
sudo nano /etc/postfix/main.cf
```

### Editar configuração de transporte
```bash
sudo nano /etc/postfix/master.cf
```

### Reiniciar serviço
```bash
sudo systemctl restart postfix
```

### Verificar status
```bash
sudo systemctl status postfix
```

### Visualizar fila de e-mails
```bash
mailq
```

### Limpar fila de e-mails
```bash
postsuper -d ALL
```

---

## Boas Práticas

- Usar TLS para conexões seguras.
- Configurar SPF, DKIM e DMARC.
- Limitar relay apenas a hosts autorizados.
- Monitorar logs regularmente.

---

## Segurança
- Bloquear portas SMTP não usadas.
- Utilizar autenticação forte.
- Monitorar tentativas de login suspeitas.

---

## Checklist Antes do Commit
- [x] Configurações revisadas e testadas
- [x] TLS habilitado e funcionando
- [x] SPF/DKIM/DMARC configurados
- [x] Logs verificados
- [x] Documentação atualizada
- [x] Fila de e-mails limpa e monitorada

---

## Referências
- Postfix Documentation: http://www.postfix.org/documentation.html  
- Arch Wiki Postfix: https://wiki.archlinux.org/title/Postfix  
