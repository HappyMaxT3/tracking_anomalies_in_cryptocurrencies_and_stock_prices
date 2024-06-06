import matplotlib.pyplot as plt
import matplotlib
import yfinance as yf
from datetime import datetime, timedelta
import statsmodels.api as sm
import pandas as pd

def make_graph(crypto, market_index, period_start, period_end):
    try:
        # Определение диапазона времени для исследования
        start_date = datetime.strptime(period_start, "%d-%m-%Y")
        start_date = start_date.strftime('%Y-%m-%d')
        end_date = datetime.strptime(period_end, "%d-%m-%Y")
        end_date = end_date + timedelta(days=1)
        end_date = end_date.strftime('%Y-%m-%d')

        # Запрос данных по криптовалюте и индексу рынка из API на заданном отрезке времени
        crypto_data = yf.download(crypto, start=start_date, end=end_date, interval='30m')
        market_data = yf.download(market_index, start=start_date, end=end_date, interval='30m')

        # Проверка наличия данных
        if crypto_data.empty or market_data.empty:
            raise ValueError("No data available for the specified tickers.")

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
        fig = plt.figure(figsize=(15, 6))
        fig.patch.set_facecolor("#0d1245")
        ax = plt.axes()
        ax.set_facecolor("#0d1245")

        plt.plot(crypto_data.index, crypto_data['Close'], color="#CCFFFF", label='Actual price')
        plt.plot(crypto_data.index, model.fittedvalues, color="#CCFFFF", linestyle=":", label='Modelled price')

        # Нахождение аномалий
        below_lower_bound = crypto_data['Close'] < lower_bound
        above_upper_bound = crypto_data['Close'] > upper_bound

        # Создание и заполнение датафрейма для информации об аномалиях
        anomalies_df = pd.DataFrame(columns=['Date', 'Time', 'Cost', 'PriceDiff', 'BorderCrossed', 'ModeledPriceDiff'])
        last_price = None
        for idx, value in crypto_data['Close'][below_lower_bound].items():
            date = idx.strftime('%Y-%m-%d')
            time = idx.strftime('%H:%M')
            cost = value
            if last_price is not None:
                price_diff = cost - last_price
            else:
                price_diff = 0
            modeled_price_diff = cost - model.fittedvalues[idx]  
            anomalies_df = pd.concat([anomalies_df, pd.DataFrame({'Date': [date], 'Time': [time], 'Cost': [cost], 'PriceDiff': [price_diff], 'BorderCrossed': ['Lower'], 'ModeledPriceDiff': [modeled_price_diff]})], ignore_index=True)
            last_price = cost

        last_price = None
        for idx, value in crypto_data['Close'][above_upper_bound].items():
            date = idx.strftime('%Y-%m-%d')
            time = idx.strftime('%H:%M')
            cost = value
            if last_price is not None:
                price_diff = cost - last_price
            else:
                price_diff = 0
            modeled_price_diff = cost - model.fittedvalues[idx]  
            anomalies_df = pd.concat([anomalies_df, pd.DataFrame({'Date': [date], 'Time': [time], 'Cost': [cost], 'PriceDiff': [price_diff], 'BorderCrossed': ['Upper'], 'ModeledPriceDiff': [modeled_price_diff]})], ignore_index=True)
            last_price = cost

        # Построение аномалий под нижней границей
        plt.scatter(crypto_data.index[below_lower_bound], crypto_data['Close'][below_lower_bound], color='#FFFF00', label='Anomalies below the lower border')

        # Построение аномалий над верхней границей
        plt.scatter(crypto_data.index[above_upper_bound], crypto_data['Close'][above_upper_bound], color='#FF00FF', label='Anomalies above the upper border')

        plt.xlabel('Date', color="white")
        plt.ylabel('Price', color="white")
        plt.tick_params(axis="x", colors="white")
        plt.tick_params(axis="y", colors="white")
        plt.gca().spines['top'].set_color('white')
        plt.gca().spines['bottom'].set_color('white')
        plt.gca().spines['left'].set_color('white')
        plt.gca().spines['right'].set_color('white')
        plt.legend(facecolor="#0d1245", labelcolor="white")

        plt.savefig('static/images/plot.png')

        return anomalies_df

    except (ValueError, KeyError) as e:
        raise RuntimeError(f"Error: {str(e)}")


