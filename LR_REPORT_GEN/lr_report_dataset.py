import sys
import json

from pyathena import connect
from datetime import datetime as DT

from lr_report_classes import LR_Report, Transaction

try:
  with open("aws_data.json") as in_file:
      aws_data = json.load(in_file)
except FileNotFoundError:
    print("JSON File: 'aws_data.json' Not Found")
    exit(1)   


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
colors = ['deeppink', 'deepskyblue', 'green', 'darksalmon', 'mediumpurple', 'darkgreen', 'darkorange', 'darkblue']
LRLC ='black'
clrStrt = 0

## CONNECT TO THE DATABASE
try:
  cursor =  connect(aws_access_key_id=aws_data["aws_access"]["access_key_id"],
                    aws_secret_access_key=aws_data["aws_access"]["secret_access_key"],
                    s3_staging_dir=aws_data["aws_access"]["s3_staging_dir"],
                    region_name=aws_data["aws_access"]["region"]
                   ).cursor()
except: 
    print("Unable to Connect to AWS Athena")

## QUERIES ##
smoke_query = 'SELECT ninety_percent FROM another.resdata WHERE pass > 500'
count_moneymakers_query = "SELECT count(Distinct transaction_name) FROM another.resdata WHERE transaction_name LIKE '%_Total'"
count_report_query = 'SELECT count(DISTINCT partition_0) FROM another.resdata'
count_official_query = "SELECT count(DISTINCT partition_0) FROM another.resdata WHERE partition_0 LIKE '%_O'"
releases_query = 'SELECT DISTINCT partition_0 FROM another.resdata'
official_releases_query = "SELECT DISTINCT partition_0 FROM another.resdata WHERE partition_0 LIKE '%_O'"
individual_report_query = "SELECT transaction_name, ninety_percent, partition_0 FROM another.resdata WHERE partition_0 = \'%s\'"


db_report_count = 0
db_report_list = []
db_official_report_list = []
db_report_dict_arr = []
dated_releases = {}
official_dated_releases = {}

## CONNECT TO AWS DATABASE ##
print("Trying Sample Query to Confirm connection")
fetch = cursor.execute(smoke_query).fetchall()

if len(fetch) > 0:
  print("Database Successfully Connected")
else:
  print("Query Unsuccessful, Check the Status of the Database")
  sys.exit(1)


db_report_count = cursor.execute(count_report_query).fetchall()[0][0]
if db_report_count == 0:
  print("Database could be empty")
  sys.exit(1)
print("Processing " + str(db_report_count) + " LoadRunner Reports for Comparison")

money_maker_count = cursor.execute(count_moneymakers_query).fetchall()[0][0]
db_official_report_count = cursor.execute(count_official_query).fetchall()[0][0]
releases = cursor.execute(releases_query).fetchall()
official_releases = cursor.execute(official_releases_query).fetchall()


for i in range(db_official_report_count):
  official_dated_releases[official_releases[i][0]] = (DT.strptime(official_releases[i][0][6:-2], "%d-%m-%Y"))

for i in range(db_report_count):
  dated_releases[releases[i][0]] = (DT.strptime(releases[i][0][6:-2], "%d-%m-%Y"))

## Sort DB report list and official report list##
official_sorted_dates = sorted(official_dated_releases.items(),key=lambda kv: kv[1])
for i in range(len(official_sorted_dates)):
  db_official_report_list.append(official_sorted_dates[i][0])


sorted_dates = sorted(dated_releases.items(),key=lambda kv: kv[1])
for i in range(len(sorted_dates)):
  db_report_list.append(sorted_dates[i][0])
  d = {'label':sorted_dates[i][0], 'value' :sorted_dates[i][0]}
  db_report_dict_arr.append(d)

## populate lists with the data (name, 90th percentile, date) ##
db_data = []
db_official_data = []

for report in db_report_list:
  q_string = individual_report_query %str(report)
  data_set = cursor.execute(q_string).fetchall()
  db_data.append(LR_Report(data_set))

for report in db_official_report_list:
  q_string = individual_report_query %str(report)
  data_set = cursor.execute(q_string).fetchall()
  db_official_data.append(LR_Report(data_set))
