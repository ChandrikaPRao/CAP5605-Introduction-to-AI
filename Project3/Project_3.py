# -*- coding: utf-8 -*-
"""
This program is a knowledge-based intelligent system that collects user 
preferences and reasons about them. It will take Attributes, Hard constraints
and preferences as input and output models as per user request.
"""
from tkinter import *
import tkinter.messagebox
import sys
import subprocess
import pandas as pd
import os
import time
from collections import OrderedDict
import copy
import shutil
import re

# User can modify the below variable values.
attribute_file_path = "A.txt"
hard_constraints_file_path = "H.txt"
preferences_file_path = "T.txt"

# Don't modify the below variables
cnf_txt_file = "CNF.txt"
hard_constraints_cnffile = cnf_txt_file.split(".")[0]+".cnf"  
hard_constraint_output_file = 'clasp_h_output_file.txt'   
hard_constraints_file_copy = "HardConstraints_copy.txt"
preferences_file_copy = "HardPreferences_copy.txt"
read_me_file = "README.md"
satisfiable_models_list=[]
preference_clasp_files_list = []
preference_cnf_files_list = []
replacements = {'OR':' ','or':' ', 'Or':' ','AND' : '0\n', 'and' : '0\n',\
                'And' : '0\n', 'NOT' : '-', 'not':'-', 'Not' : '-','--':''}
attribute_count = 0

def process_attributes(attribute_input_file):
    """
    This function read the data from Attributes file(attribute_input_file) and
    returns a pandas dataframe object attribute_df.
    """
    with open(attribute_input_file, mode = 'r') as f:
        attribute_file = f.read()
        attribute_file = attribute_file.replace(':','')
        attribute_file = attribute_file.replace(',','')
        attribute_file = os.linesep.join([s for s in attribute_file.splitlines() if s])
        attribute_df = pd.DataFrame([x.split(' ') for x in attribute_file.split('\r')])# \n or \r
#        print "process_attributes > attribute_df : ", attribute_df
        f.close()
    return attribute_df

def convert_txt_cnf(text_file):
    """
    This function will take a .txt file as an input and convert it to .cnf file
    """
    cnf_file = str(text_file).split('.')
    cnf_file = cnf_file[0]+".cnf"
    if os.path.exists(cnf_file):
        os.remove(cnf_file)
    else:
        pass
#        print("The file does not exist")
    base = os.path.splitext(text_file)[0]
    os.rename(text_file, base + '.cnf')

def get_attribute_value(str_attribute, attr_dataframe):
    """
    This function will read the input str_attribute and convert the
    attributes to their corresponding integer equivalents using attr_dataframe.
    """
    df_col_1 = attr_dataframe.loc[attr_dataframe[1]==str_attribute].index.values
    df_col_2 = attr_dataframe.loc[attr_dataframe[2]==str_attribute].index.values
    if df_col_1.size > 0:
        df_col_1 = df_col_1 + 1
        return int(df_col_1)
    elif df_col_2.size > 0:
        df_col_2 = -(df_col_2 + 1)
        return int(df_col_2)
    else:
        return 9999

def convert_attribute_value_string(int_attribute, attr_dataframe):
    """
    This function will read the input int_attribute and convert the integer 
    value of the attribute to their corresponding string value in input
    attr_dataframe.
    """
    if int(int_attribute) > 0:
        attribute_name = attr_dataframe.at[abs(int(int_attribute))-1,1]
    else:
        attribute_name = attr_dataframe.at[abs(int(int_attribute))-1,2]
    return attribute_name

def convert_satisfiable_models(sat_models, attribute_dataframe):
    """
    This function will convert the satisfiable models from int format to their
    corresponding attribute name in Attribute data frame.
    """
    final_attr_list = []
#    print "satisfiable_models: ", sat_models
    for each in sat_models:
        attr_string = [convert_attribute_value_string(model,attribute_dataframe ) for model in each.split()]
        final_attr_list.append(attr_string) 
    return final_attr_list
        
def generate_cnf_file(attr_dataframe, hard_constraints_file, cnf_txt_file): 
    """
    This function will generate .cnf file from the below inputs:
        1) attr_dataframe : Input attribute file converted to a pandas 
            dataframe
        2) hard_constraints_file : Input Hard constraints file using which 
            .cnf file will be created.
        3) cnf_txt_file : The name of the .cnf file.
    """
    constraints = []
