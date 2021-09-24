
# System imports
import copy
import os
import sys

class init(object):
    def __init__(self, glob):
        self.glob = glob
    
    # Convert strings to lists
    def listify(self, message):
        if not isinstance(message, list):
            return [message]
        return message

    # Log and print to stdout
    def log_and_print(self, message, priority):
        message = self.listify(message)

        # Log and print if priority
        for line in message:
            if self.glob.log:
                self.glob.log.debug(line)
            if self.glob.stg['debug'] or priority: 
                print(line)

        # Print line break for multiple 
        if len(message) > 1 and (self.glob.stg['debug'] or priority):
            print()

    # High priority message, nonconditional
    def high(self, message):
        self.log_and_print(message, True)   

    # Low priority message, conditional on debug=True
    def low(self, message):
        self.log_and_print(message, False)            

    # Print message to log and stdout then continue
    def warning(self, message):
        self.log_and_print([self.glob.warning] + self.listify(message), True)

    # Print message to log and stdout then quit
    def error(self, message):
        message = self.listify(message)

        self.log_and_print(["", 
                            ""] + 
                            [self.glob.error] + 
                            self.listify(message) +
                            ["Check log for details."],
                            True)

        # Clean tmp files
        if self.glob.stg['clean_on_fail']:
            self.log_and_print("Cleaning up tmp files...", True)
            self.glob.lib.files.remove_tmp_files()

        self.log_and_print(["Quitting", ""], True)

        sys.exit(1)

    # Print heading text in bold
    def heading(self, message):
        message = self.listify(message)

        message[0] = self.glob.bold + message[0]
        message[-1] = message[-1] + self.glob.end

        self.log_and_print([""] + message, True)

    # Print section break
    def brk(self):
        print("---------------------------")
        print()


    # Get list of uncaptured results and print note to user
    def new_results(self):
        self.log_and_print(["Checking for uncaptured results..."], False)
        # Uncaptured results + job complete
        pending_results = self.glob.lib.get_completed_results(self.glob.lib.get_pending_results(), True)
        if pending_results:
            self.log_and_print([self.glob.note,
                                "There are " + str(len(pending_results)) + " uncaptured results found in " + 
                                self.glob.lib.rel_path(self.glob.stg['pending_path']),
                                "Run 'benchtool --capture' to send to database."], False)
        else:
            self.log_and_print(["No new results found.",
                                ""], False)


    # Print message about application exe file
    def exe_check(self, exe, search_path):   
        # Check if it exists
        exe_exists = self.glob.lib.files.exists(exe, search_path)

        if exe_exists:
            self.low(["Application executable found in:",
                            ">  " + self.glob.lib.rel_path(search_path)])
        else:
            self.error("failed to locate application executable '" + exe + "'in " + self.glob.lib.rel_path(search_path))

    # Print last 20 lines of file
    def print_file_tail(self, file_path):

        # File exists
        if not os.path.isfile(file_path):
            self.glob.lib.msg.error("File not found: " + self.glob.lib.rel_path(file_path))

        print()
        print("==> " + self.glob.lib.rel_path(file_path) + " <==")
        print("...")

        # Print last 20 lines
        with open(file_path, 'r') as fd:
                lines = fd.readlines()
                [print(x.strip()) for x in lines[max(-50, (len(lines)*-1)):]]


