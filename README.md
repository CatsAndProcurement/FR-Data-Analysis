# FR-Data-Analysis
Python script to analyze data on federal acquisition rulemaking from FederalRegister.gov

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
