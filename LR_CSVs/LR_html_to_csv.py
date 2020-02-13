import plotly.graph_objects as go
from bs4 import BeautifulSoup as BS
import sys
from datetime import datetime as DT
import operator
import csv
import re
import boto3
import time
import json

## Will take LoadRunner HTML Summary and convert it to a CSV ##
## Path to where you want the csvs to be located ##
## By: Scott Hannan Aug 8th 2019 ##
## Hopefully this doesn't become obsolete haha ##

csvPath = "~/Desktop/LR_CSVs/"

class LrReportData:
  
  def __init__(self, soup):
    self.lr_name = str(soup.find(headers="LraScenarioName").string)[15:20]
    self.lr_period = str(soup.find(class_="header_timerange").string)[:19]
    self.lr_date = DT.strptime(self.lr_period[8:-1],'%d/%m/%Y')
    self.lr_duration = str(soup.find(headers="LraDuration").string)
    self.csv_name="MoneyMakers_" + self.lr_name + "_" + self.lr_period[8:-1].replace("/", "-") + ".csv"
    self.data = soup.find_all("span", class_="VerBl8")
    
    self.csv_cell_data = []
    self.csv_header_data = []
  
    for i in range(len(self.data)):
      if 'HTTP' in str(self.data[i].string):
        break
      if i % 9 == 0:
        self.csv_cell_data.append(re.sub(r'(_\d+_)', '_', str(self.data[i].string)))
        continue
     
      self.csv_cell_data.append(str(self.data[i].string).replace(",",""))
    
    self.data = soup.find_all("span", class_="Verdana2")
    
    for i in range(len(self.data)):
      if 'HTTP' in str(self.data[i].string):
        break
      if 'SLA Status' in str(self.data[i].string):
        continue
      self.csv_header_data.append(str(self.data[i].string).replace(" ","_").replace("90", "ninety").replace(".",""))


def html_to_csv( LrReport ):
  with open(LrReport.csv_name, 'w+') as csvfile:
    fw = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
    print("WRITING HEADERS...")
    fw.writerow(LrReport.csv_header_data)
    print("FILLING IN CELL DATA...")
    for i in range (0, len(LrReport.csv_cell_data),9):
      row = []
      for j in range(9):
        row.append(LrReport.csv_cell_data[j+i])
      fw.writerow(row)

  ### Upload to S3 DB ###
  
  key =  LrReport.csv_name
  
  if sys.argv[1] == "--official":
    outPutname =  "data/" + LrReport.lr_name + "_" + LrReport.lr_period[8:-1].replace("/", "-") + "_O/" +  LrReport.csv_name
    print("ADDING OFFICIAL DATA TO S3...")

  else:
    outPutname = "data/" + LrReport.lr_name + "_" + LrReport.lr_period[8:-1].replace("/", "-") + "_U/" +  LrReport.csv_name
    print("ADDING UNOFFICIAL DATA TO S3...")

  s3 = boto3.client('s3')
  s3.upload_file(key, bucketName, outPutname)

if (len(sys.argv) < 2):
  print('You must supply the path to a loadrunner summary to convert to a csv')
  print('USAGE: LR_html_to_csv.py [--official] "filePath1" "filePath2" ... "filePathN"')
  print('USE --official BEFORE your files to add official results into the table')
  print('If --official is not specified then data in S3 will be considered unofficial')
  sys.exit(0)

else:
  with open("../LR_REPORT_GEN/aws_data.json") as in_file:
    aws_data = json.load(in_file)


  for i in range (1, len(sys.argv),1):
    if sys.argv[i] == "--official":
      continue
    with open(sys.argv[i]) as fp:
      soup = BS(fp, features="html.parser")
      bucketName = aws_data["s3_bucketname"]
      html_to_csv(LrReportData(soup))

  ## CRAWL DATA AFTER UPLOAD TO UPDATE AWS S3 DB ##
  crawler = boto3.client(service_name='glue', region_name=aws_data["aws_access"]["region"])
  resp = crawler.get_crawler(Name=aws_data["glue_crawler_name"])
  if  resp['Crawler']['State'] != "READY":
    print("Crawler already running, please try again in a few moments")
    sys.exit(0)

  crawler.start_crawler(Name='getdat')
  resp = crawler.get_crawler(Name='getdat')

  while resp['Crawler']['State'] != "READY":
    resp = crawler.get_crawler(Name=aws_data["glue_crawler_name"])
    time.sleep(10)
    print("Polling Crawler for finished status...")
    print("Current Status is " + resp['Crawler']['State'])

  ## Restart App_Server to Update App Database ##
  print("BeanStalking...")
  beanstalk = boto3.client('elasticbeanstalk')
  beanstalk.restart_app_server(EnvironmentId=aws_data["beanstalk_env_id"])


