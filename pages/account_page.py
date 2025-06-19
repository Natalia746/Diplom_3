import allure
from url import *
from .base_page import BasePage
from locators.recover_password_locators import RecoverLocators
from locators.checking_personal_account_locators import AccountLocators


class Account(BasePage):
    @allure.step("Перейти в личный кабинет")
    def go_to_account_page(self):
        self.go_to_site(ACCOUNT_PAGE)

    @allure.step("Клик по ссылке 'История заказов'")
    def click_order_history_link(self):
        self.wait_for_overlay_to_disappear(RecoverLocators.OVERLAY_LOCATOR, timeout=30)

        # Для Firefox - специальная обработка с кликом через JavaScript
        if self.driver.name == "firefox":
            # Находим элемент ссылки
            link = self.wait_for_element_clickable(AccountLocators.ORDER_HISTORY_LINK, timeout=15)
            # Прокручиваем к элементу
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center', behavior: 'instant'});",
                link
            )
            # Клик через JavaScript (обход перекрытия)
            self.driver.execute_script("arguments[0].click();", link)
        else:
            # Стандартная обработка для других браузеров
            self.click_element(AccountLocators.ORDER_HISTORY_LINK)

    @allure.step("Клик по кнопке 'Выход'")
    def click_logout_button(self):
        self.wait_for_overlay_to_disappear(RecoverLocators.OVERLAY_LOCATOR, timeout=45)
        # Для Firefox - специальная обработка с кликом через JavaScript
        if self.driver.name == "firefox":
            # Находим элемент кнопки
            button = self.wait_for_element_clickable(AccountLocators.LOGOUT_BUTTON, timeout=30)
            # Прокручиваем к элементу
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center', behavior: 'instant'});",
                button
            )
            # Клик через JavaScript (обход перекрытия)
            self.driver.execute_script("arguments[0].click();", button)
        else:
            # Стандартная обработка для других браузеров
            self.click_element(AccountLocators.LOGOUT_BUTTON)