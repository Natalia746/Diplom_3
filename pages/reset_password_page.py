from .base_page import BasePage
import allure
from locators.recover_password_locators import RecoverLocators

class ResetPasswordPage(BasePage):

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
            self.click_element_js(RecoverLocators.SHOW_PASSWORD_BUTTON)
        else:
            # Стандартная обработка для других браузеров
            self.click_element(RecoverLocators.SHOW_PASSWORD_BUTTON)