import pytest
from selenium import webdriver
from url import *
import pytest
import allure
from pages.main_page import MainPage
from pages.login_page import LoginPage
from data import REGISTERED_EMAIL, REGISTERED_PASSWORD
from locators.main_page_locators import MainPageLocators
from locators.recover_password_locators import RecoverLocators
from locators.checking_personal_account_locators import AccountLocators


@pytest.fixture
def authorized_user(driver):
    """Фикстура для авторизации пользователя перед тестом"""
    main_page = MainPage(driver, timeout=15)
    login_page = LoginPage(driver, timeout=15)

    main_page.wait_for_element_clickable(MainPageLocators.ACCOUNT_BUTTON)
    main_page.click_element(MainPageLocators.ACCOUNT_BUTTON)

    login_page.input_text(RecoverLocators.EMAIL_INPUT, REGISTERED_EMAIL)
    login_page.input_text(RecoverLocators.PASSWORD_INPUT, REGISTERED_PASSWORD)
    login_page.click_element(AccountLocators.SUBMIT_BUTTON)

    main_page.wait_for_element_visible(MainPageLocators.ACCOUNT_BUTTON)
    yield driver


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

    yield driver  # Возвращаем драйвер для использования в тесте
