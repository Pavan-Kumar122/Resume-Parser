from __future__ import unicode_literals
import docx2txt
import re
import spacy
import nltk, os, subprocess, code, glob, traceback, inspect
import pandas as pd
import pdf_extract as rs

nlp = spacy.load('en_core_web_sm')
my_text = docx2txt.process("Prerana_Rath.docx")  # DOC TEXT
pdf_text = rs.convert("Rushikesh_Dixit_Resume.pdf")  # Pdf TEXT


class parse():
    def __init__(self):
        docx_file = glob.glob("docx_resume/*.docx")
        doc_file = glob.glob("docx_resume/*.doc")
        pdf_file = glob.glob("pdf_resume/*.pdf")
        text_file = glob.glob("resumes/*.txt")

        files = set(doc_file + docx_file + pdf_file + text_file)
        files = list(files)
        # print(files)
        print("%d files identified" % len(files))

        for f in files:
            self.readFile(f)

    def readFile(self, filename):
        extension = filename.split(".")[-1]
        # f = filename.split('.')[0]
        # print(f)
        if extension == "docx":
            print("doc file")
            doc_text = docx2txt.process(filename)
            self.candidate_name(doc_text)
            self.extract_email(doc_text)
            self.extract_linkedIn_link(doc_text)
            self.extract_number(doc_text)
            self.extract_skills1(doc_text)
        else:
            print("pdf file")
            text_pdf = rs.convert(filename)
            self.candidate_name(text_pdf)
            self.extract_email(text_pdf)
            self.extract_linkedIn_link(text_pdf)
            self.extract_number(text_pdf)
            self.extract_skills1(text_pdf)

    def candidate_name(self, filename):
        lines = []

        tokens = []
        sentences = []
        lines = [el.strip() for el in filename.split("\n") if len(el) > 0]
        lines = [nltk.word_tokenize(el) for el in lines]
        lines = [nltk.pos_tag(el) for el in lines]

        sentences = nltk.sent_tokenize(filename)  # Split/Tokenize into sentences (List of strings)
        sentences = [nltk.word_tokenize(sent) for sent in
                     sentences]  # Split/Tokenize sentences into words (List of lists of strings)
        tokens = sentences
        sentences = [nltk.pos_tag(sent) for sent in
                     sentences]  # Tag the tokens - list of lists of tuples - each tuple is (<word>, <tag>)
        dummy = []
        for el in tokens:
            dummy += el
        tokens = dummy

        indianNames = open("allNames.txt", "r").read().lower()

        indianNames = set(indianNames.split())

        otherNameHits = []
        nameHits = []
        name = None

        grammar = r'NAME: {<NN.*><NN.*><NN.*>*}'

        chunkParser = nltk.RegexpParser(grammar)

        all_chunked_tokens = []
        for tagged_tokens in lines:
            # Creates a parse tree
            if len(tagged_tokens) == 0: continue  # Prevent it from printing warnings
            chunked_tokens = chunkParser.parse(tagged_tokens)
            all_chunked_tokens.append(chunked_tokens)
            for subtree in chunked_tokens.subtrees():

                if subtree.label() == 'NAME':
                    for ind, leaf in enumerate(subtree.leaves()):
                        if leaf[0].lower() in indianNames and 'NN' in leaf[1]:
                            # Case insensitive matching, as indianNames have names in lowercase
                            # Take only noun-tagged tokens
                            # Surname is not in the name list, hence if match is achieved add all noun-type tokens
                            # Pick upto 3 noun entities
                            hit = " ".join([el[0] for el in subtree.leaves()[ind:ind + 3]])
                            # Check for the presence of commas, colons, digits - usually markers of non-named entities
                            if re.compile(r'[\d,:]').search(hit): continue
                            nameHits.append(hit)
                            # Need to iterate through rest of the leaves because of possible mis-matches
            # Going for the first name hit
            if len(nameHits) > 0:
                nameHits = [re.sub(r'[^aA-zZ \-]', '', el).strip() for el in nameHits]
                name = " ".join([el[0].upper() + el[1:].lower() for el in nameHits[0].split() if len(el) > 0])
        print(name)

    def extract_skills1(self, filename):
        nlp_text = nlp(filename)

        # removing stop words and implementing word tokenization
        tokens = [token.text for token in nlp_text if not token.is_stop]

        # reading the csv file
        data = pd.read_csv("skills.csv")

        # extract values
        skills = list(data.columns.values)

        skillset = []

        # check for one-grams (example: python)
        for token in tokens:
            if token.lower() in skills:
                skillset.append(token)

        # check for bi-grams and tri-grams (example: machine learning)
        for token in nlp_text.noun_chunks:
            token = token.text.lower().strip()
            if token in skills:
                skillset.append(token)

        print([i.capitalize() for i in set([i.lower() for i in skillset])])

    def extract_email(self, filename):
        extract_email = re.compile(r'\S+@\S+')  # pattern for email extraction

        print(extract_email.findall(filename))  # Email Extraction

    def extract_number(self, filename):
        extract_number = re.compile(r'[\+\(]?[0-9][0-9 .\-\(\)]{8,}[0-9]', re.VERBOSE)  # pattern for number extraction

        phone_numbers = extract_number.findall(filename)

        print(phone_numbers)  # number extraction

    def extract_linkedIn_link(self, filename):
        extract_linkedIn_link = re.compile(r'\S+linkedin\S+')  # pattern for linkedin extraction

        print(extract_linkedIn_link.findall(filename))  # LinkedIn profile Extraction


