import xml.etree.ElementTree as ET
from rdflib import Graph, Literal, namespace, Namespace, XSD, URIRef

snellman = Namespace('http://ldf.fi/snellman/')


def create_bio_table_row(elem, bio_list):
    row_list = []
    name = elem.find('title').text
    start, end = name.split('–')
    s_year, s_month = date(start)
    e_year, e_month = date(end)
    path = elem.find('path')
    row_list.append(path.find('alias').text)
    row_list.append(s_year)
    row_list.append(s_month)
    row_list.append(e_year)
    row_list.append(e_month)
    row_list.append(elem.find('nid').text)
    bio_list.append(row_list)

def make_table(bio_list):
    for event, elem in ET.iterparse('export.xml', events=("start", "end")):
        if event == 'end':
            if elem.tag == 'node':
                if elem.find('type').text == 'matrikkeli':
                    create_bio_table_row(elem, bio_list)

def date(date):
    month, year = date.strip().split(' ')
    month_number = month_to_number(month)
    return year, month_number

def month_to_number(month):
    if month == 'TAMMIKUU':
        return '01'
    if month == 'HELMIKUU':
        return '02'
    if month == 'MAALISKUU':
        return '03'
    if month == 'HUHTIKUU':
        return '04'
    if month == 'TOUKOKUU':
        return '05'
    if month == 'KESÄKUU':
        return '06'
    if month == 'HEINÄKUU':
        return '07'
    if month == 'ELOKUU':
        return '08'
    if month == 'SYYSKUU':
        return '09'
    if month == 'LOKAKUU':
        return '10'
    if month == 'MARRASKUU':
        return '11'
    if month == 'JOULUKUU':
        return '12'