#    print "generate_cnf_file > cnf_txt_file : ",cnf_txt_file
    clause_count = 0
    
    statinfo = os.stat(hard_constraints_file)
    statinfo.st_size
#    print"statinfo.st_size : ",statinfo.st_size
    
    if os.stat(hard_constraints_file).st_size == 0:
        with open(hard_constraints_file, mode = 'w+') as h_f:
            hc_file = h_f.read().strip()
#            print "hc_file", hc_file
#            print "There are no hard constraints defined."
            new_attr_df = attr_dataframe[1]+ " " + attr_dataframe[2].map(str)
#            print "new_attr_df", new_attr_df
            no_hc_data=""
            for attr in new_attr_df:
                no_hc_data = no_hc_data + attr + '\n'
#            print "no_hc_data : ",no_hc_data
            no_hc_data = no_hc_data.replace(" ", " OR ")
#            print "no_hc_data : ",no_hc_data    
            h_f.write(no_hc_data)
            h_f.close()

    with open(hard_constraints_file, mode = 'r') as h_f:
        
        hc_file = h_f.read().strip()
#        print "hc_file",hc_file
        for hc_constraint in hc_file.split('\n'):
#            print "hc_constraint",type(hc_constraint)
#            print "hc_constraint after split:", hc_constraint
            hc_constraint = re.sub(r"\bNOT\b", "-", hc_constraint)
            hc_constraint = re.sub(r"\bNot\b", "-", hc_constraint)
            hc_constraint = re.sub(r"\bnot\b", "-", hc_constraint)
            hc_constraint = re.sub(r"\bAND\b", "0\n", hc_constraint)
            hc_constraint = re.sub(r"\band\b", "0\n", hc_constraint)
            hc_constraint = re.sub(r"\bAnd\b", "0\n", hc_constraint)
            hc_constraint = re.sub(r"\bOR\b", " ", hc_constraint)       
            hc_constraint = re.sub(r"\bOr\b", " ", hc_constraint)       
       
#            print "hc_constraint after replace:", hc_constraint  
            hc_constraint = hc_constraint.split()
#            print "Now type of hc_constraint : ",type(hc_constraint)
            hc_constraint[:] = [x if x != '0' else '0\n' for x in hc_constraint]
#            print "hc_constraint: ",hc_constraint
            for hc_constraint_var in hc_constraint:
#                print "hc_constraint_var : ",hc_constraint_var
                if hc_constraint_var == '-' or hc_constraint_var == ' ' or hc_constraint_var == '0\n':
                    pass
                elif hc_constraint_var == '0':
                    pass
#                    print "hc_constraint_var: ",hc_constraint_var
                else:
                    attribute_value = get_attribute_value(hc_constraint_var,attr_dataframe)
#                    print "attribute_value before:" , attribute_value
                    attribute_value = str(attribute_value) + " "
#                    print "attribute_value after:" , attribute_value
                    if attribute_value == 9999:
                        return 9999
                    hc_constraint = [w.replace(hc_constraint_var, str(attribute_value)) for w in hc_constraint]
                
            hc_constraint.append(' 0\n')
            constraints.append(hc_constraint)
#            print "hc_constraint: ",hc_constraint
#            print "constraints : ",constraints
            clause_count += 1  
        h_f.close()
        
    global attribute_count
    with open(cnf_txt_file, mode = 'w+') as c_f:
        cnf_first_line = "p cnf " + str(attribute_count) + " " + str(clause_count) + "\n"
        c_f.write(cnf_first_line)
        for constraint_var in constraints:
            cnf_constraint =''
            for cnf_var in constraint_var:
                cnf_constraint = cnf_constraint + cnf_var
            cnf_constraint = cnf_constraint.replace('--','')
            c_f.write(cnf_constraint)
        c_f.close()
#    print "Its working till line 180"
    convert_txt_cnf(cnf_txt_file)
    return 1
    
def constraint_solver(cnf_file, output_file):
    '''
    This function will run the clasp in command prompt and save the output \
    a file. It will calculate the number of models and if its greater than
    zero, it will retrieve all the possible solutions.
    '''  
    if os.stat(cnf_file).st_size == 0:
        return 8888    
    satisfiable_models_list = []
    clasp_command = os.path.dirname(os.path.realpath(__file__)) + "\\clasp"
