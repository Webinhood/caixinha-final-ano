from app import create_app, db
from app.models import User
from validate_docbr import CPF

def init_db():
    app = create_app()
    with app.app_context():
        # Create tables
        db.create_all()
        
        # Lista de CPFs válidos para teste
        test_cpfs = [
            '529.982.247-25',
            '111.444.777-35',
            '123.456.789-09',
            '987.654.321-00',
            '248.438.034-80',
            '099.827.865-09',
            '923.176.840-05',
            '478.621.453-03',
            '746.824.890-70',
            '168.995.350-09',
            '378.542.669-08',
            '598.741.852-03',
            '785.369.140-91',
            '159.753.468-20',
            '753.951.846-37'
        ]
        
        # Remove todos os usuários existentes (para testes)
        User.query.delete()
        
        print("CPFs válidos para teste:")
        for cpf in test_cpfs:
            print(f"- {cpf}")
        
        db.session.commit()
        print("\nBanco de dados inicializado com sucesso!")

if __name__ == '__main__':
    init_db()
