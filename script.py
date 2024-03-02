import matplotlib.pyplot as plt
import yfinance as yf
from datetime import datetime, timedelta

# Определение диапазона времени для исследования
start_date = (datetime.now() - timedelta(weeks=3)).strftime('%Y-%m-%d')
end_date = datetime.now().strftime('%Y-%m-%d')  # Установка в качестве даты конца сегоднешей
# Запрос данных по акции из API на заданном отрезке времени с интервалом 15 минут
symbol = 'AAPL'  # Тикер акции
stock_data = yf.download(symbol, start=start_date, end=end_date, interval="15m")

# Запрос данных по портфелю акций на заданном отрезке времени с интервалом 15 минут
market_index_symbol = '^GSPC'  # Тикер портфеля
market_data = yf.download(market_index_symbol, start=start_date, end=end_date, interval="15m")

# Вычисление корреляции
correlation = stock_data['Close'].corr(market_data['Close'])

# Создание модели и получение остатков
model = stock_data['Close'].rolling(window=3).mean()
residuals = stock_data['Close'] - model

# Расчет среднего и общего отклонения остатков
mean_residuals = residuals.mean()
std_residuals = residuals.std()

# Определение нижней и верхней границ аномальных значений
lower_bound = mean_residuals - 2 * std_residuals
upper_bound = mean_residuals + 2 * std_residuals

# Создание графика
plt.figure(figsize=(15, 6))
plt.plot(stock_data.index, stock_data['Close'], color="green", label='Реальная цена акции')
plt.plot(model.index, model, color="green", linestyle=":", label='Модель цены акции')

# Фильтрация аномалий на основе корреляции
filtered_lower_bound = (residuals < lower_bound) & (correlation < 0)
filtered_upper_bound = (residuals > upper_bound) & (correlation < 0)

plt.scatter(stock_data[filtered_lower_bound].index, stock_data[filtered_lower_bound]['Close'],
            color='red', label='Аномалии, перешедшие нижнюю границу')
plt.scatter(stock_data[filtered_upper_bound].index, stock_data[filtered_upper_bound]['Close'],
            color='blue', label='Аномалии, перешедшие верхнюю границу')

plt.xlabel('Дата')
plt.ylabel('Цена')
plt.title('Вычисление аномалий в цене акции')
plt.legend()

plt.show()
