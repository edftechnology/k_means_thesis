# agents.md

## Missão do Agente
Você é responsável por instalar, configurar e manter o módulo de segurança Warsaw, garantindo compatibilidade com os bancos suportados e funcionamento adequado durante transações.

O agente deve:
- Instalar e configurar o Warsaw corretamente.
- Verificar se o serviço está ativo e funcional.
- Diagnosticar e corrigir problemas de inicialização ou compatibilidade.
- Documentar procedimentos e ajustes feitos.

---

## Procedimento de Exploração

### Verificar se o Warsaw está instalado
```bash
dpkg -l | grep warsaw
```

### Instalar Warsaw (Debian/Ubuntu)
```bash
sudo dpkg -i warsaw_setup.deb
sudo apt --fix-broken install
```

### Iniciar serviço
```bash
sudo systemctl start warsaw
```

### Verificar status do serviço
```bash
systemctl status warsaw
```

### Habilitar inicialização automática
```bash
sudo systemctl enable warsaw
```

### Verificar portas utilizadas
```bash
sudo netstat -tulnp | grep warsaw
```

---

## Boas Práticas

- Baixar o instalador apenas de fontes oficiais do banco.
- Verificar compatibilidade antes de atualizar o sistema.
- Manter backup do instalador para reinstalação rápida.

---

## Segurança
- Garantir que apenas o Warsaw oficial esteja instalado.
- Monitorar conexões de rede do módulo para detectar anomalias.
- Remover versões antigas antes de atualizar.

---

## Checklist Antes do Commit
- [x] Warsaw instalado a partir de fonte oficial
- [x] Serviço ativo e funcional
- [x] Inicialização automática configurada
- [x] Portas de rede verificadas
- [x] Compatibilidade com navegador confirmada
- [x] Documentação atualizada

---

## Referências
- Suporte Warsaw: https://www.dieboldnixdorf.com.br/  
- Arch Wiki Warsaw: https://wiki.archlinux.org/title/Warsaw  
