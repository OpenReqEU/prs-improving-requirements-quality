# -*- coding: utf-8 -*-

# Functionality imports
import datetime
from collections import defaultdict
import spacy
import json
import re
from nltk.corpus import wordnet as wn
wn.ensure_loaded()


class RequirementChecker:

    LITERATURE_DICT = {
        "NOVEL1" : {
            "Title": "",
            "Authors": "",
            "Order": 0
        },
        "NOVEL2" : {
            "Title": "",
            "Authors": "",
            "Order": 1
        },
        "YWRN10" : {
                    "Title": "Automatic detection of nocuous coordination ambiguities in natural language requirements",
                    "Authors": "Hui Yang, Alistair Willis, Anne N. De Roeck, B. Nuseibeh",
                    "Order": 2
        },
        "FFJK14" : {
                    "Title": "Rapid Requirements Checks with Requirements Smells: Two Case Studies",
                    "Authors": "Henning Femmer, Daniel Méndez Fernándeza, Elmar Juergens, Michael Klose, Ilona Zimmer, Jörg Zimmer",
                    "Order": 3
        },
        "XLLS11" : {
                    "Title": "Mining comparative opinions from customer reviews for Competitive Intelligence",
                    "Authors": "Kaiquan Xu, Stephen Shaoyi Liao, Jiexun Li, Yuxia Song",
                    "Order": 4
        },
        "GCK10" : {
                    "Title": "Ambiguity Detection: Towards a Tool Explaining Ambiguity Sources",
                    "Authors": "Benedikt Gleich, Oliver Creighton, Leonid Kof",
                    "Order": 5
        },
        "TB13" : {
                    "Title": "The Design of SREE — A Prototype Potential Ambiguity Finder for Requirements Specifications and Lessons Learned",
                    "Authors": "Sri Fatimah Tjong, Daniel M. Berry",
                    "Order": 6
        }
    }

    LEXICON_LOCATION = './app/lexicons'

    def __init__(self, reqs, config=None):
        self.reqs = reqs
        self.config = config if config else {}
        self.nlp = spacy.load('en')

    def check_lexical(self):
        def whole_word_regexp(w):
            # Handle spaces in strings
            w = w.replace(' ', '\s')

            try:
                return re.compile(r'\b{0}\b'.format(w), flags=re.I|re.X)
            except re.error:
                return re.compile(r'\b\{0}\b'.format(w), flags=re.I|re.X)

        # Load lexical lexicon
        amb_lex = json.load(open(f'{self.LEXICON_LOCATION}/ambiguity_lexicon.json', encoding = 'utf-8'))

        # Find and save ambiguities
        ambs_found = {}
        # For each requirement sent
        for req_i, req in enumerate(self.reqs):
            # if req_i % 500 == 0:
            #     print(f'check_lexical: {req_i} of {len(self.reqs)} at {str(datetime.datetime.now()).split(".")[0]}')
            ambs_found[req.id] = []
            # Go over all phrases in lexicon
            for _, amb_obj in amb_lex.items():
                # Go over all phrases in lexicon
                for word_phrase in amb_obj['lexicon']:
                    # Search for all word phrases in requirement
                    for match in re.finditer(whole_word_regexp(word_phrase), req.text):
                        ambs_found[req.id].append(self._get_ambiguity_object(amb_obj, match))
        return ambs_found

    def check_regexs(self):

        # Load ambiguity regex JSON document
        amb_regexes = json.load(open(f'{self.LEXICON_LOCATION}/ambiguity_regexs.json', encoding = 'utf-8'))

        # Find and save ambiguities
        ambs_found = {}
        # For each requirement sent
        for req_i, req in enumerate(self.reqs):
            # if req_i % 500 == 0:
            #     print(f'check_regexs: {req_i} of {len(self.reqs)} at {str(datetime.datetime.now()).split(".")[0]}')
            ambs_found[req.id] = []
            # Go over all regular expressions in lexicon
            for _, amb_obj in amb_regexes.items():

                # TODO: Add split for sentences since the regular expressions are expecting single sentences.

                # Create Python regular expression object
                regexp = re.compile(amb_obj['regexp'], flags=re.I|re.X)
                # Search for all regexps in requirement
                for match in re.finditer(regexp, req.text):
                    ambs_found[req.id].append(self._get_ambiguity_object(amb_obj, match))
        return ambs_found

    def check_pos_regexs(self):
        def convert_to_truple(token):
            return "{0}°{1}°{2}".format(token.text, token.tag_, token.lemma_)

        # Get the original indexes, before the truple design messed with it
        def get_original_indexes(req_original_string, req_tokenized_string, req_truple_string, match):
            # Add up extra letters (indexes) due to truple design
            def count_extra_indexes(up_to_index):
                # Count the extra letters in a given truple
                def count_extra_letters(req_truple):
                    try:
                        split = req_truple.split('°')
                        return len(split[1]) + len(split[2]) + 2
                    except:
                        # TODO Needs investigation on the visualization of this change. If the above fails, something still needs to be fixed
                        return 0

                # Calculate space added by tokenization process
                def count_tokenize_space(req_original_string, req_tokenized_string):
                    orig_i = 0
                    tokn_i = 0
                    while tokn_i < len(req_tokenized_string):
                        if req_original_string[orig_i] != req_tokenized_string[tokn_i]:
                            tokn_i += 1
                            continue
                        orig_i += 1
                        tokn_i += 1
                    return tokn_i - orig_i

                # Remove string after the index
                words_pre_index = req_truple_string[:up_to_index].split()
                # Calculate extra indexes added by the truple system
                extra_truple_indexes = sum([count_extra_letters(req_truple) for req_truple in words_pre_index])
                # Update the 'up_to_index' to reflect the newly discovered mistakes
                up_to_index = up_to_index - extra_truple_indexes
                # Calculate the extra indexes added by the tokenizing process
                extra_tokenize_space = count_tokenize_space(req_original_string[:up_to_index], req_tokenized_string[:up_to_index])

                return extra_truple_indexes + extra_tokenize_space
            return (
                match.start() - count_extra_indexes(match.start()),
                match.end() - count_extra_indexes(match.end()))

        # Load ambiguity pos regex JSON document
        amb_pos_regexps = json.load(open(f'{self.LEXICON_LOCATION}/ambiguity_pos_regexs.json', encoding = 'utf-8'))

        # Find and save ambiguities
        ambs_found = {}
        # For each requirement sent
        for req_i, req in enumerate(self.reqs):
            # print(f'check_pos_regexs: {req_i} of {len(self.reqs)} at {str(datetime.datetime.now()).split(".")[0]}')
            ambs_found[req.id] = []
            # Convert requirement into nlp doc
            doc = self.nlp(req.text)
            # Create list of truples strings (word, POS tag, lemma) with degree symbol in between each part
            truple_list = [convert_to_truple(token) for token in doc]

            # Create variables for easier and more readable use later
            req_original_string = req.text
            req_tokenized_string = ' '.join([token.text for token in doc])
            req_truple_string = ' '.join(truple_list)  # Convert into string so regex can be performed

            # TODO: Add split for sentences since the regular expressions are expecting single sentences.

            # Check against each regular expression in the lexicon
            for _, amb_obj in amb_pos_regexps.items():
                # Create Python regular expression object
                regexp = re.compile(amb_obj['regexp'], flags=re.I|re.X)
                # Search for all regexps in requirement
                for match in re.finditer(regexp, req_truple_string):
                    # Get the original indexes, since the truple string design messes with them
                    orig_indexes = get_original_indexes(
                        req_original_string, req_tokenized_string, req_truple_string, match)

                    orig_text = ' '.join([req_truple.split('°')[0] for req_truple in match[0].split()])
                    # Save this found ambiguity
                    ambs_found[req.id].append(self._get_ambiguity_object(
                        amb_obj, match,
                        new_text=orig_text,
                        new_indexes=orig_indexes))
        return ambs_found

    def check_compound(self):

        # Load lexical lexicon
        amb_lex = json.load(open(f'{self.LEXICON_LOCATION}/ambiguity_compounds.json', encoding = 'utf-8'))

        # Find and save ambiguities
        ambs_found = {}
        # For each requirement sent
        for req_i, req in enumerate(self.reqs):
            # if req_i % 500 == 0:
            #     print(f'check_compound: {req_i} of {len(self.reqs)} at {str(datetime.datetime.now()).split(".")[0]}')
            ambs_found[req.id] = []
            # Convert requirement into nlp doc
            doc = self.nlp(req.text)
            # Go over all phrases in lexicon
            for _, amb_obj in amb_lex.items():
                for chunk in doc.noun_chunks:
                    compound_list = [token for token in chunk if (token.dep_ == 'compound')
                                         or (token.tag_ in ('NN', 'NNS', 'NNP', 'NNPS') and token.dep_ in ('nmod', 'amod'))
                                         or (token.tag_ == 'VBG' and token.dep_ == 'nmod')
                                         or token == chunk.root]
                    if len(compound_list) > 2:
                        new_text = ' '.join([t.text for t in compound_list])
                        new_indexes = [compound_list[0].idx, compound_list[-1].idx + len(compound_list[-1].text)]
                        ambs_found[req.id].append(self._get_ambiguity_object(amb_obj, new_text=new_text, new_indexes=new_indexes))
        return ambs_found

    def check_nominalization(self):

        # Load nominalization suffix lexicon
        amb_nom = json.load(open(f'{self.LEXICON_LOCATION}/ambiguity_nominalization.json', encoding = "utf-8"))

        # Find and save ambiguities
        ambs_found = {}
        # For each requirement sent
        for req_i, req in enumerate(self.reqs):
            # if req_i % 500 == 0:
            #     print(f'check_nominalization: {req_i} of {len(self.reqs)} at {str(datetime.datetime.now()).split(".")[0]}')
            ambs_found[req.id] = []
            # Go over all phrases in lexicon
            for _, amb_obj in amb_nom.items():
                # Convert requirement into nlp doc
                doc = self.nlp(req.text)
                # Generate a list of gerund nouminalizations that have pos VB
                nominalizations = [[t for t in token.subtree] for token in doc
                                   if(token.text[-3:] in amb_obj['gerund']
                                      or token.text[-4:] in amb_obj['gerund_plural'])
                                     and token.tag_ == 'VBG'
                                     and token.dep_ not in ('root', 'aux', 'advmod', 'compound', 'acl')
                                     and doc[token.i - 1].dep_ != 'aux'
                                     and token.text.lower() not in amb_obj['rule_exceptions']]

                # Generate a list of nominalizations with pos NN based on suffixes
                nouns = [token for token in doc if (token.lemma_[-4:] in amb_obj['suffixes_len4']
                                                    or token.lemma_[-3:] in amb_obj['suffixes_len3']
                                                    or token.lemma_[-2:] in amb_obj['suffixes_len2'])
                         and token.tag_ in ('NN', 'NNS')
                         and wn.synsets(token.text)]
                # Filter list of nouns based on semantic hierarchy
                for token in nouns:
                    # Generate and flatten the list of hypernyms for each noun
                    hypernyms = list(
                        map(lambda x: x.name().split('.')[0],
                            sum(wn.synsets(token.text)[0].hypernym_paths(), [])))
                    # Only consider nouns that express an event or a process
                    if [l for l in hypernyms if l in ['event', 'process', 'act']] \
                            and token.text.lower() not in amb_obj['rule_exceptions']:
                        nominalizations.append([t for t in token.subtree])

                # Return all ambiguous nominalization sequences found
                for token_seq in nominalizations:
                    if token_seq:
                        new_text = ' '.join([t.text for t in token_seq])
                        new_indexes = [token_seq[0].idx, token_seq[-1].idx + len(token_seq[-1].text)]
                        ambs_found[req.id].append(
                            self._get_ambiguity_object(amb_obj, new_text=new_text, new_indexes=new_indexes))
        return ambs_found

    def check_quality(self):

        def combine_ambs_found(all_ambs_found):
            combined_ambs_found = defaultdict(list)
            # For each result returned by a different API
            for ambs_found in all_ambs_found:
                # For each requirement
                for req_id, amb in ambs_found.items():
                    combined_ambs_found[req_id].extend(amb)
            # Sort the internal lists, and return the final list
            return {k:sorted(v, key=lambda key: key['index_start']) for k,v in combined_ambs_found.items()}

        # Algorithms to run
        algs_to_run = [
            self.check_lexical,
            self.check_regexs,
            self.check_pos_regexs,
            self.check_compound,
            self.check_nominalization
        ]

        # Curate algorithms based on the config, if it has been set
        if 'algorithms' in self.config:
            algorithms = self.config['algorithms']
            if 'Lexical' not in algorithms:
                algs_to_run.remove(self.check_lexical)
            if 'RegularExpressions' not in algorithms:
                algs_to_run.remove(self.check_regexs)
            if 'POSRegularExpressions' not in algorithms:
                algs_to_run.remove(self.check_pos_regexs)
            if 'CompoundNouns' not in algorithms:
                algs_to_run.remove(self.check_compound)
            if 'Nominalization' not in algorithms:
                algs_to_run.remove(self.check_nominalization)

        # Run all of the algorithms
        ambs_found = [alg() for alg in algs_to_run]

        return combine_ambs_found(ambs_found)

    def _get_ambiguity_object(self, amb_obj, regex_match=None, *, new_text=None, new_indexes=None):
        return {
            "title"             : amb_obj['title'],
            "description"       : amb_obj['description'],
            "language_construct": amb_obj['language_construct'],
            "text"              : new_text if new_text else regex_match[0],
            "index_start"       : new_indexes[0] if new_indexes else regex_match.start(),
            "index_end"         : new_indexes[1] if new_indexes else regex_match.end()
        }

