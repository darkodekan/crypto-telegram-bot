import matplotlib.pyplot as plt
import matplotlib.dates as mdates


def plot_graph(title, dates, prices, img_path):
    fig = plt.figure()
    plt.plot(dates, prices, color="#FFFFFF")
    plt.title(title)
    ax = plt.gca()
    formatter = mdates.DateFormatter("%m/%y")
    fig.patch.set_facecolor("#000000")
    ax.xaxis.set_major_formatter(formatter)

    ax.spines['bottom'].set_color('white')
    ax.spines['top'].set_color('white')
    ax.spines['left'].set_color('white')
    ax.spines['right'].set_color('white')
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    
    plt.rcParams.update({"text.color":"white"})
    locator = mdates.MonthLocator()
    ax.xaxis.set_major_locator(locator)
    ax.set_facecolor("black")
    plt.xticks(rotation=45)
    fig.savefig(img_path)


