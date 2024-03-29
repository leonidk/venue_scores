# [Venue Scores Website](https://leonidk.github.io/venue_scores/)
This is the source code and project history for the following publication. 

**Venue Analytics: A Simple Alternative to Citation-Based Metrics** by Leonid Keselman ([arXiv version here](https://arxiv.org/abs/1904.12573))

This paper proposes an automatic pipeline for ranking and organizing academic conferences in Computer Science. It uses all the data from [DBLP](https://dblp.org/), featuring millions of authors, millions of papers and thousands of publication venues. 
* For ranking, the basic contribution is to formulate conference ranking as a linear regression task, from publication history to targets like NSF Grant Amount, Faculty Status, or Salary. These conference rankings can vary over time, and be used to evaluate individual academics, universities as well. This also includes a PageRank baseline for author and conference ranking.
* For organizing, there is a proposed method for organizing venues into groups based on a lower dimensional embedding based on the author x venues matrix; this allows for natural data-driven clusters such as Graphics, AI, ML, Vision, PL, etc. 
* These rankings do not require or depend on citation data, are fairly robust to changing the regression targets, and can be used to evaluate/organize anyone who has ever published a paper in Computer Science. These rankings resemble citation-based metrics like h-index, despite not using citation data. 
* University rankings implied by our scores correlate highly with peer assesement of university rankings (e.g. US News).
* These produced scores can be used to perform interesting queries about academic value and relationships. The venue-level and year-level granularity of these rankings, along with faculty affiliation data from CRankings, allows for filtering and analysis to ask questions such as "Which University produces the most value in the subfields of Robotics, Computer Vision and Machine Learning in the years 2005 to 2015?". We can also produce nearest neighbors for any Computer Science academic to find authors who publish a similiar distribution of work, even if they publish in different conferences.
* Preprint archives and short papers have been excluded from most of our analysis via a filter (see pipeline information below). However, you're free to fork this project and add it back in if you'd like! 
* See the paper for more technical details. 

# requirements
Initial development and testing was on a MacOS 10.13 system. However to work on Ubuntu 18.04 LTS, the following command installed all needed tools on top of a fresh install
`sudo apt-get install python3.6 python3-lxml wget python3-nbconvert python3-notebook jupyter-nbconvert jupyter python3-numpy python3-scipy python3-pandas python3-matplotlib python3-sklearn python3-xmltodict python3-unidecode`

Then simply run `make` and the project will build graphs and csv data files for school, author and conference rankings. 

## overview
The dependencies for this project are Jupyter Notebooks with Python3 and numpy, scipy, pandas, lxml and scikit-learn libraries. Run `make` to download all of the appropriate data from DBLP, [CSRankings](https://github.com/emeryberger/CSrankings), the NSF, Transparent California, and Scholar Rank. The Makefile script will then pre-process the data (using `my_dblp_parser.py` and `cleanup_venues.ipynb`) into three main datafiles, `useful_authors_list.pkl.gz useful_papers.pkl.gz useful_venue_list.pkl.gz`.  Then the following programs are useful in generating rankings and clusterings
* `cleaned_venues_to_weights.ipynb` generates conference rankings using a regression function. The top notebook block contains a variety of settings and hyper-parameters to chose what dataset to fit.
* `combine_weights.ipynb` combines multiple weight files (or uses just a single one) to perform analysis against existing conference rankings 
* `pagerank.ipynb` generates PageRank baselines for conference and author ranking
* `cluster_new.ipynb` clusters conferences into categories

This code was all developed and run on a personal laptop. 

### extra files
* `download` stores downloaded files
* `old_version` contains the first version of this codebase, mostly for historical reference
* `old_ranks` contains other ranking data. Including `uni_rank_*.csv`, which are rankings contain university ranking data from many sources, all with consistent university naming. `correlation_cleaned.csv` contains the dataset of CMU faculty members with their traditional ranking measures. `traditional_conf_scores.csv` contains the traditional conference ranking data (along with `msar.json`). `ranks.csv` is a snapshot of the CSRankings ranks from our development time. `r1.csv` is a list of all R1 Research Universities. `faculty_affil_scholar.csv` contains the data parsed from [ScholarRank](http://www.dabi.temple.edu/~vucetic/CSranking/details/). 
* `acm2017` contains data files for processing and aligning [CSRankings](https://github.com/emeryberger/CSrankings) data with [ScholarRank](http://www.dabi.temple.edu/~vucetic/CSranking/details/) data. 


