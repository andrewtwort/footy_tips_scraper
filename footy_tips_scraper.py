# import packages
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import tkinter as tk
import os
import numpy as np
import pandas as pd
import csv

# Key parameters to direct to the correct webpage (these can be found in the url for your competition)
competitionId = "######"
CompId = "######"

# Set the working directory
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

# Define GUI form
def return_entry_fields(event=None):
	''' Create simple GUI form with three user fields '''
	entry_array = [e1.get(),e2.get(),e3.get()]
	form.quit()
	return entry_array

# Create the form incl. AFL icon 
form = tk.Tk()
form.bind('<Return>', return_entry_fields)
form.title("Footy Tips Scraper")
form.iconbitmap("afl.ico")
form.minsize(350,130)
form.geometry("350x130")

# User form fields
tk.Label(form, text="Username",width = 10).grid(row=0, pady=5, padx = 5)
tk.Label(form, text="Password",width = 10).grid(row=1, pady=5, padx = 5)
tk.Label(form, text="Round",width = 10).grid(row=2, pady=5, padx = 5)

e1 = tk.Entry(form,width = 30)
e2 = tk.Entry(form,width = 30, show="*") # Do not display password in plain text within GUI
e3 = tk.Entry(form,width = 30)

# Placeholder values for ease of entry
e1.insert(0, "username@email.com")
e2.insert(0, "plain_text_password_lolz")
e3.insert(0, "1")

e1.grid(row=0, column=1)
e2.grid(row=1, column=1)
e3.grid(row=2, column=1)

# Bind the enter button and actions
button = tk.Button(form, text="Enter", command=return_entry_fields).grid(row=1, column=3, sticky=tk.W, pady=5, padx=5)

tk.mainloop()

my_results = return_entry_fields()

# Load the webscraper incl. base parameters
login_address = "http://www.footytips.com.au/home"
me_login = my_results[0] # from user form
me_password = my_results[1] # from user form

# Check that user form parameters are not empty
if (me_login.__len__() == 0) or (me_password.__len__() == 0):
	print("Details are missing.\nExiting programme.")
	quit()

# Initiate Chrome instance
browser = webdriver.Chrome()
browser.get(login_address)
print("Loading Chrome: ",login_address)

try:
	# Search for page fields
	login_field = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH,"//div[@class='login-form']//input[@id='ft_username']")))
	password_field = browser.find_element_by_xpath("//div[@class='login-form']//input[@id='ft_password']")
	print("Login fields found")

	# Enter user parameters and ENTER key to submit data
	login_field.send_keys(me_login)
	password_field.send_keys(me_password)
	password_field.send_keys(u'\ue007')
	print("Entered login data")
 
except:
	print("Unable to login. Check user details or page fields.")
	quit()

# Validate round input
round = my_results[2]
while not round:
	try:
		round = int(input("Select round: "))
	except ValueError:
		print("Invalid round")

print("Loading data page")

# Launch browser with complete URL
info_address = "https://www.footytips.com.au/competitions/afl/ladders/?competitionId="+competitionId+"&round="+str(round)+"&view=ladderTips&gameCompId="+CompId
browser.get(info_address)

try: 
	login_field = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH,"//div[@class='pull-right site-ladder-search']//input[@id='quickFindText']")))
	print("Found text on page")
	data_table = browser.find_element_by_xpath("//div[@class='scrollable']//table[@class='table ladder-main table-horizontal ladder-mini comps-ladder scrollable-table ng-scope who-tipped-what']")
	print("Found data table on page")

	results_headers = []
	results_body = []

	for x in data_table.find_elements_by_xpath('.//th'):
		results_headers.append(x.text.replace('\n',''))
		print(x.text)

	for y in data_table.find_elements_by_xpath('.//tr'):
		results_holder = y.text.split('\n')
		results_body.append(results_holder)
	# Remove poorly formatted header row
	results_body.pop(0)

