from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.common.action_chains import ActionChains

driver = webdriver.Chrome()
driver.maximize_window()
driver.get('https://store.steampowered.com/login/')

# variables edit
login = ''
password = ''
text_library = "EN LA BIBLIOTECA" # text library
quantity_game_verificated = 100 

# Preencha os campos de login (substitua 'seu_usuario' e 'sua_senha' pelas suas credenciais reais)
username_field = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(
    (By.CSS_SELECTOR, '.newlogindialog_TextInput_2eKVn')))
username_field.send_keys(login)

password_field = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(
    (By.CSS_SELECTOR, '.newlogindialog_TextInput_2eKVn[type="password"]')))
password_field.send_keys(password)

login_button = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(
    (By.CSS_SELECTOR, '.newlogindialog_SubmitButton_2QgFE')))
login_button.click()

# Aguarde a aprovação manual do Steam Guard
input("Aguardando a aprovação manual do Steam Guard... Pressione Enter quando aprovado.")

# Aguarde o login ser concluído
WebDriverWait(driver, 10).until(
    EC.url_contains('https://store.steampowered.com/'))

# Lista para armazenar os nomes dos jogos adicionados ao carrinho
added_games = []

# Adicionando jogos ao carrinho
filter_parameters = 'sort_by=Price_ASC&category1=998&category2=29&hidef2p=1&ndl=1'
search_url = f'https://store.steampowered.com/search/?{filter_parameters}'
driver.get(search_url)

# Aguardar o carregamento dos resultados da pesquisa
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, 'search_resultsRows')))

result_rows = driver.find_elements(By.CSS_SELECTOR, '.search_result_row')
for row in result_rows:
    owned_flags = row.find_elements(By.CSS_SELECTOR, '.ds_flag.ds_owned_flag')
    for flag in owned_flags:
        if "EN LA BIBLIOTECA" in flag.text:
            driver.execute_script("arguments[0].remove();", row)
            break

# Obter os links dos resultados da pesquisa
search_results = []

# Lista para armazenar os links dos resultados que não possuem o elemento a ser excluído
filtered_results = []

while len(search_results) < quantity_game_verificated:
    # Role a página para baixo para carregar mais resultados
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Aguarde o carregamento dos novos resultados da pesquisa
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'search_resultsRows')))

    # Atualize a lista de resultados
    search_results = driver.find_elements(
        By.CSS_SELECTOR, '#search_resultsRows > a')

    # Filtrar os resultados da pesquisa
    filtered_results = []
    for result in search_results:
        owned_flags = result.find_elements(
            By.CSS_SELECTOR, '.ds_flag.ds_owned_flag')
        if owned_flags:
            continue  # Ignorar o resultado que possui o elemento a ser excluído
        filtered_results.append(result)

    # Excluir os elementos indesejados
    for result in search_results:
        owned_flags = result.find_elements(
            By.CSS_SELECTOR, '.ds_flag.ds_owned_flag')
        if owned_flags:
            driver.execute_script("arguments[0].remove();", result)

    search_results = filtered_results

    # Verificar se já foram encontrados o número desejado de jogos verificados
    if len(search_results) >= quantity_game_verificated:
        break

