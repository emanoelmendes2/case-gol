import pandas as pd
from app import create_app, db
from app.models import Voo

def load_data():
    # Carregar os dados do CSV, pulando a primeira linha de cabeçalho adicional
    df = pd.read_csv('Dados_Estatisticos.csv', delimiter=';', skiprows=1, low_memory=False)

    # Verificar as primeiras linhas e os nomes das colunas
    print(df.head())
    print(df.columns)

    # Filtrar os dados
    df = df[(df['EMPRESA_SIGLA'] == 'GLO') & 
            (df['GRUPO_DE_VOO'] == 'REGULAR') & 
            (df['NATUREZA'] == 'DOMÉSTICA')]

    # Criar a coluna MERCADO
    df['MERCADO'] = df.apply(lambda row: ''.join(sorted([row['AEROPORTO_DE_ORIGEM_SIGLA'], row['AEROPORTO_DE_DESTINO_SIGLA']])), axis=1)

    # Selecionar as colunas necessárias
    df = df[['ANO', 'MES', 'MERCADO', 'RPK']]

    # Remover linhas com valores NaN na coluna RPK
    df = df.dropna(subset=['RPK'])

    # Verificar duplicatas
    duplicates = df[df.duplicated(subset=['ANO', 'MES', 'MERCADO'], keep=False)]
    if not duplicates.empty:
        print("Duplicatas encontradas:")
        print(duplicates)

    # Remover duplicatas
    df = df.drop_duplicates(subset=['ANO', 'MES', 'MERCADO'])

    # Inserir os dados no banco de dados
    app = create_app()
    with app.app_context():
        for _, row in df.iterrows():
            voo = Voo(ano=row['ANO'], mes=row['MES'], mercado=row['MERCADO'], rpk=row['RPK'])
            db.session.add(voo)
        db.session.commit()

if __name__ == "__main__":
    load_data()