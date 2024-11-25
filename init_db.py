from app import app, db, Bird
from werkzeug.security import generate_password_hash
from app import User

def init_db():
    with app.app_context():
        # Создаем таблицы
        db.create_all()

        # Проверяем, есть ли уже данные в таблице Bird
        if Bird.query.first() is None:
            # Добавляем начальные данные о птицах
            birds = [
                Bird(
                    species='Обыкновенный снегирь',
                    scientific_name='Pyrrhula pyrrhula',
                    description='Певчая птица семейства вьюрковых. Самцы имеют ярко-красную грудку, серую спину и черную шапочку.',
                    habitat='Лесные территории, парки и сады'
                ),
                Bird(
                    species='Большая синица',
                    scientific_name='Parus major',
                    description='Широко распространенная синица с желтой грудкой и зеленовато-голубой спинкой.',
                    habitat='Леса, парки, городские территории'
                ),
                Bird(
                    species='Полевой жаворонок',
                    scientific_name='Alauda arvensis',
                    description='Небольшая певчая птица буровато-серой окраски с характерным мелодичным пением.',
                    habitat='Открытые поля, луга, степи'
                ),
                Bird(
                    species='Белая трясогузка',
                    scientific_name='Motacilla alba',
                    description='Стройная птица с длинным хвостом, черно-белым оперением и характерными покачиваниями хвостом.',
                    habitat='Берега водоемов, населенные пункты'
                ),
                Bird(
                    species='Обыкновенный соловей',
                    scientific_name='Luscinia luscinia',
                    description='Небольшая певчая птица буроватой окраски, известная своим красивым пением.',
                    habitat='Лиственные леса, парки с густым подлеском'
                )
            ]
            
            for bird in birds:
                db.session.add(bird)

        # Создаем тестового пользователя, если его еще нет
        if User.query.filter_by(username='test_user').first() is None:
            test_user = User(
                username='test_user',
                email='test@example.com',
                password=generate_password_hash('password123')
            )
            db.session.add(test_user)

        # Сохраняем изменения
        db.session.commit()
        print('База данных успешно инициализирована')

if __name__ == '__main__':
    init_db()
