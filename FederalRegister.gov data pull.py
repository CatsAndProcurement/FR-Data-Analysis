# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 18:05:21 2020

@author: CatsAndProcurement

The purpose of the script is to 
download a user-defined dataset via the 
Federal Register (FR) web API, then 
aggregate and display the data using Pandas.

The FR is the official daily journal of 
the US government; it notifies the public of 
proposed and final changes to federal government 
regulations, among other matters.

A web application program interface (API) 
allows access to FR datasets.

Here's a sample FR web API call:
https://www.federalregister.gov/documents/search?
format=csv&
conditions%5Bpublication_date%5D%5Bgte%5D=1%2F1%2F2017&
conditions%5Bpublication_date%5D%5Blte%5D=12%2F31%2F2019&
conditions%5Bterm%5D=%22Federal+Acquisition+Regulation%22&
conditions%5Btype%5D%5B%5D=RULE&
conditions%5Btype%5D%5B%5D=PRORULE&
conditions%5Btype%5D%5B%5D=NOTICE

"""

# Pandas lets us do fancy calculations
import pandas as pd
# Datetime lets us convert date strings into integers
import datetime as dt

# Laying out for the user what the code is supposed to do
print("\n"
      "Hi! This Python script will extract data from the FederalRegister.gov"
      " site jointly run by National Archives and Records Administration (NARA),"
      " and the U.S. Government Publishing Office (GPO).\n"
      "It will pull data on final rules, proposed rules, and notices that"
      " pertain to the Federal Acquisition Regulation (CFR Title 48) or "
      "agency-level equivalents and illustrate them by month.\n"
      "Then it'll use Pandas (a Python module for data analysis) to"
      " calculate totals based on year and month.\n"
      "WARNING: There's a max of 1,000 records, so if your search applies to"
      " more than that, the data will be incomplete."
      "\n\n")

# Asks user for a starting date, with a loop to verify it's a valid date
while True:
    try:
        # This asks the user for a start date
        fromDate = input("Extract data from date (MM/DD/YYYY): ")
        # Breaks apart data into month, day, year
        fromMonth,fromDay,fromYear = fromDate.split("/")
        # Forces an error to occur if the date isn't valid
        dt.datetime(int(fromYear),int(fromMonth),int(fromDay))
    except ValueError:
        # Lets user know they screwed up
        print("Sorry, that date format wasn't clear. "
              "Can you please enter it again?")
        # Returns to the start of the loop
        continue
    else:
        # Exits the loop if the date is not invalid
        break

# Asks user for an ending date, with a loop to verify it's a valid date
while True:
    try:
        # This asks the user for an end date
        tillDate = input("Extract data until date (MM/DD/YYYY): ")
        # Breaks apart data into month, day, year
        tillMonth,tillDay,tillYear = tillDate.split("/")
        # Forces an error to occur if the date isn't valid
        dt.datetime(int(tillYear),int(tillMonth),int(tillDay))
    except ValueError:
        # Lets user know they screwed up
        print("Sorry, that date format wasn't clear. "
              "Can you please enter it again?")
        # Returns to the start of the loop
        continue
    else:
        # Exits the loop if the date is not invalid
        break

# Here's some code to specify the string variable we want to search for
# (This is currently hardcoded for simplicity's sake)
callTerm = "Federal Acquisition Regulation"
# Replaces spaces with plus signs in accordance with FR web API requirements
callTerm = callTerm.replace(" ","+")

# Code to specify type(s) of FR notice
# (final rules and proposed rules currently hardcoded, for simplicity)
callType1 = "RULE"
callType2 = "PRORULE"
# The following API call parameter is disabled by default, see the API call code 
# for details on what will be added to queries if it's enabled
callType3 = "NOTICE"

# Code to build web API call:
callURL = ("https://www.federalregister.gov/documents/search?"
           +"format=csv"
           +"&conditions%5Bpublication_date%5D%5Bgte%5D="
           +fromMonth+"%2F"+fromDay+"%2F"+fromYear
           +"&conditions%5Bpublication_date%5D%5Blte%5D="
           +tillMonth+"%2F"+tillDay+"%2F"+tillYear
           +"&conditions%5Bterm%5D=%22"+callTerm+"%22"
           +"&conditions%5Btype%5D%5B%5D="+callType1
           +"&conditions%5Btype%5D%5B%5D="+callType2
           # This API call parameter is disabled by default; if enabled it'll add 
           # all FR notices to the query, not just final and proposed rules
           # This will include stuff like requests for comment, requests for 
           # information, announcement of public meetings, et cetera
           #+"&conditions%5Btype%5D%5B%5D="+callType3
           )

# Lets user know where we're pulling their data from
print("\nAccessing data from: \n" + callURL)

# OK, now we pull the data from the website into a Pandas dataframe
dfFR = pd.read_csv(callURL)
# And print out the column headers so we can see the data we're working with
print(dfFR.columns)
# Print out the publication date data so we can see the data structure
print(dfFR["publication_date"])

# Now we'll create two new columns of data for the year and month
# (based on the FR web API's 'publication_date' format of '09/30/2019')
# (also converts the values into numeric instead of strings)
dfFR["Year"] = pd.to_numeric(dfFR["publication_date"].str[-4:])
dfFR["Month"] = pd.to_numeric(dfFR["publication_date"].str[:2])

# And a basic, hardcoded column to reliably count each FR notice
dfFR["Number of Notices"] = 1

# Create a column for YYYY-MM
dfFR["Year and Month"] = dfFR["Year"].astype(str).str.rjust(4,"0") + "-" + dfFR["Month"].astype(str).str.rjust(2,"0")
print(dfFR["Year and Month"])

# Creates a new dataframe with only lowest available year
dfFRmin = dfFR[dfFR.Year == dfFR["Year"].min()].reset_index(drop=True)
# Creates dataframe with only highest available year
dfFRmax = dfFR[dfFR.Year == dfFR["Year"].max()].reset_index(drop=True)
# Stores the highest and lowest year/month information
minYear = dfFR["Year"].min()
minMonth = dfFRmin["Month"].min()
maxYear = dfFR["Year"].max()
maxMonth = dfFRmax["Month"].max()

# Summarizes data pull in English
print("\nCalculations based on FR notices published from "+fromDate+" to "+
      tillDate+".")

# Creates a new dataframe that we'll use to chart the FR notices for each
# YYYY-MM in the date range specified by the user
dfFRPvt = pd.DataFrame(columns=("Year and Month","Number of FR Notices"))

# This loop cycles through each YYYY-MM combination from min to max
# It creates a new dataframe, adding the sum from each possible YYYY-MM
for y in range (minYear,maxYear+1):
    # If y is the initial year, starts the annual loop on selected month
    if y == minYear:
        startMonth = minMonth
    # If y isn't the initial year, starts the annual loop in January
    else:
        startMonth = 1
    # If y is the final year, ends the annual loop on selected month
    if y == maxYear:
        endMonth = maxMonth
    # If y isn't the final year, ends the annual loop in December
    else:
        endMonth = 12
    # Annual loop that cycles through each month in each year
    for m in range (startMonth,endMonth+1):
        # Creates variable for every YYYY-MM in the target range
        loopYearMonth = str("%04d" % y) + "-" + str("%02d" % m)
        # Counts the notices for each YYYY-MM variable in the dfFR dataframe
        sumYearMonth = dfFR.loc[dfFR["Year and Month"] == loopYearMonth,
                                "Number of Notices"].sum()
        # Creates a new row to add to the pivot dataframe
        appendRow = {"Year and Month":loopYearMonth,"Number of FR Notices":sumYearMonth}
        # Adds the new row to the pivot dataframe
        dfFRPvt = dfFRPvt.append(appendRow,ignore_index=True)

# Brief description of the chart we're going to create
print("\nThe following chart displays Federal Register (FR) proposed rule and final "+
      "rulemaking notices related to the Federal Acquisition Regulation (FAR) or "+
      "agency-level equivalents.\n")
# Creates a pandas bar chart to visualize FR notices over time
dfFRPvt.plot.bar(x="Year and Month",
                 y="Number of FR Notices",
                 title=("Federal Register notices, by year and month"),
                 figsize=(10,6))



