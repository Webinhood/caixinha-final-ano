from app import create_app, db
from app.models import ValidIdentifier

def init_db():
    app = create_app()
    with app.app_context():
        # Create tables
        db.create_all()
        
        # Add some test identifier codes
        test_codes = ['123', '456', '789', '001', '002']
        for code in test_codes:
            if not ValidIdentifier.query.filter_by(code=code).first():
                identifier = ValidIdentifier(code=code)
                db.session.add(identifier)
        
        db.session.commit()
        print("Database initialized with test codes:", test_codes)

if __name__ == '__main__':
    init_db()
