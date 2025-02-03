import BD_input_file
from process_status.status_handler import JSONStatus

if __name__ == '__main__':
    status = JSONStatus(
        master_file_path=r'\\NT2KWB972SRV03\SHAREDATA\CPP-Data\CBO Westbury Managers\LEADERSHIP\Bot Folder\Automated Scripts Status.json',
        process_name='Sample Script'
    )
    status.update_status('Running')
    try:            
        BD_input_file.facs_report_prep()
        BD_input_file.save_hcx_report()
    except Exception as e:
        status.update_status('Failed', errors=str(e))