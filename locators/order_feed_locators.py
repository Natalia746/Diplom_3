from selenium.webdriver.common.by import By


class OrderFeedPageLocators:
     FEED_HEADING = (By.XPATH, "//h1[text()='Лента заказов']")
     FIRST_ORDER_IN_LIST = (By.XPATH,"(//li[contains(@class, 'OrderHistory_listItem__2x95r')])[1]")# Первый заказ в списке
     ORDER_NUMBER_IN_LIST = (By.XPATH, "(//p[contains(@class, 'text_type_digits-default')])[1]")
     ORDER_NUMBER_IN_MODAL = (By.CSS_SELECTOR, "p.text.text_type_digits-default.mb-10.mt-5")
     MODAL_CONTAINER = (By.CSS_SELECTOR, "div.Modal_orderBox__1xWdi") # Модальное окно заказа
     COMPOSITION_TITLE = (By.XPATH, "//p[contains(@class, 'text_type_main-medium') and text()='Cостав']") # Надпись Состав в модальном окне
     ORDER_NUMBER_IN_FEED = (By.XPATH, "//p[contains(@class, 'text_type_digits-default')]")
     ORDER_LIST = (By.CSS_SELECTOR, "ul[class*='OrderFeed_orderList']")
     ORDER_NUMBERS = (By.XPATH, "//p[contains(@class, 'text_type_digits-default')]")
     TOTAL_ORDERS_COUNTER = (By.XPATH, "//p[contains(@class, 'OrderFeed_number') and contains(@class, 'text_type_digits-large')]")
     ORDERS_COUNTER_TODAY = (By.CSS_SELECTOR, "p.OrderFeed_number__2MbrQ.text.text_type_digits-large")
     STATUS = (By.CSS_SELECTOR, "li.text.text_type_digits-default.mb-2")
