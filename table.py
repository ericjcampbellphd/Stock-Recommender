import pandas as pd
import pickle

def get_table(year, quarter):


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

    with open('filtered_X_test_predicted.pickle', 'rb') as handle:
        filtered_X_test_predicted = pickle.load(handle)

    sorted_report = []

    for index in range(len(filtered_X_test_predicted)):

        row = filtered_X_test_predicted.iloc[index]
        _date = row['Report Date']


        if(_date.year == year and month_to_quarter[_date.month] == quarter):

            temp = []
            temp.append(row['Company'])
            temp.append(_date)
            temp.append(row['Predicted Surprise EPS'])
            temp.append(row['Recommendation'])

            sorted_report.append(temp)


    return sorted_report


