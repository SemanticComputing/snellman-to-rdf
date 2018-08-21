import xml.etree.ElementTree as ET

def read():
    for event, elem in ET.iterparse('export.xml', events=("start", "end")):
        if event == 'end':
            if elem.tag == 'node':
                if elem.find('type').text == 'matrikkeli':
                    reku(elem)


def reku(elem):
    for child in elem:
        try:
            print(child.tag, child.attrib, child.text)
        except:
            pass
        reku(child)

read()
