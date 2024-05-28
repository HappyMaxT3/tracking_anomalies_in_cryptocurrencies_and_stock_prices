import matplotlib.pyplot as plt
import matplotlib
import yfinance as yf
from datetime import datetime, timedelta
import statsmodels.api as sm

def make_graph(crypto, market_index, period_start, period_end):
    # Определение диапазона времени для исследования
    start_date = datetime.strptime(period_start, "%d-%m-%Y")
    start_date.strftime('%Y-%m-%d')
    end_date = datetime.strptime(period_end, "%d-%m-%Y")
    end_date.strftime('%Y-%m-%d')

    # Запрос данных по криптовалюте и индексу рынка из API на заданном отрезке времени
    crypto_data = yf.download(crypto, start=start_date, end=end_date, interval='30m')
    market_data = yf.download(market_index, start=start_date, end=end_date, interval='30m')

    # Выравнивание наборов данных
    crypto_data, market_data = crypto_data.align(market_data, join='inner', axis=0)

    # Построение модели регрессии
    X = sm.add_constant(market_data['Close'])
    y = crypto_data['Close']
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
    plt.plot(crypto_data.index, crypto_data['Close'], color="green", label='Actual price')
    plt.plot(crypto_data.index, model.fittedvalues, color="green", linestyle=":", label='Modelled price')

    # Нахождение аномалий
    below_lower_bound = crypto_data['Close'] < lower_bound
    above_upper_bound = crypto_data['Close'] > upper_bound

    # Построение аномалий под нижней границей
    plt.scatter(crypto_data.index[below_lower_bound], crypto_data['Close'][below_lower_bound], color='red', label='Anomalies below the lower border')

    # Построение аномалий над верхней границей
    plt.scatter(crypto_data.index[above_upper_bound], crypto_data['Close'][above_upper_bound], color='blue', label='Anomalies above the upper border')

    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()

    plt.savefig('static/images/plot.png')


def detect_anomalies(crypto, market_index):
    # Определение диапазона времени для исследования
    start_date = (datetime.now() - timedelta(weeks=1)).strftime('%Y-%m-%d')
    end_date = datetime.now().strftime('%Y-%m-%d')

    # Запрос данных по криптовалюте и индексу рынка из API на заданном отрезке времени
    crypto_data = yf.download(crypto, start=start_date, end=end_date, interval='30m')
    market_data = yf.download(market_index, start=start_date, end=end_date, interval='30m')

    # Выравнивание наборов данных
    crypto_data, market_data = crypto_data.align(market_data, join='inner', axis=0)

    # Построение модели регрессии
    X = sm.add_constant(market_data['Close'])
    y = crypto_data['Close']
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
    below_lower_bound = crypto_data['Close'] < lower_bound
    above_upper_bound = crypto_data['Close'] > upper_bound

    # Проверка наличия аномалий сегодня
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    if (crypto_data.index.date == today) & below_lower_bound:
        anomalies_today = "fallen"
    if (crypto_data.index.date == today) & above_upper_bound:
        anomalies_today = "increased"

    return anomalies_today