def make_crypto_graph(crypto, period_start, period_end):
    try:
        # Определение диапазона времени для исследования
        start_date = datetime.strptime(period_start, "%d-%m-%Y")
        start_date = start_date.strftime('%Y-%m-%d')
        end_date = datetime.strptime(period_end, "%d-%m-%Y")
        end_date = end_date + timedelta(days=1)
        end_date = end_date.strftime('%Y-%m-%d')

        # Запрос данных по криптовалюте и индексу рынка из API на заданном отрезке времени
        crypto_data = yf.download(crypto, start=start_date, end=end_date, interval='30m')

        # Проверка наличия данных
        if crypto_data.empty:
            raise ValueError("No data available for the specified ticker.")

        # Вычисление модели цены методом EMA
        window_size = 20
        ema = crypto_data['Close'].ewm(span=window_size, adjust=False).mean()

        # Вычисление остатков и скользящего стандартного отклонения остатков
        residuals = crypto_data['Close'] - ema
        rolling_std_residuals = residuals.rolling(window=window_size, min_periods=1).std()

        # Инициализация множителей чувствительности
        lower_bound_multiplier = 1.5
        upper_bound_multiplier = 1.5

        # Функция для вычисления аномалий
        def calculate_anomalies(lower_bound_multiplier, upper_bound_multiplier):
            lower_bound = ema - lower_bound_multiplier * rolling_std_residuals
            upper_bound = ema + upper_bound_multiplier * rolling_std_residuals
            below_lower_bound = crypto_data['Close'] < lower_bound
            above_upper_bound = crypto_data['Close'] > upper_bound
            return below_lower_bound, above_upper_bound

        # Настройка чувствительности на основе количества аномалий
        target_anomalies = 0.05 * len(crypto_data)  # Целевое значение 5% точек данных как аномалии
        tolerance = 0.01 * len(crypto_data)  # Допустимое отклонение от целевого значения

        for _ in range(10): 
            below_lower_bound, above_upper_bound = calculate_anomalies(lower_bound_multiplier, upper_bound_multiplier)
            total_anomalies = below_lower_bound.sum() + above_upper_bound.sum()

            if abs(total_anomalies - target_anomalies) <= tolerance:
                break  # Чувствительность в пределах допустимого диапазона

            if total_anomalies > target_anomalies:
                lower_bound_multiplier += 0.1
                upper_bound_multiplier += 0.1
            else:
                lower_bound_multiplier -= 0.1
                upper_bound_multiplier -= 0.1

        # Построение графиков текущей и предполагаемой цены
        matplotlib.use('Agg')
        fig = plt.figure(figsize=(15, 6))
        fig.patch.set_facecolor("#0d1245")
        ax = plt.axes()
        ax.set_facecolor("#0d1245")
        plt.plot(crypto_data.index, crypto_data['Close'], color="#CCFFFF", label='Actual price')
        plt.plot(crypto_data.index, ema, color="#CCFFFF", linestyle=":", label='Modeled price')

        # Создание и заполнение датафрейма для информации об аномалиях
        anomalies_df = pd.DataFrame(columns=['Date', 'Time', 'Cost', 'PriceDiff', 'BorderCrossed', 'ModeledPriceDiff'])
        last_price = None
        for idx, value in crypto_data['Close'][below_lower_bound].items():
            date = idx.strftime('%Y-%m-%d')
            time = idx.strftime('%H:%M')
            cost = value
            if last_price is not None:
                price_diff = cost - last_price
            else:
                price_diff = 0
            modeled_price_diff = cost - ema[idx]
            anomalies_df = pd.concat([anomalies_df, pd.DataFrame({'Date': [date], 'Time': [time], 'Cost': [cost], 'PriceDiff': [price_diff], 'BorderCrossed': ['Lower'], 'ModeledPriceDiff': [modeled_price_diff]})], ignore_index=True)
            last_price = cost

        last_price = None
        for idx, value in crypto_data['Close'][above_upper_bound].items():
            date = idx.strftime('%Y-%m-%d')
            time = idx.strftime('%H:%M')
            cost = value
            if last_price is not None:
                price_diff = cost - last_price
            else:
                price_diff = 0
            modeled_price_diff = cost - ema[idx]
            anomalies_df = pd.concat([anomalies_df, pd.DataFrame({'Date': [date], 'Time': [time], 'Cost': [cost], 'PriceDiff': [price_diff], 'BorderCrossed': ['Upper'], 'ModeledPriceDiff': [modeled_price_diff]})], ignore_index=True)
            last_price = cost

        # Построение аномалий под нижней границей
        plt.scatter(crypto_data.index[below_lower_bound], crypto_data['Close'][below_lower_bound], color='#FFFF00', label='Anomalies below the lower bound')

        # Построение аномалий над верхней границей
        plt.scatter(crypto_data.index[above_upper_bound], crypto_data['Close'][above_upper_bound], color='#FF00FF', label='Anomalies above the upper bound')

        plt.xlabel('Date', color="white")
        plt.ylabel('Price', color="white")
        plt.tick_params(axis="x", colors="white")
        plt.tick_params(axis="y", colors="white")
        plt.gca().spines['top'].set_color('white')
        plt.gca().spines['bottom'].set_color('white')
        plt.gca().spines['left'].set_color('white')
        plt.gca().spines['right'].set_color('white')
        plt.legend(facecolor="#0d1245", labelcolor="white")
        plt.legend(facecolor="#0d1245", labelcolor="white")

        plt.savefig('static/images/plot.png')

        return anomalies_df

    except (ValueError, KeyError) as e:
        raise RuntimeError(f"Error: {str(e)}")


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
    today = datetime.now().strftime('%Y-%m-%d')
    anomalies_today = None
    if (crypto_data.index.date == today) & below_lower_bound.any():
        anomalies_today = "fallen"
    elif (crypto_data.index.date == today) & above_upper_bound.any():
        anomalies_today = "increased"

    return anomalies_today


