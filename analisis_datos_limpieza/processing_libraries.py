
import pandas as pd
import numpy as np

for year in range(2015,2017):

    input_data = "/home/lain/Redes-Sociales-con-Enfoque-Difuso/other_datasets/libraries_surveys/filtered_"+str(year)+"-Libraries-CSV.csv"
    print input_data
    nominal_array = ['eminuse', 'intmob','home3nw','smart1', 'Desktop_laptop','printed_books_read','audiobooks_heard','Ebooks_read','library_loan_ebooks',
                    'borrow_print_books','help_from_librarian','sit_and_Study','class_to_use_computer', 'Attend_group_meeting','internet_use_library']
    freq_array = ['Freq_Twitter','Freq_Instagram','Freq_Pinterest','Freq_Facebook', 'amount_books_read', 'freq_library_visit','freq_virtual_library_visit','freq_mobile_library_visit']

    df_data = pd.read_csv(input_data)#,index_col=False, header=0, usecols=['eminuse', 'intmob','home3nw','smart1','low_budget_e_reader_1_high_2_no_3','Desktop_laptop','Freq_Twitter','Freq_Instagram','Freq_Pinterest','Freq_Facebook','amount_books_read','printed_books_read','audiobooks_heard','Ebooks_read','freq_library_visit','freq_virtual_library_visit','freq_mobile_library_visit','library_loan_ebooks','borrow_print_books','help_from_librarian','sit_and_Study','class_to_use_computer','Attend_group_meeting','internet_use_library','library_impact_your_family','library_impact_community'])

    for nom in nominal_array:
        df_data[nom] = np.where(df_data[nom] != 1, 0, 1)

    df_data['low_budget_e_reader_1_high_2_no_3'] = np.where(df_data['low_budget_e_reader_1_high_2_no_3'] == 1, 0.5, np.where(df_data['low_budget_e_reader_1_high_2_no_3'] == 2, 1, 0))

    df_data['library_impact_your_family'] = np.where(df_data['library_impact_your_family'] == 2, 0.5, np.where(df_data['library_impact_your_family'] == 3, 1, 0))

    df_data['library_impact_community'] = np.where(df_data['library_impact_community'] == 2, 0.5, np.where(df_data['library_impact_community'] == 3, 1, 0))


    df_preproc = df_data[freq_array].apply(lambda x: (x - x.min()) / (x.max() - x.min()))

    df_output = pd.concat([df_data, df_preproc], axis=1)

    df_output.sample(frac=0.2).to_csv("/home/lain/Redes-Sociales-con-Enfoque-Difuso/other_datasets/libraries_surveys/clean/"+str(year)+"_v5_libraries.csv")

 
