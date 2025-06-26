from .base_page import BasePage
import allure
from selenium.webdriver.common.by import By
from locators.order_feed_locators import OrderFeedPageLocators
import time


class OrderFeedPage(BasePage):

    @allure.step("Перейти на страницу Лента заказов")
    def go_to_login_page(self):
        self.go_to_site(ORDER_FEED_PAGE)

