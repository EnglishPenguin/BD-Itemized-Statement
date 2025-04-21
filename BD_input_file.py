import pandas as pd
from datetime import date, timedelta
from xlsx2csv import Xlsx2csv
from logger_setup import logger
import os
import time
from glob import glob

def facs_report_prep():
    # File Paths to be used for the file conversion
    # select Y or M drive depending on if GOA job has been completed
    xlsx_file_path = "\\\\NT2KWB972SRV03\\SHAREDATA\\CPP-Data\\Sutherland RPA\\BD IS Printing\\FACS Input"
    # xlsx_file_path = "\\NASDATA201\SHAREDATA\MV-RCR01\SHARED\\RC Experience\\Bad Debt\\FACS Open Inventory"
    xlsx_f = f"{xlsx_file_path}\\Bad-Debt_Review.xlsx"
    csv_file_path = "\\\\NT2KWB972SRV03\\SHAREDATA\\CPP-Data\\Sutherland RPA\\BD IS Printing\\FACS Input"
    csv_f = f"{csv_file_path}\\Bad-Debt_Review.csv"
    # Get the file stat information
    file_stat = os.stat(xlsx_f)
    today = date.today()
    fd_yyyymmdd = today.strftime('%Y%m%d')
    fd_mmddyyyy = today.strftime('%m/%d/%Y')

    # Access the last modified time
    last_modified_time = time.strftime('%m/%d/%Y', time.localtime(file_stat.st_mtime)) 
    logger.info(f'Current date is: {fd_mmddyyyy}')
    logger.info(f'FACS Report Last Updated: {last_modified_time}')
    if last_modified_time != fd_mmddyyyy:
        logger.critical('FACS report has not been updated')
    else:
        logger.success(f'FACS report for {last_modified_time} to be converted')

    # Converts the .xlsx to a .csv for Chunk Processing
    try:
        logger.info('Starting xlsx to csv conversion')
        Xlsx2csv(xlsx_f, outputencoding="utf-8").convert(csv_f)
    except FileNotFoundError:
        logger.error(f"Bad-Debt_Review.xlsx does not exist")
    else:
        logger.success(f"Bad-Debt_Review.xlsx successfully converted to .CSV")

    # Set the columns and chunk size to be used; Initialize open list and chunk iteration
    cols = ['CLIENT ACCT', 'CLCORR', 'DISPO']
    chunk_size = 10 ** 5
    data = []
    iteration = 0
    
    # Process the .csv in chunks for quicker handling
    for chunk in pd.read_csv(csv_f, usecols=cols, chunksize=chunk_size, low_memory=False):
        iteration += 1
        logger.info(f"Chunk Reader on Iteration #{iteration}")
        try:
            # Filters the chunk for the required values
            chunk = chunk[chunk['CLCORR'] == 'PAANS']
            chunk = chunk.loc[(chunk['DISPO'] == '3IBR') | 
                            (chunk['DISPO'] == '3DVR') | 
                            (chunk['DISPO'] == '5IBR') | 
                            (chunk['DISPO'] == '5DVR'), 
                            ['CLIENT ACCT', 'CLCORR', 'DISPO']
                            ]
        except KeyError:
            logger.error(f"KeyError found in Iteration #{iteration}")
            continue
        else:
            # Appends the chunk to the dataframe
            data.append(chunk)
        finally:
            logger.info(f"{len(chunk)} lines added from Iteration #{iteration}.")
        
    # Concatenate the list of dataframes into one dataframe
    df_main = pd.concat(data)
    logger.success(f"There are {len(df_main)} statements to be printed")

    # determine the file date
    logger.info(f"File date is {fd_mmddyyyy}")

    # Set the outpath and save the .csv with the correct naming convention
    out_path = '\\\\NT2KWB972SRV03\\SHAREDATA\\CPP-Data\\Sutherland RPA\\BD IS Printing'
    out_file = f'{fd_yyyymmdd}_BADDEBT_FACS_INBOUND.csv'
    df_main.to_csv(f'{out_path}\\{out_file}', index=False)
    logger.success(f"{out_file} saved to {out_path}")

