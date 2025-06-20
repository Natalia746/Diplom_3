import allure
import pytest
from locators.main_page_locators import MainPageLocators
from locators.order_feed_locators import OrderFeedPageLocators
from pages.main_page import MainPage
from pages.order_feed_page import OrderFeedPage
from url import *
from pages.account_page import Account
from locators.checking_personal_account_locators import AccountLocators


@allure.epic("Лента заказов")
class TestOrderHistory:
    @allure.title("Клик по заказу в Ленте заказов открывает модальное окно с деталями заказа")
    def test_click_order_opens_details_modal(self, driver):
        main_page = MainPage(driver)
        main_page.click_element( MainPageLocators.ORDER_FEED_BUTTON)

        order_feed_page = OrderFeedPage(driver)
        order_feed_page.current_url_should_be(ORDER_FEED_PAGE)
        order_feed_page.element_should_be_present(OrderFeedPageLocators.FIRST_ORDER_IN_LIST)
        order_feed_page.click_element(OrderFeedPageLocators.FIRST_ORDER_IN_LIST)
        order_feed_page.element_should_be_present(OrderFeedPageLocators.MODAL_CONTAINER)
        order_feed_page.element_should_be_present(OrderFeedPageLocators.COMPOSITION_TITLE)

    @allure.title("Заказы из истории пользователя отображаются в Ленте заказов")
    def test_user_orders_displayed_in_feed(self, driver, authorized_user):
        main_page = MainPage(driver)
        account_page = Account(driver, timeout=15)

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
        main_page.click_element(MainPageLocators.ORDER_BUTTON)
        main_page.wait_for_element_visible(MainPageLocators.ORDER_IN_PROGRESS_TEXT)
        account_page.go_to_account_page()
        with allure.step("Переход в историю заказов"):
            main_page = MainPage(driver)
            main_page.click_account_button()

            account_page.current_url_should_be(ACCOUNT_PAGE)
            account_page.click_order_history_link()
            account_page.element_should_be_present(AccountLocators.ORDER_HISTORY_ACTIVE_LINK)

        with allure.step("Получение номера заказа"):
            account_page.scroll_to_element()
            order_number = account_page.get_element_text(
                AccountLocators.MY_FIRST_ORDER_NUMBER
            ).strip()
            assert order_number.startswith("#"), "Номер заказа должен начинаться с #"
            allure.attach(order_number, name="Order Number")

        with allure.step("Переход в ленту заказов"):
            account_page.click_element(MainPageLocators.ORDER_FEED_BUTTON)
            order_feed_page = OrderFeedPage(driver)
            # Проверяем заголовок
            heading_text = order_feed_page.get_element_text(OrderFeedPageLocators.FEED_HEADING)
            assert "Лента заказов" in heading_text, f"Заголовок не содержит 'Лента заказов': {heading_text}"

        with allure.step("Поиск заказа в ленте"):
            try:
                order_feed_page.wait_for_order_in_feed(order_number, timeout=30)
            except Exception as e:
                allure.attach(
                    driver.get_screenshot_as_png(),
                    name="final_check_failed",
                    attachment_type=allure.attachment_type.PNG
                )
                raise






