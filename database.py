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

def test():
    def test1(tx):
        result = tx.run("GRANT ROLE PUBLIC TO neo4j")
        return list(result)
    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        driver.verify_connectivity()
    with driver.session(database="neo4j") as session:
        result = session.execute_read(test1)
    session.close()
    driver.close()
    return result