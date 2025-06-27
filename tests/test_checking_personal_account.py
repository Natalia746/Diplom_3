import allure
import pytest
from locators.recover_password_locators import RecoverLocators
from locators.main_page_locators import MainPageLocators
from pages.login_page import LoginPage
from pages.main_page import MainPage
from pages.account_page import Account
from locators.checking_personal_account_locators import AccountLocators
from url import *


@allure.epic("Личный кабинет")
class TestAccountUI:

    @allure.title("Переход в аккаунт по клику на кнопку Личный кабинет авторизованного пользователя")
    def test_authorized_user_can_access_personal_account(self, driver, registered_and_authorized_user):
        main_page = MainPage(driver, timeout=15)
        main_page.click_account_button()

        current_url = driver.current_url
        assert current_url == ACCOUNT_PAGE, \
            f"Ожидался URL личного кабинета '{ACCOUNT_PAGE}', но получен '{current_url}'"


    @allure.title("Переход в раздел История заказов из Личного кабинета")
    def test_navigate_to_order_history_from_account(self, driver, registered_and_authorized_user):
        main_page = MainPage(driver, timeout=15)
        main_page.click_account_button()

        account_page = Account(driver, timeout=15)
        account_page.current_url_should_be(ACCOUNT_PAGE)
        account_page.click_element_js(AccountLocators.ORDER_HISTORY_LINK)
        current_url = account_page.get_current_url()
        assert current_url == ORDER_HISTORY_PAGE, \
            f"Ожидался URL истории заказов '{ORDER_HISTORY_PAGE}', но получен '{driver.current_url}'"


    @allure.title("Выход из аккаунта из Личного кабинета")
    def test_user_logout(self, driver,registered_and_authorized_user):
        main_page = MainPage(driver, timeout=20)
        main_page.click_account_button()
        account_page = Account(driver, timeout=20)
        account_page.wait_for_element_clickable(AccountLocators.LOGOUT_BUTTON)
        account_page.click_logout_button()
        login_page = LoginPage(driver, timeout=30)
        login_page.wait_for_url_to_be(LOGIN_URL, timeout=30)
        main_page.go_to_site()
        main_page.wait_for_element_visible(MainPageLocators.LOGIN_BUTTON)
        assert main_page.is_element_visible(MainPageLocators.LOGIN_BUTTON), \
            "Кнопка входа не отображается после выхода из аккаунта"










