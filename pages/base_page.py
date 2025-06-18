import allure
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver
from url import *
from selenium.common.exceptions import TimeoutException


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
    def element_should_be_present(self, locator, timeout=10):
        element = self.find_element(locator, timeout)
        assert element.is_displayed(), f"Элемент {locator} не отображается"

    @allure.step("Дождаться кликабельности элемента: {locator}")
    def wait_for_element_clickable(self, locator, timeout=10):
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
    def wait_for_url_change(self, original_url, timeout=10):
        WebDriverWait(self.driver, timeout).until(
            lambda driver: driver.current_url != original_url
        )

    @allure.step("Дождаться URL: {url}")
    def wait_for_url_to_be(self, url, timeout=10):
        WebDriverWait(self.driver, timeout).until(
            EC.url_to_be(url)
        )

    @allure.step("Дождаться видимости элемента: {locator}")
    def wait_for_element_visible(self, locator, timeout=15):
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator),
            message=f"Element {locator} not visible after {timeout} sec"
        )