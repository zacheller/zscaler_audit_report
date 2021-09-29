
import time
import http.client
import json
import csv


zscalerCloudName = "zsapi.zscalerthree.net"



def generate_report():
    """
    # Generates Report from last 24 hours
    :return:
    """
    conn = http.client.HTTPSConnection(zscalerCloudName)

    startTime = time.time()  # Timestamp in epoch of the admin's last login (
    endTime = startTime - 24 * 3600  # Timestamp in epoch of the admin's last logout

    '''
    The request body can also include the following attributes:

    actionTypes: The action performed by the admin in the ZIA Admin Portal (i.e., Admin UI) or API. Possible values for actionTypes.
    category: The location in the ZIA Admin Portal (i.e., Admin UI) where the actionType was performed. Possible values for category.
    subcategories: The area within a category where the actionType was performed. Possible values for subcategories.
    actionResult: The outcome (i.e., Failure or Success) of an actionType.
    actionInterface: The interface (i.e., Admin UI or API) where the actionType was performed.
    clientIP: The source IP address for the admin.
    adminName: The admin's login ID.
    '''

    payload = {"startTime": startTime, "endTime": endTime}

    headers = {'content-type': "application/json", 'cache-control': "no-cache"}

    conn.request("POST", "/api/v1/auditlogEntryReport", json.dumps(payload), headers)

    res = conn.getresponse()
    data = res.read()

    print("Generate Report POST Request response: " + data.decode("utf-8"))


# Sends a GET Request every `sleepTime` seconds until report is generated
def check_report_status(sleepTime, tries):
    count = 0
    complete = False

    while (complete == False and count < tries):
        conn = http.client.HTTPSConnection(zscalerCloudName)
        conn.request("GET", "/api/v1/auditlogEntryReport")
        res = conn.getresponse()
        data = res.read()
        # print(data.decode("utf-8"))
        if "COMPLETE" in data.decode("utf-8"):
            complete = True
        else:
            count = count + 1
            time.sleep(sleepTime)
    print("After " + str(count) + " attempt(s), the script ", end='')
    return complete


def download_CSV(filename):
    conn = http.client.HTTPSConnection(zscalerCloudName)
    conn.request("GET", "/api/v1/auditlogEntryReport/download")
    res = conn.getresponse()
    data = res.read()

    dataStr = data.decode("utf-8")
    print(dataStr)
    print(repr(data))

    # TODO depending on response format, will need to parse to save to CSV
    # https://www.geeksforgeeks.org/python-save-list-to-csv/

    file = open(filename, "w")
    file.write(dataStr)
    file.close()


def main():
    # TODO create Authenticated Session - Need Credentials

    generate_report()

    secondsToSleep = 1
    tries = 5
    success = check_report_status(secondsToSleep, tries)
    if not success:
        print('failed to obtain an audit report. Service may be down.')
        return -1

    filename = "test_report.csv"
    download_CSV(filename)

    print('successfully obtained the audit report and saved it as: ' + filename)


if __name__ == "__main__":
    main()