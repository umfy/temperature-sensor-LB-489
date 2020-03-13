import matplotlib.pyplot as plt
import datetime as dt
import pandas as pd
from pandas.plotting import register_matplotlib_converters
import matplotlib.dates as mdates
import statistics
from SensorTest_stat import sampling


def read_file(filename):
    try:
        temperature_df = pd.read_csv(filename)
    except:
        print('Nie znaleziono pliku o nazwie', filename)
        exit(-1)

    # set datetime
    dates = temperature_df.iloc[:, 0]
    date_stripped = [dt.datetime.strptime(d, '%Y-%m-%d-%H-%M') for d in dates]

    return temperature_df, date_stripped


def write_stats():
    std_ = []
    avrg_ = []
    for i in range(0, 4):
        std_.append(statistics.pstdev(temperature_array.iloc[:, i + 1]))
        avrg_.append(statistics.mean(temperature_array.iloc[:, i + 1]))
    avrg_ = [round(x, 2) for x in avrg_]
    std_ = [round(x, 2) for x in std_]
    return avrg_, std_


def create_plots(places_, temperature_df, dates, time_of_sleep=600):
    samples = time_of_sleep * temperature_df.shape[0]
    n_sensors = temperature_array.iloc[:, 1:].shape[1]
    fig, axs = plt.subplots(n_sensors)
    plt.subplots_adjust(left=0.05, bottom=0.14, right=0.99, top=0.97, wspace=0.20, hspace=0.25)

    for i in range(n_sensors):
        axs[i].plot(dates, temperature_array.iloc[:, i + 1])
        # Subplot Titles from list 'places'
        axs[i].set_title(places_[i])

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
        elif temperature_array.shape[0] > 604800:
            plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
            plt.gca().xaxis.set_major_locator(mdates.DayLocator())
    # ładniejsza oś x
    plt.gcf().autofmt_xdate()
    plt.show()


'''MAIN CODE BEGINS HERE'''
register_matplotlib_converters()
# Ustal kolejność nazw czujników
places = ['50R1', '45R1', '40R1', '35R1']
# Podaj nazwę pliku z danymi
file = 'Temp_data_test2.csv'
temperature_array = read_file(file)[0]
date_x = read_file(file)[1]

print("Wartosci średnie dla kolejnych czujnikow: \n", write_stats()[0])
print("Odchylenie Standardowe dla kolejnych czujnikow: \n", write_stats()[1])

create_plots(places, temperature_array, date_x, sampling)
print (type(temperature_array))
