import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, MonthLocator
from mplfinance.original_flavor import candlestick_ohlc
from matplotlib.dates import date2num
import matplotlib.patches as patches
import datetime
import math


## Create a figure and axis
fig = plt.figure(figsize=(6, 6))
fig.patch.set_facecolor('#121416')
gs = fig.add_gridspec(6,6)

fig_1 = fig.add_subfigure(gs[0:4, 0:4])
fig_1.set_facecolor("#282828")
ax1 = fig_1.subplots()

fig_2 = fig.add_subfigure(gs[0, 4:6])
fig_2.set_facecolor("#282828")
ax2 = fig_2.subplots()

fig_3 = fig.add_subfigure(gs[1, 4:6])
fig_3.set_facecolor("#282828")
ax3 = fig_3.subplots()

fig_4 = fig.add_subfigure(gs[2, 4:6])
fig_4.set_facecolor("#282828")
ax4 = fig_4.subplots()

fig_5 = fig.add_subfigure(gs[3, 4:6])
fig_5.set_facecolor("#282828")
ax5 = fig_5.subplots()

fig_6 = fig.add_subfigure(gs[4, 4:6])
fig_6.set_facecolor("#282828")
ax6 = fig_6.subplots()

fig_7 = fig.add_subfigure(gs[5, 4:6])
fig_7.set_facecolor("#282828")
ax7 = fig_7.subplots()

fig_8 = fig.add_subfigure(gs[4, 0:4])
fig_8.set_facecolor("#282828")
ax8 = fig_8.subplots()

fig_9 = fig.add_subfigure(gs[5, 0:4])
fig_9.set_facecolor("#282828")
ax9 = fig_9.subplots()

## Design plot
def figure_design(ax):
    ax.set_facecolor('#091217')
    ax.tick_params(axis='both', labelsize=9, colors='white')
    ## ax.ticklabel_format(useOffset=False)
    ax.spines['bottom'].set_color('#808080')
    ax.spines['top'].set_color('#808080')
    ax.spines['left'].set_color('#808080')
    ax.spines['right'].set_color('#808080')

## Create Subplot
def subplot_plot(ax, sub_stock_code, data, latest_price, latest_change, latest_volume):
  ax.clear()
  ax.plot(list(range(1, len(data['close']) + 1)), data['close'], color="white", linewidth=2)

  ymin = data['close'].min()
  ymax = data['close'].max()
  ystd = data['close'].std()

  if not math.isnan(ymax) and ymax != 0:
    ax.set_ylim([ymin - ystd * 0.5, ymax + ystd * 3])

  ax.text(0.02, 0.95, sub_stock_code, transform=ax.transAxes, color='#FFBF00', fontsize=11,
           fontweight='bold', horizontalalignment='left', verticalalignment='top')
  ax.text(0.2, 0.95, latest_price, transform=ax.transAxes, color='white', fontsize=11,
           fontweight='bold', horizontalalignment='left', verticalalignment='top')
  if latest_change[0] == '-':
      colorcode = '#ff3503'
  else:
      colorcode = '#18b800'

  ax.text(0.4, 0.95, latest_change, transform=ax.transAxes, color=colorcode, fontsize=11,
           fontweight='bold', horizontalalignment='left', verticalalignment='top')
  
  ax.grid(which='both', linestyle='--', color='#5D5D5D', linewidth=0.3)

  figure_design(ax)
  ax.axes.xaxis.set_visible(False)
  ax.axes.yaxis.set_visible(False)


def read_data_ohlc(filepath):

    ## Đọc file
    df = pd.read_csv(filepath, index_col='time', parse_dates=['time'])
    df = df[['ticker', 'open', 'high', 'low', 'close' ,'latest_change', 'volume']]
    df['date'] = df.index
    df.index = pd.DatetimeIndex(df.index)
    df['MA20'] = df['close'].rolling(20).mean()
    df['MA50'] = df['close'].rolling(50).mean()
    df['MA200'] = df['close'].rolling(200).mean()

    latest_info = df.iloc[-1, :]
    latest_price = latest_info['close']
    latest_change = str(latest_info['latest_change']) if (latest_info['latest_change'][0] == '-') else '+' + str(latest_info['latest_change'])
    latest_volume = latest_info['volume']

    return df, latest_price, latest_change, latest_volume


