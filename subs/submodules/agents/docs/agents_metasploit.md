# agents.md

## Missão do Agente
Você é responsável por executar e gerenciar testes de penetração usando o Metasploit Framework de forma ética, segura e autorizada. Todas as atividades devem seguir políticas de segurança e possuir autorização formal.

O agente deve:
- Executar testes apenas em sistemas autorizados.
- Documentar módulos utilizados, parâmetros e resultados.
- Minimizar impactos nos sistemas durante os testes.
- Manter o Metasploit atualizado e configurado corretamente.

---

## Procedimento de Exploração

### Verificar versão instalada
```bash
msfconsole --version
```

### Iniciar Metasploit
```bash
msfconsole
```

### Buscar exploits
```bash
search nome_exploit
```

### Selecionar exploit
```bash
use caminho/exploit
```

### Configurar parâmetros
```bash
set RHOSTS alvo
set RPORT porta
```

### Executar exploit
```bash
run
```

### Listar sessões ativas
```bash
sessions
```

### Interagir com sessão
```bash
sessions -i ID
```

---

## Boas Práticas

- Sempre realizar testes com autorização documentada.
- Atualizar módulos com `msfupdate`.
- Registrar logs e evidências de execução.
- Utilizar exploits mais recentes e seguros.

---

## Segurança
- Não explorar sistemas sem autorização.
- Armazenar relatórios de forma segura.
- Encerrar sessões e limpar rastros após testes.

---

## Checklist Antes do Commit
- [x] Autorização formal obtida
- [x] Módulos e parâmetros documentados
- [x] Testes realizados sem impacto crítico
- [x] Metasploit atualizado
- [x] Logs e evidências armazenados
- [x] Sessões encerradas corretamente

---

## Referências
- Metasploit Unleashed: https://www.offsec.com/metasploit-unleashed/  
- Rapid7 Metasploit Docs: https://docs.rapid7.com/metasploit/  
