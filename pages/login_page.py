from .base_page import BasePage
from selenium.webdriver.common.by import By
import allure
from locators.recover_password_locators import RecoverLocators
from url import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC


class LoginPage(BasePage):

    @allure.step("Перейти на страницу логина")
    def go_to_login_page(self):
        self.go_to_site(LOGIN_PAGE)

    @allure.step("Нажать ссылку восстановления пароля")
    def click_restore_password_link(self):
        if self.driver.name == "firefox":
            self.wait_for_element_clickable(RecoverLocators.RESTORE_LINK, timeout=15)
            self.click_element(RecoverLocators.RESTORE_LINK)
        else:
            self.click_element(RecoverLocators.RESTORE_LINK)

        allure.attach(
            name="Нажата ссылка восстановления",
            body="Клик по 'Восстановить пароль'",
            attachment_type=allure.attachment_type.TEXT
        )

    @allure.step("Проверить наличие ссылки восстановления")
    def should_be_restore_link(self):
        self.element_should_be_present(RecoverLocators.RESTORE_LINK)







