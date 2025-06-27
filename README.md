# Diplom_3
Проект автоматизации тестирования Stellar Burgers
Этот проект содержит автоматизированные тесты для веб-приложения Stellar Burgers. 
Тесты покрывают основные функциональные возможности приложения, включая личный кабинет пользователя,
восстановление пароля, работу с конструктором бургеров и лентой заказов.

project/
├── allure-results/
├── locators/                # Локаторы для элементов страниц
│   ├── main_page_locators.py
│   ├── order_feed_locators.py
│   ├── recover_password_locators.py
│   └── checking_personal_account_locators.py
├── pages/                  # Page Object модели
│   ├── account_page.py
│   ├── login_page.py
│   ├── main_page.py
│   ├── order_feed_page.py
│   ├── password_recovery_page.py
│   └── reset_password_page.py
├── tests/                  # Тесты
│   ├── test_checking_personal_account.py
│   ├── test_checking_the_basic_functionality.py
│   ├── test_order_feed.py
│   └── test_password_recovery.py
├── conftest.py
├── .gitignore
├── data.py                 # Тестовые данные
├── url.py                  # URL-адреса приложения
├── requirements.txt        # Зависимости Python
└── README.md               # Этот файл

Установка и запуск
Установите зависимости:

pip install -r requirements.txt
Запустите тесты с генерацией отчета Allure:

pytest --alluredir=./allure-results
Для просмотра отчета:

allure serve ./allure-results
Тестовые сценарии
Проект включает следующие группы тестов:

Личный кабинет (TestAccountUI):

Доступ авторизованного пользователя

Переход в историю заказов

Выход из аккаунта

Основной функционал (TestBasicFunctionalityUI):

Навигация по приложению

Работа с модальными окнами

Добавление ингредиентов в заказ

Оформление заказа

Лента заказов (TestOrderHistory):

Просмотр деталей заказа

Отображение заказов пользователя

Проверка счетчиков заказов

Восстановление пароля (TestPasswordRecoveryUI):

Восстановление пароля

Проверка полей ввода
