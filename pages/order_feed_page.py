from .base_page import BasePage
import allure
from selenium.webdriver.common.by import By
from locators.order_feed_locators import OrderFeedPageLocators
import time


class OrderFeedPage(BasePage):

    @allure.step("Перейти на страницу Лента заказов")
    def go_to_login_page(self):
        self.go_to_site(ORDER_FEED_PAGE)

    @allure.step("Ожидание появления заказа {order_number} в ленте заказов")
    def wait_for_order_in_feed(self, order_number, timeout=30):
        try:
            # Ждем появления списка заказов
            self.wait_for_element_visible(OrderFeedPageLocators.ORDER_LIST, timeout)

            # Прокручиваем и ищем заказ
            start_time = time.time()
            while time.time() - start_time < timeout:
                # Ищем все видимые номера заказов
                order_elements = self.driver.find_elements(*OrderFeedPageLocators.ORDER_NUMBERS)

                # Проверяем каждый элемент
                for element in order_elements:
                    if order_number in element.text:
                        # Скроллим к найденному элементу для уверенности
                        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
                        return True

                # Если не нашли - скроллим вниз
                last_order = order_elements[-1] if order_elements else None
                if last_order:
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", last_order)

                # Небольшая пауза перед следующей проверкой
                time.sleep(1)

            # Если не нашли после всех попыток
            allure.attach(
                self.driver.get_screenshot_as_png(),
                name="order_not_found",
                attachment_type=allure.attachment_type.PNG
            )
            found_numbers = [el.text for el in order_elements]
            raise AssertionError(
                f"Заказ {order_number} не найден в ленте. Найдены: {found_numbers}"
            )

        except Exception as e:
            allure.attach(
                self.driver.get_screenshot_as_png(),
                name="error_snapshot",
                attachment_type=allure.attachment_type.PNG
            )
            raise AssertionError(f"Ошибка при поиске заказа: {str(e)}")