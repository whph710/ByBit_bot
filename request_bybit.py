import requests


def get_bybit_linear_tickers_usdt():
    """
    Получает список тикеров линейных контрактов, номинированных в USDT, от API Bybit.

    Возвращает:
        list: Список тикеров, исключая те, которые содержат "0" в названии.
    """
    url = "https://api.bybit.com/v5/market/tickers?category=linear"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Проверяем, успешный ли был запрос
        data = response.json()
        tickers_all = [pair["symbol"] for pair in data["result"]["list"]]
        tickers = [ticker for ticker in tickers_all if "USDT" in ticker]  # Выбираем только USDT
        tickers = [ticker for ticker in tickers if "0" not in ticker]  # Список, исключив элементы, содержащие "0"
        return tickers
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return []


def get_bybit_last_kline_data(symbol, interval=5, limit=50):
    """
    Получает последние данные свечей (kline) для указанного символа и интервала от API Bybit.

    Параметры:
        symbol (str): Символ актива, для которого нужно получить данные свечей.
        interval (str): Интервал времени, для которого нужно получить данные свечей.
        limit (int, optional): Количество свечей, которое нужно получить. По умолчанию 50.

    Возвращает:
        list: Список данных свечей для указанного символа и интервала.
    """
    url = "https://api.bybit.com/v5/market/kline"
    params = {
        "category": "linear",
        "symbol": symbol,
        "interval": str(interval),
        "limit": limit  # Количество свечей, которое нужно получить
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Проверяем, успешный ли был запрос
        data = response.json()
        return data["result"]["list"]
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return []
