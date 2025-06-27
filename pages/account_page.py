import allure
from url import *
from .base_page import BasePage
from locators.recover_password_locators import RecoverLocators
from locators.checking_personal_account_locators import AccountLocators


class Account(BasePage):

    @allure.step("Клик по кнопке 'Выход'")
    def click_logout_button(self):
        self.wait_for_overlay_to_disappear(RecoverLocators.OVERLAY_LOCATOR, timeout=30)
        # Для Firefox - специальная обработка с кликом через JavaScript
        if self.driver.name == "firefox":
            self.click_element_js(AccountLocators.LOGOUT_BUTTON)
        else:
            self.click_element(AccountLocators.LOGOUT_BUTTON)