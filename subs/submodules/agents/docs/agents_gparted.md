# agents.md

## Missão do Agente
Você é responsável por gerenciar partições de disco usando o GParted, garantindo que operações de redimensionamento, criação, exclusão e formatação sejam feitas com segurança e sem perda de dados.

O agente deve:
- Planejar alterações de partições antes da execução.
- Garantir backup de dados importantes.
- Confirmar que o disco não está em uso antes de modificações.
- Documentar alterações feitas.

---

## Procedimento de Exploração

### Verificar versão instalada
```bash
gparted --version
```

### Listar discos disponíveis
No GParted, selecione no menu suspenso o disco desejado ou no terminal:
```bash
lsblk
```

### Criar nova partição
1. Selecionar espaço não alocado.
2. **Novo** > definir tipo, tamanho e sistema de arquivos.
3. Aplicar alterações.

### Redimensionar partição
1. Selecionar partição.
2. **Redimensionar/Mover**.
3. Definir novo tamanho e aplicar alterações.

### Formatar partição
1. Selecionar partição.
2. **Formatar para** > escolher sistema de arquivos.
3. Aplicar alterações.

---

## Boas Práticas

- Sempre fazer backup antes de modificar partições.
- Evitar modificar partições montadas.
- Utilizar sistemas de arquivos compatíveis com o uso planejado.
- Verificar integridade do sistema de arquivos após alterações (`fsck`).

---

## Segurança
- Operar somente em discos autorizados.
- Garantir que não há processos acessando o disco.
- Evitar uso em discos com setores defeituosos sem verificação prévia.

---

## Checklist Antes do Commit
- [x] Backup realizado dos dados importantes
- [x] Disco/desmontado antes das alterações
- [x] Sistema de arquivos adequado configurado
- [x] Alterações aplicadas e verificadas
- [x] Documentação das modificações feita
- [x] Ferramenta atualizada

---

## Referências
- GParted Documentation: https://gparted.org/documentation.php  
- Arch Wiki GParted: https://wiki.archlinux.org/title/GParted  
