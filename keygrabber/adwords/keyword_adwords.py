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
traffic_estimator_service = client.GetTrafficEstimatorService('https://adwords.google.com', 'v201101')


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
	
	selector_estimator_service = {
		'campaignEstimateRequests': [{
			'adGroupEstimateRequests': [{
				'keywordEstimateRequests': [
					{
						'keyword': {
							'xsi_type': 'Keyword',
							'matchType': mode,
							'text': keyword
						}
					}
				],
				'maxCpc': {
					'xsi_type': 'Money',
					'microAmount': '1000000'
				}
			}],
			'targets': [
				{
					'xsi_type': 'CountryTarget',
					'countryCode': 'IT'
				},
				{
					'xsi_type': 'LanguageTarget',
					'languageCode': 'it'
				}
			]
		}]
	}
	
	estimates = None
	ret = None	
	
	ret = targeting_idea_service.Get(selector)[0]
	#do not get cpc for now
	#estimates = traffic_estimator_service.Get(selector_estimator_service)[0]

	global_searches = None
	regional_searches = None
	if ret is not None and 'entries' in ret and ret['entries']:
	  for key in ret['entries']:
			data = Utils.GetDictFromMap(key['data'])
			if 'value' in data['GLOBAL_MONTHLY_SEARCHES']:
				global_searches = data['GLOBAL_MONTHLY_SEARCHES']['value']
			if 'value' in data['AVERAGE_TARGETED_MONTHLY_SEARCHES']:
				regional_searches = data['AVERAGE_TARGETED_MONTHLY_SEARCHES']['value']
	
	if estimates is not None:
	  ad_group_estimate = estimates['campaignEstimates'][0]['adGroupEstimates'][0]
	  keyword_estimates = ad_group_estimate['keywordEstimates']
	  for index in xrange(len(keyword_estimates)):
		estimate = keyword_estimates[index]

		# Find the mean of the min and max values.
		mean_avg_cpc = (long(estimate['max']['averageCpc']['microAmount']) +
						long(estimate['max']['averageCpc']['microAmount'])) / 2
		mean_avg_pos = (float(estimate['min']['averagePosition']) +
						float(estimate['max']['averagePosition'])) / 2
		mean_clicks = (float(estimate['min']['clicksPerDay']) +
					   float(estimate['max']['clicksPerDay'])) / 2
		mean_total_cost = (long(estimate['min']['totalCost']['microAmount']) +
						   long(estimate['max']['totalCost']['microAmount'])) / 2

		print ('Results for the keyword with text \'%s\' and match type \'%s\':'
			   % (keyword, keyword))
		print '  Estimated average CPC: %s' % mean_avg_cpc
		print '  Estimated ad position: %s' % mean_avg_pos
		print '  Estimated daily clicks: %s' % mean_clicks
		print '  Estimated daily cost: %s' % mean_total_cost
	  
	return dict(global_searches = global_searches, regional_searches = regional_searches)
        
if __name__ == "__main__":
	for i in ['scaricare emule']:
		print i
		print get_keyword_info(i)

