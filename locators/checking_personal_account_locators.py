from selenium.webdriver.common.by import By


class AccountLocators:
    SUBMIT_BUTTON = (By.XPATH, "//button[text()='Войти']")
    ORDER_HISTORY_LINK = (By.XPATH,"//a[text()='История заказов']")
    ORDER_HISTORY_ACTIVE_LINK = (
    By.XPATH, "//a[contains(@class, 'Account_link_active__2opc9') and text()='История заказов']")
    LOGOUT_BUTTON = (By.XPATH, "//button[contains(@class, 'Account_button__14Yp3') and text()='Выход']")