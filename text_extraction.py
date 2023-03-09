# .env\Scripts\activate
import spacy
from spacy.matcher import PhraseMatcher, Matcher
import pandas as pd
import en_core_web_sm

action_words = ['layoff', 'fire']
number_unit = ['people','employee', 'job']

ex1title = 'Microsoft continues with previously announced layoffs, as Seattle-area total nears 1,500 people'
ex1 = '''
Microsoft notified another round of workers this week that they’re losing their jobs as part of the 10,000 layoffs announced by the company on Jan. 18.
A notice filed with the Washington state Employment Security Department indicates that this round impacts 617 workers at the company’s headquarters in Redmond, Wash., and offices in nearby Bellevue, and Issaquah.
That’s in addition to the 878 Microsoft workers previously notified that they were losing their jobs in the region, bringing the total to nearly 1,500 in the Seattle area.
The latest cuts are part of the 10,000 previously announced by the company globally, a Microsoft representative confirmed. Microsoft said originally that the layoffs would be made between January and the end of March, the end of the company’s fiscal third quarter.
The Surface, HoloLens and Xbox units were among those hit by the latest layoffs, according to a report by Bloomberg News, citing anonymous people familiar with the matter and a memo to employees from Microsoft Gaming CEO Phil Spencer. Bloomberg reported that the HoloLens cuts raise questions about whether Microsoft will move ahead with a third version of the mixed-reality headset.
Microsoft’s results for its fiscal second quarter revealed new levels of caution among the business customers responsible for a large portion of its business. Microsoft reported sluggish revenue growth, up 2% overall to $52.7 billion. Profits dropped 7% to $17.4 billion, not counting a $1.2 billion charge related to the cutbacks.
The 10,000 cuts are the second-largest workforce reduction in Microsoft’s history.
Microsoft is one of numerous tech companies to make layoffs in recent months, including Facebook parent Meta, Amazon, and Salesforce, in addition to many startups in the Seattle area and Silicon Valley.
'''
ex2title = 'Zoom is the latest tech firm to announce layoffs, and its CEO will take a 98% pay cut'
ex2 = '''
Zoom, which became a hallmark of the COVID-19 pandemic, is the latest tech company now turning to layoffs as it looks to navigate life after it.
The company is laying off some 1,300 employees, or about 15% of its workforce, CEO Eric Yuan announced Tuesday in a note to staff. He did not specify the breakdown of U.S. and non-U.S. employees.
'''
ex3title = 'Zwift announces new layoffs reducing 15% of workforce'
ex3 = '''
Zwift has internally announced a restructuring that is resulting in a reduction of the workforce by 15%, or approximately 80 people in total. The change is largely coming out of a “fresh look” at things with Zwift’s recently added Co-CEO, Kurt Beidler. Kurt came from Amazon back three months ago in December 2022, and has taken over the bulk of day-to-day operations from existing co-founder, and also Co-CEO, Eric Min. Zwift says these changes are largely about “investing in the fundamentals” rather than “spending on brand”. In other words, Kurt Beidler is prioritizing budget allocation on product development rather than marketing efforts.
The layoffs impact all teams, but the bulk are hitting the marketing and so-called “people” teams the deepest. The “people” teams are basically the HR and other non-product functions. The marketing teams are hit the hardest, and I’m told there will be some recognizable names in there from all levels of the company, once those names are announced publicly internally tomorrow. The impacted teams are mostly in the UK and US.
Zwift started announcing the changes at 1AM Pacific Time today (March 7th, 2023) in a company-wide e-mail from co-CEO Eric Min. That email was followed up immediately with an invitation to a virtual meeting for all impacted employees. In other words, if you didn’t get the meeting invite, you were good. In the previous round of layoffs last spring (where Zwift laid off 150 employees after shelving their smart-bike and own-designed hardware division), Zwift employees grew frustrated that they sat in limbo between the initial re-org announcement, and then hearing from their manager in 1:1 meetings that they were or weren’t impacted. Those individual meetings are still occurring this time, but are following the CEO meeting with those impacted.
Zwift says those impacted are being awarded a “generous severance package”,  as well as also being awarded their twice-annual bonus packages, as the payout period for those ran through the end of this month (March). They’ll get this past 6-month period bonus award. Further, employees will get career support, and then those in the US will get extensions of their health care packages.
Note that none of the marketing reduction is set to impact Zwift’s external community resources (which receive funding from Zwift), nor does it impact partnerships like Zwift’s sponsorship of the Women’s Tour de France.
Zwift says the intent of the restructuring is to “re-prioritize where budgets are spent”, specifically by “investing more in product development, both hardware and software”. While not good for Zwift marketing employees, this is likely to appeal to Zwift consumers/users, as it’s basically Zwift admitting that they need to focus more on the product and less on talking about the product. This is a common complaint found in almost every Zwift (or related) forum.
'''
def extract_key_sentence(text):
    # https://stackoverflow.com/questions/62776477/how-to-extract-sentences-with-key-phrases-in-spacy
    nlp = spacy.load("en_core_web_sm")
    phrase_matcher = PhraseMatcher(nlp.vocab)
    phrases = ['layoff', 'lay', 'off']
    patterns = [nlp(text) for text in phrases]
    phrase_matcher.add('layoff', None, *patterns)

    doc = nlp(text)
    key_sentences = []
    for sent in doc.sents:
        for match_id, start, end in phrase_matcher(nlp(sent.text)):
            if nlp.vocab.strings[match_id] in ["layoff"]:
                key_sentence = sent.text
                key_sentence = key_sentence.replace('\n', '')
                key_sentences.append(key_sentence)
    return key_sentences

def pos_extract(text, company, action, number):
    # https://spacy.io/usage/rule-based-matching
    nlp = spacy.load("en_core_web_sm")
    matcher = Matcher(nlp.vocab)
    
    company_pattern = [{'POS':'PROPN', 'OP' : '+'}]
    matcher.add("company", [company_pattern])

    action_pattern = [{'POS':'NOUN', 'OP' : '+'}]
    matcher.add("action", [action_pattern])

    number_pattern = [{'POS':'NUM', 'OP' : '{1}'}, {'POS':'ADJ', 'OP' : '*'}, {'POS':'NOUN', 'OP' : '+'}]
    matcher.add("number", [number_pattern])


    doc = nlp(text)
    matches = matcher(doc)
    print('type, start_index, end_index, phrase')
    for match_id, start, end in matches:
        string_id = nlp.vocab.strings[match_id]
        span = doc[start:end] 
        print(string_id, start, end, span.text)

        # simply extract the first PROPN
        if not company and string_id == 'company':
            company = doc[start].text
        
        if not action and string_id == 'action':
            for word in action_words:
                if word in doc[start].text:
                    action = -1
        if not number and string_id == 'number':
            for word in number_unit:
                if word in doc[end-1].text:
                    number = doc[start].text
    
    print()
    print('company:', company)
    print('action', action)
    print('number:', number)
    print('====')
    return company, action, number



def print_pos_tags(doc):
    features = []
    for token in doc:
        features.append({'token' : token.text, 'pos' : token.pos_})
    print(features)





company = None
action = None # 1 means hire, -1 means layoff
number = None

company, action, number = pos_extract(ex1title, company, action, number)
#====================
company = None
action = None # 1 means hire, -1 means layoff
number = None

for s in [ex2title]:
    company, action, number = pos_extract(s, company, action, number)
for s in extract_key_sentence(ex2):
    company, action, number = pos_extract(s, company, action, number)


