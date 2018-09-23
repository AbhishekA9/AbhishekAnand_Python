#Program Name :  eod_positions.py
#Description  :  Finds the EOD positions of accounts along with Delta
#Author       :  Abhishek Anand
#Date         :  23 Sep 2018


import csv
import json
import os
import pandas as pd

print("Loading os module in python.....")
print("Loading pandas module in python.....")
#get current working directory
cwd=os.getcwd()


#function to read Begin of Day positions file, returns begin of day postions as dictionary

def read_sod_file(filename):
    sod_positions=[]
    with open(filename,"rb") as input_file:
        r=csv.DictReader(input_file)
        for line in r:
            sod_positions.append(line)
    return sod_positions

#function to read transactions file , returns transction data as dictionary
def read_transact_file(filename):
    f=open(filename)
    s=f.read()
    #Load the transactions in dictionary
    transactions_input = json.loads(s)
    return transactions_input

#function to calculate EOD positions, returns eod postions as dictionary

def calc_eod_position(sod_positions,transactions_input):
    for transaction in transactions_input:
        for position in sod_positions:
            if transaction['Instrument'] == position['Instrument']:
                if transaction['TransactionType'] =='B':
                    if position['AccountType'] == 'E':
                        (position['Quantity']) = str(int(transaction['TransactionQuantity']) + int(position['Quantity']))
                    else:
                        (position['Quantity']) = str(int(position['Quantity'])-int(transaction['TransactionQuantity']))
                else:
                    if position['AccountType'] == 'E':
                        (position['Quantity']) = str(int(position['Quantity']) - int(transaction['TransactionQuantity']))
                    else:
                        (position['Quantity']) = str(int(transaction['TransactionQuantity']) + int(position['Quantity']))
    return sod_positions

#function to wrie eod position text file

def write_eod_file(filename,eod_dict):
    keys= ['Instrument','Account','AccountType','Quantity','Delta']
    with open(filename,"wb") as output_file:
        dict_writer= csv.DictWriter(output_file,keys)
        dict_writer.writeheader()
        dict_writer.writerows(eod_dict)

#function to find delta, returns eod positions dictonary with delta
def find_delta(sod_positions,eod_positions):
    for sod_position in sod_positions:
        for eod_position in eod_positions:
            if ( sod_position['Instrument'] == eod_position['Instrument'] and sod_position['Account'] == eod_position['Account']
                 and sod_position['AccountType'] == eod_position['AccountType']):
                eod_position['Delta'] = str(int(eod_position['Quantity']) - int(sod_position['Quantity']))
    return eod_positions

#function to find the instrument with max transaction volume
def find_max_vol(eod_positions_delta):
    df=pd.DataFrame(eod_positions_delta)
    df=df.apply(pd.to_numeric,errors='ignore')
    df['Delta'] = df['Delta'].abs()
    i= df['Delta'].idxmax()
    print ("Instrument with higest net volume is:"),(df.loc[i,'Instrument'])
    j= df['Delta'].idxmin()
    print ("Instrument with lowest net volume is:"),(df.loc[j,'Instrument'])
    
    
    
    
    
    
    

try:
    sod_positions = read_sod_file("Input_StartOfDay_Positions.txt")
    transactions_input = read_transact_file("1537277231233_Input_Transactions.txt")
    eod_positions = calc_eod_position(sod_positions,transactions_input)
    sod_positions = read_sod_file("Input_StartOfDay_Positions.txt")
    eod_positions_delta = find_delta(sod_positions,eod_positions)
    write_eod_file("EndOfDay_Positions.txt",eod_positions_delta)
    find_max_vol(eod_positions_delta)
    
    print("Process completed Successfully!")
except IOError:
    print("Sorry File Not Found!Check if input files are present in "),cwd
except Exception:
    print("Something went wrong, please contact admin!")



    

    


 





                    
