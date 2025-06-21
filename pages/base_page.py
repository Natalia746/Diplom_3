import allure
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver
from url import *
from selenium.common.exceptions import TimeoutException
from locators.recover_password_locators import RecoverLocators
from selenium.webdriver.common.action_chains import ActionChains
import time

class BasePage:

    def __init__(self, driver: WebDriver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)
        self.base_url = BASE_URL

    @allure.step("Открыть страницу по пути: {path}")
    def go_to_site(self, path=""):
        url = f"{self.base_url}{path}"
        self.driver.get(url)
        allure.attach(
            name="Открыта страница",
            body=url,
            attachment_type=allure.attachment_type.TEXT
        )

    @allure.step("Найти элемент: {locator}")
    def find_element(self, locator, timeout=10):
        element = WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator),
            message=f"Element {locator} not found"
        )
        return element

    @allure.step("Кликнуть по элементу: {locator}")
    def click_element(self, locator, timeout=10):
        element = WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )
        element.click()

    @allure.step("Проверить URL страницы")
    def current_url_should_be(self, expected_url):
        current_url = self.driver.current_url
        assert current_url == expected_url, \
            f"Текущий URL '{current_url}' не соответствует ожидаемому '{expected_url}'"
        allure.attach(
            name="Проверка URL",
            body=f"Ожидаемый: {expected_url}\nФактический: {current_url}",
            attachment_type=allure.attachment_type.TEXT
        )

    @allure.step("Проверить наличие элемента: {locator}")
    def element_should_be_present(self, locator, timeout=20):
        element = self.find_element(locator, timeout)
        assert element.is_displayed(), f"Элемент {locator} не отображается"

    @allure.step("Дождаться кликабельности элемента: {locator}")
    def wait_for_element_clickable(self, locator, timeout=20):
        return WebDriverWait(self.driver, timeout).until(
        EC.element_to_be_clickable(locator),
        message=f"Element {locator} not clickable"
        )

    @allure.step("Дождаться исчезновения оверлея")
    def wait_for_overlay_to_disappear(self, overlay_locator, timeout=30):
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.invisibility_of_element_located(overlay_locator),
                message=f"Overlay {overlay_locator} did not disappear"
            )
        except TimeoutException:
            # Вместо игнорирования - явная ошибка
            allure.attach(
                name="Оверлей не исчез",
                body=self.driver.get_screenshot_as_png(),
                attachment_type=allure.attachment_type.PNG
            )
            raise AssertionError(f"Оверлей {overlay_locator} не исчез за {timeout} секунд")

    @allure.step("Ввести текст '{text}' в элемент: {locator}")
    def input_text(self, locator, text, timeout=10):
        element = self.find_element(locator, timeout)
        element.clear()
        element.send_keys(text)

    @allure.step("Дождаться изменения URL")
    def wait_for_url_change(self, original_url, timeout=30):
        WebDriverWait(self.driver, timeout).until(
            lambda driver: driver.current_url != original_url
        )

    @allure.step("Дождаться URL: {url}")
    def wait_for_url_to_be(self, url, timeout=10):
        WebDriverWait(self.driver, timeout).until(
            EC.url_to_be(url)
        )

    @allure.step("Дождаться видимости элемента: {locator}")
    def wait_for_element_visible(self, locator, timeout=30):
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator),
            message=f"Element {locator} not visible after {timeout} sec"
        )

    @allure.step("Дождаться подсветки поля пароля")
    def wait_for_password_highlight(self, timeout=10):
        # Ожидаем появления класса подсветки
        WebDriverWait(self.driver, timeout).until(
            lambda d: "input__placeholder-focused" in d.find_element(
                *RecoverLocators.PASSWORD_LABEL
            ).get_attribute("class"),
            message="Подсветка поля пароля не появилась"
        )

    @allure.step("Проверка появления подсветки у поля ввода пароля")
    def check_password_highlight(self, should_be_highlighted=True):
        wrapper = self.find_element(RecoverLocators.PASSWORD_INPUT)
        classes = wrapper.get_attribute("class")
        if should_be_highlighted:
            assert "input__placeholder-focused" in classes, "Поле должно быть подсвечено"
        else:
            assert "input__placeholder-focused" not in classes, "Поле не должно быть подсвечено"

    @allure.step("Проверить наличие класса у элемента")
    def element_should_have_class(self, locator, expected_class, timeout=30, message=None):
        element = self.wait_for_element_visible(locator, timeout)
        actual_classes = element.get_attribute("class").split()
        error_message = message or f"Элемент {locator} не содержит класс {expected_class}. Актуальные классы: {actual_classes}"
        assert expected_class in actual_classes, error_message

    @allure.step("Дождаться исчезновения элемента: {locator}")
    def wait_for_element_invisible(self, locator, timeout=30):
        WebDriverWait(self.driver, timeout).until(
            EC.invisibility_of_element_located(locator),
            message=f"Element {locator} is still visible after {timeout} sec"
        )

    @allure.step("Дождаться текста '{text}' в элементе: {locator}")
    def wait_for_text_in_element(self, locator, text, timeout=10):
        WebDriverWait(self.driver, timeout).until(
            EC.text_to_be_present_in_element(locator, text),
            message=f"Текст '{text}' не появился в элементе {locator} за {timeout} секунд"
        )

    @allure.step("Перетащить элемент в корзину")
    def drag_and_drop_element(self, source_locator, target_locator):
        source = self.wait_for_element_clickable(source_locator)
        target = self.wait_for_element_visible(target_locator)
        ActionChains(self.driver).drag_and_drop(source, target).perform()

    @allure.step("Получить текст элемента")
    def get_element_text(self, locator, timeout=10):
        element = self.wait_for_element_visible(locator, timeout)
        return element.text

    @allure.step("Перетащить ингредиент {ingredient_locator} в корзину {target_locator}")
    def drag_ingredient_to_constructor(self, ingredient_locator, target_locator, confirmation_locator=None, timeout=30):
        """
        Универсальный метод для перетаскивания ингредиента в конструктор
        :param ingredient_locator: Локатор перетаскиваемого ингредиента
        :param target_locator: Локатор целевой области (корзины)
        :param confirmation_locator: Локатор для подтверждения успешного добавления (опционально)
        :param timeout: Максимальное время ожидания
        """
        if self.driver.name.lower() == "firefox":
            # Специальная обработка для Firefox
            source = self.find_element(ingredient_locator)
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", source)
            time.sleep(1)  # Небольшая пауза для стабилизации
            target = self.find_element(target_locator)
            self.js_drag_and_drop(source, target)
        else:
            # Стандартное перетаскивание для других браузеров
            self.drag_and_drop_element(ingredient_locator, target_locator)

        # Ожидание подтверждения добавления, если передан confirmation_locator
        if confirmation_locator:
            self.wait_for_element_visible(confirmation_locator, timeout)

    @allure.step("Выполнить JS drag-and-drop")
    def js_drag_and_drop(self, source, target):
        """
        Альтернативная реализация drag-and-drop через JavaScript
        для браузеров, где стандартный ActionChains не работает
        """
        js_script = """
        function createEvent(typeOfEvent) {
            var event = document.createEvent("CustomEvent");
            event.initCustomEvent(typeOfEvent, true, true, null);
            event.dataTransfer = {
                data: {},
                setData: function(key, value) {
                    this.data[key] = value;
                },
                getData: function(key) {
                    return this.data[key];
                }
            };
            return event;
        }

        function dispatchEvent(element, event, transferData) {
            if (transferData) {
                event.dataTransfer = transferData;
            }
            if (element.dispatchEvent) {
                element.dispatchEvent(event);
            } else if (element.fireEvent) {
                element.fireEvent("on" + event.type, event);
            }
        }

        function simulateHTML5DragAndDrop(source, target) {
            var dragStartEvent = createEvent('dragstart');
            dispatchEvent(source, dragStartEvent);

            var dropEvent = createEvent('drop');
            dispatchEvent(target, dropEvent, dragStartEvent.dataTransfer);

            var dragEndEvent = createEvent('dragend');
            dispatchEvent(source, dragEndEvent, dropEvent.dataTransfer);
        }

        simulateHTML5DragAndDrop(arguments[0], arguments[1]);
        """
        self.driver.execute_script(js_script, source, target)

    @allure.step("Проскроллить до элемента: {locator}")
    def scroll_to_element(self, locator, timeout=10):

        element = self.find_element(locator, timeout)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", element)

