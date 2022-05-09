import os
import table_methods as TB

class transaction_mngr:
    separator = " ; "
    def __init__(self, database_name):
        reserved_tables = set()
        #initialize a file that stores all table locks
        if not os.path.exists("databases/"+ database_name.lower() + "/locks"):
            os.mkdir("databases/" + database_name.lower() + "/locks")
        if not os.path.exists("databases/"+ database_name.lower() + "/temp_tables"):
            os.mkdir("databases/" + database_name.lower() + "/temp_tables")
    #checks if a particular table is locked
    def locked(self, database_name, table_name):
        if os.path.exists("databases/"+ database_name.lower() + "/locks/" + table_name.lower() + ".lock"):
            return True
        else:
            return False

    def has_table(self, database_name, table_name):
        return (database_name, table_name) in self.reserved_tables()

    #lockes the desired table, if its unlocked, o.w. it throws an error
    def lock(self, database_name, table_name):
        exists = (database_name.lower(), table_name.lower()) in self.reserved_tables
        if ((not(exists)) and self.locked(database_name, table_name)):
            raise Exception("Already Locked")
        else:
            #checks if current transaction manager already locked the table
            temp_table_path = "databases/" + database_name.lower() + "/temp_tables/" + table_name.lower() + ".txt"
            if(not exists):
                #create table lock
                table_lock = open("databases/" + database_name.lower() + "/locks/" + table_name.lower() + ".lock", "x")
                table_lock.close()
                #create temp table
                temp_table = open(temp_table_path, "x")
                temp_table.close()
                self.reserved_tables.add((database_name.lower(), table_name.lower()))
            #o.w. do nothing as the table is already managed by the transaction manager
            return temp_table_path
    
    #adds the appropriatly updated record to the temp table
    def add_update(self, database_name, table_name, index, record):
        try:
            table_file = open("databases/" + database_name.lower() + "/temp_tables/" + table_name.lower() + ".txt", "a")
            #initialize the first element to be the index and add the sepaarator
            temp = str(index) + transaction_mngr.separator
            for element in record:
                temp += str(element)
                temp += transaction_mngr.separator
            table_file.write(temp+ "\n")
            table_file.close()
        except:
            pass

    #commits current transactions to thier respective tables
    def commit(self):
        for tuple in self.reserved_tables:
            self.merge(tuple[0], tuple[1])
            self.unlock(tuple)
        self.reserved_tables.clear()
    #aborts all current operations in the transaction
    def abort(self):
        for tuple in self.reserved_tables:
            self.unlock(tuple)
        self.reserved_tables.clear()

    #unlocks the desired table
    def unlock(self, database_name, table_name):
        #remove temp table
        os.remove("databases/" + database_name.lower() + "/temp_tables/" + table_name.lower() + ".txt")
        #remove lock last
        os.remove("databases/" + database_name.lower() + "/locks/" + table_name.lower() + ".lock")

    #merges the updates in a temp table to the original during commits
    def merge(self, database_name, table_name):
        original_table = TB.load_table(database_name, table_name)
        #load the temp table to memory
        temp_table_file = open("databases/" + database_name.lower() + "/temp_tables/" + table_name.lower() + ".txt", "r")
        list_of_indexes = []
        list_of_tuples = []
        lines = temp_table_file.readlines()
        #generate a list of tuples, that were modified, and a list of thier respective indexes in the table
        for line in lines:
            token_list = line.split(transaction_mngr.separator)
            list_of_indexes.append(int(token_list[0]))
            list_of_tuples.append(token_list[1:])

        #*** no tpye conversion is performed, so it may need to be added ot fix buugs later
        for i in range(0, len(list_of_indexes)):
            original_table[list_of_indexes[i]] = list_of_tuples[i]
        
        #save updates to disk
        TB.save_table(database_name, table_name, original_table)