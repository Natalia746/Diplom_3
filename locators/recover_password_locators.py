from selenium.webdriver.common.by import By


class RecoverLocators:
    RESTORE_LINK = (By.XPATH, "//a[text()='Восстановить пароль']")
    RECOVER_BUTTON = (By.XPATH, "//button[text()='Восстановить']")
    OVERLAY_LOCATOR = (By.CLASS_NAME, "Modal_modal_overlay__x2ZCr")
    EMAIL_INPUT = (By.XPATH, "//div[label[contains(text(),'Email')]]//input")
    SHOW_PASSWORD_BUTTON = (By.XPATH, "//div[contains(@class, 'input__icon') and contains(@class, 'input__icon-action')]")
    PASSWORD_INPUT =  (By.CSS_SELECTOR, "input[type='password'].input__textfield")
    PASSWORD_LABEL = (By.XPATH, "//label[contains(@class, 'input__placeholder') and text()='Пароль']")
    ILLUMINATED_PASSWORD_FIELD = (By.CSS_SELECTOR, "div.input_status_active")
    ILLUMINATED_PASS_FIELD=(By.XPATH, "//label[contains(@class, 'input__placeholder') and "
                                      "contains(@class, 'input__placeholder-focused') and "
                                        "text()='Пароль']")




