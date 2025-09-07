# AGENTS.md

## Missão do Agente
Você é responsável por explorar, compreender e evoluir este código Python, seguindo práticas profissionais de desenvolvimento. Todas as modificações devem preservar a integridade, legibilidade e consistência do projeto.

O agente deve:
- Mapear a base de código antes de editar.
- Compreender dependências internas e externas.
- Criar visualizações de arquitetura (mapa de chamadas, grafo de módulos).
- Executar testes e validar a cobertura antes de integrar mudanças.

---

## Procedimento de Exploração Inteligente

### Mapear estrutura de diretórios
```bash
tree -L 3 --dirsfirst
```

### Identificar pontos de entrada
```bash
grep -R "if __name__ == '__main__':" .
```

### Encontrar classes e funções principais
```bash
grep -R "class " src/ script/ scripts/ 2>/dev/null | cut -d: -f1 | sort -u
grep -R "def " src/ script/ scripts/ 2>/dev/null | cut -d: -f1 | sort -u
```

### Listagem de dependências por importância
```bash
pip install pipdeptree
pipdeptree --warn silence | sort
```

Se o projeto usar `pyproject.toml`:
```bash
grep -A 20 "^\[tool.poetry.dependencies\]" pyproject.toml
```

### Criar mapa de chamadas de funções
```bash
pip install pycallgraph
pycallgraph graphviz -- ./src/main.py ./script/main.py ./scripts/main.py 2>/dev/nul
```

### Criar grafo de dependências entre módulos
```bash
pip install pydeps
pydeps src/ script/ scripts/ --show-deps --max-bacon=2 --output=deps.svg
```

### Detectar funções não utilizadas
```bash
pip install vulture
vulture src/ script/ scripts/
```

### Encontrar imports quebrados ou não utilizados
```bash
pip install autoflake
autoflake --remove-all-unused-imports --check --recursive src/ script/ scripts/
``
### Localizar pontos críticos de complexidade
```bash
pip install radon
radon cc src/ script/ scripts/ -s -a
``
---

## Configuração do Ambiente
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Se usar Poetry:
```bash
poetry install
```

---

## Padrões de Código
- Seguir **PEP8** e **PEP257**.
- Formatar com:
  ```bash
  black .
  ```
- Lint:
  ```bash
  flake8 .
  ```
- Nomes em inglês, descritivos.
- Docstrings no formato Sphinx.

---

## Estilo de Docstring (Sphinx)
```python
def velocity_profile(y: float, D: float, ue: float) -> float:
    r"""
    Perfil de velocidade para escoamento de Couette incompressível.

    .. math::

        u(y) = u_e \cdot \frac{y}{D}

    Args:
        y: coordenada normal [m]
        
        D: distância entre superfícies [m]
        
        ue: velocidade da superfície móvel [m/s]

    Returns:
        Velocidade na posição y [m/s]
    """
    return ue * (y / D)
```

---

## Testes
```bash
pytest --maxfail=1 --disable-warnings -q
pytest --cov=src
```

---

## Fluxo de Trabalho (Git)
- Criar branch:
  ```bash
  git checkout -b feature/nome
  ```
- Commits:
  ```
  [Tipo] Descrição curta
  ```
- Antes do PR:
  - Lint, formatação, testes.
  - Nenhum arquivo temporário ou sensível.

---

## Execução de Scripts
- Cabeçalho:
  ```python
  # -*- coding: utf-8 -*-
  ```
- Teste rápido:
  ```python
  if __name__ == '__main__':
      print("Script executado com sucesso!")
  ```

---

## Segurança
- Não commitar credenciais.
- Usar `.env`.
- Validar entradas.

---

## Checklist Antes do Commit
- [x] Código formatado (`black`)
- [x] Lint (`flake8`) sem erros
- [x] Testes passaram (`pytest`)
- [x] Cobertura ≥ 90%
- [x] Documentação atualizada
- [x] Nenhum dado sensível incluso

---

## Referências
- PEP 8 - Style Guide for Python Code  
- PEP 257 - Docstring Conventions  
- HALLIDAY, D.; RESNICK, R.; WALKER, J. *Fundamentals of Physics*. 7th ed. Wiley, 2005  
