import re, os
from invoke import task
from lxml import etree
from ecmb_validator import ecmbValidator


def printError(msg):
	print('\033[1;31;40m  ERROR: ' + msg + '\033[0m', flush=True)
	
def printSuccess(msg):
	print('\033[1;32;40m  ' + msg + '\033[0m', flush=True)


@task
def validate(ctx, file_name):

	validator_obj = ecmbValidator(printError)
	
	print('\n', flush=True)

	if validator_obj.validate(file_name):
		printSuccess('File is valid!')

	print('\n', flush=True)