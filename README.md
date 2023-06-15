# Steam Cart Automator

Is tool that automates the process of adding games to the cart on the Steam platform.
Developed and tested on the Linux operating system.

## Prerequisites

- Python 3.x: https://www.python.org/downloads/
- Selenium: `pip install selenium`
- ChromeDriver: Download the appropriate ChromeDriver for your operating system from the official ChromeDriver website (https://sites.google.com/a/chromium.org/chromedriver/downloads) if necessary.

### ExchangeRate API

This project uses the ExchangeRate API to convert currencies. Make sure you have a valid API key for the ExchangeRate API.

1. Sign up at https://www.exchangerate-api.com/.
2. Obtain your free API key.

NOTE: The game currency is set to 'ARS$', if it is a different currency, replace all occurrences with the corresponding currency. And the conversion is being made to BRL '(R$ (REAL))'

### SteamDB.info

1. The games are manually retrieved from the website, so go to: https://steamdb.info/
2. Go to the `Sales` tab, apply any desired filters, and open the DevTools.
3. Select the <tbody> tag that encompasses all the games and copy the element.
4. In the `steam_game_verificated.py` file, paste the element.

### Update steam_cart_add.py
1. Replace `"YOUR_LOGIN"` and `"YOUR_PASSWORD"`.

### Update steam_value.py
1. Replace `"YOUR_API_KEY"`.

## Usage

1. Clone this repository to your local machine.
2. Run the steam_value.py script to verify that the data is being fetched correctly:
    ```bash python3 steam_value.py
3. Run the steam_cart_add.py script to start the process of adding games to the cart:
    ```bash python3 steam_cart_add.py
4. Once you have accepted the Steam Guard verification, press `ENTER` and wait.
5. After completing the addition of all the games, complete the purchase and close the browser or press `ENTER` again.

## Contribution

Contributions are welcome! If you encounter any issues or have suggestions for improvement, feel free to open an issue or submit a pull request.




