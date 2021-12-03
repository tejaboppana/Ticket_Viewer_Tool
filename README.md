**TICKET_VIEWER_TOOL**

This is a tool that will connect to the Zendesk API and fetch the tickets and display them in a readabel format. Below are the features of the tool :

- It can display all the tickets available at the same time with 25 tickets per page 
- It can display individual tickets based on the Ticket ID specified.

**REQUIREMENTS AND INSTALLATION**

1. In order to run the tool succesfully, you need to have Python 3 installed. 

2. The libraries used in the tool are requests,tabulate(for displaying the data in tabular format) and mock (for testing). There is a requirements.txt file added in the code which can be used to install the requirements . Run the below command :

`pip3 install -r requirments.txt`

3. If you are facing any issues while installing, please ensure that you have pip3 installed in your machine. You can use this [link](https://docs.python-guide.org/) to see the steps to install pip3 based on the OS that you are using. 

**USAGE**

1. In order to use the tool , download the source code in the directory and then above requirements are met.

2. Run the following command to start the tool :
`python3 ticket_viewer.py`

**TESTING**

In order to perform the unit testing run the below command :

`python3 unit_test.py`

