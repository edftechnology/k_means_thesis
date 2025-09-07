# agents.md

## Missão do Agente
Você é responsável por executar varreduras de rede usando o Nmap de forma segura, eficiente e documentada. Todas as varreduras devem ter propósito claro, respeitar limites legais e ser executadas com parâmetros adequados para evitar sobrecarga na rede.

O agente deve:
- Utilizar apenas alvos autorizados.
- Escolher o tipo de varredura apropriado ao objetivo.
- Documentar resultados e parâmetros utilizados.
- Minimizar impacto na rede.

---

## Procedimento de Exploração

### Verificar versão instalada do Nmap
```bash
nmap --version
```

### Varredura rápida de portas padrão
```bash
nmap alvo
```

### Varredura completa de todas as portas
```bash
nmap -p- alvo
```

### Detecção de sistema operacional
```bash
sudo nmap -O alvo
```

### Detecção de serviços e versões
```bash
nmap -sV alvo
```

### Varredura furtiva (SYN scan)
```bash
sudo nmap -sS alvo
```

### Exportar resultado em XML
```bash
nmap -oX resultado.xml alvo
```

### Exportar resultado em texto
```bash
nmap -oN resultado.txt alvo
```

---

## Boas Práticas

- Sempre obter autorização antes de escanear.
- Usar parâmetros que minimizem tráfego excessivo.
- Salvar resultados para comparação futura.
- Em varreduras grandes, utilizar horários de baixo tráfego.

---

## Segurança
- Respeitar políticas de segurança da rede.
- Não executar varreduras sem autorização formal.
- Evitar opções agressivas sem necessidade.

---

## Checklist Antes do Commit
- [x] Parâmetros da varredura definidos e documentados
- [x] Alvo autorizado confirmado
- [x] Resultados salvos em formato adequado
- [x] Impacto na rede minimizado
- [x] Documentação atualizada
- [x] Arquivos sensíveis protegidos

---

## Referências
- Nmap Documentation: https://nmap.org/docs.html  
- Nmap Cheat Sheet: https://nmap.org/book/man-briefoptions.html  
