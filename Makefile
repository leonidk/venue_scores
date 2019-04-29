

all: useful_papers.pkl.gz download/nsffile acm2017/all_professors.xlsx acm2017/all_departments.xlsx download/university-of-california-2015.csv download/university-of-california-2016.csv download/university-of-california-2017.csv
.PHONY: all

dblp-aliases.csv: 
	wget -N https://raw.githubusercontent.com/emeryberger/CSrankings/gh-pages/dblp-aliases.csv 

csrankings.csv:
	wget -N https://raw.githubusercontent.com/emeryberger/CSrankings/gh-pages/csrankings.csv

download/university-of-california-2017.csv: |download
	cd download && wget -nc https://transcal.s3.amazonaws.com/public/export/university-of-california-2017.csv

download/university-of-california-2016.csv: |download
	cd download && wget -nc https://transcal.s3.amazonaws.com/public/export/university-of-california-2016.csv

download/university-of-california-2015.csv: |download
	cd download && wget -nc https://transcal.s3.amazonaws.com/public/export/university-of-california-2015.csv

# DBLP XML dataset
# lets just make this as new as possible
download/dblp.xml.gz: |download
	#cd download && wget -nc https://dblp.org/xml/release/dblp-2019-01-01.xml.gz 
	cd download && wget -nc https://dblp.org/xml/dblp.xml.gz

# DBLP's corresponding DTD file
download/dblp.dtd: |download
	#cd download && wget -nc https://dblp.org/xml/release/dblp-2017-08-29.dtd
	cd download && wget -nc https://dblp.org/xml/dblp.dtd

new_pagerank_people.pkl: useful_papers.pkl.gz
	jupyter nbconvert --ExecutePreprocessor.timeout=-1 --to notebook --execute pagerank.ipynb

faculty-affiliations.csv: csrankings.csv
	python3 gen_fac_affil.py 

parsed_files.pkl.gz: faculty-affiliations.csv download/dblp.xml.gz download/dblp.dtd
	python3 my_dblp_parser.py

useful_papers.pkl.gz: parsed_files.pkl.gz dblp-aliases.csv
	jupyter nbconvert --ExecutePreprocessor.timeout=-1 --to notebook --execute cleanup_venues.ipynb
	rm cleanup_venues.nbconvert.ipynb
# folder for downloading
download/nsf: | download
	mkdir -p $@

download:
	mkdir -p $@

nsf2.pkl: download/nsffile 
	jupyter nbconvert --ExecutePreprocessor.timeout=-1 --to notebook --execute parse_nsf.ipynb
	rm parse_nsf.nbconvert.ipynb

acm2017/all_professors.xlsx:
	cd acm2017 && wget -nc http://www.dabi.temple.edu/~vucetic/CSranking/raw_data/all_professors.xlsx
acm2017/all_departments.xlsx:
	cd acm2017 && wget -nc http://www.dabi.temple.edu/~vucetic/CSranking/raw_data/all_departments.xlsx

download/nsffile: download/nsf/1970.zip download/nsf/1971.zip download/nsf/1972.zip download/nsf/1973.zip download/nsf/1974.zip download/nsf/1975.zip download/nsf/1976.zip download/nsf/1977.zip download/nsf/1978.zip download/nsf/1979.zip download/nsf/1980.zip download/nsf/1981.zip download/nsf/1982.zip download/nsf/1983.zip download/nsf/1984.zip download/nsf/1985.zip download/nsf/1986.zip download/nsf/1987.zip download/nsf/1988.zip download/nsf/1989.zip download/nsf/1990.zip download/nsf/1991.zip download/nsf/1992.zip download/nsf/1993.zip download/nsf/1994.zip download/nsf/1995.zip download/nsf/1996.zip download/nsf/1997.zip download/nsf/1998.zip download/nsf/1999.zip download/nsf/2000.zip download/nsf/2001.zip download/nsf/2002.zip download/nsf/2003.zip download/nsf/2004.zip download/nsf/2005.zip download/nsf/2006.zip download/nsf/2007.zip download/nsf/2008.zip download/nsf/2009.zip download/nsf/2010.zip download/nsf/2011.zip download/nsf/2012.zip download/nsf/2013.zip download/nsf/2014.zip download/nsf/2015.zip download/nsf/2016.zip download/nsf/2017.zip download/nsf/2018.zip download/nsf/2019.zip 
	touch $@

download/nsf/1970.zip: |download/nsf
	cd download/nsf && wget -nc --content-disposition https://www.nsf.gov/awardsearch/download?DownloadFileName=1970\&All=true

