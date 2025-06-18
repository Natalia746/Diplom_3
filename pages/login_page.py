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

    @allure.step("Клик по кнопке показать/скрыть пароль")
    def click_show_password(self):
        self.wait_for_overlay_to_disappear(RecoverLocators.OVERLAY_LOCATOR, timeout=30)

        # Для Firefox - специальная обработка с кликом через JavaScript
        if self.driver.name == "firefox":
            # Находим элемент кнопки
            button = self.wait_for_element_clickable(RecoverLocators.SHOW_PASSWORD_BUTTON, timeout=30)

            # Прокручиваем к элементу
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center', behavior: 'instant'});",
                button
            )

            # Клик через JavaScript (обход перекрытия)
            self.driver.execute_script("arguments[0].click();", button)
        else:
            # Стандартная обработка для других браузеров
            self.click_element(RecoverLocators.SHOW_PASSWORD_BUTTON)

    def check_password_highlight(self, should_be_highlighted=True):
        wrapper = self.find_element(RecoverLocators.PASSWORD_INPUT)
        classes = wrapper.get_attribute("class")
        if should_be_highlighted:
            assert "input__placeholder-focused" in classes, "Поле должно быть подсвечено"
        else:
            assert "input__placeholder-focused" not in classes, "Поле не должно быть подсвечено"

    @allure.step("Дождаться подсветки поля пароля")
    def wait_for_password_highlight(self, timeout=10):
        # Ожидаем появления класса подсветки
        WebDriverWait(self.driver, timeout).until(
            lambda d: "input__placeholder-focused" in d.find_element(
                *RecoverLocators.PASSWORD_LABEL
            ).get_attribute("class"),
            message="Подсветка поля пароля не появилась"
        )

        # Дополнительная проверка через видимость элемента подсветки
        self.wait_for_element_visible(RecoverLocators.ILLUMINATED_PASSWORD_FIELD, timeout)

