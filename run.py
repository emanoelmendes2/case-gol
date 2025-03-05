from app import create_app

app = create_app()
""" Inicializa a aplicação Flask """

if __name__ == "__main__":
    app.run(debug=True)