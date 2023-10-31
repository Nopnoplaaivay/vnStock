import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, MonthLocator
from mplfinance.original_flavor import candlestick_ohlc
from matplotlib.ticker import FuncFormatter
from matplotlib.dates import date2num
import datetime
from datetime import date, datetime
import math
from vnstock import *


stocks = ['TV2', 'VCG', 'HSG', 'SSI', 'MWG', 'GIL', 'DXG']

## ------------- COMBINE COLUMN FUNC ------------- ##
def combine_columns(row):
    return f"{row['change']} ({row['%_change']}%)"
## ------------- COMBINE COLUMN FUNC ------------- ##



## -------------------------------- GET STOCK DATA FUNC -------------------------------- ##
def real_time_stock(stock_code):
    # time_stamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    stock_hist = stock_historical_data(stock_code, "2022-01-01",
                                         str(date.today()), "1D", "stock")
    stock_hist["%_change"] = round(((stock_hist['close'] - stock_hist['close'].shift(1))
                                    / stock_hist['close'].shift(1)) * 100, 2)
    stock_hist['change'] = (stock_hist['close'] - stock_hist['close'].shift(1))
    stock_hist['latest_change'] = stock_hist.apply(combine_columns, axis=1)
    return stock_hist
## -------------------------------- GET STOCK DATA FUNC -------------------------------- ##



## -------------------------- EXPORT STOCKS DATA --------------------------- ##
for stock in stocks:
  stock_data = real_time_stock(stock)
  index_with_nan = stock_data.index[stock_data.isnull().any(axis=1)]
  stock_data.drop(index_with_nan, inplace=True)
  stock_data.to_csv(f'./Data/{stock}.csv', index=False, header=True)
  print(f"EXPORT {stock} DATA SUCCESSFUL!")
## -------------------------- EXPORT STOCKS DATA --------------------------- ##



## -------------------------------- COMPUTE RSI FUNC -------------------------------- ##
def compute_RSI(data, time_window):
    diff = data.diff(1).dropna()

    up_chg = 0 * diff
    down_chg = 0 * diff

    up_chg[diff > 0] = diff[diff > 0]
    down_chg[diff < 0] = diff[diff < 0]

    up_chg_avg = up_chg.ewm(com=time_window-1, min_periods=time_window).mean()
    down_chg_avg = down_chg.ewm(com=time_window-1, min_periods=time_window).mean()

    rs = abs(up_chg_avg / down_chg_avg)
    rsi = 100 - 100 / (1 + rs)

    return rsi
## -------------------------------- COMPUTE RSI FUNC -------------------------------- ##




## ------------- CREATE FIGURES & AXIS -------------##

## ------------- Entire Plot ---------- ##
fig = plt.figure(figsize=(6, 6))        ##
fig.patch.set_facecolor('#121416')      ##
gs = fig.add_gridspec(6,6)              ##
## ------------- Entire Plot ---------- ##

## ------------- Main Plot ------------ ##
fig_1 = fig.add_subfigure(gs[0:4, 0:4]) ##
fig_1.set_facecolor("#282828")          ##
ax1 = fig_1.subplots()                  ##
## ------------- Main Plot ------------ ##

## ------------- Right Sub Plots ------ ##
fig_2 = fig.add_subfigure(gs[0, 4:6])   ##
fig_2.set_facecolor("#282828")          ##
ax2 = fig_2.subplots()                  ##
                                        ##
fig_3 = fig.add_subfigure(gs[1, 4:6])   ##
fig_3.set_facecolor("#282828")          ##
ax3 = fig_3.subplots()                  ##
                                        ##
fig_4 = fig.add_subfigure(gs[2, 4:6])   ##
fig_4.set_facecolor("#282828")          ##
ax4 = fig_4.subplots()                  ##
                                        ##
fig_5 = fig.add_subfigure(gs[3, 4:6])   ##
fig_5.set_facecolor("#282828")          ##
ax5 = fig_5.subplots()                  ##
                                        ##
fig_6 = fig.add_subfigure(gs[4, 4:6])   ##
fig_6.set_facecolor("#282828")          ##
ax6 = fig_6.subplots()                  ##
                                        ##
