# agents.md

## Missão do Agente
Você é responsável por configurar e gerenciar o TeamViewer, garantindo acesso remoto seguro e estável, seguindo as políticas de segurança definidas.

O agente deve:
- Configurar acesso remoto de forma segura.
- Manter o TeamViewer atualizado.
- Documentar ID e configurações importantes.
- Garantir que conexões sejam feitas apenas com usuários autorizados.

---

## Procedimento de Exploração

### Verificar versão instalada
```bash
teamviewer --version
```

### Iniciar TeamViewer
```bash
teamviewer
```

### Obter ID e senha
Ao abrir a interface gráfica, o ID e senha temporária são exibidos.

### Configurar acesso não supervisionado
1. Abrir TeamViewer.
2. Acessar **Extras > Opções**.
3. Configurar senha pessoal para acesso permanente.

### Conectar a outro dispositivo
Na interface do TeamViewer:
1. Inserir ID do parceiro.
2. Clicar em **Conectar**.
3. Inserir senha quando solicitado.

---

## Boas Práticas

- Alterar senha pessoal periodicamente.
- Utilizar autenticação de dois fatores.
- Limitar acesso a dispositivos autorizados.
- Manter software sempre atualizado.

---

## Segurança
- Não compartilhar ID e senha publicamente.
- Desabilitar TeamViewer quando não estiver em uso prolongado.
- Monitorar histórico de conexões.

---

## Checklist Antes do Commit
- [x] Versão do TeamViewer atualizada
- [x] Acesso não supervisionado configurado de forma segura
- [x] Autenticação de dois fatores ativada
- [x] Senha pessoal definida e protegida
- [x] Documentação atualizada
- [x] Histórico de conexões verificado

---

## Referências
- TeamViewer Documentation: https://www.teamviewer.com/en/docs/  
- Secure TeamViewer Guide: https://community.teamviewer.com/  
