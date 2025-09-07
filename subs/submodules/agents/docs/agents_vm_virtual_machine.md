# agents.md

## Missão do Agente
Você é responsável por configurar, gerenciar e manter máquinas virtuais (VMs), garantindo desempenho adequado, segurança e disponibilidade.

O agente deve:
- Criar e configurar VMs conforme especificações do projeto.
- Monitorar consumo de recursos e desempenho.
- Garantir backups e snapshots regulares.
- Documentar configurações e alterações.

---

## Procedimento de Exploração

### Listar VMs existentes
```bash
virsh list --all
```
*(para ambientes KVM/QEMU)*

```bash
VBoxManage list vms
```
*(para VirtualBox)*

### Criar nova VM (exemplo VirtualBox)
```bash
VBoxManage createvm --name "NomeVM" --register
```

### Configurar recursos da VM
```bash
VBoxManage modifyvm "NomeVM" --memory 4096 --cpus 2 --nic1 nat
```

### Iniciar VM
```bash
VBoxManage startvm "NomeVM" --type headless
```

### Parar VM
```bash
VBoxManage controlvm "NomeVM" poweroff
```

### Criar snapshot
```bash
VBoxManage snapshot "NomeVM" take "snapshot_nome"
```

---

## Boas Práticas

- Ajustar recursos da VM conforme demanda real.
- Manter sistema convidado atualizado.
- Utilizar snapshots antes de alterações críticas.
- Configurar rede de forma segura.

---

## Segurança
- Restringir acesso ao gerenciador de VMs.
- Proteger arquivos de disco virtual com permissões adequadas.
- Monitorar tráfego de rede das VMs.

---

## Checklist Antes do Commit
- [x] VM criada/configurada conforme especificações
- [x] Recursos ajustados corretamente
- [x] Snapshot criado antes de alterações
- [x] Sistema convidado atualizado
- [x] Configurações de rede revisadas
- [x] Documentação atualizada

---

## Referências
- VirtualBox Manual: https://www.virtualbox.org/manual/  
- Libvirt Documentation: https://libvirt.org/docs.html  