for index, result in enumerate(search_results[:quantity_game_verificated], start=1):
    # Rolar a página para que o resultado seja visível
    driver.execute_script("arguments[0].scrollIntoView();", result)

    # Posicionar o mouse sobre o resultado
    actions = ActionChains(driver)
    actions.move_to_element(result)
    actions.perform()

    result_name_element = result.find_element(By.CLASS_NAME, 'title')
    game_name = result_name_element.text.strip()

    # Verificar se o jogo está visível na página
    if not result.is_displayed():
        print(
            f'The game "{game_name}" is not visible on the page. Skipped adding to cart.')
        print()
        continue

    # Verificar se o nome do jogo está vazio
    if game_name == "":
        print(f'The game name is empty. Skipped adding to cart.')
        print()
        continue

    # Verificar se o jogo já foi adicionado ao carrinho
    if game_name in added_games:
        print(
            f'The game {index}: "{game_name}" is already added to cart. Skipped adding to cart.')
        print()
        continue

    # Abrir o jogo em uma nova aba
    try:
        result_link = result.get_attribute('href')
        driver.execute_script(f"window.open('{result_link}', '_blank');")

        # Mudar para a nova aba aberta
        driver.switch_to.window(driver.window_handles[-1])

        # Aguardar a página ser atualizada após clicar no link do jogo
        WebDriverWait(driver, 10).until(
            EC.url_contains('https://store.steampowered.com/'))
        
        # Verificar se o campo de seleção de idade está presente
        if driver.find_elements(By.ID, 'ageYear'):
            # Localizar o campo de ano
            year_element = driver.find_element(By.ID, 'ageYear')

            # Clicar no campo de ano para abrir a lista suspensa
            year_element.click()

            try:
                # Localizar e clicar no elemento de ano desejado
                desired_year_element = driver.find_element(
                    By.XPATH, f'//option[@value="1990"]')
                desired_year_element.click()

                # Aguardar a página ser atualizada após selecionar o ano
                WebDriverWait(driver, 10).until(
                    EC.url_contains('https://store.steampowered.com/'))

                # Localizar o elemento de "Ver página" e clicar nele
                view_page_button = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'view_product_page_btn')))
                view_page_button.click()

                # Aguardar a página ser atualizada após clicar no botão "Ver página"
                WebDriverWait(driver, 10).until(
                    EC.url_contains('https://store.steampowered.com/app/'))

            except NoSuchElementException:
                # Se o campo de ano desejado não estiver disponível, continuar sem selecionar
                pass

        if len(driver.find_elements(By.CLASS_NAME, 'already_in_library')) > 0:
            print(
                f'The game "{game_name}" is already in the library. Skipped adding to cart.')
            print()
            continue

        try:
            # Rolar a página para que o elemento seja visível
            window_height = driver.execute_script("return window.innerHeight")
            driver.execute_script(f"window.scrollBy(0, {window_height})")

            # Adicionar o jogo ao carrinho
            add_to_cart_btn = WebDriverWait(driver, 10).until(
                 EC.element_to_be_clickable((By.CSS_SELECTOR, '.btn_addtocart:not(#demoGameBtn) a.btn_green_steamui')))
            add_to_cart_btn.click()

            time.sleep(1)

            added_games.append(game_name)
            print(f'Added "{game_name}" to cart.')

        except ElementNotInteractableException:
            print(
                f'The game "{game_name}" cannot be interacted with. Skipped adding to cart.')
            print()
            continue

        except StaleElementReferenceException:
            print(
                f'The element of the game "{game_name}" is stale. Skipped adding to cart.')
            print()
            continue

        except Exception as e:
            print(f'Failed to add the game "{game_name}" to cart: {str(e)}')
            print()
            continue

    except Exception as e:
        print(f'Failed to open the game "{game_name}": {str(e)}')
        print()

    finally:
        # Verificar se o identificador da janela atual é válido
        if driver.current_window_handle in driver.window_handles:
            # Fechar a aba atual e voltar para a aba principal
            driver.close()
            driver.switch_to.window(driver.window_handles[0])

# Ir para a página do carrinho
driver.get('https://store.steampowered.com/cart/')

# Verificar quais jogos foram adicionados corretamente
# Esperar 3 segundos para garantir que a página esteja totalmente carregada
driver.implicitly_wait(3)

cart_items = driver.find_elements(By.CSS_SELECTOR, '.cart_item')
added_game_names = [item.find_element(
    By.CSS_SELECTOR, '.cart_item_desc > a').text.strip() for item in cart_items]

for game_name in added_games:
    if game_name in added_game_names:
        print(f'Successfully added "{game_name}" to cart.')
    else:
        print(f'Failed to add "{game_name}" to cart.')

# Depois do restante do código, adicione a seguinte linha para aguardar a interação do usuário
input("Once the purchase is complete, press Enter to close the browser...")