download/nsf/1971.zip: |download/nsf
	cd download/nsf && wget -nc --content-disposition https://www.nsf.gov/awardsearch/download?DownloadFileName=1971\&All=true

download/nsf/1972.zip: |download/nsf
	cd download/nsf && wget -nc --content-disposition https://www.nsf.gov/awardsearch/download?DownloadFileName=1972\&All=true

download/nsf/1973.zip: |download/nsf
	cd download/nsf && wget -nc --content-disposition https://www.nsf.gov/awardsearch/download?DownloadFileName=1973\&All=true

download/nsf/1974.zip: |download/nsf
	cd download/nsf && wget -nc --content-disposition https://www.nsf.gov/awardsearch/download?DownloadFileName=1974\&All=true

download/nsf/1975.zip: |download/nsf
	cd download/nsf && wget -nc --content-disposition https://www.nsf.gov/awardsearch/download?DownloadFileName=1975\&All=true

download/nsf/1976.zip: |download/nsf
	cd download/nsf && wget -nc --content-disposition https://www.nsf.gov/awardsearch/download?DownloadFileName=1976\&All=true

download/nsf/1977.zip: |download/nsf
	cd download/nsf && wget -nc --content-disposition https://www.nsf.gov/awardsearch/download?DownloadFileName=1977\&All=true

download/nsf/1978.zip: |download/nsf
	cd download/nsf && wget -nc --content-disposition https://www.nsf.gov/awardsearch/download?DownloadFileName=1978\&All=true

download/nsf/1979.zip: |download/nsf
	cd download/nsf && wget -nc --content-disposition https://www.nsf.gov/awardsearch/download?DownloadFileName=1979\&All=true

download/nsf/1980.zip: |download/nsf
	cd download/nsf && wget -nc --content-disposition https://www.nsf.gov/awardsearch/download?DownloadFileName=1980\&All=true

download/nsf/1981.zip: |download/nsf
	cd download/nsf && wget -nc --content-disposition https://www.nsf.gov/awardsearch/download?DownloadFileName=1981\&All=true

download/nsf/1982.zip: |download/nsf
	cd download/nsf && wget -nc --content-disposition https://www.nsf.gov/awardsearch/download?DownloadFileName=1982\&All=true

download/nsf/1983.zip: |download/nsf
	cd download/nsf && wget -nc --content-disposition https://www.nsf.gov/awardsearch/download?DownloadFileName=1983\&All=true

download/nsf/1984.zip: |download/nsf
	cd download/nsf && wget -nc --content-disposition https://www.nsf.gov/awardsearch/download?DownloadFileName=1984\&All=true

download/nsf/1985.zip: |download/nsf
	cd download/nsf && wget -nc --content-disposition https://www.nsf.gov/awardsearch/download?DownloadFileName=1985\&All=true

download/nsf/1986.zip: |download/nsf
	cd download/nsf && wget -nc --content-disposition https://www.nsf.gov/awardsearch/download?DownloadFileName=1986\&All=true

download/nsf/1987.zip: |download/nsf
	cd download/nsf && wget -nc --content-disposition https://www.nsf.gov/awardsearch/download?DownloadFileName=1987\&All=true

download/nsf/1988.zip: |download/nsf
	cd download/nsf && wget -nc --content-disposition https://www.nsf.gov/awardsearch/download?DownloadFileName=1988\&All=true

download/nsf/1989.zip: |download/nsf
	cd download/nsf && wget -nc --content-disposition https://www.nsf.gov/awardsearch/download?DownloadFileName=1989\&All=true

download/nsf/1990.zip: |download/nsf
	cd download/nsf && wget -nc --content-disposition https://www.nsf.gov/awardsearch/download?DownloadFileName=1990\&All=true

download/nsf/1991.zip: |download/nsf
	cd download/nsf && wget -nc --content-disposition https://www.nsf.gov/awardsearch/download?DownloadFileName=1991\&All=true

download/nsf/1992.zip: |download/nsf
	cd download/nsf && wget -nc --content-disposition https://www.nsf.gov/awardsearch/download?DownloadFileName=1992\&All=true

download/nsf/1993.zip: |download/nsf
	cd download/nsf && wget -nc --content-disposition https://www.nsf.gov/awardsearch/download?DownloadFileName=1993\&All=true

download/nsf/1994.zip: |download/nsf
	cd download/nsf && wget -nc --content-disposition https://www.nsf.gov/awardsearch/download?DownloadFileName=1994\&All=true

