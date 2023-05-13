from crawl_news import crawl_reuters
from text_extraction import predict
from crawl_company import wiki_info
from database import getCompanyNodeAll, getIndustryNodeAll, getActivityNodeAll
from csv_transform import updateCompanyInfo, updateActivityInfo
import json
import csv

# Crawl the web to get news, store data directly in data.json
crawl_reuters('layoffs', 0, 262, 20)

#############################################################

# Make predictions based on the news raw data
news = json.load(open('data.json', encoding='utf-8'))
prediction = predict(news)
with open('prediction.json', 'w', encoding='utf-8') as f:
    json.dump(prediction, f, ensure_ascii=False, indent=4)

#############################################################

# Compose the csv files
companyCsv = [[None]*3]
industryCsv = [[None]*2]
includeCsv = [[None]*2]
subsidaryCsv = [[None]*4]
activityCsv = [[None]*9]
prediction = json.load(open('prediction.json', encoding='utf-8'))
data = json.load(open('data.json', encoding='utf-8'))
availableCompanyIndex = len(getCompanyNodeAll())+1
availableIndustryIndex = len(getIndustryNodeAll())+1
availableActivityIndex = len(getActivityNodeAll())+1

for i in range(len(prediction)):
    if not prediction[i]['company']:
        print('No company detected in the news; omit import')
    
    companyInfo = wiki_info(prediction[i]['company'])
    if companyInfo:
        realCompanyName = companyInfo['Company Name']
        companyId, availableCompanyIndex, availableIndustryIndex = updateCompanyInfo(\
            realCompanyName, companyCsv, subsidaryCsv, availableCompanyIndex, \
            industryCsv, includeCsv, availableIndustryIndex)
        if companyId:
            if prediction[i]["action"] and prediction[i]["number"]:
                employeeChange = prediction[i]["action"]*prediction[i]["number"]
            elif prediction[i]["action"] and prediction[i]["percent"] and companyInfo["Number of employees"]:
                employeeChange = prediction[i]["action"]*prediction[i]["percent"]*0.01*companyInfo["Number of employees"]
            else:
                employeeChange = 0
            activityCsv, availableActivityIndex = updateActivityInfo(i, \
                availableActivityIndex, companyId, realCompanyName, \
                employeeChange, data, activityCsv, companyCsv)

with open('.csv/company.csv', 'w', encoding='utf-8', newline='') as csvfile: 
    csvwriter = csv.writer(csvfile) 
    csvwriter.writerow(['companyId', 'companyName', 'employeeNumber']) 
    csvwriter.writerows(companyCsv)

with open('.csv/subsidiary.csv', 'w', encoding='utf-8', newline='') as csvfile: 
    csvwriter = csv.writer(csvfile) 
    csvwriter.writerow(['parentId', 'parentName', 'subsidiaryId', 'subsidiaryName']) 
    csvwriter.writerows(subsidaryCsv)

with open('.csv/industry.csv', 'w', encoding='utf-8', newline='') as csvfile: 
    csvwriter = csv.writer(csvfile) 
    csvwriter.writerow(['industryId', 'industryName']) 
    csvwriter.writerows(industryCsv)

with open('.csv/include.csv', 'w', encoding='utf-8', newline='') as csvfile: 
    csvwriter = csv.writer(csvfile) 
    csvwriter.writerow(['industryId', 'companyId']) 
    csvwriter.writerows(includeCsv)

with open('.csv/activity.csv', 'w', encoding='utf-8', newline='') as csvfile: 
    csvwriter = csv.writer(csvfile) 
    csvwriter.writerow(['activityId', 'companyId', 'companyName', 'employeeChange', \
                        'newsTitle', 'newsSnippet', 'newsLink', 'confidence', 'date']) 
    csvwriter.writerows(activityCsv)
