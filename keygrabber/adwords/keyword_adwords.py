import os
import sys
sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'adwords_api_python_14.2.1' ))
from adspygoogle.adwords.AdWordsClient import AdWordsClient
from adspygoogle.common import Utils

client = AdWordsClient(path=os.path.join(os.path.abspath(os.path.dirname(__file__)), 'adwords_api_python_14.2.1' ))
# Initialize appropriate service.
campaign_service = client.GetCampaignService(
    'https://adwords.google.com', 'v201101')
    
targeting_idea_service = client.GetTargetingIdeaService('https://adwords.google.com', 'v201101')


def get_keyword_info(keyword, mode='BROAD'):
	selector = {
		'searchParameters': [{
			'type': 'RelatedToKeywordSearchParameter',
			'keywords': [{
				'text': keyword,
				'matchType': mode
			}]
		},{
		   'type': 'KeywordMatchTypeSearchParameter',
		   'keywordMatchTypes': [mode]
		},{
		   'type': 'LanguageTargetSearchParameter',
		   'languageTargets': [{'languageCode':'it'}]
		},{
		   'type': 'CountryTargetSearchParameter',
		   'countryTargets': [{'countryCode':'IT'}]
		}],
		'ideaType': 'KEYWORD',
		'requestType': 'STATS',
		'requestedAttributeTypes': ['GLOBAL_MONTHLY_SEARCHES', 'AVERAGE_TARGETED_MONTHLY_SEARCHES'],
		'paging': {
			'startIndex': '0',
			'numberResults': '1000'
		}
	}

	#execute until no exceptions
	for i in range(30):
		try:
			ret = targeting_idea_service.Get(selector)[0]
		except:
			continue
		else:
			break

	
	if 'entries' in ret and ret['entries']:
	  for key in ret['entries']:
			global_searches = None
			regional_searches = None
			data = Utils.GetDictFromMap(key['data'])
			if 'value' in data['GLOBAL_MONTHLY_SEARCHES']:
				global_searches = data['GLOBAL_MONTHLY_SEARCHES']['value']
			if 'value' in data['AVERAGE_TARGETED_MONTHLY_SEARCHES']:
				regional_searches = data['AVERAGE_TARGETED_MONTHLY_SEARCHES']['value']
	return dict(global_searches = global_searches, regional_searches = regional_searches)
        
if __name__ == "__main__":
	print get_keyword_info('test')
