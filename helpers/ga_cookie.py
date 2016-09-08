import re
import unittest
from datetime import datetime

class GoogleAnalyticsCookie():
    """ Parses the utma (visitor) and utmz (referral) Google Analytics cookies """
    utmz = dict(
        domain_hash = None,
        timestamp = None,
        session_counter = None,
        campaign_number = None,
        campaign_data = dict(
            source = None,
            name = None,
            medium = None,
            term = None,
            content = None
        )
    )       
    utma = dict(
        domain_hash = None,
        random_id = None,
        first_visit_at = None,
        previous_visit_at = None,
        current_visit_at = None,
        session_counter = None
    )     
    
          
    def __init__(self, utmz=None, utma=None):
        self.utmz = dict(
            domain_hash = None,
            timestamp = None,
            session_counter = None,
            campaign_number = None,
            campaign_data = dict(
                source = None,
                name = None,
                medium = None,
                term = None,
                content = None
            )
        )        
        
        self.utma = dict(
            domain_hash = None,
            random_id = None,
            first_visit_at = None,
            previous_visit_at = None,
            current_visit_at = None,
            session_counter = None
        )        
        if utmz:
            self.utmz = self.__parse_utmz(utmz)
        if utma:
            self.utma = self.__parse_utma(utma)
        
    def __parse_utmz(self, cookie):
        """ Parses the utmz cookie for visitor information """
        parsed = cookie.split('.')
        if len(parsed) < 5:
            return self.utmz 
        
        #rejoin when src or cct might have a dot i.e. utmscr=example.com
        parsed[4] = ".".join(parsed[4:])    
        
        translations = dict(
            utmcsr = 'source',
            utmccn = 'name',
            utmcmd = 'medium',
            utmctr = 'term',
            utmcct = 'content'
        )
        
        parsed_campaign_data = self.utmz['campaign_data']
        
        for params in parsed[4].split('|'):
            key_value = params.split('=')
            if translations.has_key(key_value[0]):
                parsed_campaign_data[translations[key_value[0]]] = key_value[1]
        
        # Override campaign data when visitor comes from Google AdWords    
        if re.search('gclid=', cookie):
            parsed_campaign_data = dict(
                source = 'google',
                name = None,
                medium = 'cpc',
                content = None,
                term = parsed_campaign_data['term']
            )
                
        return dict(
            domain_hash = parsed[0],
            timestamp = parsed[1],
            session_counter = parsed[2],
            campaign_number = parsed[3],
            campaign_data = parsed_campaign_data
        )
        
    def __parse_utma(self, cookie):
        """ Parses the utma cookie for referral information """
        parsed = cookie.split('.')
        if len(parsed) != 6:
            return self.utma
        
        return dict(
            domain_hash = parsed[0],
            random_id = parsed[1],
            first_visit_at = datetime.fromtimestamp(float(parsed[2])),
            previous_visit_at = datetime.fromtimestamp(float(parsed[3])),
            current_visit_at = datetime.fromtimestamp(float(parsed[4])),
            session_counter = parsed[5]
        )
if __name__ == '__main__':
    utmz = request.cookies['__utmz'] if 'utmz' in request.cookies else None
    utma = request.cookies['__utma'] if 'utma' in request.cookies else None
    gac = GoogleAnalyticsCookie(utmz=utmz, utma=utma)
