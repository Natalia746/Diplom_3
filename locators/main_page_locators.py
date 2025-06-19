from selenium.webdriver.common.by import By

class MainPageLocators:
    ACCOUNT_BUTTON = (By.XPATH, "//p[text()='Личный Кабинет']")
    CONSTRUCTOR_BUTTON = (By.XPATH, "//p[text()='Конструктор']")
    HEADING = (By.XPATH, "//h1[text()='Соберите бургер']")