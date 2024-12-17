import pandas as pd
pd.set_option('display.max_columns', None)  # Отображение всех столбцов
pd.set_option('display.width', None)  # Автоматическое определение ширины консоли
pd.set_option('display.max_rows', None)  # Отображение всех строк


def analyze_api_data(data):
    # Преобразование данных в DataFrame
    df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'sum'])

    # Преобразование времени из timestamp в человеко-читаемый формат
    #df['timestamp'] = pd.to_datetime(df['timestamp'].astype(int), unit='ms')

    # Преобразование числовых данных
    for col in ['open', 'high', 'low', 'close', 'volume', 'sum']:
        df[col] = df[col].astype(float)

    # Анализ трендов
    df['trend'] = df['close'] - df['open']

    # Возвращение таблицы с результатами
    return df[['timestamp', 'open', 'high', 'low', 'close', 'volume', 'sum', 'trend']]


