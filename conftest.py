import pytest
from selenium import webdriver
from url import *
import allure
from pages.main_page import MainPage
from pages.login_page import LoginPage
from data import REGISTERED_EMAIL, REGISTERED_PASSWORD
from locators.main_page_locators import MainPageLocators
from locators.recover_password_locators import RecoverLocators
from locators.checking_personal_account_locators import AccountLocators
import requests
import time



@pytest.fixture(params=["chrome", "firefox"])
def driver(request):
    if request.param == "chrome":
        driver = webdriver.Chrome()
        driver.set_window_size(1920, 1080)
        driver.get(BASE_URL)
    elif request.param == "firefox":
        driver = webdriver.Firefox()
        driver.set_window_size(1920, 1080)
        driver.get(BASE_URL)
        driver.implicitly_wait(30)
    yield driver
    driver.quit()


@pytest.fixture
def go_to_account_page(driver):
    """Фикстура для перехода на страницу аккаунта"""
    main_page = MainPage(driver)

    with allure.step("Ожидание кликабельности кнопки аккаунта"):
        main_page.wait_for_element_clickable(MainPageLocators.ACCOUNT_BUTTON)

    with allure.step("Проверка текущего URL"):
        main_page.current_url_should_be(BASE_URL)

    with allure.step("Клик по кнопке аккаунта"):
        main_page.click_element(MainPageLocators.ACCOUNT_BUTTON)

    yield driver


@pytest.fixture
def registered_and_authorized_user(driver):
    """Фикстура для регистрации, авторизации и последующего удаления пользователя"""
    # 1. Регистрация пользователя через API
    email = f'test_user_{time.time()}@example.com'
    password = 'P@ssw0rd123'
    name = 'Test User'

    user_data = {
        "email": email,
        "password": password,
        "name": name
    }

    response = requests.post(
        BASE_URL + REGISTER,
        json=user_data
    )
    assert response.status_code == 200, f"Failed to register user: {response.text}"
    token = response.json()['accessToken']
    user_data['token'] = token

    # 2. Авторизация в UI
    main_page = MainPage(driver, timeout=15)
    login_page = LoginPage(driver, timeout=15)

    main_page.wait_for_element_clickable(MainPageLocators.ACCOUNT_BUTTON)
    main_page.click_element(MainPageLocators.ACCOUNT_BUTTON)

    login_page.input_text(RecoverLocators.EMAIL_INPUT, email)
    login_page.input_text(RecoverLocators.PASSWORD_INPUT, password)
    login_page.click_element(AccountLocators.SUBMIT_BUTTON)
    # Ожидаем появления кнопки заказа как признака успешной авторизации
    main_page.wait_for_element_visible(MainPageLocators.ORDER_BUTTON, timeout=20)

    yield {
        "driver": driver,
        "email": email,
        "password": password,
        "name": name,
        "token": token
    }

    # 3. Удаление пользователя после теста
    delete_response = requests.delete(
        BASE_URL + DELETE_USER,
        headers={'Authorization': token}
    )
    assert delete_response.status_code == 202, f"Failed to delete user: {delete_response.text}"

