# LMS — 32.1 Валидаторы, пагинация и тесты

## Что добавлено
- `lms/validators.py` — `YoutubeLinkValidator`: в материалах разрешены только ссылки на youtube.com
  (подключён в `Meta.validators` сериализаторов урока и курса, понятный текст ошибки)
- Модель `Subscription` (пользователь + курс, пара уникальна)
- `POST /subscriptions/` с `{"course_id": <id>}` — подписывает, если подписки нет, и отписывает, если есть
- Поле `is_subscribed` в выдаче курса — подписан ли текущий пользователь
- `lms/paginators.py` — `LmsPagination` (page_size=5, page_size_query_param, max_page_size=50) для курсов и уроков
- Тесты `lms/tests.py`, `users/tests.py`: CRUD уроков с разными правами, подписка, курсы, пагинация, пользователи
- Отчёт покрытия — `coverage_report.txt` (97%)

## Запуск
```
pip install -r requirements.txt
python manage.py migrate
python manage.py loaddata groups.json
python manage.py runserver
```

## Тесты и покрытие
```
coverage run --source='.' manage.py test
coverage report
```
