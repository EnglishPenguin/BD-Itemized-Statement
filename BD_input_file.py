import pandas as pd
from datetime import date, timedelta
from xlsx2csv import Xlsx2csv
from logger_setup import logger
from glob import glob

def facs_report_prep():
    # determine the file date
    today = date.today()
    fd_yyyymmdd = today.strftime('%Y%m%d')
    fd_mmddyyyy = today.strftime('%m/%d/%Y')
    logger.info(f"File date is {fd_mmddyyyy}")

    # File Paths to be used for the file conversion
    xlsx_file_path = "\\\\NASDATA201\\SHAREDATA\\MV-RCR01\\SHARED\\RC Experience\\Bad Debt\\FACS Open Inventory\\BOT FACS Reports"
    
    # FACS File Naming Convention yyyymmdd_FACS_BADDEBT_IB_INBOUND.xlsx
    xlsx_f = f"{xlsx_file_path}\\{fd_yyyymmdd}_FACS_BADDEBT_IB_INBOUND.xlsx"
        
    # Read the csv into a dataframe
    df_main = pd.read_excel(xlsx_f, engine='openpyxl')
    logger.success(f"There are {len(df_main)} statements to be printed")

    # Adjust FACS report to match expected format
    col_names = {
        "FACS ACCT":"FACS ACCT",
        "Client ACCT":"CLIENT ACCT",
        "Dispo":"DISPO",
        "Last Name":"Last Name",
        "First Name":"First Name",
        "Product Line":"Product Line",
        "CLCORR":"CLCORR",
        "ZZACPAANSGROUP":"ZZACPAANSGROUP"
    }
    cols_to_keep = [
        "CLIENT ACCT",
        "DISPO",
        "CLCORR",
        "ZZACPAANSGROUP"
    ]

    df_main.rename(columns=col_names, inplace=True)
    df_main = df_main[cols_to_keep]
  
    # Set the outpath and save the .csv with the correct naming convention
    out_path = '\\\\NT2KWB972SRV03\\SHAREDATA\\CPP-Data\\Sutherland RPA\\BD IS Printing'
    ### test out path
    # out_path = 'Y:/RC Experience/Bad Debt/FACS Open Inventory/BOT FACS Reports/testing'
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
    ### test out path
    # out_path = f'Y:/RC Experience/Bad Debt/FACS Open Inventory/BOT FACS Reports/testing/{file_name}'

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