#    print "clasp_command",clasp_command
    command = [clasp_command, cnf_file,"-n","0"]
    with open(output_file, "w") as outfile:
        subprocess.call(command, stdout = outfile)
    subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    
    df_output = pd.read_csv(output_file)   
    models = str(df_output.iloc[-4])    
    final_models = models.split(':')
    total_model_count = final_models[1]
    total_model_count = total_model_count.replace("\nName","")
    total_model_count = total_model_count.strip()
    total_model_count = total_model_count.replace('+','')
    total_model_count = int(total_model_count)

    if total_model_count > 0:
        total_df_rows = len(df_output.index)
        for df_index in range(3, total_df_rows-6, 2):
            str_model = str(df_output.iloc[[df_index]])
            str_model = str_model.replace('c clasp version 3.3.2\n','')
            str_model = str_model.split('v ')
            str_model = str_model[1]
            str_model = str_model[:-1]    
            satisfiable_models_list.append(str_model)      
    else:
#        print "This problem cannot be solved!"
        empty_list = []
        return empty_list

    return satisfiable_models_list  

def order_preferences(preferences):   
    """
    This function will take input as the feasible models along with their
    associated penalty points and return a OrderedDict of models by penalty.
    """
    reordered_preferences = OrderedDict(sorted(preferences.items(), key = lambda t: t[1]))
    return reordered_preferences

def preference_solver(attribute_df, preferences_file, models_list):
    '''
    This function will read the preferences file and rearrange the feasible 
    models by preference.
    '''
#    print "preferences_file = ",preferences_file   
    preference_clause_count = 0
    preference_count = 0
    model_num = 0
    preference_models_dict = {}
    model_penalty = 0
#    print "Yes, I am working till here"
    with open(preferences_file, mode = 'r') as t_file:
        t_f = t_file.read().strip()     
        i = 1
        for preference in t_f.split('\n'):
            if preference == '':
                return []
            else:
#                print "preference at line 273 : ",preference
                preference = preference.split(',')
                preference_penalty = preference[1]
                preference = preference[0]
#                print "preference:",preference
#                print "preference_penalty: ",preference_penalty
                preference = re.sub(r"\bNOT\b", "-", preference)
#                preference = re.sub(r"\bNot\b", "-", preference)
#                preference = re.sub(r"\bnot\b", "-", preference)
                preference = re.sub(r"\bAND\b", "0\n", preference)
#                preference = re.sub(r"\band\b", "0\n", preference)
#                preference = re.sub(r"\bAnd\b", "0\n", preference)
                preference = re.sub(r"\bOR\b", " ", preference)       
#                preference = re.sub(r"\bOr\b", " ", preference)       
#                preference = re.sub(r"\bor\b", " ", preference)                           
#                print "preference:",preference
                
                
                
                
                
                
                for substring in preference.split():
#                    substring[:] = [x if x != '0' else '0\n' for x in substring]
                    if substring == '-' or substring == ' ' or substring == '0' or substring == '0\n':
                        pass
                    else:
#                        print "At line 302 - substring: ",substring
                        attribute_value = get_attribute_value(substring, attribute_df)
                        if attribute_value == 9999:
#                            print "Line 304 - attribute_value:", attribute_value
                            return 9999                    
                        preference = preference.replace(substring,str(attribute_value))
                     
                preference = preference + ' 0\n'
#                preference = preference.replace('--','')
                preference = preference.replace('- ','-')
                preference_clause_count = preference.count('0')
                preference_count = preference_count + 1
    
                global attribute_count
                clause_count = int(attribute_count) + int(preference_clause_count)   
                        
                for sat_models in models_list:
    
                    sat_model = sat_models.replace(' ',' 0\n')
                    model_num += 1            
                    preference_txt_file = "Preferences_p"+ str(preference_count) +"m" + str(model_num) +".txt"
                    preferences_output_file = "clasp_t_output_p"+ str(preference_count) +"m" + str(model_num) +".txt"
                    preference_clasp_files_list.append(preferences_output_file)
                    with open(preference_txt_file, mode = 'w+') as p_f:
                        p_cnf_first_line = "p cnf " + str(attribute_count) + " " + str(clause_count) + "\n"
                        p_f.write(p_cnf_first_line)
                        preference = preference.replace('--','')
                        p_f.write(preference)
                        p_f.write(sat_model)                
                    convert_txt_cnf(preference_txt_file)
                   
                    preference_cnf_file = preference_txt_file.split(".")[0]+".cnf"
                    preference_cnf_files_list.append(preference_cnf_file)
                    preference_sat_models = constraint_solver(preference_cnf_file,preferences_output_file)
