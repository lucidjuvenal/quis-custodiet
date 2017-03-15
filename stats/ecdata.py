import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from collections import namedtuple
from scipy.optimize import curve_fit
from scipy import asarray as ar,exp
from matplotlib.pyplot import subplot2grid
from scipy.stats import linregress
import statsmodels.api as sm


"""
To save list of all parroquias:

regions = df.groupby(['provincia_nombre','canton_nombre','parroquia_nombre'])
keys = regions.indices.keys()
keys = sorted(keys)

with open('provincia_canton_parroquia_.dat','w') as f:
    for key in keys:
        f.write(';'.join(key) + '\n')

"""

show = True
save = True

df02a = '../data_prior/presidential_election_2002a.dta'
df02b = '../data_prior/presidential_election_2002b.dta'

df06a = '../data_prior/presidential_election_2006a.dta'
df06b = '../data_prior/presidential_election_2006b.dta'

df09 = '../data_prior/presidential_election_2009.dta'

df13 = '../data_prior/presidential_election_2013.dta'


## =============================================================================

def gauss(x,a,x0,sigma):
	return a*exp(-(x-x0)**2/(2*sigma**2))

## =============================================================================

def fitGauss(data):

	dx = 0.02
	bins = np.arange(0, 1 + 2*dx, dx) - dx/2

	histo = plt.hist(data, bins=bins, \
			range=(0,1), color='red', label="somelabel")

	# fit Gaussian to histogram
	histX = histo[1][2:] - dx/2
	p0 = [100,0.6,0.5]  # ht/cen/sig 
	popt, pcov = curve_fit(gauss, histX, histo[0][1:], p0)

	return popt

## =============================================================================

def plotGauss(data,popt):

	if show:
		print	" height : ", popt[0], "\n" \
				" center : ", popt[1], "\n" \
				"  width : ", popt[2], "\n"

	# plot the gaussian
	gOut = gauss(bins, popt[0], popt[1], popt[2])
	line, = plt.plot(bins,gOut, 'k--', linewidth=3)

	# prettify
	plt.ylim(0,100)
	plt.xlim(0,1)
	plt.xticks(np.arange(0,1.1,0.1))
	plt.title("Fraction of votes", size=24)
	plt.xlabel("Fraction", size=18)
	plt.ylabel("Number of precincts", size=18)
	plt.legend()
	plt.draw()

## =============================================================================

# http://stackoverflow.com/questions/19379295/linear-regression-with-pandas-dataframe


def fit_line1(x, y):
    """Return slope, intercept of best fit line."""
    # Remove entries where either x or y is NaN.
    clean_data = pd.concat([x, y], 1).dropna(0) # row-wise
    (_, x), (_, y) = clean_data.iteritems()
    slope, intercept, r, p, stderr = linregress(x, y)
    return slope, intercept # could also return stderr

def fit_line2(x, y):
    """Return slope, intercept of best fit line."""
    X = sm.add_constant(x)
    model = sm.OLS(y, X, missing='drop') # ignores entires where x or y is NaN
    fit = model.fit()
    return fit.params[1], fit.params[0] # could also return stderr in each via fit.bse


def fit_line3(x, y, w):
    """Return slope, intercept of best fit line."""
    X = sm.add_constant(x)
    model = sm.WLS(y, X, w, missing='drop') # ignores entires where x or y is NaN
    fit = model.fit()
    return fit.params[1], fit.params[0] # could also return stderr in each via fit.bse

## =============================================================================

def calc_unc(ycount,tot):
	""" 
	for computing errors of some frac, ycount/total
	any points with zero counts are set to 1 for computing errorbar

	params
	------


	formula:
	Z = Y/X
	dz = Z * sqrt( (dx/X)**2 + (dy/Y)**2 )
	dz = Z * sqrt( 1/X + 1/Y )

	W = 1/dz**2 
	W = 1/Z**2 * (1/X + 1/Y)
	"""
	Y = ycount.copy()
	Y[Y==0] = 1
	return Y/tot * np.sqrt( 1./Y + 1./tot)

#	return 1./dz**2

## =============================================================================

