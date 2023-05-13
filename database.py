from crawl_company import wiki_info
from neo4j import GraphDatabase
import configparser
config = configparser.ConfigParser()
config.read('config.ini')
URI = config['neo4j']['uri']
AUTH = (config['neo4j']['username'], config['neo4j']['password'])

def getCompanyId(name):

    def queryCompanyId(tx, name):
        result = tx.run(
            "MATCH (c:company {companyName: $name}) RETURN c.companyId",
            name=name)
        records = list(result)
        return records

    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        driver.verify_connectivity()
    with driver.session(database="neo4j") as session:
        records = session.execute_read(queryCompanyId, name=name)
    session.close()
    driver.close()
    if records:   
        return records[0].data()['c.companyId']
    return None

def getCompanyById(companyId):

    def helper(tx, companyId):
        result = tx.run("MATCH (c:company) \
                        WHERE c.companyId = $companyId \
                        RETURN c", companyId=companyId)
        records = list(result)
        return records

    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        driver.verify_connectivity()
    with driver.session(database="neo4j") as session:
        records = session.execute_read(helper, \
                    companyId=companyId)
    session.close()
    driver.close()
    if records:
        return records[0]
    return None

def getCompanyNodeAll():

    def helper(tx):
        result = tx.run("MATCH (c:company) RETURN c")
        records = list(result)
        return records

    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        driver.verify_connectivity()
    with driver.session(database="neo4j") as session:
        records = session.execute_read(helper)
    session.close()
    driver.close()
    return records

def getIndustryNodeAll():

    def helper(tx):
        result = tx.run("MATCH (i:industry) RETURN i")
        records = list(result)
        return records

    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        driver.verify_connectivity()
    with driver.session(database="neo4j") as session:
        records = session.execute_read(helper)
    session.close()
    driver.close()
    return records

def getActivityNodeAll():

    def helper(tx):
        result = tx.run("MATCH (a:activity) RETURN a")
        records = list(result)
        return records

    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        driver.verify_connectivity()
    with driver.session(database="neo4j") as session:
        records = session.execute_read(helper)
    session.close()
    driver.close()
    return records

def getActivityNodeByEmployee(company, employeeChange):

    def helper(tx, num, company):
        result = tx.run("MATCH (a:activity) \
                        WHERE a.employeeChange = $num and \
                        a.companyName = $company\
                        RETURN a", num=num, company=company)
        records = list(result)
        return records

    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        driver.verify_connectivity()
    with driver.session(database="neo4j") as session:
        records = session.execute_read(helper, \
                    num=employeeChange, company=company)
    session.close()
    driver.close()
    if records:
        return records[0]
    return None

def getIndustryId(name):

    def helper(tx, name):
        result = tx.run(
            "MATCH (i:industry {industryName: $name}) RETURN i.industryId",
            name=name)
        records = list(result)
        return records

    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        driver.verify_connectivity()
    with driver.session(database="neo4j") as session:
        records = session.execute_read(helper, name=name)
    session.close()
    driver.close()
    if records:   
        return records[0].data()['i.industryId']
    return None