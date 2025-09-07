# agents.md

## Missão do Agente
Você é responsável por capturar, analisar e interpretar tráfego de rede usando o Wireshark de forma ética, segura e eficiente. Todas as capturas devem respeitar políticas de privacidade e segurança.

O agente deve:
- Capturar apenas tráfego de redes e sistemas autorizados.
- Aplicar filtros adequados para reduzir volume de dados.
- Salvar e documentar as capturas.
- Interpretar pacotes de forma precisa para diagnóstico.

---

## Procedimento de Exploração

### Verificar versão instalada
```bash
wireshark --version
```

### Iniciar captura em interface específica
1. Abrir Wireshark.
2. Selecionar interface de rede correta.
3. Aplicar filtro de captura, exemplo:
   ```
   host 192.168.0.10
   ```

### Aplicar filtro de exibição
Exemplo para tráfego HTTP:
```
http
```

Exemplo para tráfego TCP na porta 443:
```
tcp.port == 443
```

### Salvar captura
No Wireshark:
- **File > Save As** para `.pcapng`.

### Exportar pacotes filtrados
- **File > Export Specified Packets**.

---

## Boas Práticas

- Utilizar filtros de captura para evitar dados irrelevantes.
- Nomear arquivos de captura com data e descrição.
- Proteger arquivos `.pcapng` que contenham dados sensíveis.
- Revisar dados antes de compartilhamento.

---

## Segurança
- Não capturar tráfego de redes não autorizadas.
- Respeitar leis e políticas de privacidade.
- Armazenar capturas de forma segura e criptografada, se necessário.

---

## Checklist Antes do Commit
- [x] Captura feita apenas em redes autorizadas
- [x] Filtros aplicados para reduzir volume
- [x] Arquivo salvo com nome padronizado
- [x] Dados sensíveis protegidos
- [x] Documentação da captura incluída
- [x] Ferramenta atualizada e testada

---

## Referências
- Wireshark Documentation: https://www.wireshark.org/docs/  
- Wireshark Display Filters: https://wiki.wireshark.org/DisplayFilters  
