
import unittest
from unittest import mock
from cli_manager import *
from ticket_viewer import *

class Mockresponse:                             # Mock response object to be used for testing 
    def __init__(self,json_data):
        self.json_data = json_data
    
    def json(self):
        return self.json_data

def test_get_requests_singlepage(url,headers):              # test requests.get functions when there is one page in the response 
    sample_json = {"next_page": None, "tickets" : [{ "subject":"abcdef", "created_at" : "2021-11-28T19:26:18Z", "requester_id" : 1, "submitter_id" : 2}]}
    sample_response = Mockresponse(sample_json)
    sample_response.status_code = 200
    return sample_response

def test_get_requests_multipage(url,headers):               # test requests.get when there are 2 pages in the response
    if url != "next_page_url":
        sample_json = {"next_page": "next_page_url", "tickets" : [{ "subject":"abcdef", "created_at" : "2021-11-28T19:26:18Z", "requester_id" : 1, "submitter_id" : 2}]}
    else:
        sample_json = {"next_page": None, "tickets" : [{ "subject":"abcdef", "created_at" : "2021-11-28T19:26:18Z", "requester_id" : 1, "submitter_id" : 2}]}
    sample_response = Mockresponse(sample_json)
    sample_response.status_code = 200
    return sample_response

def test_get_requests_badresponse(url,headers):                 # test requests.get when the response is non 200 
    sample_json = {"next_page": None, "tickets" : [{ "subject":"abcdef", "created_at" : "2021-11-28T19:26:18Z", "requester_id" : 1, "submitter_id" : 2}]}
    sample_response = Mockresponse(sample_json)
    sample_response.status_code = 400
    return sample_response


class CliManager_TestCase(unittest.TestCase):
    def test_format_date(self):                     # unit test for format_date function 
        date = "2021-11-28T19:26:18Z"
        modified_date = format_date(date)
        self.assertTrue(str(modified_date)=="Date: 28/11/2021 Time: 19:26:18 UTC")

class TicketViewer_TestCase(unittest.TestCase):        
    @mock.patch('requests.get', side_effect = test_get_requests_singlepage)
    def test_request_tickets_singlepage(self,test_get):                                     # unit test for request_tickets() function when the response for request.get has one page 
        headers_dict = {"Accept":"application/json","Authorization": "Bearer abcdefghijk"}
        resp_list = request_tickets("url",headers_dict)
    #    self.assertTrue(len(resp_list) == 1)
    #    self.assertIsInstance(resp_list,list)
        self.assertListEqual(resp_list,[[{ "subject":"abcdef", "created_at" : "2021-11-28T19:26:18Z", "requester_id" : 1, "submitter_id" : 2}]])

    @mock.patch('requests.get', side_effect = test_get_requests_multipage)
    def test_request_tickets_multipage(self,test_get):                                          # unit test for request_tickets() function when the response for request.get has multiple page
        headers_dict = {"Accept":"application/json","Authorization": "Bearer abcdefghijk"}
        ticket_list = request_tickets("url",headers_dict)
    #    self.assertTrue(len(ticket_list) == 2)
    #    self.assertIsInstance(ticket_list,list)
        self.assertListEqual(ticket_list,[[{ "subject":"abcdef", "created_at" : "2021-11-28T19:26:18Z", "requester_id" : 1, "submitter_id" : 2}],[{ "subject":"abcdef", "created_at" : "2021-11-28T19:26:18Z", "requester_id" : 1, "submitter_id" : 2}]])


    @mock.patch('requests.get', side_effect = test_get_requests_badresponse)
    def test_request_tickets_badresponse(self,test_get):                                        # unit test for request_tickets() function when the response for request.get has non 200 response code 
        headers_dict = {"Accept":"application/json","Authorization": "Bearer abcdefghijk"}
        response_list = request_tickets("url",headers_dict)
        self.assertTrue(response_list == False)    

    def test_parse_tickets(self):                                                           # unit test for the parse_tickets() function 
        list = [[{ "subject":"abcdef", "created_at" : "2021-11-28T19:26:18Z", "requester_id" : 1, "submitter_id" : 2},{"subject":"efghijk", "created_at": "2021-12-28T19:26:18Z","requester_id" : 2, "submitter_id" : 3}],[{"subject":"lmnopqrst", "created_at": "2021-01-28T19:26:18Z","requester_id" : 3, "submitter_id" : 4}]]
        t_list = []
        for l_t in list:
            parse_tickets(l_t,t_list)
        self.assertListEqual(t_list,[{ "subject":"abcdef", "created_at" : "2021-11-28T19:26:18Z", "requester_id" : 1, "submitter_id" : 2},{"subject":"efghijk", "created_at": "2021-12-28T19:26:18Z","requester_id" : 2, "submitter_id" : 3},{"subject":"lmnopqrst", "created_at": "2021-01-28T19:26:18Z","requester_id" : 3, "submitter_id" : 4}])
        
if __name__ == '__main__':
    unittest.main()