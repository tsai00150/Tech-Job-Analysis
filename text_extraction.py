import spacy
from spacy.matcher import PhraseMatcher, Matcher

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
            number.append(doc[start].text.replace(',', ''))
        
        if string_id == 'percent':
            percent.append(doc[start].text)
    
    return company, action, number


def print_pos_tags(doc):
    features = []
    for token in doc:
        features.append({'token' : token.text, 'pos' : token.pos_})
    print(features)




def predict(news):
    prediction = []
    for i in range(len(news)):
        prediction.append({}) 
        company = []
        action = []
        number = []
        percent = []
        for s in [news[i]['title']]:
            company, action, number = pos_extract(s, company, action, number, percent)
        for s in extract_key_sentence(news[i]['paragraph']):
            company, action, number = pos_extract(s, company, action, number, percent)
        prediction[i]['company'] = None if not company else max(company ,key=company.count)
        prediction[i]['action'] = None if not action else max(action, key=action.count)
        try:
            prediction[i]['number'] = int(max(number, key=number.count))
        except:
            prediction[i]['number'] = None
        try:
            prediction[i]['percent'] = int(max(percent, key=percent.count))
        except:
            prediction[i]['percent'] = None
        prediction[i]['date'] = news[i]['date']
    return prediction



