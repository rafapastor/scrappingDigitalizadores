import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from urllib.parse import urlparse

# URL del catálogo de digitalizadores
url_catalogo = 'https://www.acelerapyme.gob.es/kit-digital/catalogo-digitalizadores'

# Realizar la solicitud HTTP a la página principal del catálogo
response = requests.get(url_catalogo)
soup = BeautifulSoup(response.content, 'html.parser')

# Lista para almacenar la información de las empresas
empresas = []

# Encontrar todos los elementos que contienen la información de las empresas
# Nota: Es posible que necesites ajustar los selectores según la estructura HTML de la página
for empresa_div in soup.find_all('div', class_='digitalizador-item'):
    nombre = empresa_div.find('h3').get_text(strip=True)
    municipio = empresa_div.find('p', class_='municipio').get_text(strip=True)
    web = empresa_div.find('a', class_='web')['href']
    
    # Intentar obtener el correo electrónico desde la página web de la empresa
    try:
        response_web = requests.get(web)
        soup_web = BeautifulSoup(response_web.content, 'html.parser')
        email = None
        for mailto in soup_web.select('a[href^=mailto]'):
            email = mailto['href'].replace('mailto:', '').strip()
            break
        if not email:
            # Si no se encuentra un correo electrónico, generar uno genérico
            dominio = urlparse(web).netloc
            email = f'info@{dominio}'
    except Exception as e:
        print(f'Error al procesar la web de {nombre}: {e}')
        email = 'No disponible'
    
    # Agregar la información de la empresa a la lista
    empresas.append({
        'Nombre de la empresa': nombre,
        'Municipio': municipio,
        'Web': web,
        'Email': email
    })
    
    # Pausa para evitar sobrecargar el servidor
    time.sleep(1)

# Crear un DataFrame de pandas con la información de las empresas
df = pd.DataFrame(empresas)

# Guardar el DataFrame en un archivo Excel
df.to_excel('empresas_kit_digital.xlsx', index=False)