# parse()


def candidate_name(string):
    lines = []
    tokens = []
    sentences = []
    lines = [el.strip() for el in string.split("\n") if len(el) > 0]
    lines = [nltk.word_tokenize(el) for el in lines]
    lines = [nltk.pos_tag(el) for el in lines]

    sentences = nltk.sent_tokenize(string)  # Split/Tokenize into sentences (List of strings)
    sentences = [nltk.word_tokenize(sent) for sent in
                 sentences]  # Split/Tokenize sentences into words (List of lists of strings)
    tokens = sentences
    sentences = [nltk.pos_tag(sent) for sent in
                 sentences]  # Tag the tokens - list of lists of tuples - each tuple is (<word>, <tag>)
    dummy = []
    for el in tokens:
        dummy += el
    tokens = dummy

    indianNames = open("allNames.txt", "r").read().lower()
    # Lookup in a set is much faster
    indianNames = set(indianNames.split())

    otherNameHits = []
    nameHits = []
    name = None

    grammar = r'NAME: {<NN.*><NN.*><NN.*>*}'

    chunkParser = nltk.RegexpParser(grammar)

    all_chunked_tokens = []
    for tagged_tokens in lines:
        # Creates a parse tree
        if len(tagged_tokens) == 0: continue  # Prevent it from printing warnings
        chunked_tokens = chunkParser.parse(tagged_tokens)
        all_chunked_tokens.append(chunked_tokens)
        for subtree in chunked_tokens.subtrees():
            #  or subtree.label() == 'S' include in if condition if required
            if subtree.label() == 'NAME':
                for ind, leaf in enumerate(subtree.leaves()):
                    if leaf[0].lower() in indianNames and 'NN' in leaf[1]:
                        # Case insensitive matching, as indianNames have names in lowercase
                        # Take only noun-tagged tokens
                        # Surname is not in the name list, hence if match is achieved add all noun-type tokens
                        # Pick upto 3 noun entities
                        hit = " ".join([el[0] for el in subtree.leaves()[ind:ind + 3]])
                        # Check for the presence of commas, colons, digits - usually markers of non-named entities
                        if re.compile(r'[\d,:]').search(hit): continue
                        nameHits.append(hit)
                        # Need to iterate through rest of the leaves because of possible mis-matches
        # Going for the first name hit
        if len(nameHits) > 0:
            nameHits = [re.sub(r'[^aA-zZ \-]', '', el).strip() for el in nameHits]
            name = " ".join([el[0].upper() + el[1:].lower() for el in nameHits[0].split() if len(el) > 0])
            otherNameHits = nameHits[1:]
    #    infoDict['name'] = name
    #    infoDict['otherNameHits'] = otherNameHits
    #
    #    if debug:
    #        print("\n", pprint(infoDict), "\n")
    #        code.interact(local=locals())
    # print(name, otherNameHits)
    print(name)


candidate_name(my_text)


def extract_skills1(resume_text):
    nlp_text = nlp(resume_text)

    # removing stop words and implementing word tokenization
    tokens = [token.text for token in nlp_text if not token.is_stop]

    # reading the csv file
    data = pd.read_csv("skills.csv")

    # extract values
    skills = list(data.columns.values)

    skillset = []

    # check for one-grams (example: python)
    for token in tokens:
        if token.lower() in skills:
            skillset.append(token)

    # check for bi-grams and tri-grams (example: machine learning)
    for token in nlp_text.noun_chunks:
        token = token.text.lower().strip()
        if token in skills:
            skillset.append(token)

    print([i.capitalize() for i in set([i.lower() for i in skillset])])

print("SKILL SET")
extract_skills1(my_text)

extract_email = re.compile(r'\S+@\S+')  # pattern for email extraction

extract_linkedIn_link = re.compile(r'\S+linkedin\S+')  # pattern for linkedin extraction

extract_number = re.compile(r'[\+\(]?[0-9][0-9 .\-\(\)]{8,}[0-9]', re.VERBOSE)  # pattern for number extraction

phone_numbers = extract_number.findall(my_text)

print(phone_numbers)  # number extraction

print(extract_email.findall(my_text))  # Email Extraction

print(extract_linkedIn_link.findall(my_text))  # LinkedIn profile Extraction
