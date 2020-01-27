Knowledge-based intelligent system:
	This is a knowledge-based intelligent system that collects user preferences and reasons about them. 
	This system provides information about the feasible models based on user input.
	This system also recommends the optimal model based on user preferences.

Getting Started:
	Download the "Project3" folder to a local drive. 
	
	This folder has 
	1) Three .txt files (A.txt for Attributes, H.txt for Hard constraints, T.txt for Preference information) - These files can be edited and saved to provide input application using these files.
	2) clasp.exe - A SAT solver that is used by the application to compute feasible objects for hard constraints and for checking if a truth assignment satisfies a formula. 
	3) 'N01412075_Project_3.py' - A file that contains the source code for the application.

Below are few important things to note before using the application:


	1) The three input files for Attributes (A.txt), Hard constraints (H.txt) and Preferences (T.txt) should always be present in the same directory as source code.
	2) Do not edit the source code except for line numbers 18, 19, 20 wherein you can change the file names of the input files (make sure you place these files in the same directory as the source code) you want the program to read. 
		23 > attribute_file_path = "A.txt"
		24 > hard_constraints_file_path = "H.txt"
		25 > preferences_file_path = "T.txt"
	3) Use only upper case logical operators (OR, AND, NOT) in the H.txt or T.txt files and when editing the Hard constraints or Preferences through GUI 
	4) If the logical operators (OR, AND, NOT) are present as part of attribute values, user camel case or lower care for such attributes (example - "Orange" or "orange")
	5) The values input into Hard constraints and Preferences should be present in Attributes. There will be errors if there are any new values in Hard constraints and Preferences that are not present in Attributes.
	6) Add/Edit/Update Attributes first before updating Hard constraints and Preferences.
	7) Hard constraints and Preferences cannot be empty or blank. Atleast one constraint is required for each.
	8) If there are any unforseen errors, please quit program and re-open. If it does not work, please kill process and re-open.
	9) If the updates from GUI fails, use the import files to add/update data, import and check results

Pre-requisites:

	1) Python 2.7 should be installed on the system on which the application will be used

Running the tests:

	1) Execute the 'Project_3.py' file. It should open a GUI that will enable you to:
	a) Import Attributes, Hard constraints and Preferences data from files using the menu option. This feature imports the data files from the source directory. You can either edit the data from GUI or update the files directly.
	b) Add/update/delete Attributes, Hard constraints and Preferences data from GUI and save the data.
	c) Find if there are feasible objects for the hard constraints defined.
	d) Randomly compare two feasible objects and show the preference between the two.
	e) Find an optimal object w.r.t. preferences specified.
	f) Find all optimal objects w.r.t. preferences specified. 
