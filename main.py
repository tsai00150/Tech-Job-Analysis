from crawl_news import crawl_reuters
from text_extraction import predict
from database import getCompanyNodeAll, getActivityNodeAll
from csv_transform import updateCompanyInfo
import json
import csv

# The crawled data stores directly in data.json
crawl_reuters()

#############################################################

# Make predictions based on the news raw data
news = json.load(open('data.json', encoding='utf-8'))
prediction = predict(news)
with open('prediction.json', 'w', encoding='utf-8') as f:
    json.dump(prediction, f, ensure_ascii=False, indent=4)

#############################################################

# compose the csv files
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
    else:
        companyId, availableCompanyIndex = updateCompanyInfo(\
            prediction[i]['company'], companyCsv, subsidaryCsv, availableCompanyIndex)
        if prediction[i]["number"]:
            employeeChange = prediction[i]["action"]*prediction[i]["number"]
        elif prediction[i]["percent"]:
            employeeChange = prediction[i]["action"]*prediction[i]["percent"]*0.01
        else:
            employeeChange = 0
        activityCsv.append([availableActivityIndex, companyId, prediction[i]['company'], \
                            employeeChange, data[i]['title'], None, \
                            data[i]['link'], 0.5, data[i]['date']])
        availableActivityIndex += 1

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
