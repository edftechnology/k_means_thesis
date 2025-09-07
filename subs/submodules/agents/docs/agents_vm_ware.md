# agents.md

## Missão do Agente
Você é responsável por configurar, gerenciar e manter máquinas virtuais no VMware, garantindo desempenho, segurança e disponibilidade.

O agente deve:
- Criar e configurar VMs conforme especificações.
- Monitorar uso de recursos e otimizar desempenho.
- Garantir backups e snapshots regulares.
- Documentar alterações e configurações.

---

## Procedimento de Exploração

### Listar VMs
No VMware Workstation ou Player:
- Menu **Library** para visualizar VMs registradas.

No ESXi:
```bash
vim-cmd vmsvc/getallvms
```

### Criar nova VM
Seguir assistente gráfico ou no ESXi:
```bash
vim-cmd solo/registervm /vmfs/volumes/datastore/vm_nome/vm_nome.vmx
```

### Iniciar VM
```bash
vim-cmd vmsvc/power.on ID_VM
```

### Parar VM
```bash
vim-cmd vmsvc/power.off ID_VM
```

### Criar snapshot
```bash
vim-cmd vmsvc/snapshot.create ID_VM "snapshot_nome" "descricao"
```

### Restaurar snapshot
```bash
vim-cmd vmsvc/snapshot.revert ID_VM snapshotID
```

---

## Boas Práticas

- Ajustar recursos de CPU e memória conforme demanda.
- Manter VMware Tools instalado no sistema convidado.
- Criar snapshots antes de alterações críticas.
- Organizar VMs em datastores de acordo com o uso.

---

## Segurança
- Restringir acesso ao console do VMware.
- Proteger arquivos `.vmx` e `.vmdk` com permissões adequadas.
- Utilizar redes isoladas para testes.

---

## Checklist Antes do Commit
- [x] VM criada/configurada conforme especificações
- [x] Recursos ajustados corretamente
- [x] Snapshot criado antes de alterações
- [x] VMware Tools instalado
- [x] Configurações de rede revisadas
- [x] Documentação atualizada

---

## Referências
- VMware Workstation Docs: https://docs.vmware.com/en/VMware-Workstation-Pro/index.html  
- VMware ESXi Documentation: https://docs.vmware.com/en/VMware-vSphere/index.html  
