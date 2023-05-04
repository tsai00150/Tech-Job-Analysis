from crawl_news import crawl_reuters
from text_extraction import predict
from crawl_company import wiki_info
from database import getCompanyNodeAll, getActivityNodeAll
from csv_transform import updateCompanyInfo, updateActivityInfo
import json
import csv

# Crawl the web to get news, store data directly in data.json
# crawl_reuters('layoffs', 0, 262, 20)

#############################################################

# Make predictions based on the news raw data
# news = json.load(open('data.json', encoding='utf-8'))
# prediction = predict(news)
# with open('prediction.json', 'w', encoding='utf-8') as f:
#     json.dump(prediction, f, ensure_ascii=False, indent=4)

#############################################################

# Compose the csv files
companyCsv = [[None]*3]
subsidaryCsv = [[None]*4]
activityCsv = [[None]*9]
prediction = json.load(open('prediction.json', encoding='utf-8'))
data = json.load(open('data.json', encoding='utf-8'))
availableCompanyIndex = len(getCompanyNodeAll())+1
availableActivityIndex = len(getActivityNodeAll())+1

for i in range(len(prediction)):
    if not prediction[i]['company']:
        print('No company detected in the news; omit import')
    
    companyInfo = wiki_info(prediction[i]['company'])
    if companyInfo:
        realCompanyName = companyInfo['Company Name']
        companyId, availableCompanyIndex = updateCompanyInfo(\
            realCompanyName, companyCsv, subsidaryCsv, availableCompanyIndex)
        if companyId:
            if prediction[i]["action"] and prediction[i]["number"]:
                employeeChange = prediction[i]["action"]*prediction[i]["number"]
            elif prediction[i]["action"] and prediction[i]["percent"]:
                employeeChange = prediction[i]["action"]*prediction[i]["percent"]*0.01
            else:
                employeeChange = 0
            activityCsv, availableActivityIndex = updateActivityInfo(i, \
                availableActivityIndex, companyId, realCompanyName, \
                employeeChange, data, activityCsv, companyCsv)

with open('.csv/company.csv', 'w', encoding='utf-8', newline='') as csvfile: 
    csvwriter = csv.writer(csvfile) 
    csvwriter.writerow(['companyId', 'companyName', 'employeeNumber']) 
    csvwriter.writerows(companyCsv)

with open('.csv/subsidary.csv', 'w', encoding='utf-8', newline='') as csvfile: 
    csvwriter = csv.writer(csvfile) 
    csvwriter.writerow(['parentId', 'parentName', 'subsidaryId', 'subsidaryName']) 
    csvwriter.writerows(subsidaryCsv)

with open('.csv/activity.csv', 'w', encoding='utf-8', newline='') as csvfile: 
    csvwriter = csv.writer(csvfile) 
    csvwriter.writerow(['activityId', 'companyId', 'companyName', 'employeeChange', \
                        'newsTitle', 'newsSnippet', 'newsLink', 'confindence', 'date']) 
    csvwriter.writerows(activityCsv)