def save_hcx_report():
    # 20231221_PAANS_BADDEBT_IB_BOT.csv
    today = date.today()
    fd_yyyymmdd = today.strftime('%Y%m%d')
    file_name = f'{fd_yyyymmdd}_PAANS_BADDEBT_IB_BOT.csv'
    in_path = f'\\\\NASDATA201\\SHAREDATA\\MV-RCR01\\SHARED\\RC Experience\\DO NOT REMOVE - HCx Ontario Reports\\{file_name}'
    out_path = f'\\\\NT2KWB972SRV03\\SHAREDATA\\CPP-Data\\Sutherland RPA\\BD IS Printing\\{file_name}'

    try:
        with open(in_path, 'r') as source_file:
            logger.info(f'Reading source file from {in_path}')
            source_content = source_file.read()
        with open(out_path, 'w') as destination_file:
            logger.info(f'Saving file to {out_path}')
            destination_file.write(source_content)
    except FileNotFoundError:
        logger.error(f'{file_name} not found at source location')
        exit()
    else:
        logger.success(f'HCX report successfully saved to {out_path}')

def define_duplicates():
    logger.info('Defining duplicates')
    date = date.today()
    year = date.strftime('%Y')
    shs_inputs = f"\\\\NT2KWB972SRV03\\SHAREDATA\\CPP-Data\\Sutherland RPA\\BD IS Printing\\{year}"
    # from the shs_inputs glob together all .csv files
    files = glob(shs_inputs + "\\*.csv")
    # from the list of files only pull the last 4 files
    files = files[-4:]
    # read each file into a dataframe
    dfs = [pd.read_csv(file) for file in files]
    # concatenate all the dataframes into one
    df = pd.concat(dfs)
    # keep only the column 'HCENPTACCT'
    df = df[['HCENPTACCT']]
    # drop duplicate rows
    df = df.drop_duplicates()
    # write the dataframe to a csv file
    df.to_csv(f'{shs_inputs}\\Previous 4 Days.csv', index=False)

def remove_duplicates():
    define_duplicates()
    today = date.today()
    fd_yyyymmdd = today.strftime('%Y%m%d')
    year = today.strftime('%Y')
    hcx_file_name = f'{fd_yyyymmdd}_PAANS_BADDEBT_IB_BOT.csv'
    facs_file_name = f'{fd_yyyymmdd}_BADDEBT_FACS_INBOUND.csv'
    inputs_file_path = '\\\\NT2KWB972SRV03\\SHAREDATA\\CPP-Data\\Sutherland RPA\\BD IS Printing\\'
    prev_sub_file_path = f'\\\\NT2KWB972SRV03\\SHAREDATA\\CPP-Data\\Sutherland RPA\\BD IS Printing\\{year}\\Previous 4 Days.csv'

    df_facs = pd.read_csv(f'{inputs_file_path}\\{facs_file_name}')
    df_hcx = pd.read_csv(f'{inputs_file_path}\\{hcx_file_name}')
    logger.info(f'Total rows in FACS: {len(df_facs)} before removing duplicates')
    logger.info(f'Total rows in HCX: {len(df_hcx)} before removing duplicates')
    df_prev_sub = pd.read_csv(prev_sub_file_path)

    logger.info('Identifying duplicates for FACS and HCX')
    df_facs = identify_duplicates(df_prev_sub, df_facs, 'CLIENT ACCT', 'FACS')
    df_hcx = identify_duplicates(df_prev_sub, df_hcx, 'HCENPTACCT', 'HCX')
    logger.info('Duplicates identified and removed')
    logger.info('Saving files to \\\\NT2KWB972SRV03\\SHAREDATA\\CPP-Data\\Sutherland RPA\\BD IS Printing\\')
    df_facs.to_csv(f'{inputs_file_path}\\{facs_file_name}', index=False)
    df_hcx.to_csv(f'{inputs_file_path}\\{hcx_file_name}', index=False)

    
def identify_duplicates(df_prev, df_review, review_column, id):
    # compare df_review with df_prev, drop duplicates from df_review if they appear in df_prev
    df_review = df_review[~df_review[review_column].isin(df_prev['HCENPTACCT'])]
    logger.info(f'Total rows in {id}: {len(df_review)} after removing duplicates')
    return df_review
