import json
from tabulate import tabulate
import datetime
from pprint import pprint

MAXTICKETS_PERPAGE = 25

def input_message():                                                    # Initial message for the user 
    print('Choose the appropriate view mode :  \n')
    print('*-* Press \'ALL\' to view all the tickets \n')
    print('*-* Press \'SINGLE\' to view a specific ticket \n')
    print('*-* Press \'EXIT\' to exit from the tool \n')


def cli_display(ticket_list):
    while True:
        input_message()
        user_input = input("- ")                                        # After the message is displayed , need to get an input from the user 
        if (user_input == 'ALL'):
            display_all(ticket_list,0)
        elif(user_input == 'SINGLE'):
            display_individual(ticket_list)
        elif(user_input == 'EXIT'):
            return
        else:
            print('Enter a valid mode/option as mentioned above \n')

def format_date(date):                                                          # Format the date to a readable format 
    modified_date = datetime.datetime.strptime(date,'%Y-%m-%dT%H:%M:%SZ')
    str = "Date: {day}/{mon}/{yr} Time: {hr}:{min}:{sec} UTC" \
		.format(day=modified_date.day, mon=modified_date.month, yr=modified_date.year, hr=modified_date.hour,min=modified_date.minute,sec=modified_date.second)
    return str

def print_tickets_page(ticket_list,start,end):                                   # function to print one page of tickets , size = 25 
    if end > len(ticket_list):
        end = len(ticket_list)
    table_list = []
    for ticket in ticket_list[start:end]:
        table_list.append([ticket['id'],ticket['subject'],format_date(ticket['created_at']),ticket['requester_id'],ticket['submitter_id']])
    print(tabulate(table_list,headers=["TICKET_ID","SUBJECT","CREATION_TIME","REQUESTER_ID","SUBMITTER_ID"],tablefmt="pipe"))
    print('\n');
    
def display_all(ticket_list,start):                                         # Function which helps users to naviagte through multiple pages 
    begin = start
    invalid_flag = False
    while True:
        if invalid_flag == False:
            print_tickets_page(ticket_list,begin,begin+MAXTICKETS_PERPAGE)
        if begin > 0:                                                       # Condition for pages to the left to exist 
            left_pages = True
            print('Press \'L\' to go to the previous page \n')
        else:
            left_pages = False
        if begin+MAXTICKETS_PERPAGE < len(ticket_list):                     # condition for the pages to the right to exisit 
            right_pages = True
            print('Press \'R\' to go to the next page \n')
        else:
            right_pages = False
        print('Press \'M\' to go to the main menu \n')                                                  
        user_input = input("- ")

        if user_input == 'L' and left_pages== True:
            begin = begin - MAXTICKETS_PERPAGE
            invalid_flag = False
        elif user_input == 'R' and right_pages == True:
            begin = begin + MAXTICKETS_PERPAGE
            invalid_flag = False
        elif user_input == 'M':
            print('Returning to the Main Menu \n')
            invalid_flag == False
            return
        else:
            print('Enter a Valid Input \n')
            invalid_flag = True
     

def print_individual_ticket(ticket):                    # printing individual tickets 
    table = [[ticket['id'],ticket['subject'],format_date(ticket['created_at']),ticket['requester_id'],ticket['submitter_id']]]
    print('\n')
    print(tabulate(table,headers=["TICKET_ID","SUBJECT","CREATION_TIME","REQUESTER_ID","SUBMITTER_ID"],tablefmt="pipe"))
    print('\n')
    string = 'DESCRIPTION' + '\n' + '----------------------------------' + '\n' + ticket['description']
    print(string)


def display_individual(ticket_list):                        #Fetching the user input for the ID of the ticket to be printed 
    print('Enter the ID of the ticket to view \n')
    user_input = input("- ")
    list_t = ticket_list
    for ticket in ticket_list:
        if str(ticket['id']) == user_input:
            print_individual_ticket(ticket)
            return
    print('Ticket with this ID does not exist \n')