def getFracs(dat, codigo=None):
	"""
	dat is dataframe

	returns dfrac, a dataframe grouped by precinct (id_provcantparr+sexo)

	'valfrac' : valfrac.values, \
	'votefrac' :votefrac.values, \
	'nullfrac' : nulls.values * 1.0/tot, \	# voided ballots
	'blankfrac' : blank.values * 1.0/tot, \
	'nullcount' : nulls, \
	'blankcount': blank, \
	'total' : tot, \

	"""

	if 'precinct' in dat.columns:
		indcol = 'precinct'
	else:
		indcol = 'id_provcantparr'

	# scalar value of registered voters, being a lazy progammer
	tot = dat.groupby(indcol).electores.mean()


	# 
	blank = dat.groupby(indcol).votos_en_blanco.mean()
	nulls = dat.groupby(indcol).votos_nulos.mean()


	# total valid votes across all candidates
	valid = dat.groupby(indcol).candidato_votos.sum()

	# fraction of voters that cast valid ballots
	valfrac = valid / tot

	if codigo:
		# if given a numer code
		win = dat.candidato_votos[dat.candidato_codigo==code]
	else:
		# extract votes for winner
		win = dat.candidato_votos[dat.candidato_estado=='electos']

	#
	votefrac = win * 1.0 / valid.values


	dfrac = pd.DataFrame( \
		data={	'valfrac' : valfrac.values, \
				'votefrac' :votefrac.values, \
				'nullfrac' : nulls.values * 1.0/tot, \
				'blankfrac' : blank.values * 1.0/tot, \
				'nullcount' : nulls, \
				'blankcount': blank, \
				'total' : tot, \
		},\
		index=valfrac.index)

	return dfrac

## =============================================================================

def plotFinger(dfrac, path, df, candidato_codigo=None):
	'''
	Plot the election fingerprint.

	Input:
		dfrac -
		path - string to filepath

	Given list of frac DataFrames, extract data and plot 2d histogram
	'''	

	# metadata
	if candidato_codigo:
		# plotted candidate assigned
		code = candidato_codigo
	else:
		# winner code
		code = df[df.candidato_estado=='electos'].candidato_codigo.values[0]

	name = df[df.candidato_codigo==code].candidato_nombre.values[0]
	name = name.split()[0]

	if path:
		yr = path.split('_')[-1]
		yr = yr.split('.')[0]
	leg = yr + ' ' + name


	# plot histogram
	ax0 = plt.subplot2grid( (4,3), (0,0), rowspan=3, colspan=3)

#	http://matplotlib.org/examples/color/colormaps_reference.html
	# perceptually-uniform are: viridis, inferno, plasma, magma
	cmap = plt.get_cmap('plasma')

	# plot with bins
	histo = ax0.hist2d( \
		dfrac.valfrac.values, dfrac.votefrac.values, \
		bins=100, range=[[0,1],[0,1]], \
		cmin=1, cmax=5, cmap=cmap, \
#		label = "test label"
		);

	xticks = np.arange(0,1.1,0.1)
	yticks = xticks
	ax0.set_xticks(xticks)
	ax0.set_yticks(yticks)

	ax0.set_title("Election fingerprint, " + leg, size=20)
	ax0.set_ylabel("Fraction voting for winner", size=16)


	# cumulative subplot
	ax1 = plt.subplot2grid( (4,3), (3,0), rowspan=1, colspan=3)

	hvals = np.ma.array(histo[0], mask=np.isnan(histo[0]))
	hsum = np.ma.sum(hvals,axis=1)
	hsum = hsum.cumsum()
	hsum = hsum / hsum.max()

	ax1.plot( histo[1][1:], hsum, 'b-' )

	ax1.axis( [0, 1, -0.1, 1.1 ])
	ax1.plot( [0, 1], [0, 0], 'k--')
	ax1.plot( [0, 1], [1, 1], 'k--')

	ax1.set_xticks(xticks)
	ax1.set_xlabel("Fraction of valid ballots", size=16)

	if save:
		plt.savefig('fingerprint_' + yr + '_' + name + '.png')

	if show:
		plt.show();

