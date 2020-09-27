"""
http://github.com/bobk/jiracl

jiracl.py
this code demonstrates how to implement a simple Jira command line using the jira-python and cmd modules
see documentation on operation before using

this is template code for others to copy and extend, so extensive error checking has not been added yet

"""


import cmd
import getpass
import sys
import csv
from jira import JIRA


class commands(cmd.Cmd):
    """
    main class required by the cmd module, this class contains the variables and functions that constitute the command line
    """

    connection = None
    server_name = None
    project_name = None
    issue_key = None
    user_name = None

    def args_list(self, args_string):
        """
        internal function for taking the single comma-delimited args string and converting it to a list, and handling
        any quotes or delimiters in the values, if they exist
        """

#   assumes just a single line of input
        line = csv.reader([args_string], skipinitialspace=True, delimiter=',', quotechar='\'')
        return next(line)


    def set_prompt(self):
        """
        internal function for setting the Python prompt to the current server, project and issue if they each exist
        """

        self.prompt = ">>> "
        if (self.server_name is not None):
            self.prompt = '>' + self.server_name + '>'
        else:
            return

        if (self.project_name is not None):
            self.prompt = self.prompt + self.project_name + '>'
        else:
            return

        if (self.issue_key is not None):
            self.prompt = self.prompt + self.issue_key + '>'

        return


    def do_set_server(self, line):
        """
        set_server <servername,username>
        Opens a connection to the Jira server
        Example: set_server http://mySERVERorIP:port,myusername
        """

        line_list = self.args_list(line)
        self.server_name = line_list[0]
        self.user_name = line_list[1]

        password = getpass.getpass("Enter password: ")

        self.connection = JIRA(self.server_name, auth=(self.user_name, password))
        print("Connected to server: " + str(self.connection.server_info()))

        self.set_prompt()
        return


    def do_set_project(self, line):
        """
        set_project <projectname>
        Sets the current project to the specified projectname
        Example: set_project MYPROJECT
        """

        line_list = self.args_list(line)
        self.project_name = line_list[0]
        print("Set to project: " + str(self.project_name))

        self.set_prompt()
        return


    def do_create_issue(self, line):
        """
        create_issue <summary, description, [assignee]>
        Create a new issue in the current project, with the specified summary and description and optional assignee. 
        If assignee is not specified, the new issue will be assigned to the current user.
        Example: create_issue 'My summary','My description',myusername
        """

        line_list = self.args_list(line)
        summary = line_list[0]
        description = line_list[1]
        if (len(line_list) == 3):
            assignee = line_list[2]
        else:
            assignee = self.user_name

        issue = self.connection.create_issue(project=self.project_name, summary=summary, description=description, issuetype={'name': 'Task'})
        self.connection.assign_issue(issue, assignee)

        self.issue_key = issue.key

        self.set_prompt()
        return


    def do_set_issue(self, line):
        """
        set_issue <issuekey>
        Sets the current issue to the specified issuekey
        Example: set_issue MYPROJECT-123
        """

        line_list = self.args_list(line)
        issue_key = line_list[0]

        self.issue_key = issue_key
        print("Set to issue: " + str(self.issue_key))

        self.set_prompt()
        return


    def do_show_issue(self, line):
        """
        show_issue <issuekey>
        Shows several fields for the specified issuekey, or for the current issue
        Example: show_issue MYPROJECT-123
                 show_issue
        """

        if (line != ''):
            line_list = self.args_list(line)
            issue_key = line_list[0]
        else:
            issue_key = self.issue_key

        print("Issue: " + str(self.connection.issue(issue_key)))
        print("Summary: " + str(self.connection.issue(issue_key).fields.summary))
        print("Status: " + str(self.connection.issue(issue_key).fields.status))
        print("Description: " + str(self.connection.issue(issue_key).fields.description[:100]))
        print("Assignee: " + str(self.connection.issue(issue_key).fields.assignee))

        return


    def do_assign_issue(self, line):
        """
        assign_issue <[assignee], [issuekey]>
        Assigns the assignee to the specified issuekey, or to the current issuekey
        Example: assign_issue
                 assign_issue myusername
                 assign_issue myusername,MYPROJECT-123
        """

        if (line != ''):
            line_list = self.args_list(line)
            if (len(line_list) == 2):
                assignee = line_list[0]
                issue_key = line_list[1]
            elif (len(line_list) == 1):
                assignee = line_list[0]
                issue_key = self.issue_key
            else:
                assignee = self.user_name
                issue_key = self.issue_key
        else:
            assignee = self.user_name
            issue_key = self.issue_key

        issue = self.connection.issue(issue_key)
        self.connection.assign_issue(issue, assignee)

        return


    def do_exit(self, line):
        """
        this lets us use the 'exit' command to get out of the command line
        """

        sys.exit(0)

        return


    def do_EOF(self, line):
        """
        required by cmd
        """

        return True

    
if __name__ == '__main__':
    commands().cmdloop()
