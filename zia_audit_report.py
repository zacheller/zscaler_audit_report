from helpers.zia_api_calls import ZiaTalker
import time


def check_report_status(zs):
    count = 0
    complete = False
    while (complete == False and count < 4):
        response = zs.list_auditlogEntryReport()
        if "complete" in response.get('status').lower():
            complete = True
        else:
            count = count + 1
            time.sleep(3)
    if not complete:
        raise ValueError("Was not possible to generate the report")
    return complete


def write_csv(csv_report):
    """
    Function to write to csv file
    :param csv_report:
    :return: none
    """


def get_audit_report(api_key, user, password, cloud='zscalerthree.net'):
    zs = ZiaTalker(f'zsapi.{cloud}')
    zs.authenticate(api_key, user, password)
    zs.add_auditlogEntryReport()
    check_report_status(zs.list_auditlogEntryReport())
    zs.download_auditlogEntryReport()
