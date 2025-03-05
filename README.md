# Case Gol

## Descrição
Este projeto é um dashboard para visualização de gráficos RPK por Ano-Mês.

## Instalação

### 1. Caso deseje criar do zero as migrations e o banco de dados:
```bash
flask db init
flask db migrate -m "Initial migration"

```

### 2. Para popular o banco de dados primeiro adicionar o arquivo em csv na pasta do projeto e depois rodar o comando:
```bash
flask db upgrade
python load_data.py
```

### 3. Para gerar a imagem docker:
```bash
docker-compose build
```
### 4. Para rodar o projeto:
```bash
docker-compose up
```

