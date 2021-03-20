import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime




def plot_graph(title, dates, prices_coins, img_path):
    fig = plt.figure()
    plt.title("|".join(title))

    #print("inside plot graph")
    for prices in prices_coins:
        plt.plot(dates, prices, color="#FFFFFF")

    print("hey")
    ax = plt.gca()
    fig.patch.set_facecolor("#000000")
    ax.spines['bottom'].set_color('white')
    ax.spines['top'].set_color('white')
    ax.spines['left'].set_color('white')
    ax.spines['right'].set_color('white')
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    
    plt.rcParams.update({"text.color":"white"})
    min_year = dates[0]
    max_year = dates[-1]
    days = (max_year - min_year).days
    years = days // 365
    

    if days > 60:
        formatter = mdates.DateFormatter("%m/%y")
        locator = mdates.MonthLocator(interval=days//365+1) #interval cant be 0, bug appears
        plt.xticks(rotation=45)

    else:
        formatter = mdates.DateFormatter("%d/%m/%y")
        locator = mdates.WeekdayLocator(interval=2)
        plt.xticks(rotation=30)


    ax.xaxis.set_major_formatter(formatter)

    ax.xaxis.set_major_locator(locator)
    ax.set_facecolor("black")
    print("saving image")

    fig.savefig(img_path)


if __name__ == "__main__":
    from datetime import datetime
    plot_graph("hey", [datetime(2016, 7, 7), datetime(2014, 2, 3), datetime(2015,1,2)], [1,2,5], "img.png")