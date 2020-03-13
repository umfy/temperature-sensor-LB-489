import matplotlib.pyplot as plt
import pandas as pd
from pandas.plotting import register_matplotlib_converters
import matplotlib.dates as mdates
import statistics
from SensorTest_stat import sampling


def read_file(file_):
    try:
        df = pd.read_csv(file_, sep=';')
    except:
        print('Nie znaleziono pliku o nazwie', file_)
        exit(-1)
    df.reset_index
    df = df.iloc[:, 1:]

    pd.to_datetime(df['time'], format='%Y-%m-%d-%H-%M', errors='ignore')
    df.iloc[:, 1:] = df.iloc[:, 1:].astype(float)
    # df.iloc[:, 1:] = pd.to_numeric(df['DataFrame Column'],errors='coerce')
    return df


def write_stats(df_):
    std_ = []
    avrg_ = []
    for i in range(1, 5):
        std_.append(statistics.pstdev(df_.iloc[:, i]))
        avrg_.append(statistics.mean(df_.iloc[:, i]))
    avrg_ = [round(x, 2) for x in avrg_]
    std_ = [round(x, 2) for x in std_]
    return avrg_, std_


def create_plots(df_, time_of_sleep=600):
    samples = time_of_sleep * df_.shape[0]
    n_sensors = df_.iloc[:, 1:].shape[1]
    fig, axs = plt.subplots(n_sensors)
    plt.subplots_adjust(left=0.05, bottom=0.14, right=0.99, top=0.97, wspace=0.20, hspace=0.25)

    for i in range(n_sensors):
        axs[i].plot(df_.iloc[:, 0], df_.iloc[:, i + 1])
        # Subplot Titles from list 'places'
        axs[i].set_title(df_.columns[i + 1])

    for ax in axs.flat:
        ax.set(xlabel='Czas pomiaru', ylabel='Temperatura')
        ax.label_outer()
        ax.grid()
        if samples < 1800:
            plt.gca().xaxis.set_major_locator(mdates.MinuteLocator())
            plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
        elif samples < 86400:
            plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
            plt.gca().xaxis.set_major_locator(mdates.HourLocator())
        elif df_.shape[0] > 604800:
            plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
            plt.gca().xaxis.set_major_locator(mdates.DayLocator())
    # ładniejsza oś x
    plt.gcf().autofmt_xdate()
    plt.show()


'''MAIN CODE BEGINS HERE'''
register_matplotlib_converters()
file = 'data.csv'
temperature_df = read_file(file)

print("Wartosci średnie dla kolejnych czujnikow: \n", write_stats(temperature_df)[0])
print("Odchylenie Standardowe dla kolejnych czujnikow: \n", write_stats(temperature_df)[1])

create_plots(temperature_df, sampling)
