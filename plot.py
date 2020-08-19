import pandas as pd
import numpy as np
import pickle
from collections import OrderedDict
from bokeh.io import output_file, show
from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.embed import file_html
from datetime import datetime

def get_plot(year, quarter):

    with open('filtered_X_test_predicted_plot_data.pickle', 'rb') as handle:
        filtered_X_test_predicted_plot_data = pickle.load(handle)
    with open('dowjones_date_quarter_price_dict.pickle', 'rb') as handle:
        dowjones_date_quarter_price_dict = pickle.load(handle)

    month_to_quarter = {
                            1 : 1,
                            2 : 1,
                            3 : 1,
                            4 : 2,
                            5 : 2,
                            6 : 2,
                            7 : 3,
                            8 : 3,
                            9 : 3,
                            10: 4,
                            11: 4,
                            12: 4
                        }

    int_to_quarter = { 
                        1:'Jan 1 - Mar 31',
                        2:'Apr 1 - Jun 30',
                        3:'Jul 1 - Sep 30',
                        4:'Oct 1 - Dec 31',
                    }

    #Get dow jones data
    xdatastr = dowjones_date_quarter_price_dict[(str(year), int_to_quarter[quarter])].keys()
    xdata = [datetime.strptime(i, '%Y-%m-%d') for i in xdatastr]
    ypricedata = list(dowjones_date_quarter_price_dict[(str(year), int_to_quarter[quarter])].values())
    ydata = [(i-ypricedata[-1])*100/ypricedata[-1] for i in ypricedata]

    #Get ML model data
    _columns = filtered_X_test_predicted_plot_data.columns
    filtered_dict = {c:[] for c in _columns}

    for index in range(len(filtered_X_test_predicted_plot_data)):

        row = filtered_X_test_predicted_plot_data.iloc[index]
        _date = row['Report Date']

        if(_date.year == year and month_to_quarter[_date.month] == quarter):
            
            for col, value in zip(_columns, row):

                filtered_dict[col].append(value)

    df = pd.DataFrame(filtered_dict)
    df = df.sort_values(by='Report Date')

    running_cost = 0
    running_profit = 0
    investment_yield = {}

    for index in range(len(df)):

        row = df.iloc[index]
        cost = row['Cost']
        profit = row['Profit']
        _date = row['Report Date']

        running_cost += cost
        running_profit += profit
        temp_yield = running_profit * 100 / running_cost
        investment_yield[_date] = temp_yield

    investment_yield = {datetime(d.year, d.month, d.day): v for d, v in investment_yield.items()}

    #expand ML data to whole quarter
    #print('xdata')
    #print(xdata)
    #print(type(xdata[0]))
    #print(type(list(investment_yield.keys())[0]))
    investment_yield1 = {}

    for _date in xdata:

        temp = datetime(_date.year, _date.month, _date.day)
        if investment_yield.get(temp) is None:
            investment_yield1[_date] = 0

        else:
            investment_yield1[_date] = investment_yield[_date]


    #backward fill
    current_yield = 0
    for _date in [i for i in reversed(xdata)]:
        
        if investment_yield1[_date] != 0:
            current_yield = investment_yield1[_date]

        else:
            investment_yield1[_date] = current_yield

    #print(investment_yield1)
    MLxdata = list(investment_yield1.keys())
    MLydata = list(investment_yield1.values())

    MLxdata = [datetime(d.year, d.month, d.day) for d in MLxdata]


    try:
        names = ['ML Predictor Investment Return:',
                '{}%'.format(np.round(MLydata[0], decimals=2)),
                'Naive Investment Return:',
                '{}%'.format(np.round(ydata[0], decimals=2))]
    except:
        print('No data for this selection')
        names = ['ML Predictor Investment Return:',
                '{}%'.format(0, decimals=2),
                'Naive Investment Return:',
                '{}%'.format(np.round(ydata[0], decimals=2))]

    p = figure(
        tools=['pan','box_zoom','reset','save'],
        title="Machine Learning and Naive Model Portfolio Growth",
            x_axis_label='Date', y_axis_label='Portfolio Growth (% Change)',
            x_axis_type='datetime')

    p.width = 600
    p.height = 400


    p.line(xdata, ydata, color='black', legend_label='Dow Jones Index Fund (Naive)')

    p.line(MLxdata, MLydata, color='red', legend_label='ML Predictor Model')
    p.legend.location = 'top_left'

    html = file_html(p, CDN, _always_new=True)
    with open('templates/plot.html','w') as f:
         f.write(html)


    return names
