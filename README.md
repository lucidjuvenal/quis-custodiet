# quis-custodiet
Who watches the vote-counters?  We do.

Stalin observed that "the people who cast the votes decide nothing, the people who count the votes decide everything".  We figure that the hackers who analyze the data before the vote-counters get their grubby little paws on the ballots can stop that.

This project is to ensure the integrity of elections in developing countries by making the results transparent and verifiable.  For the test case we're looking at the 2017 Ecuador presidential election, but similar methods are used in Peru, Bolivia, Uganda, etc.  We have a pretty good outline for the plan, but are open to suggestions.



The basics: In Ecuador, each precinct has a number of people who are randomly assigned to open the ballot boxes and count the votes (by hand!) starting at 5pm.  For each ballot box, they fill out a tally sheet (there are around 50,000 of these boxes/sheets across the country).  The tally sheet itself is part of the public record, but the sheets are sent to a government agency which adds up all the tally sheets and announces a winner.  We would like to verify that the government agency doesn't do anything funny with the numbers.

The political parties typically hire veedores ("watchers") to observe the votes during the counting process.  The veedores will take pictures of the tally sheets and upload them to Twitter with the hashtag #Ecuador2017, with the text body being the list of candidates and votes.

On the back end, we will be pulling the Twitter feed.  We'll need to run some image recognition to read the pictures and extract the vote totals for each candidate.  The values from the images will be compared to the text, and if there are discrepancies, the images will be sent to Mechanical Turk for verification.  There will almost certainly be some tally sheets that are sent in by multiple veedores, so we can use that for verification as well.

As the values for the tally sheets come in, we will update the database.  We'll run some statistical analyses on the data, and publish various results to a website in real time.  We'll need to have the totals and projected totals for each district, and listings for which ballot boxes have been recorded.

The key here is to make it pretty fast.  The polls close at 5pm, and the tally sheets will be completed 2-3 hours later.  If the government were to try anything fishy, they would announce the results quite early, by roughly 10pm.  By pushing the results to a public website as fast as we can, we will severely restrict the government's ability to make up phony numbers.  It is nice if we can provide access to the images, but not mandatory (transparency is less important than the credible threat of having the information).

There are a few ways to try and rig an election.  One is to take blank ballots (voting is mandatory, but sometimes people put them into the box unmarked) and mark them for the rigging candidate.  Another is to take ballots for an opposition candidate, but mark them so that they become null (invalid).  Both of those leave a statistical signature.  So we can plot, at the parroquia level, the fraction of null ballots versus fraction for the two candidates (it should remain independent).  We can also plot blank ballots versus fraction for the two candidates (again, should remain independent).  There is previous academic work exploring these and other similar correlations.


One powerful cross-check will be the statistical analysis.  We have databases of the previous elections, down to the "parroquia" level (heirarchy is Provincia > Canton > Parroquia > Zona > Junta).  As a final check, we want to be able to scrape the official government website in the weeks leading up to election day.  We can check for the districts which demonstrated the strongest irregularities.


components:

	Prior to election day:
		website for our results
		building database for ballot boxes, poss. including demographics
		registering veedores prior to the election
		scraping official site for analysis


	On election day:	
		pulling Twitter feed
		image processing
		turking inconsistencies
		comparing to expected number of voters per box / parrochia
		updating database
		statistical analysis
		push results to website


	After election day:
		basic maintenance
		making images available for transparency purposes


Numerical estimates:
	10 Million voters (mandatory voting, so 90%+ turnout)
	240 voters/box => 50k ballot boxes (41.6k)
	2 images/box => 100k images
	1 Mb/image => 100 GB data

