from .base_page import BasePage
import allure

class PasswordRecovery(BasePage):

    allure.step("Перейти на страницу восстановления пароля")
    def go_to_password_recovery_page(self):
        self.go_to_site(FORGOT_PASSWORD_URL)