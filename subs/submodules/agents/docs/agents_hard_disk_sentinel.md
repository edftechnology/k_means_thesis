# agents.md

## Missão do Agente
Você é responsável por monitorar e diagnosticar o estado de saúde dos discos rígidos e SSDs utilizando o Hard Disk Sentinel, garantindo a prevenção de falhas e a integridade dos dados.

O agente deve:
- Verificar regularmente o status dos discos.
- Interpretar relatórios de saúde e desempenho.
- Documentar alterações e alertas críticos.
- Realizar ações preventivas antes que ocorram falhas.

---

## Procedimento de Exploração

### Verificar versão instalada
```bash
hdsentinel -V
```

### Executar análise de status
```bash
hdsentinel
```

### Obter relatório detalhado
```bash
hdsentinel -r /caminho/relatorio.txt
```

### Monitorar temperatura e saúde em tempo real
```bash
watch -n 10 hdsentinel
```

### Exportar dados de desempenho
```bash
hdsentinel -export /caminho/desempenho.txt
```

---

## Boas Práticas

- Verificar status de discos semanalmente.
- Configurar alertas automáticos para degradação de saúde.
- Registrar histórico de desempenho.
- Substituir discos com saúde inferior a 80% preventivamente.

---

## Segurança
- Armazenar relatórios em local seguro.
- Proteger acesso a informações de hardware sensíveis.
- Garantir backup antes de testes de stress.

---

## Checklist Antes do Commit
- [x] Status dos discos verificado
- [x] Relatório gerado e armazenado
- [x] Temperatura monitorada
- [x] Alertas configurados
- [x] Histórico atualizado
- [x] Documentação atualizada

---

## Referências
- Hard Disk Sentinel Documentation: https://www.hdsentinel.com/help/en/  
- Hard Disk Sentinel CLI Guide: https://www.hdsentinel.com/command_line.php  