def detect_crypto_anomalies(crypto):
    # Определение диапазона времени для исследования
    start_date = (datetime.now() - timedelta(weeks=1)).strftime('%Y-%m-%d')
    end_date = datetime.now().strftime('%Y-%m-%d')

    # Запрос данных по криптовалюте и индексу рынка из API на заданном отрезке времени
    crypto_data = yf.download(crypto, start=start_date, end=end_date, interval='30m')

    # Проверка наличия данных
    if crypto_data.empty:
        raise ValueError("No data available for the specified ticker.")

    # Вычисление модели цены методом EMA
    window_size = 20
    ema = crypto_data['Close'].ewm(span=window_size, adjust=False).mean()

    # Вычисление остатков и скользящего стандартного отклонения остатков
    residuals = crypto_data['Close'] - ema
    rolling_std_residuals = residuals.rolling(window=window_size, min_periods=1).std()

    # Инициализация множителей чувствительности
    lower_bound_multiplier = 1.5
    upper_bound_multiplier = 1.5

    # Функция для вычисления аномалий
    def calculate_anomalies(lower_bound_multiplier, upper_bound_multiplier):
        lower_bound = ema - lower_bound_multiplier * rolling_std_residuals
        upper_bound = ema + upper_bound_multiplier * rolling_std_residuals
        below_lower_bound = crypto_data['Close'] < lower_bound
        above_upper_bound = crypto_data['Close'] > upper_bound
        return below_lower_bound, above_upper_bound

    # Настройка чувствительности на основе количества аномалий
    target_anomalies = 0.05 * len(crypto_data)  # Целевое значение 5% точек данных как аномалии
    tolerance = 0.01 * len(crypto_data)  # Допустимое отклонение от целевого значения

    for _ in range(10):
        below_lower_bound, above_upper_bound = calculate_anomalies(lower_bound_multiplier, upper_bound_multiplier)
        total_anomalies = below_lower_bound.sum() + above_upper_bound.sum()

        if abs(total_anomalies - target_anomalies) <= tolerance:
            break  # Чувствительность в пределах допустимого диапазона

        if total_anomalies > target_anomalies:
            lower_bound_multiplier += 0.1
            upper_bound_multiplier += 0.1
        else:
            lower_bound_multiplier -= 0.1
            upper_bound_multiplier -= 0.1

    last_price = None
    for idx, value in crypto_data['Close'][above_upper_bound].items():
        date = idx.strftime('%Y-%m-%d')
        time = idx.strftime('%H:%M')
        cost = value
        if last_price is not None:
            price_diff = cost - last_price
        else:
            price_diff = 0
        modeled_price_diff = cost - ema[idx]
        anomalies_df = pd.concat([anomalies_df, pd.DataFrame(
            {'Date': [date], 'Time': [time], 'Cost': [cost], 'PriceDiff': [price_diff], 'BorderCrossed': ['Upper'],
             'ModeledPriceDiff': [modeled_price_diff]})], ignore_index=True)
        last_price = cost

    # Проверка, была ли аномалия сегодня
    today = datetime.now().strftime('%Y-%m-%d')
    anomalies_today = None
    if (crypto_data.index.date == today) & below_lower_bound.any():
        anomalies_today = "fallen"
    elif (crypto_data.index.date == today) & above_upper_bound.any():
        anomalies_today = "increased"

    return anomalies_today