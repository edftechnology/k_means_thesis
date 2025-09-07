# agents.md

## Missão do Agente
Você é responsável por configurar, manter e restaurar backups do sistema utilizando o Timeshift, garantindo pontos de restauração consistentes e recuperação confiável.

O agente deve:
- Configurar backups automáticos conforme política definida.
- Garantir que os snapshots estejam íntegros.
- Testar a restauração periodicamente.
- Documentar configurações e procedimentos.

---

## Procedimento de Exploração

### Verificar versão instalada
```bash
timeshift --version
```

### Listar snapshots existentes
```bash
sudo timeshift --list
```

### Criar snapshot manual
```bash
sudo timeshift --create --comments "Snapshot manual"
```

### Restaurar snapshot
```bash
sudo timeshift --restore
```

### Configurar backups automáticos
Abrir interface gráfica ou editar configurações via terminal:
```bash
sudo timeshift --setup
```

---

## Boas Práticas

- Configurar backups automáticos diários ou semanais conforme uso.
- Armazenar snapshots em disco separado para maior segurança.
- Utilizar rótulos descritivos para snapshots manuais.
- Excluir arquivos temporários e cache antes de criar backups.

---

## Segurança
- Proteger local de armazenamento dos snapshots contra acesso não autorizado.
- Monitorar espaço em disco para evitar falhas na criação de backups.
- Restaurar apenas de fontes confiáveis.

---

## Checklist Antes do Commit
- [x] Backups automáticos configurados
- [x] Snapshot manual criado e verificado
- [x] Teste de restauração realizado
- [x] Espaço em disco suficiente confirmado
- [x] Local de armazenamento protegido
- [x] Documentação atualizada

---

## Referências
- Timeshift Documentation: https://teejeetech.com/timeshift/  
- Linux Mint Timeshift Guide: https://linuxmint-installation-guide.readthedocs.io/en/latest/timeshift.html  
