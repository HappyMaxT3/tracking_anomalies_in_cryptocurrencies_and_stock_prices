import matplotlib.pyplot as plt
import matplotlib
import yfinance as yf
from datetime import datetime, timedelta
import statsmodels.api as sm

def make_graph(stock, portfel, period_start, period_end):
    # Определение диапазона времени для исследования
    start_date = datetime.strptime(period_start, "%d-%m-%Y")
    start_date.strftime('%Y-%m-%d')
    end_date = datetime.strptime(period_end, "%d-%m-%Y")
    end_date.strftime('%Y-%m-%d')

    # Запрос данных по акции и портфелю из API на заданном отрезке времени
    symbol = stock
    market_index_symbol = portfel
    stock_data = yf.download(symbol, start=start_date, end=end_date, interval='30m')
    market_data = yf.download(market_index_symbol, start=start_date, end=end_date, interval='30m')

    # Выравнивание наборов данных
    stock_data, market_data = stock_data.align(market_data, join='inner', axis=0)

    # Построение модели регрессии
    X = sm.add_constant(market_data['Close'])
    y = stock_data['Close']
    model = sm.OLS(y, X).fit()

    # Расчет остатков и плавающего стандартного отклонения остатков
    residuals = model.resid
    rolling_std_residuals = residuals.rolling(window=20, min_periods=1).std()

    # Определение границ аномалий с использованием стандартного отклонения
    lower_bound_multiplier = 1.5
    upper_bound_multiplier = 1.5
    lower_bound = model.fittedvalues - lower_bound_multiplier * rolling_std_residuals
    upper_bound = model.fittedvalues + upper_bound_multiplier * rolling_std_residuals

    # Построение графиков текущей и предполагаемой цены
    matplotlib.use('Agg')
    plt.figure(figsize=(15, 6))
    plt.plot(stock_data.index, stock_data['Close'], color="green", label='Реальная цена акции')
    plt.plot(stock_data.index, model.fittedvalues, color="green", linestyle=":", label='Модель цены акции')

    # Нахождение аномалий
    below_lower_bound = stock_data['Close'] < lower_bound
    above_upper_bound = stock_data['Close'] > upper_bound

    # Построение аномалий под нижней границей
    plt.scatter(stock_data.index[below_lower_bound], stock_data['Close'][below_lower_bound], color='red', label='Аномалии, перешедшие нижнюю границу')

    # Построение аномалий над верзней границей
    plt.scatter(stock_data.index[above_upper_bound], stock_data['Close'][above_upper_bound], color='blue', label='Аномалии, перешедшие верхнюю границу')

    plt.xlabel('Дата')
    plt.ylabel('Цена')
    plt.title('Вычисление аномалий в цене акции')
    plt.legend()


    # Отображение графика
    #plt.show()

    plt.savefig('static/images/plot.png')
    


def detect_anomalies(stock, portfel):
    # Определение диапазона времени для исследования
    start_date = (datetime.now() - timedelta(weeks=1)).strftime('%Y-%m-%d')
    end_date = datetime.now().strftime('%Y-%m-%d')

    # Запрос данных по акции и портфелю из API на заданном отрезке времени
    symbol = stock
    market_index_symbol = portfel
    stock_data = yf.download(symbol, start=start_date, end=end_date, interval='30m')
    market_data = yf.download(market_index_symbol, start=start_date, end=end_date, interval='30m')

    # Выравнивание наборов данных
    stock_data, market_data = stock_data.align(market_data, join='inner', axis=0)

    # Построение модели регрессии
    X = sm.add_constant(market_data['Close'])
    y = stock_data['Close']
    model = sm.OLS(y, X).fit()

    # Расчет остатков и плавающего стандартного отклонения остатков
    residuals = model.resid
    rolling_std_residuals = residuals.rolling(window=20, min_periods=1).std()

    # Определение границ аномалий с использованием стандартного отклонения
    lower_bound_multiplier = 1.5
    upper_bound_multiplier = 1.5
    lower_bound = model.fittedvalues - lower_bound_multiplier * rolling_std_residuals
    upper_bound = model.fittedvalues + upper_bound_multiplier * rolling_std_residuals

    # Нахождение аномалий
    below_lower_bound = stock_data['Close'] < lower_bound
    above_upper_bound = stock_data['Close'] > upper_bound

    # Проверка наличия аномалий сегодня
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    if (stock_data.index.date == today) & below_lower_bound:
        anomalies_today = "fallen"
    if (stock_data.index.date == today) & above_upper_bound:
        anomalies_today = "increased"

    return anomalies_today