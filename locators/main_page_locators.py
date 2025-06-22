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
    INGREDIENT_MODAL_CLOSE_BUTTON = (By.CSS_SELECTOR, "button.Modal_modal__close_modified__3V5XS")
    INGREDIENT_COUNTER = (By.XPATH, "//p[text()='Соус Spicy-X']/ancestor::a//div[contains(@class, 'counter_counter__')]/p")
    INGREDIENT_SAUCE = (
    By.XPATH, "//p[@class='BurgerIngredient_ingredient__text__yp3dH' and text()='Соус Spicy-X']/ancestor::a")  # Ингредиент
    DROP_AREA = (By.CSS_SELECTOR, "ul.BurgerConstructor_basket__list__l9dp_")  # Область сброса
    CONSTRUCTOR_SAUCE_SPICY = (By.CSS_SELECTOR, "div.constructor-element img[alt='Соус Spicy-X']")
    ORDER_IN_PROGRESS_TEXT = (
    By.XPATH, "//p[contains(@class, 'text_type_main-small') and contains(text(), 'Ваш заказ начали готовить')]")
    BUN_IMAGE =(By.XPATH, "//img[@class='constructor-element__image' and @alt='Краторная булка N-200i (верх)']")
    ORDER_BUTTON = (By.XPATH, "//button[contains(text(), 'Оформить заказ')]")
    ORDER_CLOSE_BUTTON = (By.CSS_SELECTOR, "button.Modal_modal__close__TnseK")
    ORDER_NUMBER_LOCATOR = (By.XPATH, "//h2[contains(@class, 'Modal_modal__title') and contains(@class, 'text_type_digits-large')]")
    LOADING_ANIMATION = (By.CSS_SELECTOR, "img.Modal_modal__loading__3534A")
    TICK_ANIMATION_LOCATOR = (By.CSS_SELECTOR, "img.Modal_modal__image__2nh17[alt='tick animation']")

