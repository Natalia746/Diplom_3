import allure
import pytest
from data import *
from locators.recover_password_locators import RecoverLocators
from locators.main_page_locators import MainPageLocators
from pages.login_page import LoginPage
from pages.main_page import MainPage
from pages.account_page import Account
from locators.checking_personal_account_locators import AccountLocators
from url import *


@allure.epic("Основной функционал")
class TestBasicFunctionalityUI:

    @allure.feature("Навигация")
    @allure.title("Переход в конструктор по клику на 'Конструктор'")
    def test_navigation_to_constructor(self, driver, go_to_account_page):
        login_page = LoginPage(driver, timeout=30)
        main_page = MainPage(driver, timeout=30)

        login_page.current_url_should_be(LOGIN_URL)
        login_page.click_element(MainPageLocators.CONSTRUCTOR_BUTTON)
        main_page.current_url_should_be(BASE_URL)
        heading_text = main_page.find_element(MainPageLocators.HEADING).text
        assert heading_text == "Соберите бургер", \
            f"Текст заголовка не совпадает. Ожидалось: 'Соберите бургер', Фактически: '{heading_text}'"




