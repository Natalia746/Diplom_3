from .base_page import BasePage
import allure


class OrderFeedPage(BasePage):

    @allure.step("Перейти на страницу Лента заказов")
    def go_to_login_page(self):
        self.go_to_site(ORDER_FEED_PAGE)