#                    print "preference_sat_models : ",preference_sat_models

                    if len(preference_sat_models) > 0:
                        model_penalty = 0
                    else:
                        model_penalty = int(preference_penalty)
                    
                    if sat_models in preference_models_dict:
#                        print "Yes, this model already exists"
                        current_penalty = preference_models_dict.get(sat_models)
                        preference_models_dict[sat_models] = current_penalty + model_penalty
                    else: 
                        preference_models_dict[sat_models] = model_penalty
                    
                preference_clause_count = 0
                clause_count = 0
                model_num = 0
#                print "preference_models_dict : ",preference_models_dict
#                print "Yes, I am working till here - line 383"
                
            ordered_preferences = order_preferences(preference_models_dict)
            
#        print "Yes, I am working till here - line 385 - ordered_preferences", ordered_preferences
        
    return ordered_preferences

def preference_optimization(ordered_preferences_list,optimal_count):
    """
    This function takes feasible objects w.r.t. Hard constraints as input
    (ordered_preferences_list) and returns a optimal_list with all the optimal
    objects.
    """
    optimal_list = []    
    if len(ordered_preferences_list) == 0:
        return []
    
    lowest_penalty = ordered_preferences_list.items()[0][1]
#    print "lowest_penalty: ",lowest_penalty
    optimal_list.append(ordered_preferences_list.items()[0])

    for pref_index in range(1,len(ordered_preferences_list)):
        if ordered_preferences_list.items()[pref_index][1] > lowest_penalty:
#            print "All done!"
            break
        else:
            optimal_list.append(ordered_preferences_list.items()[pref_index])
    if str(optimal_count).upper() == "ALL":
        pass
#        print "Optimal list: ", optimal_list
    else:
        if int(optimal_count) > len(optimal_list):
            pass
#            print "The optimal list contains only", len(optimal_list) ,"elements"
#            print "Optimal list: ", optimal_list
        else:
            for i in range(int(optimal_count)):
                optimal_list = optimal_list[:int(optimal_count)]
#                print "Optimal list: ", optimal_list
    return optimal_list        

def get_feasible_objects():
    """
    This function will decide whether there are feasible objects w.r.t 
    Hard constraints.
    """
#    print "First line of get_feasible objects"
#    print "satisfiable_models : ", satisfiable_models
    feasible_objects = refresh_data()
    sat_model_attributes = convert_satisfiable_models(feasible_objects, attribute_dataframe) 
    
#    print "sat_model_attributes : ", sat_model_attributes, type(sat_model_attributes)
    answers_data.configure(state='normal')
    answers_data.delete(1.0, END)
    
    if len(sat_model_attributes) == 1:
        answers_data.insert(END, "There is only 1 model that satisfies the hard constraints.\nModel is:\n" + str(sat_model_attributes))
    elif len(sat_model_attributes) > 1:
        answers_data.insert(END, "There are " + str(len(sat_model_attributes)) + " models that satisy the hard constraints.\nModels are:\n" + str(sat_model_attributes))
    else:
        answers_data.insert(END, "There are no models that satisfy the hard constraints.")
        
    answers_data.configure(state='disabled')
    return

def get_optimal_object():
    """
    Optimization: This function will find an optimal object w.r.t preferences.
    """    
#    sorted_preferences = preference_solver(attribute_dataframe, preferences_file_path, satisfiable_models)
    attribute_dataframe = process_attributes(attribute_file_path)
    attribute_count = len(attribute_dataframe.index)
#    print "attribute_dataframe",attribute_dataframe
    generate_cnf_file(attribute_dataframe, hard_constraints_file_path, cnf_txt_file)
    satisfiable_models = constraint_solver(hard_constraints_cnffile,hard_constraint_output_file)
