import pandas as pd
import requests
import os

# scroll down to the bottom to implement your solution

if __name__ == '__main__':

    if not os.path.exists('../Data'):
        os.mkdir('../Data')

    # Download data if it is unavailable.
    if ('A_office_data.xml' not in os.listdir('../Data') and
            'B_office_data.xml' not in os.listdir('../Data') and
            'hr_data.xml' not in os.listdir('../Data')):
        print('A_office_data loading.')
        url = "https://www.dropbox.com/s/jpeknyzx57c4jb2/A_office_data.xml?dl=1"
        r = requests.get(url, allow_redirects=True)
        open('../Data/A_office_data.xml', 'wb').write(r.content)
        print('Loaded.')

        print('B_office_data loading.')
        url = "https://www.dropbox.com/s/hea0tbhir64u9t5/B_office_data.xml?dl=1"
        r = requests.get(url, allow_redirects=True)
        open('../Data/B_office_data.xml', 'wb').write(r.content)
        print('Loaded.')

        print('hr_data loading.')
        url = "https://www.dropbox.com/s/u6jzqqg1byajy0s/hr_data.xml?dl=1"
        r = requests.get(url, allow_redirects=True)
        open('../Data/hr_data.xml', 'wb').write(r.content)
        print('Loaded.')

        # All data in now loaded to the Data folder.

    # write your code here
    df_A = pd.read_xml('A_office_data.xml')
    df_B = pd.read_xml('B_office_data.xml')
    df_hr = pd.read_xml('hr_data.xml')

    df_hr.index = [str(i) for i in df_hr['employee_id']]
    df_A.index = ['A' + str(i) for i in df_A['employee_office_id']]
    df_B.index = ['B' + str(i) for i in df_B['employee_office_id']]

    df_offices = pd.concat([df_A, df_B])

    merged = pd.merge(df_offices, df_hr, how='left', right_index=True, left_index=True, indicator=True)
    merged_and_cleaned = merged.dropna()

    merged_and_cleaned.drop(columns=['employee_office_id', 'employee_id', '_merge'], inplace=True)
    merged_and_cleaned.sort_index(inplace=True)

    pivot_median = merged_and_cleaned.pivot_table(index='Department',
                                                  columns=['left', 'salary'],
                                                  values='average_monthly_hours',
                                                  aggfunc='median').round(2)

    currently_employed = pivot_median.loc[:, (0, 'high')] < pivot_median.loc[:, (0, 'medium')]
    employees_left = pivot_median.loc[:, (1, 'low')] < pivot_median.loc[:, (1, 'medium')]

    filtered_pivot = pivot_median.loc[currently_employed & employees_left].fillna(0)

    pivot_min_max_mean = merged_and_cleaned.pivot_table(index='time_spend_company',
                                                        columns='promotion_last_5years',
                                                        values=['satisfaction_level', 'last_evaluation'],
                                                        aggfunc=['min', 'max', 'mean']).round(2)

    filtered_min_max_mean = pivot_min_max_mean[
        pivot_min_max_mean[('mean', 'last_evaluation', 0)] > pivot_min_max_mean[('mean', 'last_evaluation', 1)]
        ]
    print(filtered_pivot.to_dict())
    print(filtered_min_max_mean.to_dict())
