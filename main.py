from internetMagazine import *


def run(base_url):
    global selection
    # запуск браузера/переход по URL
    driver_chrome = launching_the_browser(base_url)
    # авторизация на сайте
    authorization_on_the_site(driver_chrome)
    # сбор данных о продуктах
    all_products = product_data_collection(driver_chrome)
    # получить список товаров
    get_list_of_products(driver_chrome)
    try:
        selection = int(input(
            "0 - Отказаться от покупок.\n"
            ">> "
        ))
        if selection in range(1, 7):
            product_selection(driver_chrome, selection)
        elif selection == 0:
            print("Завершение программы.")
            closing_the_browser(driver_chrome)
        else:
            print("Соответствие не найдено!\n")
            closing_the_browser(driver_chrome)

    except ValueError:
        print("Нужно было ввести число!\n")
        closing_the_browser(driver_chrome)

    # переход в корзину, нажать Checkout
    click_shopping_cart_click_checkout(driver_chrome, all_products, selection)
    # заполнение формы случайными данными
    fill_with_random_data(driver_chrome)
    # проверка соответствия на финальном этапе
    final_compliance_check(driver_chrome, all_products, selection)
    # проверка наличия фразы об успешности
    check_complete_header(driver_chrome)
    # закрытие браузера
    closing_the_browser(driver_chrome)


run('https://www.saucedemo.com/')
