from crawl_company import wiki_info
from database import getCompanyId, getCompanyById, getActivityNodeByEmployee

COMPANY_SCALE_MINIMUM = [0, 1000, 10000, 100000]
SCORE_ADDED_PER_NEWS = [1, 0.5, 0.33, 0.2]

def newCompany(company, companyCsv, availableCompanyIndex):
    companyInfo = wiki_info(company)
    if not companyInfo:
        companyInfo = wiki_info(company+'_(company)')
        if not companyInfo:
            print('Company in news cannot be found in wiki: ', company)
            return None, None
    employeeNum = companyInfo['Number of employees']
    if employeeNum:
        employeeNum = employeeNum.lstrip().replace('\xa0', ' ')\
            .split(' ')[0].replace(',', '').split('[')[0]
        try:
            employeeNum = int(employeeNum)
        except:
            employeeNum = None
    companyCsv.append([availableCompanyIndex, company, employeeNum])
    return availableCompanyIndex, companyInfo

def updateCompanyInfo(company, companyCsv, subsidaryCsv, availableCompanyIndex):
    companyId = getCompanyId(company)
    if not companyId:
        for row in companyCsv:
            if row[1] == company:
                companyId = row[0]
                break
        if not companyId: 
            # new company not in database and csv, update company.csv first and get companyId
            companyId, companyInfo = newCompany(company, companyCsv, availableCompanyIndex)
            if not companyId:
                return None, availableCompanyIndex
            else:
                availableCompanyIndex += 1
                if companyInfo['sub']:
                    for subCompany in companyInfo['sub']:
                        subCompanyInfo = wiki_info(subCompany)
                        if subCompanyInfo:
                            subCompany = subCompanyInfo['Company Name']
                            subId, availableCompanyIndex = updateCompanyInfo(\
                                subCompany, companyCsv, subsidaryCsv, availableCompanyIndex)
                            if subId:
                                subsidaryCsv.append([companyId, company, subId, subCompany])
                if companyInfo['parent']:
                    parentCompany = companyInfo['parent'].split(' (')[0]
                    parentCompanyInfo = wiki_info(parentCompany)
                    if parentCompanyInfo:
                        parentCompany = parentCompanyInfo['Company Name']
                        parentId, availableCompanyIndex = updateCompanyInfo(parentCompany, companyCsv, subsidaryCsv, availableCompanyIndex)
                        if parentId:
                            subsidaryCsv.append([parentId, parentCompany, companyId, company])
                
    return companyId, availableCompanyIndex

def updateActivityInfo(dataIndex, availableActivityIndex, companyId, realCompanyName, \
                        employeeChange, data, activityCsv, companyCsv):
    activity = getActivityNodeByEmployee(realCompanyName, employeeChange)
    if activity: # the activity is in database
        totalEmployee = getCompanyById(companyId).data()['a.employeeNumber']
        if not totalEmployee:
            totalEmployee = 1
        for i in range(len(COMPANY_SCALE_MINIMUM)-1, -1, -1):
            if totalEmployee > COMPANY_SCALE_MINIMUM[i]:
                confidence = min(activity.data()['a.confidence'] + \
                            SCORE_ADDED_PER_NEWS[i], 1.0)
                activityCsv.append([activity.data()['a.activityId'], \
                                    activity.data()['a.companyId'], \
                                    activity.data()['a.companyName'], \
                                    activity.data()['a.employeeChange'], \
                                    activity.data()['a.newsTitle'] + '\n' + \
                                    data[dataIndex]['title'], \
                                    activity.data()['a.newsSnippet'], \
                                    activity.data()['a.newsLink'] + '\n' + \
                                    data[dataIndex]['link'], \
                                    confidence, \
                                    activity.data()['a.date']])
                return activityCsv, availableActivityIndex

    for i in range(len(activityCsv)): # the activity is in csv
        if activityCsv[i][2] == realCompanyName and activityCsv[i][3] == employeeChange:

            for row in companyCsv:
                if row[0] == companyId:
                    totalEmployee = 1 if not row[2] else row[2]
                    break
            else:
                totalEmployee = 1

            for j in range(len(COMPANY_SCALE_MINIMUM)-1, -1, -1):
                if totalEmployee > COMPANY_SCALE_MINIMUM[j]:
                    
                    activityCsv[i][4] += ' | ' + data[dataIndex]['title']
                    activityCsv[i][6] += ' | ' + data[dataIndex]['link']
                    activityCsv[i][7] = min(activityCsv[i][7] + SCORE_ADDED_PER_NEWS[j], 1.0)
                    break
            return activityCsv, availableActivityIndex
        
    # this is a brand new activity
    company = getCompanyById(companyId)
    if company and company.data()['a.employeeNumber']:
        totalEmployee = company.data()['a.employeeNumber']
    elif company:
        totalEmployee = 1
    else:
        for row in companyCsv:
            if row[0] == companyId:
                totalEmployee = 1 if not row[2] else row[2]
                break
        else:
            totalEmployee = 1
        
    for i in range(len(COMPANY_SCALE_MINIMUM)-1, -1, -1):
        if totalEmployee > COMPANY_SCALE_MINIMUM[i]:
            confidence = min(SCORE_ADDED_PER_NEWS[i], 1.0)
            break

    activityCsv.append([availableActivityIndex, companyId, realCompanyName, \
                    employeeChange, data[dataIndex]['title'], None, \
                    data[dataIndex]['link'], confidence, data[dataIndex]['date']])
    return activityCsv, availableActivityIndex+1