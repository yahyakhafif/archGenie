import os
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_db(app):
    database_url = os.environ.get('DATABASE_URL', 'postgresql://localhost:5432/archgenie')

    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()
        print(f'PostgreSQL Connected: {database_url}')

        from models.Style import Style
        if Style.query.first() is None:
            print('Database is empty — running auto-seed...')
            _auto_seed()


def _auto_seed():
    from models.User import User
    from models.Style import Style

    from scripts.seed_data import styles_data

    user = User.query.first()
    if not user:
        user = User(name='Test User', email='test@example.com')
        user.set_password('password123')
        db.session.add(user)
        db.session.commit()
        print(f'Default user created (ID: {user.id})')

    for s in styles_data:
        style = Style(
            name=s['name'],
            period=s['period'],
            description=s['description'],
            characteristics=s['characteristics'],
            main_features=s.get('mainFeatures', []),
            image_url=s.get('imageUrl'),
            created_by=user.id
        )
        db.session.add(style)
    db.session.commit()
    print(f'{len(styles_data)} architectural styles seeded')

    all_styles = Style.query.all()
    favs = [st for st in all_styles if '19th Century' in st.period]
    art_nouveau = next((st for st in all_styles if st.name == 'Art Nouveau'), None)
    if art_nouveau:
        favs.append(art_nouveau)
    for f in favs:
        user.favorites.append(f)
    db.session.commit()
    print(f'Added {len(favs)} favorites to default user')
