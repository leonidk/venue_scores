# venue_scores
This is the source code and project history for the following publication

**Venue Analytics: A Simple Alternative to Citation-Based Metrics** by Leonid Keselman

## overview
The dependencies for this project are Jupyter Notebooks with Python3 and numpy, scipy, pandas, lxml and scikit-learn libraries. Run `make` to download all of the appropriate data from DBLP, [CSRankings](https://github.com/emeryberger/CSrankings), the NSF, Transparent California, and Scholar Rank. The Makefile script will then pre-process the data (using `my_dblp_parser.py` and `cleanup_venues.ipynb`) into three main datafiles, `useful_authors_list.pkl.gz useful_papers.pkl.gz useful_venue_list.pkl.gz`.  Then the following programs are useful in generating rankings and clustersings
* `cleaned_venues_to_weights.ipynb` generates conference rankings using a regression function. The top notebook block contains a variety of settings and hyper-parameters to chose what dataset to fit.
* `combine_weights.ipynb` combines multiple weight files (or uses just a single one) to perform analysis against existing conference rankings 
* `pagerank.ipynb` generates PageRank baselines for conference and author ranking
* `cluster_new.ipynb` clusters conferences into categories

### extra files
* `acm2017` contains data files for processing and aligning [CSRankings](https://github.com/emeryberger/CSrankings) data with [ScholarRank](http://www.dabi.temple.edu/~vucetic/CSranking/details/) data. 
* `download` stores downloaded files
* `old_version` contains the first version of this codebase, mostly for historical reference
* `uni_rank_*.csv` rankings contain university ranking data from many sources, all with consistent university naming.
* `correlation_cleaned.csv` contains the dataset of CMU faculty members with their traditional ranking measures.
* `traditional_conf_scores.csv` contains the traditional conference ranking data. 
