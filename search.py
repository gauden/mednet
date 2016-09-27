from __future__ import print_function

import time
from Bio import Medline, Entrez

try:
    from StringIO import StringIO  # Python 2
except ImportError:
    from io import StringIO  # Python 3

try:
    import ConfigParser  # Python 2
except:
    import configparser as ConfigParser  # Python 3

try:
    config = ConfigParser.ConfigParser()
    config.read('config.cfg')
    Entrez.email = config.get('Entrez', 'email')
except ConfigParser.NoSectionError:
    print('Set up your email in a "config.cfg" file.')
    exit()


class Paper(object):

    fields = {'AB': 'Abstract',
              'CI': 'Copyright Information',
              'AD': 'Affiliation',
              'IRAD': 'Investigator Affiliation',
              'AID': 'Article Identifier',
              'AU': 'Author',
              'AUID': 'Author Identifier',
              'FAU': 'Full Author',
              'BTI': 'Book Title',
              'CTI': 'Collection Title',
              'CN': 'Corporate Author',
              'CRDT': 'Create Date',
              'DCOM': 'Date Completed',
              'DA': 'Date Created',
              'LR': 'Date Last Revised',
              'DEP': 'Date of Electronic Publication',
              'DP': 'Date of Publication',
              'EN': 'Edition',
              'FED': 'Full Editor Name',
              'ED': 'Editor Name',
              'EDAT': 'Entrez Date',
              'GS': 'Gene Symbol',
              'PG': 'Pagination',
              'PS': 'Personal Name as Subject',
              'FPS': 'Full Personal Name as Subject',
              'PL': 'Place of Publication',
              'PHST': 'Publication History Status',
              'PST': 'Publication Status',
              'PT': 'Publication Type',
              'PUBM': 'Publishing Model',
              'PMC': 'PubMed Central Identifier',
              'PMCR': 'PubMed Central Release',
              'PMID': 'PubMed Unique Identifier',
              'RN': 'Registry Number/EC Number',
              'NM': 'Substance Name',
              'SI': 'Secondary Source ID',
              'SO': 'Source',
              'SFM': 'Space Flight Mission',
              'STAT': 'Status',
              'SB': 'Subset',
              'TI': 'Title',
              'TT': 'Transliterated Title',
              'VI': 'Volume',
              'VTI': 'Volume Title',
              'GN': 'General Note',
              'GR': 'Grant Number',
              'IR': 'Investigator Name',
              'FIR': 'Full Investigator Name',
              'ISBN': 'ISBN',
              'IS': 'ISSN',
              'IP': 'Issue',
              'TA': 'Journal Title Abbreviation',
              'JT': 'Journal Title',
              'LA': 'Language',
              'LID': 'Location Identifier',
              'MID': 'Manuscript Identifier',
              'MHDA': 'MeSH Date',
              'MH': 'MeSH Terms',
              'JID': 'NLM Unique ID',
              'RF': 'Number of References',
              'OABL': 'Other Abstract Language',
              'OAB': 'Other Abstract',
              'OCI': 'Other Copyright Information',
              'OID': 'Other ID',
              'OT': 'Other Term',
              'OTO': 'Other Term Owner',
              'OWN': 'Owner'}

    def __init__(self, record):
        self.rec = record

    def __getattr__(self, attr):
        attr = attr.upper()
        if attr in self.rec:
            return self.rec[attr]
        else:
            return ''

    def __str__(self):
        return self.__make_str_rep(full=False)

    def __repr__(self):
        return self.__make_str_rep(full=True)

    def __make_str_rep(self, full=False):
        output = ''
        template = self.fields if full else self.rec
        for k, v in template.iteritems():
            if k in self.rec:
                output += '{}: {}\n'.format(k, self.rec[k])
            else:
                output += '{}: NIL ({})\n'.format(k, v)
        return output


class Search(object):

    batch_size = 100

    def __init__(self, term):
        self.term = term
        self.web_env, self.count, self.query_key = self._set_up_search()
        self.records = [Paper(rec)
                        for rec in self._retrieve_papers()]

    def _set_up_search(self):
        handle = Entrez.esearch(db="pubmed", term=self.term, usehistory="y")
        search_results = Entrez.read(handle)
        web_env = search_results["WebEnv"]
        query_key = search_results["QueryKey"]
        count = int(search_results["Count"])
        return (web_env, count, query_key)

    def _retrieve_papers(self):
        data = ''
        for start in range(0, self.count, self.batch_size):
            end = min(self.count, start + self.batch_size)
            fetch_handle = Entrez.efetch(db="pubmed", rettype="medline",
                                         retmode="text", retstart=start,
                                         retmax=self.batch_size,
                                         webenv=self.web_env,
                                         query_key=self.query_key)
            data += fetch_handle.read()
            fetch_handle.close()
        records = Medline.parse(StringIO(data))
        return records


if __name__ == '__main__':
    search = Search('Galea Gauden[Author]')

    for rec in search.records:
        # print(rec.au, rec.edat, rec.samizdat)
        print(rec)
        print(repr(rec))
        break

    print('Entrez email', Entrez.email)
    print('term', search.term)
    print('web_env', search.web_env)
    print('count', search.count)
    print('query_key', search.query_key)
