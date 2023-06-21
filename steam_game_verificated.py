from bs4 import BeautifulSoup
import requests
import math
import platform

# ExchangeRate-API API key (replace with your own key)
api_key = 'YOUR_API_KEY'

# Define the ExchangeRate-API API URL
url = f'https://v6.exchangerate-api.com/v6/{api_key}/pair/ARS/BRL'


def get_game_names_prices():

# Determine the platform (Linux or Windows)
    current_platform = platform.system()

# Specify the encoding based on the platform
    if current_platform == 'Linux':
        encoding = 'utf-8'
    elif current_platform == 'Windows':
        encoding = 'cp1252'
    else:
        encoding = 'utf-8'  # Default encoding if the platform is unknown

# Open the file in read mode
    with open('game_data.html', encoding=encoding, errors='ignore') as file:
        html = file.read()

    # Assuming you already have the HTML code of the table stored in the 'html' variable
    soup = BeautifulSoup(html, 'html.parser')

    # Find all rows ('tr') of the table
    rows = soup.find_all('tr')

    # List to store the game names and prices
    names_prices = []

    # Iterate over each row and retrieve the game name and price
    for row in rows:
        # Find all cells ('td') of the row
        cells = row.find_all('td')

        # Variables to store the game name and price
        game_name = None
        game_price = None

        # Iterate over each cell to find the game name and price
        for cell in cells:
            # Check if the cell contains a link ('a') with the class 'b'
            a = cell.find('a', class_='b')

            if a:
                # Get the text of the link, which represents the game name
                game_name = a.get_text().strip()

            # Check if the cell content contains "ARS$"
            if "ARS$" in cell.get_text():
                # Extract the price by removing the "ARS$" text and any extra characters
                price = cell.get_text().replace("ARS$", "").replace(",", ".").strip()
                try:
                    # Convert the price to a float number
                    game_price = float(price)
                except ValueError:
                    # Ignore cells that cannot be converted to float
                    pass

        # Check if both the game name and price were found
        if game_name is not None and game_price is not None:
            # Add the game name and price to the list of names and prices
            names_prices.append((game_name, game_price))

    # Return the list of game names and prices
    return names_prices


if __name__ == "__main__":
    names_prices = get_game_names_prices()

    # Print the game names and prices
    for game_name, game_price in names_prices:
        print(game_name, ":", "ARS$", game_price)
        print()

    # Calculate the sum of prices
    sum_prices_ars = sum(price for _, price in names_prices)
    item_count = len(names_prices)

    print("Item Count:", item_count)

    # Make a request to the API and get the data
    response = requests.get(url)
    data = response.json()

    # Get the ARS/BRL exchange rate
    exchange_rate = data['conversion_rate']

    # Convert the exchange rate from str to float
    exchange_rate = float(exchange_rate)

    # Convert the sum of prices from ARS to BRL
    sum_prices_brl = sum_prices_ars * exchange_rate

    print("Sum of prices in ARS$:", math.ceil(sum_prices_ars * 100) / 100)
    print("Sum of prices in BRL:", math.ceil(sum_prices_brl * 100) / 100)
