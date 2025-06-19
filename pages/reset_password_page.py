from .base_page import BasePage
import allure

class ResetPasswordPage(BasePage):

    allure.step("Перейти на страницу ввода нового пароля")
    def go_to_password_reset_page(self):
        self.go_to_site(RESET_PASSWORD_PAGE)

