from selenium.webdriver.common.by import By

class MainPageLocators:
    ACCOUNT_BUTTON = (By.XPATH, "//p[text()='Личный Кабинет']")
    CONSTRUCTOR_BUTTON = (By.XPATH, "//p[text()='Конструктор']")
    HEADING = (By.XPATH, "//h1[text()='Соберите бургер']")
    ORDER_FEED_BUTTON = (By.XPATH, "//p[text()='Лента Заказов']")
    INGREDIENT_BUN = (
    By.XPATH, "//a[contains(@class, 'BurgerIngredient_ingredient__1TVf6') and .//p[text()='Краторная булка N-200i']]")
    INGREDIENT_DETAILS_MODAL = (
    By.XPATH, "//div[contains(@class, 'Modal_modal__container__Wo2l') and .//h2[contains(text(), 'Детали ингредиента')]]")
    # модальное окно
    INGREDIENT_MODAL_NAME = (By.XPATH, "//p[text()='Краторная булка N-200i']")