#    print "load_input_data > satisfiable_models: ", satisfiable_models
    sorted_preferences = preference_solver(attribute_dataframe, preferences_file_path, satisfiable_models) 

    if len(sorted_preferences) == 0:
        answers_data.configure(state='normal')
        answers_data.delete(1.0, END)
        answers_data.insert(END, "Either no preferences are specified or there are no feasible models. Please click feasible objects for more details. If feasible models exist, all models are equally preferred.")
    else:      
    
        optimized_list = preference_optimization(sorted_preferences,1)    
        new_optimized_list = []
        for each in optimized_list:
            new_optimized_list.append(each[0])
    
        sat_model_attributes = convert_satisfiable_models(new_optimized_list, attribute_dataframe) 
    
        answers_data.configure(state='normal')
        answers_data.delete(1.0, END)
        answers_data.insert(END, str(sat_model_attributes) + " is an optimal model.")
        
    answers_data.configure(state='disabled')
    return

def get_optimal_objects():    
    """
    Omni-optimization: This function will find all optimal objects 
    w.r.t preferences.
    """
    attribute_dataframe = process_attributes(attribute_file_path)
    attribute_count = len(attribute_dataframe.index)

    generate_cnf_file(attribute_dataframe, hard_constraints_file_path, cnf_txt_file)
    satisfiable_models = constraint_solver(hard_constraints_cnffile,hard_constraint_output_file)
#    print "load_input_data > satisfiable_models: ", satisfiable_models
    sorted_preferences = preference_solver(attribute_dataframe, preferences_file_path, satisfiable_models) 

    if len(sorted_preferences) == 0:
        answers_data.configure(state='normal')
        answers_data.delete(1.0, END)
        answers_data.insert(END, "Either no preferences are specified or there are no feasible models. Please click feasible objects for more details. If feasible models exist, all models are equally preferred.")
    else:
        optimized_list = preference_optimization(sorted_preferences,"ALL")
#        print "optimized_list",optimized_list, type(optimized_list)
        new_optimized_list = []
        for each in optimized_list:
            new_optimized_list.append(each[0])
            least_penalty = each[1]
#        print "new_optimized_list", new_optimized_list    
        sat_model_attributes = convert_satisfiable_models(new_optimized_list, attribute_dataframe) 
        
        answers_data.configure(state='normal')
        answers_data.delete(1.0, END)    
        if len(sat_model_attributes) == 1:
            answers_data.insert(END, "There is only 1 optimal model : " + str(sat_model_attributes))
        elif len(sat_model_attributes) > 1:
            answers_data.insert(END, "There are " + str(len(sat_model_attributes)) + " models that are optimal (with the same least penalty of " + str(least_penalty) +").\nModels are:\n" + str(sat_model_attributes))    
            
    answers_data.configure(state='disabled')
    return        

def Exemplification():
    """
    Exemplification : This function will generate two random feasible objects, 
    and show the preference between the two (strict preference or equivalence) 
    w.r.t T.
    """
    import random
    answers_data.configure(state='normal')
    attribute_dataframe = process_attributes(attribute_file_path)
    attribute_count = len(attribute_dataframe.index)
    generate_cnf_file(attribute_dataframe, hard_constraints_file_path, cnf_txt_file)
    satisfiable_models = constraint_solver(hard_constraints_cnffile,hard_constraint_output_file)
#    print "load_input_data > satisfiable_models: ", satisfiable_models
    sorted_preferences = preference_solver(attribute_dataframe, preferences_file_path, satisfiable_models) 
#    print "sorted_preferences",sorted_preferences, type(sorted_preferences)
    
    if len(sorted_preferences) == 0:
        answers_data.configure(state='normal')
        answers_data.delete(1.0, END)
        answers_data.insert(END, "Either no preferences are specified or there are no feasible models. Please click feasible objects for more details. If feasible models exist, all models are equally preferred.")
    else:
        answers_data.configure(state='normal')
        answers_data.delete(1.0, END) 
        
        if len(sorted_preferences) < 2:
            answers_data.insert(END,"Since there is only one feasible object for the hard constraints specified, comparison cannot be done.")
        else: 
            exem_models = list((k, sorted_preferences[k]) for k in random.sample(sorted_preferences, 2))
        
