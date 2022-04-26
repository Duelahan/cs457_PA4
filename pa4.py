#Author: Tristan Bailey
#Date Created: 2/20/2022
#Last Modified: 4/26/2022
#Assignment: PA 4
#Class: CS457
#File: Main program file
#Summary: Implemented left inner and outer joins/.

#libraries
import sys
import os

#class imports
import table_methods as TB
import database_sys_class as DB
import helper_methods as helper

#helpful database sys managing object
my_db_sys = DB.database_sys()
#misc
misc= ["from", "add", "table"]

#parses the input list of strings, and then performs operations that are specified
#   by the strings, if this operations does not exist, inform the user
def parser(tokens):
    #these are tokens that start a query, each function performs the
    #   action specified by the user
    query_start = {"use": use_db, "create": create, "drop": drop, "select": select,
        "alter": alter_tb, "insert": insert_record, "delete": delete, "update": update}
    #perform the operation if it exists, otherwise inform the user
    try:
        query_start[tokens[0].lower()](tokens[1:])
    except:
        print(tokens[0] + " is not a valid query start.")

def use_db(tokens):
    my_db_sys.use_database(tokens[0])

def create(tokens):
    #if database then create the database
    if(tokens[0].lower() == "database"):
        my_db_sys.create_database(tokens[1])
    #if table then create the table
    elif(tokens[0].lower() == "table"):
        #removes the first '(' surrounding the parameters
        tokens[2] = tokens[2][1:]
        #removes the last ')' surrounding the parameters
        tokens[-1] = tokens[-1][:-1]
        #remove all commas
        tokens = [token.replace(",", "") for token in tokens]

        flip_flop = True
        param_list = []
        datatype_list = []
        #builds the list of parameters and tokens
        for token in tokens[2:]:
            #if true then string is a parameter
            if(flip_flop):
                flip_flop = False
                param_list.append(token)
            #if false then string is a datatype
            else:
                flip_flop = True
                datatype_list.append(token)
        my_db_sys.add_table(tokens[1], param_list, datatype_list)

def drop(tokens):
    if(tokens[0].lower() == "database"):
        my_db_sys.delete_database(tokens[1])
    #if table then create the table
    elif(tokens[0].lower() == "table"):
        my_db_sys.delete_table(tokens[1].lower())

def select(tokens):
    #remove any commas present in any tokens
    tokens = [elem.replace(",", '') for elem in tokens]

    #group by and order by filters, *** ignored for this PA but included for conceptual understanding
    #   and modularitty if needed in next PA's
    x = 0
    while(x != (len(tokens) - 1)):
        if((tokens[x].lower() == "group") and (tokens[x+1].lower() == "by")):
            tokens[x] = tokens[x] + " "
            tokens[x : x+2] = [''.join(tokens[x : x+2])]
            x -= 1
        elif((tokens[x].lower() == "order") and (tokens[x+1].lower() == "by")):
            tokens[x] = tokens[x] + " "
            tokens[x : x+2] = [''.join(tokens[x : x+2])]
            x -= 1
        x += 1
    try:
        #from_args is for tablenames as well as joins
        TB.print_table_attributes(my_db_sys.database_select(tokens))
    except Exception as e:
        print(e)

def alter_tb(tokens):
    #remove the table token as it is unecessary for the alter keyword
    tokens = tokens[1:]

    #*** add a valid parameter checker later

    if(tokens[1].lower() == "add"):
        #*** add a valid parameter checker later
        my_db_sys.alter_table_add(tokens[0], tokens[2], tokens[3], True)
    #subtract alter option
    elif(tokens[1].lower() == "sub"):
        my_db_sys.alter_table_add(tokens[0], tokens[2], tokens[3], False)

def insert_record(tokens):
    #removes into
    tokens = tokens[1:]
    #removes 'values' and the first '(' surrounding the parameters
    tokens[2] = tokens[2].replace('(', '')
    #removes the last ')' surrounding the parameters
    tokens[-1] = tokens[-1][:-1]
    #remove all commas
    tokens = [token.replace(",", "") for token in tokens]
    my_db_sys.insert_data(tokens[0], tokens[2:])

def delete(tokens):
    table_name = tokens[1]
    tokens = tokens[3:]
    #evaluate in groups of 3, left is var (so lower), middle is a symbol, right is value
    my_db_sys.delete_from_database(table_name, tokens)

def update(tokens):
    my_db_sys.update_table(tokens[0], tokens[2:])


def main(): 
    
    #create folder that houses databases
    if not os.path.exists("databases"):
        os.mkdir("databases")
    #TB.print_table_attributes(TB.load_table("hi", "tb1")) #["a1", "a2"], ["string", "string"]

    prev_command = True
    exit = False
    line = ""
    while not(exit):
        #this just helps when a file is piplined into standard input and does not print
        #prompt symbols for empty lines or comments
        if(prev_command):
            print("#", end = "")
        #input throws an error if it reads EOF, when utilizing standard input
        try:
                new_line = input("")

                #remove '\r' added by input
                new_line = new_line.rstrip("\r")
                #remove newlines errors if string is empty
                new_line = new_line.replace('\n', ' ')
                #remove tabs errors if string is empty
                new_line = new_line.replace('\t', ' ')
                #make sure that the paranthese is not separated from other keywords
                new_line = new_line.replace("(", " (", 1)

                new_line = new_line.replace(',', ", ")
                #dont add line if its a comment or an empty line 
                if((new_line != "") and (new_line[:2] != "--")):
                    if(line == ""):
                        line = new_line
                    else:
                        line = line + " " + new_line
                    #verify line ends in ; o.w. keep getting input from user
                    if(line[-1] == ";"):
                        try:
                            #remove semi colon
                            line = line[:-1]
                            #remove the end space if it is present
                            if(line[-1] == " "):
                                line = line[:-1]

                            mystring = line

                            tokens = mystring.split(" ")
                            #removes empty strings form the list of strings
                            tokens[:] = [x for x in tokens if x]
                            if(tokens[0].lower() == ".exit"):
                                exit = True
                            #avoids processing comments and empty lines in a file or in user input
                            elif(not(len(tokens) == 1)):
                                prev_command = True
                                #parse string and perform specified operations
                                parser(tokens)
                            else:
                                print("Single input string is invalid query.")
                        except:
                            #no command if this line is empty
                            prev_command = False
                        #reset line
                        line = ""
                    else:
                        prev_command = False
                else:
                        prev_command = False      
        except EOFError:
            exit = True
    print("All done.")

main()
