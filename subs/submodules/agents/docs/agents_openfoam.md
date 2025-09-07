# agents.md

## Missão do Agente
Você é responsável por configurar, manter e executar simulações no OpenFOAM, garantindo que os casos sejam reprodutíveis, eficientes e documentados. Todas as alterações no ambiente ou nos arquivos de caso devem ser testadas antes de integração.

O agente deve:
- Seguir padrões de organização de casos.
- Garantir compatibilidade com a versão do OpenFOAM utilizada.
- Validar malhas, condições de contorno e parâmetros de simulação.
- Documentar configurações e resultados.

---

## Procedimento de Exploração do Repositório

### Verificar estrutura de um caso
```bash
tree -L 2
```

Estrutura padrão esperada:
```
case_name/
├── 0/                # Condições iniciais
├── constant/         # Propriedades do material e malha
├── system/           # Configuração de controle e esquemas numéricos
```

### Listar versões instaladas do OpenFOAM
```bash
foamInstallationTest
```

### Carregar ambiente
```bash
source /opt/openfoamX/etc/bashrc
```
*(substituir `X` pela versão instalada)*

### Validar malha
```bash
checkMesh
```

### Executar solver
```bash
simpleFoam
```
*(ou outro solver conforme o caso)*

### Pós-processar resultados
```bash
paraFoam
```

---

## Boas Práticas

- Manter consistência na nomenclatura de pastas e arquivos.
- Validar a malha antes de rodar simulações longas.
- Utilizar `controlDict` para definir intervalo de escrita de resultados adequados.
- Sempre salvar um backup do caso antes de alterar parâmetros críticos.

---

## Segurança
- Não executar simulações pesadas no servidor principal sem agendamento.
- Proteger diretórios com dados sensíveis.
- Garantir backup das pastas `constant` e `system`.

---

## Checklist Antes do Commit
- [x] Estrutura de caso validada
- [x] Malha verificada com `checkMesh`
- [x] Solver executado sem erros
- [x] Resultados pós-processados e verificados
- [x] Documentação atualizada
- [x] Arquivos temporários removidos

---

## Referências
- OpenFOAM User Guide: https://cfd.direct/openfoam/user-guide/  
- OpenFOAM Wiki: https://openfoamwiki.net/  