#            print "Two models ",exem_models," were randomly picked from the feasible objects."
        
            new_exem_models = []
            for each in exem_models:
                new_exem_models.append(each[0])
                
#            print "New models: ", new_exem_models
            exem_models_name = convert_satisfiable_models(new_exem_models, attribute_dataframe) 
        
#            print "Two models ",exem_models_name," were randomly picked from the feasible objects."
        
            if int(exem_models[0][1]) == int(exem_models[1][1]):
#                print "Both these items are equally prefered."
                answers_data.insert(END, "Two models "+ str(exem_models_name) + " were randomly picked from the feasible objects.\nBoth these items are equally prefered.")
            elif int(exem_models[0][1]) > int(exem_models[1][1]):
#                print exem_models_name[1], "is strictly prefered over", exem_models_name[0]
                answers_data.insert(END, "Two models " + str(exem_models_name) + " were randomly picked from the feasible objects.\n" + str(exem_models_name[1])+ " is strictly prefered over " + str(exem_models_name[0]))
            elif int(exem_models[1][1]) > int(exem_models[0][1]):        
#                print exem_models_name[0], "is strictly prefered over", exem_models_name[1]    
                answers_data.insert(END, "Two models " + str(exem_models_name) + " were randomly picked from the feasible objects.\n" + str(exem_models_name[0])+ " is strictly prefered over " + str(exem_models_name[1]))
        
    answers_data.configure(state='disabled')
    return     



def import_attributes():
    """
    This function will read data from the Attributes file and display it 
    on the screen.
    """      
    f = open(attribute_file_path)
    attributes_text.delete(1.0, END)    
    attributes_string = ""    
    for i in f:
        attributes_string += i        
    attributes_text.insert(END, attributes_string)
    f.close()
    return
    
def import_hard_constraints():
    """
    This function will read data from Hard Constraints file and display it 
    on the screen.
    """    
    dir_path = os.path.dirname(os.path.realpath(__file__))
#    print "dir_path: ",dir_path
    hc_file = dir_path + "\\" + hard_constraints_file_path
#    print "hc_file", hc_file
    hc_file_copy = dir_path + "\\" + hard_constraints_file_copy
#    print "hc_file_copy", hc_file_copy
    
    shutil.copy2(hc_file, hc_file_copy)
#    print "File has been copied!"
    f = open(hard_constraints_file_path)
    hard_constraints_text.delete(1.0, END)
    attributes_string = ""
    for i in f:
        attributes_string += i        
    hard_constraints_text.insert(END, attributes_string)
    f.close()
    return

def import_preferences():
    """
    This function will read data from Preferences file and display it on the 
    screen.
    """
    f = open(preferences_file_path)
    preferences_text.delete(1.0, END)
    attributes_string = ""
    for i in f:
        attributes_string += i
        
    preferences_text.insert(END, attributes_string)
    f.close() 
    return

def openFiles(selection):
    """
    This function will call import file functions depending on the value 
    passed in the selection parameter.
    """
    if selection == "Attributes":
        import_attributes()
    elif selection == "Hard Constraints":
        import_hard_constraints()
    elif selection == "Preferences":
        import_preferences()
    return

def save_attributes():
    """
    This function will update the Attributes file with the data entered on the
    app.
    """
#    attributes_save_result = tkinter.messagebox.askyesno("Attributes data","Have you updated or deleted an attribute that still exists in the Hard constraints or Preferences file?")

    updated_data = attributes_text.get(1.0, END)
    outToFile = open(attribute_file_path, 'w')
    outToFile.write(updated_data.strip())
    outToFile.close()
    attributes_updated = True

#    if attributes_save_result == True:
#        tkinter.messagebox.showerror("Error","Please update the relevant data in Hard constraints and Preferences file before updating here.")
#    else:
#        updated_data = attributes_text.get(1.0, END)
#        outToFile = open(attribute_file_path, 'w')
#        outToFile.write(updated_data.strip())
#        outToFile.close()
#    attributes_updated = True    
    
    return
    
