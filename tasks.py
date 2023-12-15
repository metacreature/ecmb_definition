import re, os
from invoke import task
from lxml import etree


def printError(msg):
	print('\033[1;31;40m \n  ' + msg + '\n \033[0m', flush=True)
	
def printSuccess(msg):
	print('\033[1;32;40m \n  ' + msg + '\n \033[0m', flush=True)

@task
def validate(ctx, xml_path):
	
	if not os.path.exists(xml_path):
		return printError('XML not found!')

	try:			
		xml_doc = etree.parse(xml_path)
		root = xml_doc.getroot()
		ecmb_version = root.get('version')
	except:
		return printError('This is not a valid XML!')

	if not ecmb_version or not re.match(r'^[1-9][0-9]*\.[0-9]+$', ecmb_version):
		return printError('Invalid eCMB version-number!')
	
	xsd_path = f'schema/ecmb-v{ecmb_version}.xsd'
	
	if not os.path.exists(xsd_path):
		return printError(f'XSD with version "{ecmb_version}" not found!')
	
	
	xmlschema_doc = etree.parse(xsd_path)
	xmlschema = etree.XMLSchema(xmlschema_doc)
	
	if xmlschema.validate(xml_doc):
		return printSuccess('eCMB-XML is valid!')
	else:
		return printError('eCMB-XML is invalid!')
	
