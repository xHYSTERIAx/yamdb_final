![yamdb_workflow](https://github.com/xHYSTERIAx/yamdb_final/workflows/yamdb_workflow/badge.svg)

## REST API YamDB 
База отзывов о фильмах, музыке и книгах

### Стек
- Python
- Django Rest Framework
- Postgres
- Docker

### Описание
Проект YaMDb собирает отзывы (Review) пользователей на произведения (Titles). Произведения делятся на категории: «Книги», «Фильмы», «Музыка». Список категорий (Category) может быть расширен администратором. Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку. В каждой категории есть произведения: книги, фильмы или музыка. Произведению может быть присвоен жанр (Genre) из списка предустановленных. Новые жанры может создавать только администратор. Пользователи оставляют к произведениям текстовые отзывы (Review) и ставят произведению оценку в диапазоне от одного до десяти; из пользовательских оценок формируется усреднённая оценка произведения — рейтинг. На одно произведение пользователь может оставить только один отзыв.

### Запуск проекта:
- Склонируйте репозитрий на свой компьютер
- Из папки "infra/" соберите образ при помощи docker-compose
    "$ docker-compose up -d --build"
- Примените миграции
    "$ docker-compose exec web python manage.py migrate"
- Соберите статику
    "$ docker-compose exec web python manage.py collectstatic --no-input"
- Для доступа к админке не забудьте создать суперюзера
    "$ docker-compose exec web python manage.py createsuperuser"
- Проверьте работоспособность приложения, для этого перейдите на страницу:
    "http://localhost/admin/"
 

 

 ## Авторы
   - Анастасия Жалненкова