def main_plot(file_path, main_stock_code):
    ## Create Open High Low Close
    data, latest_price, latest_change, latest_volume = read_data_ohlc(file_path)

    candle_counter = range(len(data['open']) - 1)
    ohlc = []
    for  candle in candle_counter:
        item = date2num(data['date'][candle]), data['open'][candle],\
                data['high'][candle], data['low'][candle],\
                data['close'][candle]
        ohlc.append(item)

    ## Define the date format for the x-axis
    date_format = DateFormatter('%b %d')
    ax1.xaxis.set_major_formatter(date_format)

    ## Set the major locator for the x-axis
    ax1.xaxis.set_major_locator(MonthLocator(bymonthday=1))

    ## Plot the candlestick chart
    candlestick_ohlc(ax1, ohlc, width=0.6, colorup='g', colordown='r')
    ax1.plot(data['MA20'], color='pink', linestyle='-', linewidth=1, label='MA 20')
    ax1.plot(data['MA50'], color='orange', linestyle='-', linewidth=1, label='MA 50')
    ax1.plot(data['MA200'], color='#08a0e9', linestyle='-', linewidth=1, label='MA 200')

    ## Set the title and labels
    ax1.set_title('Candlestick Chart', color='pink', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Date', color='pink', fontsize=14, fontweight='bold') 
    ax1.set_ylabel('Price', color='pink', fontsize=14, fontweight='bold')
    ax1.tick_params(axis='x', labelsize=5)

    ax1.text(0.005, 1.05, main_stock_code, transform=ax1.transAxes, color='black', fontsize=18, 
                fontweight='bold', horizontalalignment='left', verticalalignment='center',
                bbox=dict(facecolor='#FFBF00'))

    ax1.text(0.12, 1.05, latest_price, transform=ax1.transAxes, color='white', fontsize=18,
                fontweight='bold', horizontalalignment='center', verticalalignment='center')

    if latest_change[0] == '-':
        colorcode = '#ff3503'
    else:
        colorcode = '#18b800'

    ax1.text(0.28, 1.05, latest_change, transform=ax1.transAxes, color=colorcode, fontsize=18, 
                fontweight='bold', horizontalalignment='center', verticalalignment='center')

    time_stamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(time_stamp)
    ax1.text(0.92, 1.05, str(time_stamp), transform=ax1.transAxes, color='white', fontsize=12, 
            fontweight='bold', horizontalalignment='center', verticalalignment='center')
    # Add major gridlines
    ax1.grid(which='both', linestyle='--', color='#5D5D5D', linewidth=0.3)

    ## Legend
    leg=ax1.legend(loc='upper left', facecolor='#121416', fontsize=10)
    for text in leg.get_texts():
        plt.setp(text, color='w')

figure_design(ax1)
figure_design(ax2)
figure_design(ax3)
figure_design(ax4)
figure_design(ax5)
figure_design(ax6)
figure_design(ax7)
figure_design(ax8)
figure_design(ax9)

## Sub Plots
## Ax2
data, latest_price, latest_change, latest_volume = read_data_ohlc('VCG.csv')
subplot_plot(ax2, 'VCG', data, latest_price, latest_change, latest_volume)
## Ax3
data, latest_price, latest_change, latest_volume = read_data_ohlc('DXG.csv')
subplot_plot(ax3, 'DXG', data, latest_price, latest_change, latest_volume)
## Ax4
data, latest_price, latest_change, latest_volume = read_data_ohlc('GIL.csv')
subplot_plot(ax4, 'GIL', data, latest_price, latest_change, latest_volume)
## Ax5
data, latest_price, latest_change, latest_volume = read_data_ohlc('HSG.csv')
subplot_plot(ax5, 'HSG', data, latest_price, latest_change, latest_volume)
## Ax6
data, latest_price, latest_change, latest_volume = read_data_ohlc('MWG.csv')
subplot_plot(ax6, 'MWG', data, latest_price, latest_change, latest_volume)
## Ax7
data, latest_price, latest_change, latest_volume = read_data_ohlc('SSI.csv')
subplot_plot(ax7, 'SSI', data, latest_price, latest_change, latest_volume)


## Main Plot
main_plot('vhc.csv', 'VHC')


## Rotate x-axis labels for better visibility
plt.xticks(rotation=45)
fig.set_size_inches(1920/80, 1080/80)  # Adjust the size as needed
plt.savefig("chart.png")

## Show the chart
plt.show()
