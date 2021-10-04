import pdb

from helpers.http_helper import HttpHelper
import time


class ZsTalker(object):
    """
    Zscaler API talker
    Documentation: https://help.zscaler.com/zia/api
    https://help.zscaler.com/zia/6.1/api
    """

    def __init__(self, cloud_name):
        self.base_uri = f'https://{cloud_name}/api/v1'
        self.hp_http = HttpHelper(host=self.base_uri, verify=True)
        self.jsessionid = None
        self.version = '1.2'

    def _obfuscateApiKey(self, seed):
        """
        Internal method to Obfuscate the API key
        :param seed: API key
        :return: timestamp,obfuscated key
        """
        now = int(time.time() * 1000)
        n = str(now)[-6:]
        r = str(int(n) >> 1).zfill(6)
        key = ""
        for i in range(0, len(str(n)), 1):
            key += seed[int(str(n)[i])]
        for j in range(0, len(str(r)), 1):
            key += seed[int(str(r)[j]) + 2]
        return now, key

    def authenticate(self, apikey, username, password):
        """
        Method to authenticate.
        :param apikey: type string: API key
        :param username: type string: A string that contains the email ID of the API admin
        :param password:  type string: A string that contains the password for the API admin
        :return:  JSESSIONID. This cookie expires by default 30 minutes from last request
        """
        timestamp, key = self._obfuscateApiKey(apikey)

        payload = {
            "apiKey": key,
            "username": username,
            "password": password,
            "timestamp": timestamp
        }
        url = '/authenticatedSession'
        response = self.hp_http.post_call(url=url, payload=payload)
        self.jsessionid = response.cookies['JSESSIONID']

    def list_auditlogEntryReport(self):
        """
        Gets the status of a request for an audit log report. After sending a POST request to /auditlogEntryReport to
        generate a report, you can continue to call GET /auditlogEntryReport to check whether the report has finished
        generating. Once the status is COMPLETE, you can send another GET request to /auditlogEntryReport/download to
        download the report as a CSV file.
        :return: json
        """

        url = "/auditlogEntryReport"

        response = self.hp_http.get_call(url, cookies={'JSESSIONID': self.jsessionid},
                                         error_handling=True)
        return response.json()

    def download_auditlogEntryReport(self):
        """
        Gets the status of a request for an audit log report. After sending a POST request to /auditlogEntryReport to
        generate a report, you can continue to call GET /auditlogEntryReport to check whether the report has finished
        generating. Once the status is COMPLETE, you can send another GET request to /auditlogEntryReport/download to
        download the report as a CSV file.
        :return: json
        """

        url = "/auditlogEntryReport/download"
        response = self.hp_http.get_call(url, cookies={'JSESSIONID': self.jsessionid},
                                         error_handling=True)
        return response

    def add_auditlogEntryReport(self, startTime, endTime, actionTypes=None, category=None,
                                subcategories=None, actionResult=None, actionInterface=None):
        """
         Creates an audit log report for the specified time period and saves it as a CSV file. The report includes audit
         information for every call made to the cloud service API during the specified time period.
         Creating a new audit log report will overwrite a previously-generated report.
        :param startTime: The timestamp, in epoch, of the admin's last login
        :param endTime: The timestamp, in epoch, of the admin's last logout.
        :param actionTypes: type list. The action performed by the admin in the ZIA Admin Portal or API
        :param actionResult: The outcome (i.e., Failure or Success) of an actionType.
        :param category: tyoe string. The location in the Zscaler Admin Portal (i.e., Admin UI) where the actionType was performed
        :param subcategories: type list. The area within a category where the actionType was performed.
        :param actionInterface: type string. The interface (i.e., Admin UI or API) where the actionType was performed.
        :return: 204 Successful Operation
        """
        url = "/auditlogEntryReport"
        payload = {"startTime": startTime,
                   "endTime": endTime,
                   }
        if category:
            payload.update(category=category)
        if subcategories:
            payload.update(subcategories=subcategories)
        if actionInterface:
            payload.update(actionInterface=actionInterface)
        if actionTypes:
            payload.update(actionTypes=actionTypes)

        response = self.hp_http.post_call(url, payload=payload, cookies={'JSESSIONID': self.jsessionid},
                                          )
        return response