## =============================================================================

# def plotFinger(dfrac, path, df, candidato_codigo=None):
def plotBadBallots(dfrac):

	xmax = 2 #0.25
	xvals = np.arange(0, 2*xmax, xmax )

	blankSlope, blankInt = fit_line1(dfrac.blankfrac, dfrac.votefrac)
	nullSlope, nullInt = fit_line1(dfrac.nullfrac, dfrac.votefrac)


	## errors 
	errNull = calc_unc( dfrac.nullcount, dfrac.total )


	"""
	The plot I prefer has nullfrac as a function of votefrac, meaning the errorbars
	are along the x-axis.  But sm.WLS assumes y-errors.  So feed into fitline, 
	then invert from:

	y = mx + b

	to:

	x = (y-b)/m


	"""
	nullm, nullb = fit_line3( dfrac.nullfrac, dfrac.votefrac, 1/errNull**2)

	if False:
		nullb = -1*nullb/nullm
		nullm = 1.0/nullm
	
	blankLine = blankInt + blankSlope * xvals
	nullLine = nullb + nullm * xvals


#	plt.plot(xvals, blankLine, 'b-')
	plt.plot(xvals, nullLine, 'r-')
	
#	blankScatt = plt.scatter( \
#		dfrac.blankfrac, dfrac.votefrac, \
#		s=50, \
#		facecolors='none', \
#		edgecolors='r', \
#		);

	nullScatt = plt.errorbar(
		dfrac.votefrac, dfrac.nullfrac, yerr = errNull, \
		fmt = 'ro', \
#		s=50, \
#		facecolors='none', \
#		edgecolors='b', \
		);

#	plt.axis([0, xmax, 0, 1])
	plt.show()


## =============================================================================




path = df09

df = pd.read_stata( path )

# remove crazy offset from candidate code
df.candidato_codigo = df.candidato_codigo - np.round(df.candidato_codigo,-2)

# use precinctcode + gender as index
df['precinct'] = df.id_provcantparr + df.sexo.astype(basestring)


print df.candidato_codigo.unique()

code = 0
dfrac = getFracs(df, code)


"""
Current status: trying to fit :
	blank ballots vs votes for candidate,
	null votes vs votes for candidate

a fair election shouldn't have any correlation for those.


the idea being to plot them on the right side of the fingerprint, so really it
will be teh inverse of those: votes vs blank, votes vs nulls

sm.WLS assumes error is the y-axis error.  So for this I'll need to fit them,
then invert the results from:

	y = m*x + b
to:
	x = (y-b)/m = 1/m*y - b/m

	votes = blank/mfit - bfit/mfit




"""

#plotFinger( dfrac, path, df, code )
plotBadBallots(dfrac)



"""
need to make weighted regression on voteshare vs blanks (and nulls), to check if there's a systemic bias for/against a candidate.  
"""


"""
	33 columns:
	dignidad_codigo			race_code
	dignidad_ambito			race_level
	dignidad_nombre			race_name

	provincia_codigo		1-27
	provincia_nombre

	candidato_codigo		code (0-7) for each candidate (3 is Correa)
	candidato_votos			sum of votes in precint
	candidato_estado		electos / NaN
	candidato_nombre	

	electores				registered voters
	numero_de_actas			number of ballot boxes


	canton_codigo			263 unique
	canton_nombre

	sexo
	votos_en_blanco
	votos_nulos

		blank + invalid + valid + no-shows = electores
		no-shows not recorded, inferred from math

	op_provincia_codigo
	op_canton_codigo
	op_parroquia_codigo
	op_tipo
	op_ambito
	op_nombre				party name
	op_siglas				party initials
	op_lista
	op_codigo
	op_votos_en_plancha		NaN


	parroquia_codigo		1248 unique
	parroquia_nombre		city?	1097 uniques
	parroquia_estado		city's state

	id_prov					27
	id_provcant				263 unique
	id_provcantparr			1248 unique : concat state/city/precinct
	id_opcodigo				8 unique : ['00048', '00095', '00005', '00056', '00119', '00100', '00076', '00075']
"""


