# agents.md

## Missão do Agente
Você é responsável por criar, manter e otimizar ambientes baseados em containers, garantindo que as imagens sejam seguras, leves e eficientes. Todas as alterações em configurações ou arquivos de container devem ser testadas antes da integração.

O agente deve:
- Seguir boas práticas na escrita de Dockerfiles e configurações de orquestração.
- Garantir segurança e performance dos containers.
- Testar imagens localmente antes do deploy.
- Documentar versões, variáveis de ambiente e portas expostas.

---

## Procedimento de Exploração do Repositório

### Listar arquivos de configuração de containers
```bash
find . -type f \( -name "Dockerfile" -o -name "docker-compose.yml" -o -name "*.yaml" \)
```

### Construir imagem localmente
```bash
docker build -t nome_imagem:tag .
```

### Rodar container em modo interativo
```bash
docker run -it --rm nome_imagem:tag /bin/bash
```

### Listar containers ativos
```bash
docker ps
```

### Ver logs do container
```bash
docker logs nome_container
```

### Subir múltiplos serviços com Docker Compose
```bash
docker-compose up -d
```

### Derrubar serviços
```bash
docker-compose down
```

---

## Boas Práticas

- Utilizar imagens base leves (ex: `alpine` quando possível).
- Minimizar número de camadas no Dockerfile.
- Definir explicitamente a versão de cada dependência.
- Configurar `.dockerignore` para evitar cópia de arquivos desnecessários.
- Utilizar variáveis de ambiente seguras via `docker-compose.yml` ou `.env`.

---

## Segurança
- Não armazenar credenciais no Dockerfile.
- Utilizar usuário não-root sempre que possível.
- Reduzir permissões de rede e acesso ao host.
- Manter imagens atualizadas com `docker pull`.

---

## Checklist Antes do Commit
- [x] Dockerfile validado e otimizado
- [x] Build executado sem erros
- [x] Testes locais concluídos com sucesso
- [x] Variáveis de ambiente seguras configuradas
- [x] Documentação atualizada
- [x] Arquivos desnecessários no `.dockerignore`

---

## Referências
- Docker Documentation: https://docs.docker.com/  
- Docker Compose Docs: https://docs.docker.com/compose/  
