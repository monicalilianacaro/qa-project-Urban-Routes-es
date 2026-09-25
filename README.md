# QA Project: Urban Routes

## Descripción del proyecto

Suite de pruebas automatizadas end-to-end para **Urban Routes**, un servicio que crea rutas para distintos tipos de transporte (a pie, scooter, bicicleta, automóvil compartido, taxi y automóvil personal), calculando el tiempo y el costo estimado del viaje.

Este proyecto en particular automatiza el **flujo de solicitud de taxi**: desde que el usuario define su ruta hasta que confirma el pedido y se le asigna un conductor. Las pruebas cubren:

- Configuración de la dirección de origen y destino
- Selección de la tarifa **Comfort**
- Registro y confirmación del número de teléfono (incluyendo la verificación por código SMS)
- Registro de una tarjeta de crédito como método de pago
- Envío de un mensaje para el conductor
- Solicitud de manta y pañuelos
- Solicitud de 2 helados
- Confirmación del pedido y verificación de que aparece el modal de búsqueda de taxi
- Verificación de que se muestra la información del conductor una vez asignado (paso opcional)

## Tecnologías y técnicas utilizadas

- **Python 3.14**
- **Selenium WebDriver** — automatización del navegador (Chrome)
- **pytest** — framework de pruebas
- **Page Object Model (POM)** — los localizadores y las acciones sobre la página viven en la clase `UrbanRoutesPage` (en `pages.py`), separados de la lógica de las pruebas (`TestUrbanRoutes`, en `main.py`), para que el código sea más mantenible y reutilizable
- **Esperas explícitas (`WebDriverWait` + `expected_conditions`)** — en lugar de esperas fijas (`time.sleep`), las pruebas esperan a que cada elemento esté visible o sea clicable, lo cual es necesario porque Urban Routes es una aplicación React (SPA) que renderiza su contenido de forma asíncrona
- **Interceptación de peticiones de red** (`driver.get_log('performance')` + Chrome DevTools Protocol) — se usa en `retrieve_phone_code()` (en `helpers.py`) para leer el código de confirmación del teléfono directamente de la respuesta del servidor, sin depender de un teléfono real
- **Pruebas independientes** (`setup_method` / `teardown_method`) — cada prueba abre y cierra su propia sesión de navegador, y arma sus propias precondiciones (dirección, tarifa) antes de ejecutar su acción y su assert. Así, si una prueba falla, no arrastra a las demás, y cualquiera se puede ejecutar sola (ej. `pytest main.py::TestUrbanRoutes::test_fill_card`)

## Estructura del proyecto

```
qa-project-Urban-Routes-es/
├── data.py       # URL del servidor y datos de prueba (dirección, teléfono, tarjeta, mensaje)
├── helpers.py    # retrieve_phone_code(): lee el código de confirmación del teléfono
├── pages.py      # UrbanRoutesPage: localizadores y métodos de interacción (Page Object)
├── main.py       # TestUrbanRoutes: casos de prueba y assertions
└── README.md
```

## Cómo ejecutar las pruebas

### 1. Requisitos previos

- Python 3.10 o superior
- Google Chrome instalado (Selenium gestiona el driver automáticamente desde la versión 4.6+)

### 2. Instalar dependencias

Desde la raíz del proyecto:

```bash
pip install selenium pytest
```

### 3. Configurar la URL del servidor

1. Genera la URL del servidor de Urban Routes desde la plataforma del curso (botón "Iniciar").
2. Copia la URL completa, incluyendo el parámetro `?lng=es`.
3. Pégala en `data.py`, en la variable `urban_routes_url`.

### 4. Ejecutar las pruebas

Desde la terminal, en la raíz del proyecto:

```bash
pytest main.py -v
```

O desde PyCharm: clic derecho sobre `main.py` → **"Run pytest in main.py"**.

Cada prueba abre su propia sesión de navegador (`setup_method`) y la cierra al terminar (`teardown_method`), por lo que son independientes entre sí: si una falla, no afecta a las demás, y cualquiera se puede ejecutar sola. Esto hace que la suite tarde más en total (se abren y cierran varias instancias de Chrome), a cambio de resultados más confiables.

### Notas

- El último test (`test_driver_info_appears`) puede tardar hasta 60 segundos, ya que espera a que se le asigne un conductor a la solicitud.
- Todas las pruebas usan los datos definidos en `data.py`, no valores escritos directamente en las pruebas, para mantener los datos de prueba centralizados y fáciles de actualizar.