download/nsf/1995.zip: |download/nsf
	cd download/nsf && wget -nc --content-disposition https://www.nsf.gov/awardsearch/download?DownloadFileName=1995\&All=true

download/nsf/1996.zip: |download/nsf
	cd download/nsf && wget -nc --content-disposition https://www.nsf.gov/awardsearch/download?DownloadFileName=1996\&All=true

download/nsf/1997.zip: |download/nsf
	cd download/nsf && wget -nc --content-disposition https://www.nsf.gov/awardsearch/download?DownloadFileName=1997\&All=true

download/nsf/1998.zip: |download/nsf
	cd download/nsf && wget -nc --content-disposition https://www.nsf.gov/awardsearch/download?DownloadFileName=1998\&All=true

download/nsf/1999.zip: |download/nsf
	cd download/nsf && wget -nc --content-disposition https://www.nsf.gov/awardsearch/download?DownloadFileName=1999\&All=true

download/nsf/2000.zip: |download/nsf
	cd download/nsf && wget -nc --content-disposition https://www.nsf.gov/awardsearch/download?DownloadFileName=2000\&All=true

download/nsf/2001.zip: |download/nsf
	cd download/nsf && wget -nc --content-disposition https://www.nsf.gov/awardsearch/download?DownloadFileName=2001\&All=true

download/nsf/2002.zip: |download/nsf
	cd download/nsf && wget -nc --content-disposition https://www.nsf.gov/awardsearch/download?DownloadFileName=2002\&All=true

download/nsf/2003.zip: |download/nsf
	cd download/nsf && wget -nc --content-disposition https://www.nsf.gov/awardsearch/download?DownloadFileName=2003\&All=true

download/nsf/2004.zip: |download/nsf
	cd download/nsf && wget -nc --content-disposition https://www.nsf.gov/awardsearch/download?DownloadFileName=2004\&All=true

download/nsf/2005.zip: |download/nsf
	cd download/nsf && wget -nc --content-disposition https://www.nsf.gov/awardsearch/download?DownloadFileName=2005\&All=true

download/nsf/2006.zip: |download/nsf
	cd download/nsf && wget -nc --content-disposition https://www.nsf.gov/awardsearch/download?DownloadFileName=2006\&All=true

download/nsf/2007.zip: |download/nsf
	cd download/nsf && wget -nc --content-disposition https://www.nsf.gov/awardsearch/download?DownloadFileName=2007\&All=true

download/nsf/2008.zip: |download/nsf
	cd download/nsf && wget -nc --content-disposition https://www.nsf.gov/awardsearch/download?DownloadFileName=2008\&All=true

download/nsf/2009.zip: |download/nsf
	cd download/nsf && wget -nc --content-disposition https://www.nsf.gov/awardsearch/download?DownloadFileName=2009\&All=true

download/nsf/2010.zip: |download/nsf
	cd download/nsf && wget -nc --content-disposition https://www.nsf.gov/awardsearch/download?DownloadFileName=2010\&All=true

download/nsf/2011.zip: |download/nsf
	cd download/nsf && wget -nc --content-disposition https://www.nsf.gov/awardsearch/download?DownloadFileName=2011\&All=true

download/nsf/2012.zip: |download/nsf
	cd download/nsf && wget -nc --content-disposition https://www.nsf.gov/awardsearch/download?DownloadFileName=2012\&All=true

download/nsf/2013.zip: |download/nsf
	cd download/nsf && wget -nc --content-disposition https://www.nsf.gov/awardsearch/download?DownloadFileName=2013\&All=true

download/nsf/2014.zip: |download/nsf
	cd download/nsf && wget -nc --content-disposition https://www.nsf.gov/awardsearch/download?DownloadFileName=2014\&All=true

download/nsf/2015.zip: |download/nsf
	cd download/nsf && wget -nc --content-disposition https://www.nsf.gov/awardsearch/download?DownloadFileName=2015\&All=true

download/nsf/2016.zip: |download/nsf
	cd download/nsf && wget -nc --content-disposition https://www.nsf.gov/awardsearch/download?DownloadFileName=2016\&All=true

download/nsf/2017.zip: |download/nsf
	cd download/nsf && wget -nc --content-disposition https://www.nsf.gov/awardsearch/download?DownloadFileName=2017\&All=true

download/nsf/2018.zip: |download/nsf
	cd download/nsf && wget -nc --content-disposition https://www.nsf.gov/awardsearch/download?DownloadFileName=2018\&All=true

download/nsf/2019.zip: |download/nsf
	cd download/nsf && wget -nc --content-disposition https://www.nsf.gov/awardsearch/download?DownloadFileName=2019\&All=true