fig_7 = fig.add_subfigure(gs[5, 4:6])   ##
fig_7.set_facecolor("#282828")          ##
ax7 = fig_7.subplots()                  ##
## ------------- Right SubPlots ------- ##

## ------------- Volume Sub Plot ------ ##
fig_8 = fig.add_subfigure(gs[4, 0:4])   ##
fig_8.set_facecolor("#282828")          ##
ax8 = fig_8.subplots()                  ##
## ------------- Volume Sub Plot ------ ##

## -------------RSI Sub Plot ---------- ##
fig_9 = fig.add_subfigure(gs[5, 0:4])   ##
fig_9.set_facecolor("#282828")          ##
ax9 = fig_9.subplots()                  ##
## -------------RSI Sub Plot ---------- ##
## ------------- CREATE FIGURES & AXIS -------------##



## -------------------- DESIGN PLOT FUNC -------------------- ##
def figure_design(ax):
    ax.set_facecolor('#091217')
    ax.tick_params(axis='both', labelsize=9, colors='white')
    ## ax.ticklabel_format(useOffset=False)
    ax.spines['bottom'].set_color('#808080')
    ax.spines['top'].set_color('#808080')
    ax.spines['left'].set_color('#808080')
    ax.spines['right'].set_color('#808080')
## -------------------- DESIGN PLOT FUNC -------------------- ##



## ---------------------------------- CREATE Subplot FUNC ----------------------------------- ##
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
## ---------------------------------- CREATE Subplot FUNC ----------------------------------- ##



## -------------------------- OPEN HIGH LOW CLOSE FUNC -------------------------- ##
def read_data_ohlc(filepath):

    ## READ FILE
    df = pd.read_csv(filepath, index_col='time', parse_dates=['time'])
    df = df[~df.index.duplicated(keep='first')]
    df = df[['ticker', 'open', 'high', 'low', 'close' ,'latest_change', 'volume']]
    df['date'] = df.index
    df.index = pd.DatetimeIndex(df.index)
    df['MA20'] = df['close'].rolling(20).mean()
    df['MA50'] = df['close'].rolling(50).mean()
    df['MA200'] = df['close'].rolling(200).mean()
    df['RSI'] = compute_RSI(df['close'], 14)

    latest_info = df.iloc[-1, :]
    latest_price = latest_info['close']
    latest_change = str(latest_info['latest_change'])\
        if (latest_info['latest_change'][0] == '-') else '+' + str(latest_info['latest_change'])
    latest_volume = latest_info['volume']

    return df, latest_price, latest_change, latest_volume
## -------------------------- OPEN HIGH LOW CLOSE FUNC -------------------------- ##



## ------------------------------------- CREATE MAIN STOCK FUNC ----------------------------------- ##
def main_plot(file_path, main_stock_code):
    ## Create Open High Low Close
    data, latest_price, latest_change, latest_volume = read_data_ohlc(file_path)

    candle_counter = range(len(data['open']) - 1)
    ohlc = []
    for  candle in candle_counter:
        item = date2num(data['date'].iloc[candle]), data['open'].iloc[candle],\
                data['high'].iloc[candle], data['low'].iloc[candle],\
                data['close'].iloc[candle]
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
    ax1.tick_params(axis='x', labelsize=5, rotation=45)

    ## Stock code 
    ax1.text(0.005, 1.05, main_stock_code, transform=ax1.transAxes, color='black', fontsize=18, 
                fontweight='bold', horizontalalignment='left', verticalalignment='center',
                bbox=dict(facecolor='#FFBF00'))

    ## Latest price
    ax1.text(0.12, 1.05, latest_price, transform=ax1.transAxes, color='white', fontsize=18,
                fontweight='bold', horizontalalignment='center', verticalalignment='center')

    if latest_change[0] == '-':
        colorcode = '#ff3503'
    else:
        colorcode = '#18b800'

    ax1.text(0.28, 1.05, latest_change, transform=ax1.transAxes, color=colorcode, fontsize=18, 
                fontweight='bold', horizontalalignment='center', verticalalignment='center')

    time_stamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"Chart on {time_stamp} get successful")
    ax1.text(0.92, 1.05, str(time_stamp), transform=ax1.transAxes, color='white', fontsize=12, 
            fontweight='bold', horizontalalignment='center', verticalalignment='center')
    # Add major gridlines
    ax1.grid(which='both', linestyle='--', color='#5D5D5D', linewidth=0.3)

    ## Legend
    leg=ax1.legend(loc='upper left', facecolor='#121416', fontsize=10)
    for text in leg.get_texts():
        plt.setp(text, color='w')

    ## figure design
    figure_design(ax1)
