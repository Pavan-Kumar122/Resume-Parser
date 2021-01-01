from __future__ import unicode_literals
import docx2txt
import re
import spacy
import nltk, os, subprocess, code, glob, traceback, inspect
from pprint import pprint
from docx import Document
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
import pandas as pd
import constants as cs
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from spacy.matcher import Matcher
import resumeparser as rs

nlp = spacy.load('en_core_web_sm')
# my_text = docx2txt.process("Rushi.docx")  # DOC TEXT

# pdf_text = rs.resume_string  # Pdf TEXT


# print(pdf_text)

#
# class Get_Data():
#
#     def __init__(self):
#         self.__matcher = Matcher(nlp.vocab)
#         print("Extracting Started")
#
#         docx_file = glob.glob("docx_resume/*.docx")
#         doc_file = glob.glob("docx_resume/*.doc")
#         pdf_file = glob.glob("pdf_resume/*.pdf")
#         text_file = glob.glob("resumes/*.txt")
#
#         # if pdf_file:
#         #     print(pdf_text)
#
#         files = set(doc_file + docx_file + pdf_file + text_file)
#         files = list(files)
#         print("%d files identified" % len(files))
#         # print(files)
#         for f in files:
#             print("File Name :-", f)
#             self.filename = self.readFile(f)
#             # print(self.filename)
#             self.extract_candidate_name(self.filename)
#             # self.extract_candidate_email(self.filename)
#             # self.extract_candidate_linkedIN_link(self.filename)
#             # self.extract_candidate_number(self.filename)
#             # self.extract_candidate_skills(self.filename)
#             print("#########################################")
#
#     def readFile(self, fileName):
#         '''
#         Read a file given its name as a string.
#         Modules required: os
#         UNIX packages required: antiword, ps2ascii
#         '''
#         extension = fileName.split(".")[-1]
#         if extension == "txt":
#             f = open(fileName, 'r')
#             string = f.read()
#             f.close()
#             return string, extension
#         elif extension == "doc":
#             # Run a shell command and store the output as a string
#             # Antiword is used for extracting data out of Word docs. Does not work with docx, pdf etc.
#             return \
#                 subprocess.Popen(['antiword', fileName], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[
#                     0], extension
#         elif extension == "docx":
#             try:
#                 temp = docx2txt.process(fileName)
#                 text_doc_files = [line.replace('\t', ' ') for line in temp.split('\n') if line]
#                 text_doc_files = ' '.join(text_doc_files)
#                 text_doc_files = ' '.join(text_doc_files.split())
#                 text_doc_files = nlp(text_doc_files)
#                 # print(text_files)
#                 return text_doc_files, extension
#             except:
#                 return ''
#                 pass
#         # elif extension == "rtf":
#         #    try:
#         #        return convertRtfToText(fileName), extension
#         #    except:
#         #        return ''
#         #        pass
#         elif extension == "pdf":
#             # ps2ascii converst pdf to ascii text
#             # May have a potential formatting loss for unicode characters
#             # return os.system(("ps2ascii %s") (fileName))
#             try:
#                 # pdf_f = rs.convert(fileName)
#                 # print(pdf_f)
#                 return rs.convertPDFToText(fileName), extension
#             except:
#                 return ''
#                 pass
#         else:
#             print('Unsupported format')
#             return '', ''
#
#     def extract_candidate_name(self, filename):
#         # filename = str(filename)
#         rs.extract_name(filename, matcher=self.__matcher)
#
#     # def extract_candidate_number(self, filename):
#     #     # filename = str(filename)
#     #     # filename.replace('\n', '')
#     #     extract_number = re.compile(r'[\+\(]?[0-9][0-9 .\-\(\)]{8,}[0-9]', re.VERBOSE)  # pattern for number extraction
#     #
#     #     phone_numbers = extract_number.findall(filename)
#     #
#     #     print(phone_numbers)
#     #
#     # def extract_candidate_email(self, filename):
#     #     # filename = str(filename)
#     #     # filename.replace('\n', '')
#     #     extract_email = re.compile(r'\S+@\S+')  # pattern for email extraction
#     #
#     #     print(extract_email.findall(filename))  # Email Extraction
#     #
#     # def extract_candidate_linkedIN_link(self, filename):
#     #     # filename = str(filename)
#     #     # filename.replace('\n', '')
#     #     extract_linkedIn_link = re.compile(r'\S+linkedin\S+')  # pattern for linkedin extraction
#     #
#     #     print(extract_linkedIn_link.findall(filename))  # LinkedIn profile Extraction
#     #
#     # def extract_candidate_skills(self, filename):
#     #     # filename = str(filename)
#     #     rs.extract_skills1(filename)
#
#
# Get_Data()
# docx_file = glob.glob("docx_resume/*.docx")
# doc_file = glob.glob("docx_resume/*.doc")
# pdf_file = glob.glob("pdf_resume/*.pdf")
# text_file = glob.glob("resumes/*.txt")
#
# files = set(doc_file + docx_file + pdf_file + text_file)
# files = list(files)
# # print(files)
# print("%d files identified" % len(files))

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

        # for i in range(len(phone_numbers)):
            #     print(phone_numbers[i])
        #     if (i >= 1):
        #         break

        print(phone_numbers)  # number extraction

    def extract_linkedIn_link(self, filename):
        extract_linkedIn_link = re.compile(r'\S+linkedin\S+')  # pattern for linkedin extraction

        print(extract_linkedIn_link.findall(filename))  # LinkedIn profile Extraction


