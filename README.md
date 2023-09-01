# Tech Job Analysis

Code for scraping hire/layoff information on the web.

Developed by Charlene Chiang and Tsai-Chen Hsieh

Note that it does not include config, json, and csv files. 

## Dashboard Overview
The first page shows the whole graph, with an option the limit the size. 
![neodash_complete_graph](pictures/neodash_complete_graph.jpg)
You can get information on layoff activities (yellow node) and filter them. 
![neodash_activity](pictures/neodash_activity.jpg)
You can check out each industry and see its layoff activities. 
![neodash_industry](pictures/neodash_industry.jpg)
You can search compaines to get the organization map, such as parent companies or subsidiaries. 
![neodash_organization](pictures/neodash_organization.jpg)


## Running the scripts 
After cloning the repository and downloading all required libraries on your environment, go to your project's root directory, create `config.ini`, following the format below:
```
[reuters]
username = <reuters username>
password = <reuters password>

[neo4j]
uri = <neo4j uri>
username = <database username>
password = <database password>
```
Also, create the folder required to store the csv files:
```bash
mkdir .csv
```
To run the script: 
```bash
python main.py
```

## Module Explanation
### Crawl the web
`crawl_reuters()` crawls Reuters to get the news. Search keyword is an input parameter, like `layoff` and `lay+off` (if your search has space, replace it with +). The next three is `startpage`: the index of the first page (usually 0), `endpage`: the total count of news for the search, `steps`: how many news for a page (usually 20). The raw data is stored in `data.json`. For each news, we have the following attributes: link, title, paragraph, date. In some rare cases where the date is not shown, then it will be replaced with `Janurary 1 2000`.

### Make predictions
Based on the raw data, apply NLP techniques to obtain the attributes, including company, action, number, percent, date. If it is not found, then it is null. The data is stored in `prediction.json`.

### Compose the csv files
Use `data.json` and `prediction.json` to turn into csv files that can be uploaded directly to the Neo4j aura web console. For each news instance, here are the steps:
1. Go through `updateCompanyInfo()`, which updates the predicted company to the database. The function recursively collects all subsidaries/parent company related to the company, and assign a new id to companies that are not found in the database. Every company is checked with the database first, so there are no conflicts when assigning ids. The data must be found in Wikipedia, which is our source for companies. If the company is not found (either through \<Company Name> or \<Company Name>_(company) ), then we do not enter it to the database. If the company from the news is not found in Wikipedia, then we simply ignore the news. 
2. Compose the required data to the csv files, under folder `.csv`. Then we can upload the data to the Neo4j Aura web console directly. 
