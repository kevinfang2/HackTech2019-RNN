from bs4 import BeautifulSoup
from requests import get
import shutil
import urllib.request
import re

baseUrl = 'https://en.wikipedia.org/wiki/'

def subCatDict(page: str) -> {str:[str]}:
    response = get(page)
    html_soup = BeautifulSoup(response.text, 'html.parser')
    pageText = html_soup.findAll(['span', 'a'])
    #print(pageText)
    allConnects = allConnections(page)
    #print(len(allConnects), len(pageText))
    numBefore = 0
    h2 = None
    relations = {h2: []}
    while len(pageText) > 0:
        while str(pageText[0])[1:3] != 'sp':
            numBefore += 1
            #print(numBefore)
            pageText = pageText[1:]
            if len(pageText) == 0:
                break
        relations[h2] = allConnects[:numBefore]
        allConnects = allConnects[numBefore:]
        if len(pageText) == 0:
            break
        h2 = str(pageText[0])[str(pageText[0]).index('>')+1:str(pageText[0]).rfind('<')]
        relations[h2] = []
        numBefore =0
        pageText = pageText[1:]

    for key in list(relations.keys()):
        if len(relations[key]) == 0:
            del relations[key]
        elif '<' in str(key):
            del relations[key]
        elif key == None:
            del relations[key]
        elif key == 'More':
            del relations[key]
        elif '(UTC)' in key:
            del relations[key]

    return relations

def allConnections(page: str) -> [str]:
    response = get(page)
    html_soup = BeautifulSoup(response.text, 'html.parser')
    urls = []
    for a in html_soup.find_all('a', href=True):
        urls.append(a['href'])
    return urls

def intersect(a: list, b: list) -> list:
    return list(set(a) & set(b))

def findBestSpan(relations: {str:[str]}, links: [str]):
    for key in relations:
        relations[key] = len(intersect(relations[key], links))
    return relations

def getBestSpan(span:{str:int}) -> str:
    string = ''
    for key in span:
        if string not in span or span[key] > span[string]:
            string = key
    return string

def getBestSection(span: str, url: str) -> str:
    response = get(url)
    html_soup = BeautifulSoup(response.text, 'html.parser')
    pageText = html_soup.findAll(['span', 'h2'])
    h2 = None
    while len(pageText) > 0:
        if span in str(pageText[0]):
            h2 = str(pageText[0])[str(pageText[0]).index('>')+1:str(pageText[0]).rfind('<')]
            return h2
        if str(pageText[0])[1:3] == 'h2':
            h2 = str(pageText[0])[str(pageText[0]).index('>')+1:str(pageText[0]).rfind('<')]

        pageText = pageText[1:]

def getParagraph(h2: str, url: str) -> str:
    regex = r'<[^>]*>'
    regex1 = r'\[\d*\]'
    response = get(url)
    html_soup = BeautifulSoup(response.text, 'html.parser')
    pageText = html_soup.findAll(['p', 'h2'])
    #incase = html._soup.findAll('p')
    p = None
    returnNext = False
    backup = None
    while len(pageText) > 0:
        if h2 in str(pageText[0]):
            returnNext = True
        elif 'h2' in str(pageText[0]) and backup == None:
            for i in range(1,len(pageText)):
                if '<p' in str(pageText[i]):
                    backup = str(pageText[i]) if backup == None else backup
        elif returnNext:
            return re.sub(regex1, '',re.sub(regex,'',str(pageText[0])))
        pageText = pageText[1:]


    return re.sub(regex1, '',re.sub(regex,'',backup))

def keyWords(paragraph: str) -> str:
    regex = r'[^\da-zA-Z ]'
    commonWords = getCommon('commonWord.txt')
    words = re.sub(regex, '', paragraph).lower().split()
    adjustParagraph = ''
    for word in words:
        if word not in commonWords:
            adjustParagraph += (word + ' ')
    return adjustParagraph[:-1]

def getCommon(commonWords: str) -> [str]:
    words = []
    with open(commonWords,'r') as infile:
         for line in infile.readlines():
             words.append(line.strip())
    return words
