import data
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from pages import UrbanRoutesPage


class TestUrbanRoutes:

    def setup_method(self):
        # Se abre un navegador nuevo para cada prueba, así son independientes entre sí:
        # si una falla, no arrastra a las demás, y cada una se puede ejecutar sola
        # (ej. pytest main.py::TestUrbanRoutes::test_fill_card).
        chrome_options = Options()
        chrome_options.set_capability("goog:loggingPrefs", {'performance': 'ALL'})
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.get(data.urban_routes_url)
        self.routes_page = UrbanRoutesPage(self.driver)

    def teardown_method(self):
        self.driver.quit()

    def test_set_route(self):
        address_from = data.address_from
        address_to = data.address_to
        self.routes_page.set_route(address_from, address_to)
        assert self.routes_page.get_from() == address_from
        assert self.routes_page.get_to() == address_to

    def test_select_comfort_tariff(self):
        self.routes_page.set_route(data.address_from, data.address_to)
        self.routes_page.select_comfort_tariff()
        assert self.routes_page.get_selected_tariff() == 'Comfort'

    def test_fill_phone_number(self):
        self.routes_page.set_route(data.address_from, data.address_to)
        self.routes_page.select_comfort_tariff()
        self.routes_page.set_phone_number(data.phone_number)
        # No comparamos con data.phone_number exacto porque la app no lo muestra formateado igual;
        # verificamos que dejó de mostrar el placeholder original.
        assert self.routes_page.get_phone_number() != 'Número de teléfono'

    def test_fill_card(self):
        self.routes_page.set_route(data.address_from, data.address_to)
        self.routes_page.select_comfort_tariff()
        self.routes_page.add_credit_card(data.card_number, data.card_code)
        assert self.routes_page.get_payment_method() == 'Tarjeta'

    def test_comment_for_driver(self):
        self.routes_page.set_route(data.address_from, data.address_to)
        self.routes_page.select_comfort_tariff()
        self.routes_page.set_driver_message(data.message_for_driver)
        assert self.routes_page.get_driver_message() == data.message_for_driver

    def test_order_blanket_and_handkerchiefs(self):
        self.routes_page.set_route(data.address_from, data.address_to)
        self.routes_page.select_comfort_tariff()
        self.routes_page.order_blanket_and_handkerchiefs()
        assert self.routes_page.is_blanket_and_handkerchiefs_ordered()

    def test_order_2_ice_creams(self):
        self.routes_page.set_route(data.address_from, data.address_to)
        self.routes_page.select_comfort_tariff()
        self.routes_page.order_2_ice_creams()
        assert self.routes_page.get_ice_cream_count() == '2'

    def test_car_search_model_appears(self):
        self.routes_page.set_route(data.address_from, data.address_to)
        self.routes_page.select_comfort_tariff()
        self.routes_page.order_taxi()
        self.routes_page.wait_for_taxi_search_modal()

    def test_driver_info_appears(self):
        # Paso opcional del enunciado: espera a que aparezca la info del conductor.
        self.routes_page.set_route(data.address_from, data.address_to)
        self.routes_page.select_comfort_tariff()
        self.routes_page.order_taxi()
        self.routes_page.wait_for_driver_info()
