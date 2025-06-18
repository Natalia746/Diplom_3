import allure
import pytest
import time
from pages.login_page import LoginPage
from url import *
from locators.recover_password_locators import RecoverLocators
from locators.main_page_locators import MainPageLocators
from data import *



@allure.epic("Переход на страницу восстановления пароля по ссылке «Восстановить пароль»")
class TestPasswordRecoveryUI:
    @allure.title("Переход на страницу восстановления пароля через личный кабинет")
    def test_password_recovery_flow(self, driver):
        login_page = LoginPage(driver,timeout=3)
        login_page.wait_for_element_clickable(MainPageLocators.ACCOUNT_BUTTON)
        login_page.current_url_should_be(BASE_URL)
        login_page.click_element(MainPageLocators.ACCOUNT_BUTTON)
        login_page.should_be_restore_link()
        login_page.click_restore_password_link()
        login_page.current_url_should_be(FORGOT_PASSWORD_URL)
        login_page.element_should_be_present(RecoverLocators.RECOVER_BUTTON)

    @allure.title("Ввод существующего email для восстановления пароля")
    def test_recover_password_with_registered_email(self, driver):

        registered_email = REGISTERED_EMAIL
        login_page = LoginPage(driver, timeout=15)

        login_page.wait_for_element_clickable(MainPageLocators.ACCOUNT_BUTTON)
        login_page.current_url_should_be(BASE_URL)
        login_page.click_element(MainPageLocators.ACCOUNT_BUTTON)
        login_page.click_restore_password_link()
        login_page.current_url_should_be(FORGOT_PASSWORD_URL)
        login_page.input_text(RecoverLocators.EMAIL_INPUT, registered_email)
        login_page.click_element(RecoverLocators.RECOVER_BUTTON)
        login_page.wait_for_url_to_be(RESET_PASSWORD_PAGE)

    @allure.title("Проверка подсветки поля пароля при клике на иконку глаза")
    def test_password_field_highlight_on_eye_click(self, driver):
        registered_email = REGISTERED_EMAIL
        login_page = LoginPage(driver, timeout=15)

        login_page.wait_for_element_clickable(MainPageLocators.ACCOUNT_BUTTON)
        login_page.current_url_should_be(BASE_URL)
        login_page.click_element(MainPageLocators.ACCOUNT_BUTTON)
        login_page.wait_for_overlay_to_disappear(RecoverLocators.OVERLAY_LOCATOR)
        login_page.click_restore_password_link()

        login_page.current_url_should_be(FORGOT_PASSWORD_URL)
        login_page.input_text(RecoverLocators.EMAIL_INPUT, registered_email)
        login_page.wait_for_element_clickable(RecoverLocators.RECOVER_BUTTON)
        login_page.click_element(RecoverLocators.RECOVER_BUTTON)

        login_page.wait_for_url_to_be(RESET_PASSWORD_PAGE)
        login_page.check_password_highlight(should_be_highlighted=False)
        login_page.click_show_password()
        login_page.wait_for_password_highlight()





