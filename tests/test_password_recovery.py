import allure
import pytest
import time
from pages.login_page import LoginPage
from url import *
from locators.recover_password_locators import RecoverLocators
from locators.main_page_locators import MainPageLocators
from data import *
from pages.main_page import MainPage
from pages.password_recovery_page import PasswordRecovery
from pages.reset_password_page import ResetPasswordPage


@allure.epic("Переход на страницу восстановления пароля по ссылке «Восстановить пароль»")
class TestPasswordRecoveryUI:
    @allure.title("Переход на страницу восстановления пароля через личный кабинет")
    def test_password_recovery_flow(self, driver):
        main_page = MainPage(driver, timeout=3)
        main_page.wait_for_element_clickable(MainPageLocators.ACCOUNT_BUTTON)
        main_page.current_url_should_be(BASE_URL)
        main_page.click_element(MainPageLocators.ACCOUNT_BUTTON)

        login_page = LoginPage(driver, timeout=3)

        login_page.should_be_restore_link()
        login_page.click_restore_password_link()

        password_recovery_page = PasswordRecovery(driver, timeout=3)

        password_recovery_page.current_url_should_be(FORGOT_PASSWORD_URL)
        password_recovery_page.element_should_be_present(RecoverLocators.RECOVER_BUTTON)

    @allure.title("Ввод существующего email для восстановления пароля")
    def test_recover_password_with_registered_email(self, driver):

        registered_email = REGISTERED_EMAIL
        main_page = MainPage(driver, timeout=15)

        main_page.wait_for_element_clickable(MainPageLocators.ACCOUNT_BUTTON)
        main_page.current_url_should_be(BASE_URL)
        main_page.click_element(MainPageLocators.ACCOUNT_BUTTON)
        login_page = LoginPage(driver, timeout=15)
        login_page.click_restore_password_link()
        password_recovery_page = PasswordRecovery(driver, timeout=5)
        password_recovery_page.current_url_should_be(FORGOT_PASSWORD_URL)
        password_recovery_page.input_text(RecoverLocators.EMAIL_INPUT, registered_email)
        password_recovery_page.click_element(RecoverLocators.RECOVER_BUTTON)
        password_recovery_page.wait_for_url_to_be(RESET_PASSWORD_PAGE)

    @allure.title("Проверка подсветки поля пароля при клике на иконку глаза")
    def test_password_field_highlight_on_eye_click(self, driver):
        registered_email = REGISTERED_EMAIL

        main_page = MainPage(driver, timeout=15)

        main_page.wait_for_element_clickable(MainPageLocators.ACCOUNT_BUTTON)
        main_page.click_element(MainPageLocators.ACCOUNT_BUTTON)

        login_page = LoginPage(driver, timeout=15)

        login_page.wait_for_overlay_to_disappear(RecoverLocators.OVERLAY_LOCATOR)
        login_page.click_restore_password_link()

        password_recovery_page = PasswordRecovery(driver, timeout=5)

        password_recovery_page.current_url_should_be(FORGOT_PASSWORD_URL)
        password_recovery_page.input_text(RecoverLocators.EMAIL_INPUT, registered_email)
        password_recovery_page.wait_for_element_clickable(RecoverLocators.RECOVER_BUTTON)
        password_recovery_page.click_element(RecoverLocators.RECOVER_BUTTON)

        reset_page = ResetPasswordPage(driver, timeout=15)

        reset_page.wait_for_url_to_be(RESET_PASSWORD_PAGE)
        reset_page.check_password_highlight(should_be_highlighted=False)
        reset_page.click_show_password()
        reset_page.wait_for_password_highlight()





