import pandas as pd
import numpy as np


def analyze_trend_lines(df, pivot_point_period=14, pivot_point_count=3):
    # Рассчитываем точки пивота
    df['pivot_high'] = df['close'].rolling(window=pivot_point_period, center=True).max()
    df['pivot_low'] = df['close'].rolling(window=pivot_point_period, center=True).min()

    # Находим позиции пивотных точек
    df['pivot_high_pos'] = df.index
    df['pivot_low_pos'] = df.index

    # Функция для получения значений пивотных точек
    def get_pivot_values(df, col, pos_col, count):
        values = []
        positions = []
        for i in range(1, count + 1):
            value = df[col].iloc[::-1].dropna().iloc[i - 1]
            position = df[pos_col].iloc[::-1].dropna().iloc[i - 1]
            values.append(value)
            positions.append(position)
        return values, positions

    # Получаем значения и позиции пивотных точек
    high_values, high_positions = get_pivot_values(df, 'pivot_high', 'pivot_high_pos', pivot_point_count)
    low_values, low_positions = get_pivot_values(df, 'pivot_low', 'pivot_low_pos', pivot_point_count)

    # Логика для трендовых линий
    trend_crossing = None
    for i in range(pivot_point_count - 1):
        for j in range(i + 1, pivot_point_count):
            if high_values[i] > high_values[j]:
                diff = (high_values[i] - high_values[j]) / (high_positions[i] - high_positions[j])
                trend_line = high_values[j] + diff * (df.index[-1] - high_positions[j])
                if df['close'].iloc[-1] < trend_line:
                    trend_crossing = ("down", 1)
                    break
            if low_values[i] < low_values[j]:
                diff = (low_values[j] - low_values[i]) / (low_positions[j] - low_positions[i])
                trend_line = low_values[j] - diff * (df.index[-1] - low_positions[j])
                if df['close'].iloc[-1] > trend_line:
                    trend_crossing = ("up", 1)
                    break

    return trend_crossing
