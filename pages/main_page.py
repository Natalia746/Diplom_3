from .base_page import BasePage
import allure
from locators.recover_password_locators import RecoverLocators
from locators.main_page_locators import MainPageLocators
from locators.order_feed_locators import OrderFeedPageLocators
from url import *


class MainPage(BasePage):

    @allure.step("Перейти на главную страницу")
    def go_to_main_page(self):
        self.go_to_site(BASE_URL)

    @allure.step("Клик по кнопке 'Личный кабинет'")
    def click_account_button(self):
        self.wait_for_overlay_to_disappear(RecoverLocators.OVERLAY_LOCATOR, timeout=30)

        # Для Firefox - специальная обработка с кликом через JavaScript
        if self.driver.name == "firefox":
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

    @allure.step("Получить значение счетчика ингредиента (по умолчанию 0, если не виден)")
    def get_ingredient_counter_value(self, counter_locator):
        """Получает значение счетчика ингредиента по указанному локатору"""
        try:
            return self.wait_for_element_visible(counter_locator, timeout=5).text
        except:
            return "0"  # Если счетчик не найден, считаем что значение 0

    @allure.step("Перейти в ленту заказов и проверить заголовок")
    def go_to_order_feed_and_check_header(self):
        """Переходит на страницу ленты заказов и проверяет наличие заголовка"""
        self.go_to_site(ORDER_FEED_PATH)
        heading_text = self.get_element_text(OrderFeedPageLocators.FEED_HEADING)
        assert "Лента заказов" in heading_text, (
            f"Заголовок не содержит 'Лента заказов': {heading_text}"
        )

    @allure.step("Открыть и проверить модальное окно ингредиента")
    def open_and_check_ingredient_modal(self):
        # Кликаем на ингредиент (например, булку)
        self.click_element(MainPageLocators.INGREDIENT_BUN)

        # Ожидаем появление модального окна
        self.wait_for_element_visible(MainPageLocators.INGREDIENT_DETAILS_MODAL)
        self.wait_for_element_visible(MainPageLocators.INGREDIENT_MODAL_NAME)

        # Получаем данные ингредиента
        name = self.get_ingredient_modal_name()
        details = {
            'calories': self.get_ingredient_detail_text(MainPageLocators.INGREDIENT_CALORIES),
            'proteins': self.get_ingredient_detail_text(MainPageLocators.INGREDIENT_PROTEINS),
            'fat': self.get_ingredient_detail_text(MainPageLocators.INGREDIENT_FAT),
            'carbohydrates': self.get_ingredient_detail_text(MainPageLocators.INGREDIENT_CARBOHYDRATES)
        }
        return name, details

    @allure.step("Получить название ингредиента в модальном окне")
    def get_ingredient_modal_name(self):
        return self.get_element_text(MainPageLocators.INGREDIENT_MODAL_NAME)

    @allure.step("Получить текст деталей ингредиента")
    def get_ingredient_detail_text(self, locator):
        return self.get_element_text(locator)

    @allure.step("Проверить видимость модального окна ингредиента")
    def is_ingredient_modal_visible(self):
        return self.is_element_visible(MainPageLocators.INGREDIENT_DETAILS_MODAL)

    @allure.step("Закрыть модальное окно ингредиента")
    def close_ingredient_modal(self):
        self.click_element(MainPageLocators.MODAL_CLOSE_BUTTON)
        self.wait_for_element_invisible(MainPageLocators.INGREDIENT_DETAILS_MODAL)
