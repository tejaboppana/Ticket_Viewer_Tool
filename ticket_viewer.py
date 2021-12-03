from argparse import ArgumentParser
import csv
import json
from pprint import pprint
import requests
from requests.exceptions import HTTPError
from cli_manager import *

url = "https://zcctejaboppana.zendesk.com/api/v2/tickets.json"                          
headers_dict = {"Accept":"application/json","Authorization": "Bearer af9ce4de80b1028ccda79fdff17764c77aba9f11bb2ef55f5ac6c4a9d5865a55"}
def request_tickets(url,headers_dict):                                      # function to make get requests and fetch the output from multiple pages (if there are multiple pages)
    resp_list = []
    try: 
        while url:                                                                  
            response = requests.get(url, headers=headers_dict)              # Using auth token for get requests 
            if response.status_code == 200:
                response_json = response.json()
                resp_list.append(response_json)
                url = response_json['next_page']                            # checking for next page 

                t_list = []
                for resp in resp_list:
                    ticket_dict = resp['tickets']                           # we are interested in only the tickets, so fetch the items from the 'tickets' key 
                    t_list.append(ticket_dict)                              # This will have array of arrays of ticket objects 

            else:
                return False

    except requests.exceptions.ConnectionError:
        return False
    return t_list

def parse_tickets(list,ticket_list):                                        # function to form a single array of ticket objects from array of array of tickets objects obtained from multiple pages 
    for tickets in list:
        ticket_list.append(tickets)
    return 

def ticket_viewer():                                                # Main function , which is responsible to fetch the Tickets using the API and then starting the Command Line Interface UI Application. 
    request_list = request_tickets(url,headers_dict)                # Get request to fetch the tickets, authentication using Oauth token 
    if request_list == False:
        print("Something went wrong while accessing the endpoint, check if the endpoint URL is correct or the connectivity is stable \n")
        return
    else:
        print('Welcome to the Zendesk Ticket Viewer Tool !! \n')    
        ticket_list = []
        for ticket in request_list:                                 # Going through each array of ticket objects and adding the objects to another array ticket_list 
            parse_tickets(ticket,ticket_list)

        cli_display(ticket_list)                                    # This ticket_list is passed to CLI_display function

if __name__ == '__main__':
    try:
        ticket_viewer()
    except KeyboardInterrupt:
        pass
    finally:
        print("Exiting from the Zendesk Ticket Viewer Tool \n")




