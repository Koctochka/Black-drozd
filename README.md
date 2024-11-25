# Орнитологическая платформа

Онлайн-платформа для орнитологических исследований, позволяющая исследователям и любителям птиц вести учет наблюдений, делиться находками и изучать информацию о различных видах птиц.

## Функциональность

- Каталог птиц с описаниями и характеристиками
- Система регистрации и авторизации пользователей
- Добавление и редактирование наблюдений
- Просмотр наблюдений других пользователей
- Загрузка фотографий птиц

## Технологии

- Python 3.8+
- Flask
- SQLAlchemy
- Flask-Login
- SQLite
- Bootstrap 5

## Установка и запуск локально

1. Клонируйте репозиторий:

```bash
git clone https://github.com/yourusername/Black-drozd.git
cd Black-drozd
```

2. Установите зависимости:

```bash
pip install -r requirements.txt
```

3. Инициализируйте базу данных:

```bash
python init_db.py
```

4. Запустите приложение:

```bash
python app.py
```

5. Откройте в браузере http://localhost:5000

## Структура проекта

```
Black-drozd/
├── app.py              # Основной файл приложения
├── init_db.py          # Скрипт инициализации базы данных
├── requirements.txt    # Зависимости проекта
├── static/
│   └── css/           # CSS стили
│       └── style.css
└── templates/         # HTML шаблоны
    ├── base.html
    ├── index.html
    ├── birds.html
    ├── observations.html
    ├── add_observation.html
    ├── edit_observation.html
    ├── login.html
    └── register.html
```

## Развертывание

1. Создайте аккаунт на GitHub если его еще нет
2. Создайте новый репозиторий
3. Загрузите код в репозиторий:

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/yourusername/Black-drozd.git
git push -u origin main
```

## Лицензия

MIT

## Авторы

- Ваше имя

## Вклад в проект

Если вы хотите внести свой вклад в проект:

1. Создайте форк репозитория
2. Создайте ветку для новой функциональности
3. Создайте pull request