def save_hardconstraints():
    """
    This function will update the Hard constraints file with the data entered 
    on the app.
    """
    updated_data = hard_constraints_text.get(1.0, END)    
    if os.stat(hard_constraints_file_path).st_size == 0:
        return 8888    
    with open(hard_constraints_file_path, 'w') as outToFile:
        outToFile.write(updated_data.strip())
        outToFile.close()        
    gen_cnf_return = generate_cnf_file(attribute_dataframe, hard_constraints_file_path, cnf_txt_file)
#    print "gen_cnf_return : ", gen_cnf_return
    if gen_cnf_return == 9999:
        tkinter.messagebox.showerror("Invalid Attribute value", "You entered an incorrect attribute value for the hard constraints. Please correct and retry.")
        with open(hard_constraints_file_copy) as revertChanges:
            hard_constraints_text.delete(1.0, END)
            attributes_string = ""
            for i in revertChanges:
                attributes_string += i    
            hard_constraints_text.insert(END, attributes_string)
            revertChanges.close()
        shutil.copy2(hard_constraints_file_copy, hard_constraints_file_path)
    hard_constraints_updated = True
    return

def save_preferences():
    """
    This function will update the Preferences file with the data entered 
    on the app.
    """
    if os.stat(preferences_file_path).st_size == 0:
        return 8888      
    updated_p_data = preferences_text.get(1.0, END)        
    with open(preferences_file_path, 'w') as outToPFile:
        outToPFile.write(updated_p_data.strip())
        outToPFile.close()        
    sorted_preferences = preference_solver(attribute_dataframe, preferences_file_path, satisfiable_models)
#    print "sorted_preferences : ", sorted_preferences
    if sorted_preferences == 9999:
        tkinter.messagebox.showerror("Invalid Attribute value", "You entered an incorrect attribute value for the preferences. Please correct and retry.")        
        with open(preferences_file_copy) as revert_p_Changes:
            preferences_text.delete(1.0, END)
            attributes_string = ""
            for i in revert_p_Changes:
                attributes_string += i    
            preferences_text.insert(END, attributes_string)
            revert_p_Changes.close()  
        shutil.copy2(preferences_file_copy, preferences_file_path)                
    preferences_updated = True
    return

def refresh_data():
    """
    This function will take the updated input data and recompute cnf files for
    both hard constraints and preferences.
    """
    global attribute_count
    attribute_dataframe = process_attributes(attribute_file_path)
    attribute_count = len(attribute_dataframe.index)
#    print "attribute_dataframe",attribute_dataframe
    generate_cnf_file(attribute_dataframe, hard_constraints_file_path, cnf_txt_file)
    satisfiable_models = constraint_solver(hard_constraints_cnffile,hard_constraint_output_file)
#    print "load_input_data > satisfiable_models: ", satisfiable_models
    sorted_preferences = preference_solver(attribute_dataframe, preferences_file_path, satisfiable_models) 
    return satisfiable_models

def delete_temp_files():
    """
    This function will delete all the temp files created during the run.
    """
    if os.path.exists(cnf_txt_file):
        os.remove(cnf_txt_file)
    if os.path.exists(hard_constraints_cnffile):
            os.remove(hard_constraints_cnffile)
    if os.path.exists(hard_constraint_output_file):
            os.remove(hard_constraint_output_file)
    if os.path.exists(hard_constraints_file_copy):
            os.remove(hard_constraints_file_copy)
    if os.path.exists(preferences_file_copy):
            os.remove(preferences_file_copy)
            
    for pref_file in preference_clasp_files_list:
        if os.path.exists(pref_file):
                os.remove(pref_file)
    for prefc_file in preference_cnf_files_list:
        if os.path.exists(prefc_file):
                os.remove(prefc_file)
           
def about_Me():
    """
    This function will read the README file and display the content of this 
    for on the app.
    """
    f = open(read_me_file)
    answers_data.delete(1.0, END)
    readme_string = ""   
    for i in f:
        readme_string += i
    answers_data.insert(END, readme_string)
    f.close() 
    return    
    
def on_closing():
    """
    This function will quit the app. delete_temp_files() function will 
    delete all the temp files created during the run.
    """
    delete_temp_files()
    app.destroy()

def attr_text_save(event):
    a_save.config(state="normal")
    h_save.config(state="disabled")
    t_save.config(state="disabled")

def hc_text_save(event):
    a_save.config(state="disabled")
    h_save.config(state="normal")
    t_save.config(state="disabled")    
    
