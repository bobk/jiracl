# jiracl

This code demonstrates how to implement a simple Jira command line using the jira and cmd modules. See documentation on operation before using. This is template code for others to copy and extend, so extensive error checking has not been added yet. Individual scripts and the functions they perform are listed below:

### jiracl.py: 
    
- simple demo of creating a command-line for Jira using jira and cmd modules
- jira: https://jira.readthedocs.io/en/master/
- cmd: https://docs.python.org/3/library/cmd.html
- listing of supported commands is in the source code
- developed on Windows 10 and tested with Python 3.8.2 64-bit against Jira Server v8.8.1
- meant to be extended later

#### execution

1) you must have a Jira instance, an username on that instance, the password for that username, and at least one project
1) should work with Jira Cloud
1) py jiracl.py
1) type "help" to see all commands
1) type "help <command>" to see help for a single command, e.g. "help set_server"
