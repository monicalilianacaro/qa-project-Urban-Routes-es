from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from helpers import retrieve_phone_code


class UrbanRoutesPage:
    # --- Formulario de dirección ---
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')

    # --- Botón para iniciar el pedido / abrir tarifas ---
    call_taxi_button = (By.XPATH, '//button[text()="Pedir un taxi"]')

    # --- Selección de tarifa Comfort ---
    comfort_tariff = (By.XPATH, '//div[@class="tcard-title" and text()="Comfort"]')
    selected_tariff_title = (By.CSS_SELECTOR, 'div.tcard.active .tcard-title')

    # --- Teléfono ---
    phone_field_button = (By.XPATH, '//div[@class="np-text" and text()="Número de teléfono"]')
    phone_input = (By.ID, 'phone')
    phone_code_input = (By.CSS_SELECTOR, 'input#code.input')  # distinto del CVV de la tarjeta (ver más abajo)
    phone_next_button = (By.XPATH, '//button[text()="Siguiente"]')
    phone_code_confirm_button = (By.XPATH, '//button[text()="Confirmar"]')
    phone_display = (By.CSS_SELECTOR, 'div.np-button .np-text')  # mismo elemento, antes y después de confirmar

    # --- Tarjeta de crédito ---
    payment_method_button = (By.XPATH, '//div[@class="pp-text" and text()="Método de pago"]')
    add_card_button = (By.XPATH, '//div[@class="pp-title" and text()="Agregar tarjeta"]')
    payment_method_display = (By.CSS_SELECTOR, 'div.pp-button .pp-value-text')  # "Efectivo" → "Tarjeta"
    card_number_input = (By.ID, 'number')
    card_code_input = (By.CSS_SELECTOR, 'input#code.card-input')  # distinto del código SMS del teléfono (ver arriba)
    card_link_button = (By.XPATH, '//button[text()="Agregar"]')  # se habilita tras perder foco el CVV
    payment_modal_close_button = (By.CSS_SELECTOR, 'button.close-button.section-close')

    # --- Mensaje para el conductor ---
    driver_message_input = (By.ID, 'comment')

    # --- Manta y pañuelos ---
    # El input real queda oculto tras el diseño del switch; se usa solo para verificar el estado.
    blanket_and_tissues_switch_input = (
        By.XPATH,
        '//div[@class="r-sw-container"][.//div[@class="r-sw-label" and text()="Manta y pañuelos"]]'
        '//input[@class="switch-input"]'
    )
    # El span visible es el que recibe el clic real del usuario.
    blanket_and_tissues_switch_slider = (
        By.XPATH,
        '//div[@class="r-sw-container"][.//div[@class="r-sw-label" and text()="Manta y pañuelos"]]'
        '//span[@class="slider round"]'
    )

    # --- Helados ---
    ice_cream_plus_button = (
        By.XPATH,
        '//div[@class="r-counter-container"][.//div[@class="r-counter-label" and text()="Helado"]]'
        '//div[@class="counter-plus"]'
    )
    ice_cream_value = (
        By.XPATH,
        '//div[@class="r-counter-container"][.//div[@class="r-counter-label" and text()="Helado"]]'
        '//div[@class="counter-value"]'
    )

    # --- Confirmar pedido de taxi ---
    order_taxi_button = (By.CSS_SELECTOR, 'button.smart-button')

    # --- Modal de búsqueda de taxi ---
    taxi_search_modal = (By.XPATH, '//div[@class="order-header-title" and text()="Buscar automóvil"]')

    # --- Modal con info del conductor (paso opcional) ---
    driver_info_modal = (By.CSS_SELECTOR, 'div.order-btn-group')

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)

    # ---------- Dirección ----------
    def set_from(self, from_address):
        field = self.wait.until(ec.visibility_of_element_located(self.from_field))
        field.send_keys(from_address)

    def set_to(self, to_address):
        field = self.wait.until(ec.visibility_of_element_located(self.to_field))
        field.send_keys(to_address)

    def get_from(self):
        return self.driver.find_element(*self.from_field).get_property('value')

    def get_to(self):
        return self.driver.find_element(*self.to_field).get_property('value')

    def set_route(self, from_address, to_address):
        """Rellena origen y destino, y dispara la búsqueda de tarifas."""
        self.set_from(from_address)
        self.set_to(to_address)
        self.wait.until(ec.element_to_be_clickable(self.call_taxi_button)).click()

    # ---------- Tarifa ----------
    def select_comfort_tariff(self):
        self.wait.until(ec.element_to_be_clickable(self.comfort_tariff)).click()

    def get_selected_tariff(self):
        return self.driver.find_element(*self.selected_tariff_title).text

    # ---------- Teléfono ----------
    def set_phone_number(self, phone_number):
        self.wait.until(ec.element_to_be_clickable(self.phone_field_button)).click()
        phone_input = self.wait.until(ec.visibility_of_element_located(self.phone_input))
        phone_input.send_keys(phone_number)
        self.wait.until(ec.element_to_be_clickable(self.phone_next_button)).click()  # dispara el envío del código SMS
        code = retrieve_phone_code(self.driver)
        code_input = self.wait.until(ec.visibility_of_element_located(self.phone_code_input))
        code_input.send_keys(code)
        self.wait.until(ec.element_to_be_clickable(self.phone_code_confirm_button)).click()

    def get_phone_number(self):
        return self.driver.find_element(*self.phone_display).text

    # ---------- Tarjeta ----------
    def add_credit_card(self, card_number, card_code):
        self.wait.until(ec.element_to_be_clickable(self.payment_method_button)).click()
        self.wait.until(ec.element_to_be_clickable(self.add_card_button)).click()

        number_input = self.wait.until(ec.visibility_of_element_located(self.card_number_input))
        number_input.send_keys(card_number)

        code_input = self.driver.find_element(*self.card_code_input)
        code_input.send_keys(card_code)

        # El botón 'link' no se activa hasta que el campo CVV pierde el foco.
        # Simulamos que el usuario presiona TAB para mover el foco fuera del campo.
        code_input.send_keys(Keys.TAB)

        link_button = self.wait.until(ec.element_to_be_clickable(self.card_link_button))
        link_button.click()

        # El panel de "Método de pago" queda abierto sobre la pantalla (overlay) y bloquea
        # los clics siguientes (manta, helados, pedir taxi) si no se cierra explícitamente.
        # Puede haber más de un botón con estas mismas clases en la página (otros paneles
        # reutilizan el mismo diseño), así que buscamos todos y hacemos clic en el visible.
        close_buttons = self.wait.until(ec.presence_of_all_elements_located(self.payment_modal_close_button))
        for button in close_buttons:
            if button.is_displayed():
                button.click()
                break

    def get_payment_method(self):
        return self.driver.find_element(*self.payment_method_display).text

    # ---------- Mensaje para el conductor ----------
    def set_driver_message(self, message):
        message_input = self.wait.until(ec.visibility_of_element_located(self.driver_message_input))
        message_input.send_keys(message)

    def get_driver_message(self):
        return self.driver.find_element(*self.driver_message_input).get_property('value')

    # ---------- Manta y pañuelos ----------
    def order_blanket_and_handkerchiefs(self):
        self.wait.until(ec.element_to_be_clickable(self.blanket_and_tissues_switch_slider)).click()

    def is_blanket_and_handkerchiefs_ordered(self):
        return self.driver.find_element(*self.blanket_and_tissues_switch_input).is_selected()

    # ---------- Helados ----------
    def order_2_ice_creams(self):
        plus_button = self.wait.until(ec.element_to_be_clickable(self.ice_cream_plus_button))
        plus_button.click()
        plus_button.click()

    def get_ice_cream_count(self):
        return self.driver.find_element(*self.ice_cream_value).text

    # ---------- Pedir taxi y esperar resultados ----------
    def order_taxi(self):
        self.wait.until(ec.element_to_be_clickable(self.order_taxi_button)).click()

    def wait_for_taxi_search_modal(self):
        self.wait.until(ec.visibility_of_element_located(self.taxi_search_modal))

    def wait_for_driver_info(self, timeout=60):
        """Paso opcional: el modal cambia de 'buscando taxi' a mostrar los datos del conductor.
        Usamos un tiempo mayor porque la asignación del conductor puede tardar."""
        WebDriverWait(self.driver, timeout).until(
            ec.visibility_of_element_located(self.driver_info_modal)
        )