from .base_page import BasePage
import allure
from selenium.webdriver.common.by import By
from locators.order_feed_locators import OrderFeedPageLocators
import time


class OrderFeedPage(BasePage):

    @allure.step("Перейти на страницу Лента заказов")
    def go_to_login_page(self):
        self.go_to_site(ORDER_FEED_PAGE)

    @allure.step("Проверка отображения заказа")
    def is_order_displayed(self, order_number):
        order_in_feed_locator = (
        By.XPATH, f"//p[contains(@class, 'text_type_digits-default') and text()='{order_number}']")
        order_in_feed = self.wait_for_element_visible(order_in_feed_locator, timeout=30)
        return order_in_feed.is_displayed()