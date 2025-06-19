from .base_page import BasePage
import allure
from locators.recover_password_locators import RecoverLocators
from locators.main_page_locators import MainPageLocators


class MainPage(BasePage):

    @allure.step("Перейти на главную страницу")
    def go_to_main_page(self):
        self.go_to_site(BASE_URL)

    @allure.step("Клик по кнопке 'Личный кабинет'")
    def click_account_button(self):
        self.wait_for_overlay_to_disappear(RecoverLocators.OVERLAY_LOCATOR, timeout=30)

        # Для Firefox - специальная обработка с кликом через JavaScript
        if self.driver.name == "firefox":
            # Находим элемент кнопки
            button = self.wait_for_element_clickable(MainPageLocators.ACCOUNT_BUTTON, timeout=30)

            # Прокручиваем к элементу
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center', behavior: 'instant'});",
                button
            )

            # Клик через JavaScript (обход перекрытия)
            self.driver.execute_script("arguments[0].click();", button)
        else:
            # Стандартная обработка для других браузеров
            self.click_element(MainPageLocators.ACCOUNT_BUTTON)

    @allure.step("Открыть и проверить модальное окно ингредиента")
    def open_and_check_ingredient_modal(self):
        self.click_element(MainPageLocators.INGREDIENT_BUN)
        self.element_should_be_present(MainPageLocators.INGREDIENT_DETAILS_MODAL)
        self.element_should_be_present(MainPageLocators.INGREDIENT_MODAL_NAME)

