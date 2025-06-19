from .base_page import BasePage
import allure

class MainPage(BasePage):

    @allure.step("Перейти на главную страницу")
    def go_to_main_page(self):
        self.go_to_site(BASE_URL)

