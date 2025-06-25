import allure
import pytest
from locators.recover_password_locators import RecoverLocators
from locators.main_page_locators import MainPageLocators
from pages.login_page import LoginPage
from pages.main_page import MainPage
from pages.account_page import Account
from locators.checking_personal_account_locators import AccountLocators
from url import *
from locators.order_feed_locators import OrderFeedPageLocators
from pages.order_feed_page import OrderFeedPage
from seletools.actions import drag_and_drop
import time
from selenium.webdriver.common.action_chains import ActionChains

@allure.epic("Основной функционал")
class TestBasicFunctionalityUI:

    @allure.feature("Навигация")
    @allure.title("Переход в конструктор по клику на 'Конструктор'")
    def test_navigation_to_constructor(self, driver, go_to_account_page):
        login_page = LoginPage(driver, timeout=15)
        main_page = MainPage(driver, timeout=15)

        login_page.current_url_should_be(LOGIN_URL)
        login_page.click_element(MainPageLocators.CONSTRUCTOR_BUTTON)
        main_page.current_url_should_be(BASE_URL)
        heading_text = main_page.find_element(MainPageLocators.HEADING).text
        assert heading_text == "Соберите бургер", \
            f"Текст заголовка не совпадает. Ожидалось: 'Соберите бургер', Фактически: '{heading_text}'"

    @allure.title("Переход на страницу ленты заказов по клику на 'Лента заказов'")
    def test_navigation_to_order_feed (self, driver):
        main_page = MainPage(driver)
        order_feed_page = OrderFeedPage(driver)

        main_page.current_url_should_be(BASE_URL)
        main_page.click_element(MainPageLocators.ORDER_FEED_BUTTON)
        heading_text =order_feed_page.find_element(OrderFeedPageLocators.FEED_HEADING).text
        assert heading_text == "Лента заказов", \
            f"Текст заголовка не совпадает. Ожидалось: 'Лента заказов', Фактически: '{heading_text}'"

    @allure.feature("Модальное окно с деталями ингредиента")
    @allure.title("Отображение модального окна с деталями ингредиента при клике")
    def test_ingredient_details_popup(self, driver):
        main_page = MainPage(driver)

        # Открываем модальное окно и получаем данные ингредиента
        name, details = main_page.open_and_check_ingredient_modal()

        # Проверяем, что название ингредиента в модальном окне соответствует выбранному
        modal_title = main_page.get_ingredient_modal_name()
        assert modal_title == name, \
            f"Название ингредиента в модальном окне '{modal_title}' не соответствует ожидаемому '{name}'"
        # Проверяем, что отображаются калории
        assert details['calories'] is not None, "Не отображаются калории ингредиента"

        # Проверяем, что отображаются белки
        assert details['proteins'] is not None, "Не отображаются белки ингредиента"

        # Проверяем, что отображаются жиры
        assert details['fat'] is not None, "Не отображаются жиры ингредиента"

        # Проверяем, что отображаются углеводы
        assert details['carbohydrates'] is not None, "Не отображаются углеводы ингредиента"

    @allure.title("Закрытие модального окна с деталями ингредиента кликом по крестику")
    def test_close_ingredient_popup_by_close_button(self, driver):
        main_page = MainPage(driver)
        main_page.open_and_check_ingredient_modal()
        main_page.click_element(MainPageLocators.INGREDIENT_MODAL_CLOSE_BUTTON)
        main_page.wait_for_element_invisible(MainPageLocators.INGREDIENT_DETAILS_MODAL)
        assert not main_page.is_element_visible(MainPageLocators.INGREDIENT_DETAILS_MODAL), \
            "Модальное окно с деталями ингредиента осталось видимым после закрытия"

    @allure.title("Счетчик ингредиента увеличивается при добавлении в заказ")
    def test_ingredient_counter_increases_when_added(self, driver):
        main_page = MainPage(driver)

        # Шаг 1: Проверить начальное состояние
        with allure.step("Проверить начальное состояние"):
            initial_counter = main_page.get_ingredient_counter_value()
            assert initial_counter == "0", f"Начальное значение счетчика должно быть 0, а получили {initial_counter}"

        # Шаг 2: Перетащить соус в корзину
        with allure.step("Перетащить соус в корзину"):
            main_page.drag_ingredient_to_constructor(
                ingredient_locator=MainPageLocators.INGREDIENT_SAUCE,
                target_locator=MainPageLocators.DROP_AREA,
                confirmation_locator=MainPageLocators.CONSTRUCTOR_SAUCE_SPICY
            )

        # Шаг 3: Проверить увеличение счетчика
        with allure.step("Проверить увеличение счетчика"):
            updated_counter = main_page.get_ingredient_counter_value()
            assert updated_counter == "1", f"После добавления ингредиента счетчик должен быть 1, а получили {updated_counter}"

    @allure.title("Авторизованный пользователь может успешно оформить заказ")
    def test_authorized_user_can_make_order(self, driver, registered_and_authorized_user):
        main_page = MainPage(driver)

        with allure.step("Перетащить ингредиенты в корзину"):
            main_page.drag_ingredient_to_constructor(
            MainPageLocators.INGREDIENT_SAUCE,
            MainPageLocators.DROP_AREA,
            MainPageLocators.CONSTRUCTOR_SAUCE_SPICY)

        main_page.drag_ingredient_to_constructor(
            MainPageLocators.INGREDIENT_BUN,
            MainPageLocators.DROP_AREA,
            MainPageLocators.BUN_IMAGE
        )
        main_page.click_element_js(MainPageLocators.ORDER_BUTTON)
        assert main_page.wait_for_element_visible(MainPageLocators.ORDER_IN_PROGRESS_TEXT)
