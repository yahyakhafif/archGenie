import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

from app import create_app
from config.db import db
from models.User import User, user_favorites
from models.Style import Style, FamousExample
from scripts.seed_data import styles_data


def add_favorites(user_id):
    user = db.session.get(User, user_id)

    all_styles = Style.query.all()

    nineteenth_century_styles = [s for s in all_styles if '19th Century' in s.period]

    art_nouveau = next((s for s in all_styles if s.name == 'Art Nouveau'), None)

    favorite_styles = nineteenth_century_styles[:]
    if art_nouveau:
        favorite_styles.append(art_nouveau)

    for style in favorite_styles:
        user.favorites.append(style)

    db.session.commit()

    print(f'Added {len(favorite_styles)} favorites to the test user')
    print('Favorites: ' + ', '.join(s.name for s in favorite_styles))


def seed():
    app = create_app()

    with app.app_context():
        try:
            db.session.execute(user_favorites.delete())
            FamousExample.query.delete()
            Style.query.delete()
            User.query.delete()
            db.session.commit()

            user = User(name='Test User', email='test@example.com')
            user.set_password('password123')
            db.session.add(user)
            db.session.commit()
            print(f'Test user created with ID: {user.id}')

            for style_data in styles_data:
                style = Style(
                    name=style_data['name'],
                    period=style_data['period'],
                    description=style_data['description'],
                    characteristics=style_data['characteristics'],
                    main_features=style_data.get('mainFeatures', []),
                    image_url=style_data.get('imageUrl'),
                    created_by=user.id
                )
                db.session.add(style)
            db.session.commit()
            print(f'{len(styles_data)} architectural styles created')

            add_favorites(user.id)

            print('Seeding completed successfully')

        except Exception as e:
            db.session.rollback()
            print(f'Seeding failed: {str(e)}')
            sys.exit(1)


if __name__ == '__main__':
    seed()