## ------------------------------------- CREATE MAIN STOCK FUNC ----------------------------------- ##



## --------------- PLOT MAIN STOCK ------------ ##
main_plot(f'./Data/{stocks[0]}.csv', stocks[0])
## --------------- PLOT MAIN STOCK ------------ ##



## ------------------------------------- PLOT SUB STOCKS ----------------------------------- ##
right_sub_plots = [ax2, ax3, ax4, ax5, ax6, ax7]
right_stocks = stocks[1:]

for i in range(6):
    data, latest_price,\
    latest_change, latest_volume = read_data_ohlc(f'./Data/{right_stocks[i]}.csv')
    subplot_plot(right_sub_plots[i], right_stocks[i],
                 data, latest_price, latest_change, latest_volume)
## ------------------------------------- PLOT SUB STOCKS ----------------------------------- ##


## ------------------------------------------- VOLUME PLOT ----------------------------------------- ##
ax8.clear()
figure_design(ax8)
ax8.axes.yaxis.set_visible(False)

data_ohlc = read_data_ohlc(f'./Data/{stocks[0]}.csv')
data = data_ohlc[0]
vol = data_ohlc[-1]

pos = data['open'] - data['close'] < 0
neg = data['open'] - data['close'] > 0
data['x_axis'] = list(range(1, len(data['volume']) + 1))
ax8.bar(data['x_axis'][pos], data['volume'][pos], color="#18b800", width=0.8, align='center')
ax8.bar(data['x_axis'][neg], data['volume'][neg], color="#ff3503", width=0.8, align='center')

ymax = data['volume'].max()
ystd = data['volume'].std()

if not math.isnan(ymax):
    ax8.set_ylim([0, ymax + ystd * 3])

ax8.text(0.01, 0.95, 'Volume: ' + "{:,}".format(int(vol)), transform=ax8.transAxes, color='white',
         fontsize=10, fontweight='bold', 
         horizontalalignment='left', verticalalignment='top')

ax8.grid(True, color='grey', linestyle='-', which='major', axis='both', linewidth=0.3)
## ------------------------------------------- VOLUME PLOT ----------------------------------------- ##



## -------------------------------------------------- RSI PLOT -------------------------------------------------- ##
ax9.clear()
figure_design(ax9)
ax9.axes.yaxis.set_visible(False)
ax9.set_ylim([-5, 105])

ax9.axhline(30, linestyle='-', color='green', linewidth=0.5)
ax9.axhline(50, linestyle='-', color='white', linewidth=0.5)
ax9.axhline(70, linestyle='-', color='red', linewidth=0.5)
ax9.plot(data['x_axis'], data['RSI'], color="#08a0e9", linewidth=1.5)

ax9.text(0.01, 0.95, 'RSI(14): ' + str(round(data['RSI'].iloc[-1], 2)), transform=ax8.transAxes, color='white',
         fontsize=10, fontweight='bold', 
         horizontalalignment='left', verticalalignment='top')

xdate = [i for i in data['date']]

def mydate(x, pos=None):
    try:
        t = xdate[int(x)].strftime('%Y-%m')
        return t
    except IndexError:
        return ''
    
ax9.xaxis.set_major_formatter(FuncFormatter(mydate))
ax8.grid(True, color='grey', linestyle='-', which='major', axis='both', linewidth=0.3)
ax9.tick_params(axis='x', which='major', labelsize=10)
## -------------------------------------------------- RSI PLOT -------------------------------------------------- ##



## --------------- PLOT SHOW ------------- ##
plt.xticks(rotation=45)
fig.set_size_inches(1920/80, 1080/80)  
plt.savefig(f"./Charts/chart_{date.today()}.png")
plt.show()
## --------------- PLOT SHOW ------------- ##

