import allure
import pytest
from data import *
from locators.recover_password_locators import RecoverLocators
from locators.main_page_locators import MainPageLocators
from pages.login_page import LoginPage
from pages.main_page import MainPage
from pages.account_page import Account
from locators.checking_personal_account_locators import AccountLocators
from url import *
from locators.order_feed_locators import OrderFeedPageLocators
from pages.order_feed_page import OrderFeedPage


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

    @allure.title("Отображение модального окна с деталями ингредиента при клике")
    def test_ingredient_details_popup(self,driver):
        main_page = MainPage(driver)
        main_page.open_and_check_ingredient_modal()

    @allure.title("Закрытие модального окна с деталями ингредиента кликом по крестику")
    def test_close_ingredient_popup_by_close_button(self, driver):
        main_page = MainPage(driver)
        main_page.open_and_check_ingredient_modal()





