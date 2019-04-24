# venue_scores
This is the source code and project history for the following publication

**Venue Analytics: A Simple Alternative to Citation-Based Metrics** by Leonid Keselman

This paper proposes an automatic pipeline for ranking and organizing academic conferences in Computer Science. For ranking, the basic contribution is to formulate conference ranking as a linear regression task, from publication history to targets like NSF Grant Amount, Faculty Status, or Salary. These conference rankings can vary over time, and be used to evaluate individual academics, universities as well. This also includes a PageRank baseline for author and conference ranking. Additionally, there is a proposed method for organizing publication venues into groups based on a lower dimensional embedding based on the author x venues matrix; this allows for natural data-driven clusters such as Graphics, AI, ML, Vision, PL, etc. 

## overview
The dependencies for this project are Jupyter Notebooks with Python3 and numpy, scipy, pandas, lxml and scikit-learn libraries. Run `make` to download all of the appropriate data from DBLP, [CSRankings](https://github.com/emeryberger/CSrankings), the NSF, Transparent California, and Scholar Rank. The Makefile script will then pre-process the data (using `my_dblp_parser.py` and `cleanup_venues.ipynb`) into three main datafiles, `useful_authors_list.pkl.gz useful_papers.pkl.gz useful_venue_list.pkl.gz`.  Then the following programs are useful in generating rankings and clusterings
* `cleaned_venues_to_weights.ipynb` generates conference rankings using a regression function. The top notebook block contains a variety of settings and hyper-parameters to chose what dataset to fit.
* `combine_weights.ipynb` combines multiple weight files (or uses just a single one) to perform analysis against existing conference rankings 
* `pagerank.ipynb` generates PageRank baselines for conference and author ranking
* `cluster_new.ipynb` clusters conferences into categories

### extra files
* `download` stores downloaded files
* `old_version` contains the first version of this codebase, mostly for historical reference
* `old_ranks` contains other ranking data. Including `uni_rank_*.csv`, which are rankings contain university ranking data from many sources, all with consistent university naming. `correlation_cleaned.csv` contains the dataset of CMU faculty members with their traditional ranking measures. `traditional_conf_scores.csv` contains the traditional conference ranking data (along with `msar.json`). `ranks.csv` is a snapshot of the CSRankings ranks from our development time. `r1.csv` is a list of all R1 Research Universities. `faculty_affil_scholar.csv` contains the data parsed from [ScholarRank](http://www.dabi.temple.edu/~vucetic/CSranking/details/). 
* `acm2017` contains data files for processing and aligning [CSRankings](https://github.com/emeryberger/CSrankings) data with [ScholarRank](http://www.dabi.temple.edu/~vucetic/CSranking/details/) data. 
