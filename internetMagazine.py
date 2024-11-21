import time

from selenium import webdriver
from faker import Faker
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# запуск браузера/переход по URL
def launching_the_browser(base_url):
    # параметры браузера
    options = webdriver.ChromeOptions()

    # закомментировать, чтобы отключить headless режим
    options.add_argument("--headless")
    # раскомментировать, чтобы оставить браузер открытым
    # options.add_experimental_option("detach", True)

    service = ChromeService(ChromeDriverManager().install())
    # открытие браузера с параметрами
    driver_chrome = webdriver.Chrome(
        options=options,
        service=service
    )
    # переход по url в браузере/развернуть на весь экран
    driver_chrome.get(base_url)
    driver_chrome.maximize_window()
    print("Запуск браузера.\nПереход по URL.")
    return driver_chrome


# авторизация на сайте
def authorization_on_the_site(driver_chrome):
    driver_chrome.find_element(By.ID, "user-name").send_keys("standard_user")
    driver_chrome.find_element(By.ID, "password").send_keys("secret_sauce")
    driver_chrome.find_element(By.ID, "login-button").click()
    print("Успешная авторизация на сайте.\n")


# сбор данных о продуктах
def product_data_collection(driver_chrome):
    all_items = []
    counter = 1
    while counter <= 6:
        all_items.append({
            "name": driver_chrome.find_element(
                By.XPATH, f"(//div[@class='inventory_item_name '])[{counter}]"
            ).text,
            "price": driver_chrome.find_element(
                By.XPATH, f"(//div[@class='inventory_item_price'])[{counter}]"
            ).text[1:]
        })
        counter += 1
    return all_items


# получить список товаров
def get_list_of_products(driver_chrome):
    print("Приветствую тебя в нашем интернет-магазине!\n")
    print("Выбери один из следующих товаров и укажи его номер:")
    sequence_number = 0
    for product in product_data_collection(driver_chrome):
        sequence_number += 1
        print(f"{sequence_number} - {product["name"]}")


# выбор продукта
def product_selection(driver_chrome, number):
    return driver_chrome.find_element(
        By.XPATH, f"(// button[@class ='btn btn_primary btn_small btn_inventory '])[{number}]"
    ).click()


# проверка выбора/стоимости продукта
def check_name_price_product(driver_chrome, all_products, number):
    value_name_select_product = all_products[number - 1]["name"]
    value_name_product_in_shopping_cart = driver_chrome.find_element(
        By.XPATH, "//div[@class='inventory_item_name']"
    ).text
    assert value_name_select_product == value_name_product_in_shopping_cart, \
        "Ошибка: Названия должны совпадать!"
    print(f"Продукт в корзине - \"{value_name_product_in_shopping_cart}\".")

    value_price_select_product = all_products[number - 1]["price"]
    value_price_product_in_shopping_cart = driver_chrome.find_element(
        By.XPATH, "//div[@class='inventory_item_price']"
    ).text
    assert value_price_select_product == value_price_product_in_shopping_cart[1:], \
        "Ошибка: Цена должна совпадать!"
    print(f"Цена продукта - {value_price_product_in_shopping_cart}.")


# переход в корзину, нажать Checkout
def click_shopping_cart_click_checkout(driver_chrome, all_products, number):
    driver_chrome.find_element(By.ID, "shopping_cart_container").click()
    print("\nПереход в корзину с продуктами.")

    check_name_price_product(driver_chrome, all_products, number)

    driver_chrome.find_element(By.ID, "checkout").click()
    print("Нажатие кнопки Checkout.\n")


# заполнение формы случайными данными, нажатие Continue
def fill_with_random_data(driver_chrome):
    fake_name = Faker("en_Us").first_name()
    fake_last_name = Faker("en_Us").last_name()
    fake_zip = Faker("en_Us").zipcode()

    driver_chrome.find_element(By.ID, "first-name").send_keys(fake_name)
    driver_chrome.find_element(By.ID, "last-name").send_keys(fake_last_name)
    driver_chrome.find_element(By.ID, "postal-code").send_keys(fake_zip)
    print(f"Форма заполнена случайными данными:\n"
          f"First Name - \"{fake_name}\"\n"
          f"Last Name - \"{fake_last_name}\"\n"
          f"Zip/Postal Code - \"{fake_zip}\".")

    driver_chrome.find_element(By.ID, "continue").click()
    print("Нажатие кнопки Continue.\n")


# проверка соответствия на финальном этапе, кнопка Finish
def final_compliance_check(driver_chrome, all_products, number):
    print("Финальная проверка.")

    check_name_price_product(driver_chrome, all_products, number)

    value_price_select_product = all_products[number - 1]["price"]
    value_price_total = driver_chrome.find_element(By.XPATH, "//div[@class='summary_subtotal_label']").text[12:]
    assert value_price_select_product == value_price_total[1:], \
        "Ошибка: Цена должна совпадать!"
    print(f"Цена всего - {value_price_total}")

    driver_chrome.find_element(By.ID, "finish").click()
    print("Нажатие кнопки Finish.\n")


# проверка наличия фразы об успешности, кнопка Back Home
def check_complete_header(driver_chrome):
    value_complete_header = driver_chrome.find_element(By.XPATH, "//h2[@class='complete-header']").text
    assert value_complete_header == "Thank you for your order!", \
        "Ошибка: Текст заголовка должен совпадать!"
    print(f"Текст заголовка - \"{value_complete_header}\".")

    driver_chrome.find_element(By.ID, "back-to-products").click()
    print("Нажатие кнопки Back Home.\n")


# закрытие браузера
def closing_the_browser(driver_chrome):
    driver_chrome.quit()
    print("Закрытие браузера.")
