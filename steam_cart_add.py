from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from steam_game_verificated import get_game_names_prices
import difflib
import datetime


driver = webdriver.Chrome()
driver.maximize_window()

driver.get('https://store.steampowered.com/login/')
# Fill in the login fields (replace 'your_username' and 'your_password' with your actual credentials)

username_field = WebDriverWait(driver, 100).until(EC.visibility_of_element_located(
    (By.CSS_SELECTOR, '.newlogindialog_TextInput_2eKVn')))
username_field.send_keys("YOUR_USERNAME")

password_field = WebDriverWait(driver, 100).until(EC.visibility_of_element_located(
    (By.CSS_SELECTOR, '.newlogindialog_TextInput_2eKVn[type="password"]')))
password_field.send_keys('YOUR_PASSWORD')

login_button = WebDriverWait(driver, 100).until(EC.visibility_of_element_located(
    (By.CSS_SELECTOR, '.newlogindialog_SubmitButton_2QgFE')))
login_button.click()


# Wait for manual Steam Guard approval
input("Waiting for Steam Guard to be manually approved... Press Enter when approved.")

# Wait for login to be completed
WebDriverWait(driver, 10).until(
    EC.url_contains('https://store.steampowered.com/'))


inf_games = []

# Adding games to the cart
games = get_game_names_prices()

for index, (game_name, game_price) in enumerate(games, start=1):
    # Search for the game on the Steam Store (replace 'your_game' with the actual search)
    driver.get(f'https://store.steampowered.com/search/?term={game_name}')

    # Wait for the search results to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'search_results')))

    wait = WebDriverWait(driver, 10)
    # Get the links of the search results
    search_results = driver.find_elements(
        By.CSS_SELECTOR, '.search_result_row')

    # Check similarity between the searched game name and the result names
    similarity_threshold = 0.9  # Adjust the similarity threshold as needed
    matching_result = None

    for result in search_results:
        result_name_element = result.find_element(By.CLASS_NAME, 'title')
        result_name = result_name_element.text.strip()

        similarity = difflib.SequenceMatcher(
            None, game_name, result_name).ratio()
        if similarity >= similarity_threshold:
            matching_result = result
            break

    if matching_result is None:
        print(f'The game "{game_name}" was not found on the Steam Store.')
        print()
        continue

    # Click on the found game link
    matching_result.click()

    # Check if the age selection field is present
    if driver.find_elements(By.ID, 'ageYear'):
        # Locate the year field
        year_element = driver.find_element(By.ID, 'ageYear')

        # Click on the year field to open the dropdown
        year_element.click()

        try:
            # Locate and click on the desired year element (replace 'YYYY' with the appropriate year)
            desired_year_element = driver.find_element(
                By.XPATH, f'//option[@value="1990"]')
            desired_year_element.click()

            # Click on the "View Page" button to open the game page
            view_page_btn = driver.find_element(By.ID, 'view_product_page_btn')
            view_page_btn.click()

            # Wait for the page to be updated after selecting the year
            WebDriverWait(driver, 10).until(
                EC.url_contains('https://store.steampowered.com/'))

            # Wait for the game page to load
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, 'game_area_purchase')))
        except NoSuchElementException:
            # If the desired year field is not available, continue without selecting
            pass

    if len(driver.find_elements(By.CLASS_NAME, 'already_in_library')) > 0:
        print(
            f'The game "{game_name}" is already in the library. Skipped adding to cart.')
        print()
        continue

    # Click on the "Add to Cart" button only if the class is "btn_addtocart" and the ID is not "demoGameBtn"
    add_to_cart_btn = driver.find_element(
        By.CSS_SELECTOR, '.btn_addtocart:not(#demoGameBtn)')
    add_to_cart_btn.click()

    game_info = {
        'name': game_name,
        'price': game_price,
        'date_added': datetime.datetime.now().strftime('%Y-%m-%d'),
        'time_added': datetime.datetime.now().strftime('%H:%M:%S')
    }
    inf_games.append(game_info)

    print(f'Game {index}: "{game_name}" has been successfully added to the cart.')
    print()

    report_file = 'steam_cart_report.txt'

with open(report_file, 'w') as f:
    f.write('Steam Cart Report\n\n')
    for index, game in enumerate(inf_games, 1):
        f.write(f'Game {index}:\n')
        f.write(f'Name: {game["name"]}\n')
        f.write(f'Price: ARS$ {game["price"]}\n')
        f.write(f'Date Added: {game["date_added"]}\n')
        f.write(f'Time Added: {game["time_added"]}\n')
        f.write('\n')

print(f'Report file "{report_file}" created.')

# After the remaining code, add the following line to wait for user interaction
input("Once the purchase is complete, press Enter to close the browser...")
