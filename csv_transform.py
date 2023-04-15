from crawl_company import wiki_info
from database import getCompanyId

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
                        subId, availableCompanyIndex = updateCompanyInfo(\
                            subCompany, companyCsv, subsidaryCsv, availableCompanyIndex)
                        if subId:
                            subsidaryCsv.append([companyId, company, subId, subCompany])
                if companyInfo['parent']:
                    parentCompany = companyInfo['parent'].split(' (')[0]
                    parentId, availableCompanyIndex = updateCompanyInfo(parentCompany, companyCsv, subsidaryCsv, availableCompanyIndex)
                    if parentId:
                        subsidaryCsv.append([parentId, parentCompany, companyId, company])
                
    return companyId, availableCompanyIndex