# -*- coding: utf-8 -*-

import BeautifulSoup as bs
import codecs

"""
Code to read the results page and generate a record with the votes for each canadidate in that district.


breadcrumb:
	div id='literalsubtitulo'

tables:
	tablamesashabilitadas		-	number of electores / juntas
	tablaSuf					-	present / absent
	tablaBlancosNulos			-	blank / null
	tablaCandi					-	scores for each candidate


f = codecs.open('test.txt','w','utf-8')
f.write(data)
f.close()

"""



def get_district(soup):
	""" Follow breadcrumb to correctly label district. """
	trail = ''

	div = soup.find(lambda tag: tag.name=='div' and tag.has_key('id') and tag['id']=='literalsubtitulo')
	if div:
		crumbs = div.text.split('&gt;')
		for crumb in crumbs:
			trail = trail + '_'.join(crumb.strip().split()) + '__'
	return trail



def get_electores(soup):
	""" Get number of electores. """

	table = soup.find(lambda tag: tag.name=='table' and tag.has_key('id') and tag['id']=="tablamesashabilitadas")
	rows = table.findAll(lambda tag: tag.name=='tr')

	# Row 1 has electores, Row 2 has juntas
	elecdata = dict()
	elecdata['elect_H'] = rows[1].find(lambda tag: tag.has_key('id') and tag['id']=='lblNumEle_H').text
	elecdata['elect_M'] = rows[1].find(lambda tag: tag.has_key('id') and tag['id']=='lblNumEle_M').text
	elecdata['junta_H'] = rows[2].find(lambda tag: tag.has_key('id') and tag['id']=='lblNumJun_H').text
	elecdata['junta_M'] = rows[2].find(lambda tag: tag.has_key('id') and tag['id']=='lblNumJun_M').text

	# convert to numeric
	for k,v in elecdata.iteritems():
		elecdata[k] = ''.join(v.split('.'))

	return elecdata


def get_suf(soup):

	# Find correct table
	table = soup.find(lambda tag: tag.name=='table' and tag.has_key('id') and tag['id']=="tablaSuf")
	rows = table.findAll(lambda tag: tag.name=='tr')

	# Extract data (row0 is header, row1 is Voters, row2 is Absent)
	sufdata = dict()
	sufdata['sufH'] = rows[1].find(lambda tag: tag.has_key('id') and tag['id']=='lblNumSufH').text
	sufdata['sufM'] = rows[1].find(lambda tag: tag.has_key('id') and tag['id']=='lblNumSufM').text
	sufdata['ausH'] = rows[2].find(lambda tag: tag.has_key('id') and tag['id']=='lblNumAusH').text
	sufdata['ausM'] = rows[2].find(lambda tag: tag.has_key('id') and tag['id']=='lblNumAusM').text

	# convert to numeric
	for k,v in sufdata.iteritems():
		sufdata[k] = ''.join(v.split('.'))

	return sufdata



def get_bad(soup):

	# Find correct table
	table = soup.find(lambda tag: tag.name=='table' and tag.has_key('id') and tag['id']=="tablaBlancosNulos")
	rows = table.findAll(lambda tag: tag.name=='tr')

	# Extract data (row0 is header, row1 is Blancos, row2 is Nullos)
	baddata = dict()
	baddata['blancoH'] = rows[1].find(lambda tag: tag.has_key('id') and tag['id']=='lblNumTotBlH').text
	baddata['blancoM'] = rows[1].find(lambda tag: tag.has_key('id') and tag['id']=='lblNumTotBlM').text
	baddata['nulloH'] = rows[2].find(lambda tag: tag.has_key('id') and tag['id']=='lblNumTotNulH').text
	baddata['nulloM'] = rows[2].find(lambda tag: tag.has_key('id') and tag['id']=='lblNumTotNulM').text

	# convert to numeric
	for k,v in baddata.iteritems():
		baddata[k] = ''.join(v.split('.'))

	return baddata



def get_scores(soup):

	table = soup.find(lambda tag: tag.name=='table' and tag.has_key('id') and tag['id']=="tablaCandi")

	# if table was found
	scores = None
	if table:
		rows = table.findAll(lambda tag: tag.name=='tr')

		# Extract data
		scores = dict()
		nombres = list()
		for row in rows[1:]:   # first row is header
			cols = row.findAll(lambda tag: tag.name=='td')

			# col 1 is Name, col 2/4/6 are total/hombres/mujers
			nombre = '_'.join(cols[1].text.split())
			nombres.append(nombre)
			scores[nombre]        = ''.join(cols[2].text.split('.'))
			scores[nombre + '_H'] = ''.join(cols[4].text.split('.'))
			scores[nombre + '_M'] = ''.join(cols[6].text.split('.'))

			try:
				assert int(scores[nombre]) == int(scores[nombre + '_H']) + int(scores[nombre + '_M'])
			except AssertionError:
				print scores
	return scores, nombres


def make_record(soup, fileout='parsedResult.csv'):

	nombres = [	'ABDALA_BUCARAM',
				'CYNTHIA_VITERI_JIMENEZ',
				'GUILLERMO_LASSO',
				'IVAN_ESPINEL_MOLINA',
				'LENÍN_MORENO_GARCÉS',
				'PACO_MONCAYO_GALLEGOS',
				'PATRICIO_ZUQUILANDA_DUQUE',
				'WASHINGTON_PESANTEZ_MUÑOZ'
				]

	# parse file
	trail = get_district(soup)
	elecdata = get_electores(soup)
	sufdata = get_suf(soup)
	baddata = get_bad(soup)
	scores, nombres = get_scores(soup)

	
	if scores:

		print sorted(nombres)
		# format results
		hombres = [	elecdata['elect_H'],
					sufdata['sufH'], 
					sufdata['ausH'], 
					baddata['blancoH'], 
					baddata['nulloH']
					]

		mujers  = [	elecdata['elect_M'],
					sufdata['sufM'],
					sufdata['ausM'],
					baddata['blancoM'],
					baddata['nulloM'] 
					]

		# put results in order, handle if name not found
		for nombre in sorted(nombres):
			try:
				hombres.append(scores[nombre + '_H'])
			except KeyError:
				print nombre
				hombres.append(' ')

			try:
				mujers.append(scores[nombre + '_M'])
			except KeyError:
				mujers.append(' ')

		# append results to file
		f = codecs.open(fileout,'a','utf-8')
		f.write( trail + 'H,' + ','.join(hombres) + '\n')
		f.write( trail + 'M,' + ','.join(mujers)  + '\n')
		f.close()



if __name__ == "__main__":
	import os
	files = os.listdir('.')
	for filename in files:
		if filename.endswith('.html') or filename.endswith('.HTML') or filename.endswith('.htm') or filename.endswith('.src'):
			print filename
			f = codecs.open(filename, 'r', 'utf-8')
			html = f.read()
			f.close()
			soup = bs.BeautifulSoup(html)
			make_record(soup)