except:
	print("Unable to locate table. Please check url parameters or try again")
	exit()

# Create pandas dataframe
out = pd.DataFrame(results_body,columns=results_headers[:])

# Format some of the output columns and split data
round_text = 'ROUND '+str(my_results[2])
out['Round_Score'], out['Round_Margin'] = out[round_text].str.split(' ', 1).str
out['Total_Score'], out['Total_Margin'] = out['TOTAL SCORE'].str.split(' ', 1).str
out['Round'] = str(my_results[2])
out.columns.values[0] = 'Round_Ranking' 

# Ensure margin values are able to be parsed as numberic values
for x in ['Round_Margin','Total_Margin']:
	out[x] = out[x].str.replace("(","")
	out[x] = out[x].str.replace(")","")
out.rename(columns={'TIPPER': 'Tipper'}, inplace=True)

# Drop some redundant columns
out.drop(['TOTAL SCORE', round_text], axis=1, inplace=True)

# Create long dataset with every tip in it (to be added to tips master file)
out2 = out.drop(['Round_Ranking', 'Round_Margin', 'Round_Score', 'Total_Score', 'Total_Margin'], axis=1)
out2 = pd.melt(out2, id_vars=['Tipper', 'Round'], var_name='Game', value_name='Result')
out2['GameID'] = "Round "+str(my_results[2])+"-"+out2['Game']

# Create leaderboard summary (to be added to leaderboard master file), need to watch out for bye rounds (e.g. rounds with less than 9 games played)
if len(out.columns) > 13:
	dropcols = [2,3,4,5,6,7,8,9,10]
	out3 = out.drop(out.columns[dropcols], axis=1)

else:
	dropcols = [2,3,4,5,6,7]
	out3 = out.drop(out.columns[dropcols], axis=1)

print("Preparing to export data")

# Check for/ create output file
def check_file_exists(filename, header_row_array):
	''' Check if output file exists and if not, creates the file including given column headers '''
	if os.path.isfile(filename) == False:
		with open(filename, 'w', newline='') as newcsv:
		    filewriter = csv.writer(newcsv, delimiter=',')
		    filewriter.writerow(header_row_array)
		    newcsv.close()

# Export data
def append_data(filename, dataframe, success_msg, fail_msg):
	''' Appends data from the dataframe to the master file except where data from that round already exists '''
	with open(filename, 'r') as f:
		csvreader = csv.reader(f, delimiter=",")
		printer = 0
		# Check if round data already exists, if yes then do not append data again
		row_count = sum(1 for row in csvreader)
		if row_count == 1: # check if file only has header row
			pass
		else:
			for row in csvreader: # iterate through existing data to check if it already includes the selected round
				if round in row[1]:
					printer += 1
		f.close()
		if printer == 0:
			dataframe.to_csv(filename, sep=',', encoding='utf-8', index=False, header=False, mode='a')
			print(success_msg)
		else:
			print(fail_msg)


# Export round data to consolidated tip master file
filename = '2019 FT Tips Master.csv'
header_row_array = ['Tipper', 'Round', 'Game', 'Result', 'GameID']
check_file_exists(filename, header_row_array)

dataframe = out2
success_msg = "\nAppended round data in tips master file."
fail_msg = "\nFailed to append data into tips master file. Data for round already exists."
append_data(filename, dataframe, success_msg, fail_msg)

# Export round data to consolidated leaderboard master file
filename = '2019 FT Leaderboard Master.csv'
header_row_array = ['Round_Ranking','Tipper','Round_Score','Round_Margin','Total_Score', 'Total_Margin', 'Round']
check_file_exists(filename, header_row_array)

dataframe = out3
success_msg = "\nAppended round data in leaderboard master file."
fail_msg = "\nFailed to append data into leaderboard master file. Data for round already exists."
append_data(filename, dataframe, success_msg, fail_msg)

# Close browser
browser.quit()
quit()