def pref_text_save(event):
    a_save.config(state="disabled")
    h_save.config(state="disabled")
    t_save.config(state="normal")  
    
def disable_save_buttons(event):
    a_save.config(state="disabled")
    h_save.config(state="disabled")
    t_save.config(state="disabled") 

#def main():

attribute_dataframe = process_attributes(attribute_file_path)
attribute_count = len(attribute_dataframe.index)
generate_cnf_file(attribute_dataframe, hard_constraints_file_path, cnf_txt_file)
satisfiable_models = constraint_solver(hard_constraints_cnffile,hard_constraint_output_file)
sorted_preferences = preference_solver(attribute_dataframe, preferences_file_path, satisfiable_models)
#    print "At start sorted_preferences:", sorted_preferences

app = Tk()
app.title("Preference solver")
app.geometry('950x450+300+300')

menubar = Menu(app)
filemenu = Menu(menubar, tearoff = 0)
filemenu.add_command(label = "Import Attributes", command = import_attributes)
filemenu.add_command(label = "Import Hard constraints", command = import_hard_constraints)
filemenu.add_command(label = "Import Preferences", command = import_preferences)
filemenu.add_separator()
filemenu.add_command(label = "Quit", command = on_closing)#app.quit#app.destroy
menubar.add_cascade(label = "File", menu = filemenu)

helpmenu = Menu(menubar, tearoff = 0)
helpmenu.add_cascade(label = "About preference solver", command = about_Me)
menubar.add_cascade(label = "Help", menu = helpmenu)

app.config(menu = menubar)

attributes_text = Text(app, wrap=WORD, width = 45, height = 10)
attributes_text.insert(END, "Select Attributes data from File > Import.\nThanks!")
attributes_text.place(relx=0.0, rely=0.2, anchor=W)
attributes_text.bind("<Key>", attr_text_save)
attributes_text.bind("<FocusIn>", attr_text_save)

hard_constraints_text = Text(app, wrap=WORD, width = 45, height = 10)
hard_constraints_text.insert(END, "Select Hard constraints data from File > Import.\nThanks!")
hard_constraints_text.place(relx=0.0, rely=0.5, anchor=W)
hard_constraints_text.bind("<FocusIn>", hc_text_save)

preferences_text = Text(app, wrap=WORD, width = 45, height = 10)
preferences_text.insert(END, "Select Preferences data from File > Import.\nThanks!")
preferences_text.place(relx=0.0, rely=0.8, anchor=W)
preferences_text.bind("<FocusIn>", pref_text_save)

answers_data = Text(app, wrap=WORD, width = 45, height = 27)
answers_data.insert(END, "Answers to the four questions will be displayed here.\nThanks!")
answers_data.place(relx=1.0, rely=0.5, anchor=E)

a_save = Button(app, text = "<- Save Attributes", state=DISABLED, width = 25, command = save_attributes)
a_save.place(relx=0.5, rely=0.2, anchor=CENTER)

h_save = Button(app, text = "<- Save Hard Constraints", state=DISABLED, width = 25, command = save_hardconstraints)
h_save.place(relx=0.5, rely=0.3, anchor=CENTER)

t_save = Button(app, text = "<- Save Preferences", state=DISABLED, width = 25, command = save_preferences)
t_save.place(relx=0.5, rely=0.4, anchor=CENTER)

button_q1 = Button(app, text="1) Feasible objects ->", width = 25, command = get_feasible_objects)
button_q1.place(relx=0.5, rely=0.5, anchor=CENTER)

button_q2 = Button(app, text="2) Exemplification ->", width = 25, command = Exemplification)
button_q2.place(relx=0.5, rely=0.6, anchor=CENTER)

button_q3 = Button(app, text="3) Optimization ->", width = 25, command = get_optimal_object)
button_q3.place(relx=0.5, rely=0.7, anchor=CENTER)

button_q4 = Button(app, text="4) Omni-optimization ->", width = 25, command = get_optimal_objects)
button_q4.place(relx=0.5, rely=0.8, anchor=CENTER)

app.protocol("WM_DELETE_WINDOW", on_closing)
app.mainloop()

#if __name__ == "__main__":
#    main()  # Calling the main method