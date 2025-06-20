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
    def test_authorized_user_can_access_personal_account(self, driver, authorized_user):
        main_page = MainPage(driver, timeout=15)
        main_page.click_account_button()

        account_page = Account(driver, timeout=15)
        account_page.current_url_should_be(ACCOUNT_PAGE)

    @allure.title("Переход в раздел История заказов из Личного кабинета")
    def test_navigate_to_order_history_from_account(self, driver, authorized_user):
        main_page = MainPage(driver, timeout=15)
        main_page.click_account_button()

        account_page = Account(driver, timeout=15)
        account_page.current_url_should_be(ACCOUNT_PAGE)
        account_page.click_order_history_link()

        account_page.wait_for_url_to_be(ORDER_HISTORY_PAGE)
        account_page.element_should_be_present(AccountLocators.ORDER_HISTORY_ACTIVE_LINK)

    @allure.title("Выход из аккаунта из Личного кабинета")
    def test_user_logout(self, driver, authorized_user):
        main_page = MainPage(driver, timeout=15)
        main_page.click_account_button()
        account_page = Account(driver, timeout=15)
        account_page.element_should_be_present(AccountLocators.LOGOUT_BUTTON)
        account_page.click_logout_button()
        login_page = LoginPage(driver, timeout=30)
        login_page.wait_for_url_to_be(LOGIN_URL, timeout=30)









