from urllib.parse import urlparse
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
import re

import os
from pathlib import Path
import sys

PACKAGE_ROOT = Path(os.path.abspath(os.path.dirname(__file__))).parent
sys.path.append(str(PACKAGE_ROOT))

from prediction_model.config import config



class FeaturesEngineering(BaseEstimator,TransformerMixin):
    def __init__(self, variables=None, label=None) -> None:
        self.variables = variables
        self.label = label
        
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        self.data_fit = self.add_carcteristics(X)
        X_fit = self.data_fit[self.variables]
        return X_fit
    
    def add_carcteristics(self, data):
        result = pd.DataFrame(data)
        #print(result)

        result["nbr_https"]= result[config.X].apply(lambda i : i.count('https'))
        result["nbr_http"]= result[config.X].apply(lambda i : i.count('http'))
        result["nbr_doubleSlash"]= result[config.X].apply(lambda i : i.count('//'))
        result["nbr_www"]= result[config.X].apply(lambda i : i.count('www'))
        result["nbr_slash"]= result[config.X].apply(lambda i : i.count('/'))
        result["nbr_@"]= result[config.X].apply(lambda i : i.count('@'))
        result["nbr_-"]= result[config.X].apply(lambda i : i.count('-'))
        result["nbr_?"]= result[config.X].apply(lambda i : i.count('?'))
        result["nbr_%"]= result[config.X].apply(lambda i : i.count('%'))
        result["nbr_="]= result[config.X].apply(lambda i : i.count('='))
        result["nbr_."]= result[config.X].apply(lambda i : i.count('.'))
        result["length"] = result[config.X].apply(lambda i : len(i))
        result["phishing_words"] = result[config.X].apply(lambda i : self.phishing_words(i))
        result["cont_digit"] = result[config.X].apply(lambda i : self.contains_digits(i))
        result["length_domain"] = result[config.X].apply(lambda i : self.domain_length(i))
        result["short_url"] = result[config.X].apply(lambda i : self.is_shortened_url(i))
        result["bad_url"] = result[config.X].apply(lambda i : self.bad_url(i))
        result["nbr_spe_c"] = result[config.X].apply(lambda i : self.count_special_characters(i))
        result["hexa"] = result[config.X].apply(lambda i : self.contains_hex_characters(i))
        result["nbr_param"] = result[config.X].apply(lambda i : self.count_query_parameters(i))
    
        return result
    
    def phishing_words(self,data):
        result = re.search('pay|pal|battle|wp|cgi|login|webscr|cmd|bin|submit|bank|secure|update|account|password',data) 

        if result:
            return 1
        else:
            return 0
    
    def contains_digits(self,url):
        for char in url:
            if  char.isdigit() :
                return 1

        return 0
    
    def domain_length(self,url):
        parsed_url = urlparse(url)
        domain = parsed_url.netloc
        
        return len(domain)
    
    def is_shortened_url(self,url):
        shorteners = ['bit.ly', 'goo.gl', 'shorte.st', 'go2l.ink', 'x.co', 'ow.ly', 't.co', 'tinyurl', 'tr.im', 'is.gd', 'cli.gs', 
        'yfrog.com', 'migre.me', 'ff.im', 'tiny.cc', 'url4.eu', 'twit.ac', 'su.pr', 'twurl.nl', 'snipurl.com', 
        'short.to', 'BudURL.com', 'ping.fm', 'post.ly', 'Just.as', 'bkite.com', 'snipr.com', 'fic.kr', 'loopt.us', 
        'doiop.com', 'short.ie', 'kl.am', 'wp.me', 'rubyurl.com', 'om.ly', 'to.ly', 'bit.do', 't.co', 'lnkd.in', 
        'db.tt', 'qr.ae', 'adf.ly', 'goo.gl', 'bitly.com', 'cur.lv', 'tinyurl.com', 'ow.ly', 'bit.ly', 'ity.im', 
        'q.gs', 'is.gd', 'po.st', 'bc.vc', 'twitthis.com', 'u.to', 'j.mp', 'buzurl.com', 'cutt.us', 'u.bb', 
        'yourls.org', 'x.co', 'prettylinkpro.com', 'scrnch.me', 'filoops.info', 'vzturl.com', 'qr.net', '1url.com', 
        'tweez.me', 'v.gd', 'tr.im', 'link.zip.net']

        for short in shorteners :
            if short in url :
                    return 1

        return 0
    
    def bad_url(self,url):
        result =re.search(str(urlparse(url).hostname), url)
        if result:
            return 1
        else:
            return 0
        
    def count_special_characters(self,url):
        special_characters = re.findall(r'[^a-zA-Z0-9]', url)
        return len(special_characters)
    
    def contains_hex_characters(self,url):
        hex_characters = re.findall(r'[0-9a-fA-F]', url)
        return 1 if hex_characters else 0
    
    def count_query_parameters(self,url):
        parsed_url = urlparse(url)
        query = parsed_url.query
        if query:
            return len(query.split('&'))
        else:
            return 0