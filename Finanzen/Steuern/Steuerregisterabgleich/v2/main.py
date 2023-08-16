'''Steuerregisterabgleich v. 2.0'''
# Author: Timon Jakob
# Date: 08.2023



if __name__ == "__main__":
    start_time = time.time()
    dataframe_cit, dataframe_tax = load_data()
    dataframe_cit = prepare_data_cit(dataframe_cit)
    dataframe_tax = prepare_data_tax(dataframe_tax)
    dataframe_missing = compare_data(dataframe_cit, dataframe_tax)
    save_data(dataframe_missing)
    runtime = time.time() - start_time
    print_statistics(dataframe_cit, dataframe_tax, dataframe_missing, runtime)
