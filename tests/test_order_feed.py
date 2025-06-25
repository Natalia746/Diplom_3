import time
import allure
import pytest
from locators.main_page_locators import MainPageLocators
from locators.order_feed_locators import OrderFeedPageLocators
from locators.recover_password_locators import RecoverLocators
from pages.main_page import MainPage
from pages.order_feed_page import OrderFeedPage
from url import *
from pages.account_page import Account
from locators.checking_personal_account_locators import AccountLocators
from selenium.webdriver.common.by import By
from pages.login_page import LoginPage


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

        assert order_feed_page.is_element_visible(OrderFeedPageLocators.MODAL_CONTAINER), \
            "Модальное окно с деталями заказа не отобразилось"

        assert order_feed_page.is_element_visible(OrderFeedPageLocators.COMPOSITION_TITLE), \
            "Не найден заголовок 'Состав' в модальном окне"

        assert len(driver.find_elements(*OrderFeedPageLocators.STATUS)) > 0, \
            "В модальном окне не отображаются ингредиенты заказа"

    @allure.title("Заказы из истории пользователя отображаются в Ленте заказов")
    def test_user_orders_displayed_in_feed(self, driver, registered_and_authorized_user):
        main_page = MainPage(driver)
        order_feed_page = OrderFeedPage(driver)

        with allure.step("Перетащить ингредиенты в корзину"):
            main_page.drag_ingredient_to_constructor(
                MainPageLocators.INGREDIENT_SAUCE,
                MainPageLocators.DROP_AREA,
                MainPageLocators.CONSTRUCTOR_SAUCE_SPICY)

            main_page.drag_ingredient_to_constructor(
                MainPageLocators.INGREDIENT_BUN,
                MainPageLocators.DROP_AREA,
                MainPageLocators.BUN_IMAGE)
            main_page.click_element_js(MainPageLocators.ORDER_BUTTON)

        with allure.step("Получить номер заказа"):

            main_page.wait_for_element_visible(MainPageLocators.TICK_ANIMATION_LOCATOR)
            order_number_element = main_page.wait_for_element_visible(MainPageLocators.ORDER_NUMBER_LOCATOR, timeout=30)
            main_page.wait_for_element_invisible(MainPageLocators.LOADING_ANIMATION)
            order_number = f"#0{order_number_element.text.strip()}"

        main_page.go_to_order_feed_and_check_header()

        with allure.step("Проверить наличие созданного заказа в ленте"):
            order_in_feed_locator = ((By.XPATH, f"//p[contains(@class, 'text_type_digits-default') and text()='{order_number}']"))
            order_in_feed = order_feed_page.wait_for_element_visible(order_in_feed_locator, timeout=30)

            assert order_in_feed.is_displayed(), f"Заказ с номером {order_number} не отображается в ленте заказов"

    @allure.feature('Лента заказов')
    @allure.story('Счётчик выполненных заказов')
    @allure.title('Проверка увеличения счётчика "Выполнено за всё время" при создании заказа')
    def test_total_orders_counter_increases(self,driver, registered_and_authorized_user):
        main_page = MainPage(driver)
        order_feed_page = OrderFeedPage(driver)

        with allure.step("Получить текущее значение счётчика 'Выполнено за всё время'"):
            main_page.go_to_site(ORDER_FEED_PATH)
            order_feed_page.wait_for_element_visible(OrderFeedPageLocators.TOTAL_ORDERS_COUNTER, timeout=20)
            initial_counter_value = int(order_feed_page.get_element_text(OrderFeedPageLocators.TOTAL_ORDERS_COUNTER))

        with allure.step("Создать новый заказ"):
            main_page.go_to_site()
            main_page.drag_ingredient_to_constructor(
                MainPageLocators.INGREDIENT_BUN,
                MainPageLocators.DROP_AREA,
                MainPageLocators.BUN_IMAGE
            )
            main_page.drag_ingredient_to_constructor(
                MainPageLocators.INGREDIENT_SAUCE,
                MainPageLocators.DROP_AREA,
                MainPageLocators.CONSTRUCTOR_SAUCE_SPICY
            )
            main_page.wait_for_element_clickable(MainPageLocators.ORDER_BUTTON)
            main_page.click_element_js(MainPageLocators.ORDER_BUTTON)
            main_page.wait_for_element_invisible(MainPageLocators.LOADING_ANIMATION, timeout=30)

        main_page.go_to_order_feed_and_check_header()

        with allure.step("Проверить увеличение счётчика 'Выполнено за всё время'"):
            updated_counter_value = int(order_feed_page.get_element_text(OrderFeedPageLocators.TOTAL_ORDERS_COUNTER))
            allure.attach(
                str(updated_counter_value),
                name="Updated counter value",
                attachment_type=allure.attachment_type.TEXT
            )

            assert updated_counter_value > initial_counter_value , (
                f"Счётчик должен был увеличиться с {initial_counter_value} , "
                f"но текущее значение {updated_counter_value}"
            )

    @allure.story('Счётчик Выполнено за сегодня')
    @allure.title('Проверка увеличения счётчика "Выполнено за сегодня" при создании заказа')
    def test_today_orders_counter_increments(self,driver, registered_and_authorized_user):
        main_page = MainPage(driver)
        order_feed_page = OrderFeedPage(driver)

        with allure.step("Получить текущее значение счётчика 'Выполнено за сегодня'"):
            main_page.go_to_site(ORDER_FEED_PATH)
            order_feed_page.wait_for_element_visible(OrderFeedPageLocators.ORDERS_COUNTER_TODAY, timeout=20)
            initial_counter_value = int(order_feed_page.get_element_text(OrderFeedPageLocators.ORDERS_COUNTER_TODAY))
        with allure.step("Создать новый заказ"):
            main_page.go_to_site()
            main_page.drag_ingredient_to_constructor(
                MainPageLocators.INGREDIENT_BUN,
                MainPageLocators.DROP_AREA,
                MainPageLocators.BUN_IMAGE
            )
            main_page.drag_ingredient_to_constructor(
                MainPageLocators.INGREDIENT_SAUCE,
                MainPageLocators.DROP_AREA,
                MainPageLocators.CONSTRUCTOR_SAUCE_SPICY
            )

            main_page.click_element_js(MainPageLocators.ORDER_BUTTON)
            main_page.wait_for_element_invisible(MainPageLocators.LOADING_ANIMATION, timeout=30)

            main_page.go_to_order_feed_and_check_header()

        with allure.step("Проверить увеличение счётчика 'Выполнено за сегодня'"):
            updated_counter_value = int(order_feed_page.get_element_text(OrderFeedPageLocators.ORDERS_COUNTER_TODAY))
            allure.attach(
                str(updated_counter_value),
                name="Updated counter value",
                attachment_type=allure.attachment_type.TEXT
            )

        assert updated_counter_value > initial_counter_value, (
            f"Счётчик должен был увеличиться с {initial_counter_value}, "
            f"но текущее значение {updated_counter_value}"
        )

    @allure.title("Номер созданного заказа отображается в разделе 'В работе'")
    def test_order_appears_in_progress_section(self, driver, registered_and_authorized_user):
        main_page = MainPage(driver)
        order_feed_page = OrderFeedPage(driver)

        with allure.step("Создать новый заказ"):
            main_page.go_to_site()
            main_page.drag_ingredient_to_constructor(
                MainPageLocators.INGREDIENT_BUN,
                MainPageLocators.DROP_AREA,
                MainPageLocators.BUN_IMAGE
            )
            main_page.drag_ingredient_to_constructor(
                MainPageLocators.INGREDIENT_SAUCE,
                MainPageLocators.DROP_AREA,
                MainPageLocators.CONSTRUCTOR_SAUCE_SPICY
            )
            main_page.click_element_js(MainPageLocators.ORDER_BUTTON)
            main_page.wait_for_element_invisible(MainPageLocators.LOADING_ANIMATION, timeout=30)

        with allure.step("Получить номер заказа"):

            main_page.wait_for_element_visible(MainPageLocators.TICK_ANIMATION_LOCATOR)
            main_page.wait_for_element_clickable(MainPageLocators.INGREDIENT_MODAL_CLOSE_BUTTON)
            order_number_element = main_page.wait_for_element_visible(MainPageLocators.ORDER_NUMBER_LOCATOR, timeout=30)
            main_page.wait_for_element_invisible(MainPageLocators.LOADING_ANIMATION)
            order_number = f"0{order_number_element.text.strip()}"

        main_page.go_to_order_feed_and_check_header()
        order_feed_page.wait_for_element_visible (OrderFeedPageLocators.STATUS)

        with allure.step("Получить номер заказа из раздела'В работе'"):
            visible_order_number = order_feed_page.get_element_text(OrderFeedPageLocators.STATUS)
        assert visible_order_number == order_number