parse()


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


# candidate_name(my_text)


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

# print("SKILL SET")
# extract_skills1(my_text)

# For education details
#
# STOPWORDS = set(stopwords.words('english'))
#
# # Education Degrees
# EDUCATION = [
#     'BE', 'B.E.', 'B.E', 'BS', 'B.S',
#     'ME', 'M.E', 'M.E.', 'MS', 'M.S',
#     'BTECH', 'B.TECH', 'M.TECH', 'MTECH',
#     'SSC', 'HSC', 'CBSE', 'ICSE', 'X', 'XII'
# ]
#
#
# def extract_education(resume_text):
#     nlp_text = nlp(resume_text)
#
#     # Sentence Tokenizer
#     nlp_text = [sent.string.strip() for sent in nlp_text.sents]
#
#     edu = {}
#     # Extract education degree
#     for index, text in enumerate(nlp_text):
#         for tex in text.split():
#             # Replace all special symbols
#             tex = re.sub(r'[?|$|.|!|,]', r'', tex)
#             if tex.upper() in EDUCATION and tex not in STOPWORDS:
#                 edu[tex] = text + nlp_text[index + 1]
#
#     # Extract year
#     education = []
#     for key in edu.keys():
#         year = re.search(re.compile(r'(((20|19)(\d{2})))'), edu[key])
#         if year:
#             education.append((key, ''.join(year[0])))
#         else:
#             education.append(key)
#     print(education)
#
#
# print("Education Details")
# extract_education(pdf_text)

# For Experience Extraction
#
# def extract_experience(resume_text):
#     '''
#     Helper function to extract experience from resume text
#     :param resume_text: Plain resume text
#     :return: list of experience
#     '''
#     wordnet_lemmatizer = WordNetLemmatizer()
#     stop_words = set(stopwords.words('english'))
#
#     # word tokenization
#     word_tokens = nltk.word_tokenize(resume_text)
#
#     # remove stop words and lemmatize
#     filtered_sentence = [w for w in word_tokens if
#                          not w in stop_words and wordnet_lemmatizer.lemmatize(w) not in stop_words]
#     sent = nltk.pos_tag(filtered_sentence)
#
#     # parse regex
#     cp = nltk.RegexpParser('P: {<NNP>+}')
#     cs = cp.parse(sent)
#
#     # for i in cs.subtrees(filter=lambda x: x.label() == 'P'):
#     #     print(i)
#
#     test = []
#
#     for vp in list(cs.subtrees(filter=lambda x: x.label() == 'P')):
#         test.append(" ".join([i[0] for i in vp.leaves() if len(vp.leaves()) >= 2]))
#
#     # Search the word 'experience' in the chunk and then print out the text after it
#     x = [x[x.lower().index('experience') + 10:] for i, x in enumerate(test) if x and 'experience' in x.lower()]
#     print(x)
#
#
# extract_experience(pdf_text)
#
# extract_email = re.compile(r'\S+@\S+')  # pattern for email extraction
#
# extract_linkedIn_link = re.compile(r'\S+linkedin\S+')  # pattern for linkedin extraction
#
# extract_number = re.compile(r'[\+\(]?[0-9][0-9 .\-\(\)]{8,}[0-9]', re.VERBOSE)  # pattern for number extraction
#
# phone_numbers = extract_number.findall(pdf_text)
#
# print(phone_numbers)  # number extraction
#
# print(extract_email.findall(my_text))  # Email Extraction
#
# print(extract_linkedIn_link.findall(my_text))  # LinkedIn profile Extraction
