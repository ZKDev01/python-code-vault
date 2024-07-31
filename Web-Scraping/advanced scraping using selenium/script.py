from selenium import webdriver

# Inicializa el controlador de Chrome
driver = webdriver.Chrome()

# Navegar
driver.get('https://uww.org/event/zagreb-open-1/results')

# Esperar a que el JS se cargue
driver.implicitly_wait(10)

# Obtener la lista de elementos div con la clase filter-group
filter_groups = driver.find_elements('filter-group')

for filter_group in filter_groups:
  text = filter_group.text
  if '2024' in text:
    print(filter_group.get_attribute('outerHTML'))
  else:
    print("FAIL: 2024")
  if '2023' in text:
    print(filter_group.get_attribute('outerHTML'))
  else: 
    print("FAIL: 2023")
