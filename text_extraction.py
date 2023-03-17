# .env\Scripts\activate
import spacy
from spacy.matcher import PhraseMatcher, Matcher

news = [{'title': 'Zwift announces new layoffs reducing 15% of workforce', 'text': '''Zwift has internally announced a restructuring that is resulting in a reduction of the workforce by 15%, or approximately 80 people in total. The change is largely coming out of a “fresh look” at things with Zwift’s recently added Co-CEO, Kurt Beidler. Kurt came from Amazon back three months ago in December 2022, and has taken over the bulk of day-to-day operations from existing co-founder, and also Co-CEO, Eric Min. Zwift says these changes are largely about “investing in the fundamentals” rather than “spending on brand”. In other words, Kurt Beidler is prioritizing budget allocation on product development rather than marketing efforts.The layoffs impact all teams, but the bulk are hitting the marketing and so-called “people” teams the deepest. The “people” teams are basically the HR and other non-product functions. The marketing teams are hit the hardest, and I’m told there will be some recognizable names in there from all levels of the company, once those names are announced publicly internally tomorrow. The impacted teams are mostly in the UK and US.Zwift started announcing the changes at 1AM Pacific Time today (March 7th, 2023) in a company-wide e-mail from co-CEO Eric Min. That email was followed up immediately with an invitation to a virtual meeting for all impacted employees. In other words, if you didn’t get the meeting invite, you were good. In the previous round of layoffs last spring (where Zwift laid off 150 employees after shelving their smart-bike and own-designed hardware division), Zwift employees grew frustrated that they sat in limbo between the initial re-org announcement, and then hearing from their manager in 1:1 meetings that they were or weren’t impacted. '''},
       {'title': 'Amazon layoffs hit workers in robotics, grocery, health and AWS divisions', 'text': '''Amazon’s 18,000-plus job layoff announced this month are being felt broadly across the company’s sprawling operations, from physical retail technology and grocery stores to robotics and drone delivery, and even in cloud computing.'''},
       {'title': 'Meta Plans Thousands More Layoffs as Soon as This Week', 'text': '''The world’s largest social networking company is eliminating more jobs, on top of a 13% reduction in November, in a bid to become a more efficient organization. In its earlier round of cuts, Meta layoff 11,000 workers in what was its first-ever major layoff.'''},
       {'title': 'Yahoo will layoff 20% of staff, or 1600 people', 'text': '''Yahoo is laying off 20% of its staff, impacting 1,600 employees in its ad tech business. '''},
       {'title': 'Microsoft joined the layoff parade. Did it really have to?', 'text': '''When Microsoft announced this week that it was laying off 10,000 employees, it wasn’t exactly a shock. Other big companies, including Salesforce, Amazon and Meta, have already been down that road, and the news leaked far and wide before the official announcement on Wednesday. Alphabet joined in today, announcing another 12,000 job cuts.'''},
       {'title': 'Salesforce to cut workforce by 10% after hiring ‘too many people’ during the pandemic', 'text': '''Salesforce has announced to lay off some 10% of its workforce, impacting more than 7,000 employees, while it will also shutter offices in “certain markets.”'''},
       {'title': 'Google parent Alphabet cuts 6% of its workforce, impacting 12,000 people', 'text': '''Alphabet, parent holding company of Google, has announced that it’s cutting around 6% of its global workforce.'''},
       {'title': 'Zoom layoffs impact 15% of staff', 'text': '''After an unfathomable boom at the onset of the pandemic, Zoom has made the decision to cut 15% of its staff, or 1,300 people.'''},
       {'title': 'GitHub lays off 10% and goes fully remote', 'text': '''The tech layoffs keep on coming. Microsoft-owned GitHub today announced that it is laying off 10% of its staff through the end of the company’s fiscal year. Before this announcement, which was first reported by Fortune, GitHub had about 3,000 employees. The company will also shutter all of its offices as their leases end, in part because of their low utilization, and move to a remote-first culture.'''},
       {'title': 'Spotify cuts 6% of its workforce, impacting 600 people', 'text':'''Music streaming service Spotify has announced that it will be conducting a round of layoffs that will impact around 6% of its global workforce. In its most recent earnings release, the company said that there were 9,808 full-time employees working for Spotify. Today’s move will impact around 600 employees.'''}]
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

def pos_extract(text, company, action, number, percent):
    # https://spacy.io/usage/rule-based-matching
    nlp = spacy.load("en_core_web_sm")
    matcher = Matcher(nlp.vocab)
    
    company_pattern = [{'POS':'PROPN', 'OP' : '+'}]
    matcher.add("company", [company_pattern])

    action_pattern1 = [{'OP' : '+', "LEMMA":{"IN":['layoff', 'cut', 'reduce']}}]
    action_pattern2 = [{'OP' : '+', "LEMMA":{"IN":['lay']}}, {'OP' : '+', "LEMMA":{"IN":['off']}}]
    matcher.add("action", [action_pattern1, action_pattern2])

    number_pattern = [{'POS':'NUM', 'OP':'{1}'}, {'TEXT':{'NOT_IN':['%']}, 'OP' : '{,5}'}, \
                      {'POS':'NOUN', 'OP':'+', "LEMMA":{"IN": ['people','employee','job','worker','staff']}}]
    matcher.add("number", [number_pattern])
    percent_pattern = [{'POS':'NUM', 'OP':'{1}'}, {'TEXT':{'IN':['%']}}, {'OP' : '{,5}'}, \
                      {'POS':'NOUN', 'OP':'+', "LEMMA":{"IN": ['people','employee','job','worker','staff']}}]
    matcher.add("percent", [percent_pattern])

    doc = nlp(text)
    matches = matcher(doc)
    for match_id, start, end in matches:
        string_id = nlp.vocab.strings[match_id]
        span = doc[start:end] 

        # simply extract the first PROPN
        if not company and string_id == 'company':
            company.append(doc[start].text)
        
        if string_id == 'action':
            action.append(-1)
        
        if string_id == 'number':
            number.append(doc[start].text)
        
        if string_id == 'percent':
            percent.append(doc[start].text)
    
    return company, action, number


def print_pos_tags(doc):
    features = []
    for token in doc:
        features.append({'token' : token.text, 'pos' : token.pos_})
    print(features)





for i in range(len(news)):
    company = []
    action = []
    number = []
    percent = []
    for s in [news[i]['title']]:
        company, action, number = pos_extract(s, company, action, number, percent)
    for s in extract_key_sentence(news[i]['text']):
        company, action, number = pos_extract(s, company, action, number, percent)
    print('company:', company)
    print('action', action)
    print('number:', number)
    print('percent', percent)
    print('====')



