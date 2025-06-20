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
    def get_ingredient_counter_value(self):
        try:
            counter = self.get_element_text(MainPageLocators.INGREDIENT_COUNTER)
            return counter if counter else "0"  # На случай если текст пустой
        except:
            # Если элемент не найден или не виден, считаем что значение 0
            return "0"

    def js_drag_and_drop(self,driver, source, target):
        driver.execute_script("""
            function triggerDragAndDrop(selectorDrag, selectorDrop) {
                var elemDrag = arguments[0], elemDrop = arguments[1];
                var dataTransfer = new DataTransfer();
                var fireEvent = function(type, elem) {
                    var event = new DragEvent(type, {
                        bubbles: true,
                        cancelable: true,
                        dataTransfer: dataTransfer
                    });
                    elem.dispatchEvent(event);
                };
                fireEvent('dragstart', elemDrag);
                fireEvent('dragenter', elemDrop);
                fireEvent('dragover', elemDrop);
                fireEvent('drop', elemDrop);
                fireEvent('dragend', elemDrag);
            }
            triggerDragAndDrop(arguments[0], arguments[1]);
        """, source, target)

