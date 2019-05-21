# Large swaths of this file are from Emery Berger and his CSRankings project
# https://github.com/emeryberger/CSrankings
# The parsing however is done straight from a DBLP snapshot with lxml, without any xmllint
from lxml import etree
from datetime import datetime
import csv
import codecs
import json
import re
import gzip
import collections
import csv
import sys
import operator
import pickle

import gzip
areadict = {
    #
    # Max three most selective venues per area for now.
    #
    # SIGPLAN
#    'plan' : ['POPL', 'PLDI', 'PACMPL'],  # PACMPL, issue POPL
    '3dv': ['3DV','3DIMPVT','3DPVT','3DIM'],
    'i3d': ['I3D','SI3D'],
    'wacv': ['WACV','WACV/MOTION'],
    'isccaaa': ['ICCASA/ICTCC','ICCASA','ICTCC'],
    'tcc': ['TCC','TCC (A1)','TCC (A2)','TCC (B1)','TCC (B2)'],
    'popl' : ['POPL'],
    'pldi' : ['PLDI'],
    'HPCC' : ['HPCC','HPCC/CSS/ICESS','HPCC/SmartCity/DSS'],
    'pkdd' : ['ECML/PKDD','ECML','PKDD'],
    'allerton': ['Allerton','Allerton Conference'],
    'ccgrid': ['CCGrid','CCGRID'],
    'cdc': ['CDC','CDC-ECE'],
    'dissys': ['Conference on Designing Interactive Systems','Symposium on Designing Interactive Systems'],
    'reqengi': ['Requirements Engineering','RE'],
    'iwost': ['IWOST','IWOST-1', 'IWOST-2'],
    'db/conf/IEEEwisa': ['WISA','IEEE WISA'] ,
    'db/conf/IEEEants': ['ANTS', 'IEEE ANTS'] ,
    'db/conf/IEEEcloud': ['CLOUD', 'IEEE CLOUD'] ,
    'db/conf/IEEEscc': ['SCC', 'IEEE SCC'] ,
    'db/conf/IEEEpact': ['PACT', 'IEEE PACT'] ,
    'db/conf/ACMmsp': [ 'Memory System Performance','Memory System Performance and Correctness'] ,
    'db/conf/ACMace': ['Advances in Computer Entertainment Technology', 'Advances in Computer Entertainment', 'ACE'] ,
    'ieede': ['IEEE Design & Test','IEEE Design & Test of Computers'],
    'ieeemce' : ['IEEE Trans. Systems, Man, and Cybernetics','IEEE Trans. Systems, Man, and Cybernetics, Part A','IEEE Trans. Systems, Man, and Cybernetics, Part B','IEEE Trans. Systems, Man, and Cybernetics, Part C'],
    # "Next tier" - see csrankings.ts
    'oopsla' : ['OOPSLA'], # Next tier
    'icfp'   : ['ICFP'],   # Next tier
    'pacmpl' : ['PACMPL'], # Special PACMPL handling below
    'sbp': ['SBP','SBP-BRiMS'],
    'db/conf/dna': ['DNA', 'DNA Computing'] ,
    'db/conf/dcc': ['DCC', 'Data Compression Conference'] ,
    'db/conf/dft': ['DFT', 'DFTS'] ,
    'db/conf/nma': ['Numerical Methods and Applications','NMA','Numerical Methods and Application'] ,
    'db/conf/ppopp': ['PPOPP', 'PPoPP'] ,
    'db/conf/approx': ['APPROX-RANDOM', 'APPROX','RANDOM'] ,
    # SIGSOFT
    #    'soft': ['ICSE', 'ICSE (1)', 'ICSE (2)', 'SIGSOFT FSE', 'ESEC/SIGSOFT FSE'],
    'icse' : ['ICSE', 'ICSE (1)'],
    'fse'  : ['SIGSOFT FSE', 'ESEC/SIGSOFT FSE','ESEC / SIGSOFT FSE'],
    'ase'  : ['ASE','Automated Software Engineering'], # Next tier
    'issta'  : ['ISSTA'], # Next tier
    'db/conf/vlsic': ['VLSIC', 'VLSI Circuits'] ,
    'db/conf/lpe': ['LPE', 'WLPE'] ,
    'db/conf/geoinfo': ['GeoInfo', 'GEOINFO'] ,
    'db/conf/iassist': ['IASSIST', 'IASSIST Conference'] ,
    'db/conf/nlucs': ['NLUCS', 'NLPCS'] ,
    'db/conf/iwec': ['ICEC', 'IWEC'] ,
    'db/conf/iasam': ['IAS', 'IAS Annual Meeting'] ,
    'db/conf/services': ['SERVICES', 'SERVICES I', 'SERVICES II'] ,
    'db/conf/pgm': ['Probabilistic Graphical Models', 'PGM'] ,
    'db/conf/isbms': ['ISBMS', 'ISMBS'],
    'db/conf/wsom': ['WSOM+', 'WSOM'] ,
    'db/conf/wmte': ['WMTE','WMUTE'] ,
    'db/conf/fgct': ['FGST', 'FGCT'] ,
    'db/conf/aips': ['ICAPS', 'AIPS', 'Expert Planning Systems'] ,
    'db/conf/vr': ['VR', 'VRAIS'] ,
    'db/conf/wowmom': ['WOWMOM', 'WoWMoM'] ,
    'db/conf/naa': ['NAA', 'WNAA'] ,
    'db/conf/bmvc': ['BMVC', 'Alvey Vision Conference'] ,
    'db/conf/iwmm': ['ISMM','IWMM'] ,
    'db/conf/ubimob': ['UbiMob', 'Ubimob'] ,
    'db/conf/iwcf': ['IWCF', 'ICWF'] ,
    'db/conf/sigcpr': ['CPR', 'SIGCPR', 'SIGMIS-CPR'] ,
    'db/conf/ifip11-4': ['iNetSec', 'iNetSeC'] ,
    'db/conf/iccS': ['ICCS','International Conference on Computational Science'] ,
    'db/conf/3dica': ['Three-Dimensional Image Capture and Applications', 'Three-Dimensional Image Processing 3DIP and Applications', 'Three-Dimensional Imaging, Interaction, and Measurement', 'Three-Dimensional Image Processing, Measurement 3DIPM, and Applications', 'Three-Dimensional Image Capture', '3D Image Processing, Measurement 3DIPM, and Applications'] ,
    'db/conf/its': ['ITS','Intelligent Tutoring Systems'] ,
    'db/conf/iotbd': ['IoTBD', 'IoTBDS'] ,
    'db/conf/iucs': ['IUCS', 'ISUC'] ,
    'db/conf/iwpec': ['IWPEC','IPEC'] ,
    'db/conf/healthcom': ['HealthCom', 'Healthcom'] ,
    'db/conf/swis': ['SIS', 'SWIS'] ,
    'db/conf/iq': ['IQ','ICIQ'] ,
    'db/conf/ifl': ['IFL', 'Implementation of Functional Languages'] ,
    'db/conf/ats': ['ATS', 'Asian Test Symposium'] ,
    'db/conf/sigite': ['SIGITE','SIGITE Conference'] ,
    'db/conf/icsm': ['ICSM','ICSME'] ,
    'db/conf/dawak': ['DaWaK', 'DaWak'] ,
    'db/conf/acssc': ['ACSSC', 'ACSCC'] ,
    'db/conf/ista': ['UNISCON', 'ISTA'] ,
    'db/conf/iotdcc': ['ICC', 'ICC 2016'] ,
    'db/conf/hm': ['Hybrid Metaheuristics', 'HM'] ,
    'db/conf/das': [ 'DAS','Document Analysis Systems'] ,
    'db/conf/lid': ['LID', 'Logic in Databases'] ,
    'db/conf/raid': ['RAID', 'Recent Advances in Intrusion Detection'] ,
    'db/conf/cgi': ['Computer Graphics International', 'CGI'] ,
    'db/conf/pci': ['Panhellenic Conference on Informatics', 'PCI'] ,
    'db/conf/wscg': ['WSCG', 'WSCG Short Papers', 'WSCG Full Papers'] ,
    'db/conf/splc': ['SPLC', 'SPLC B', 'SPLC A', 'Software Product Lines'] ,
    'db/journals/trs': ['Trans. Rough Sets', 'T. Rough Sets'] ,
    'db/journals/ijsnet': ['IJSNet', 'IJSNET'] ,
    'db/journals/cl': ['Comput. Lang.', 'Computer Languages, Systems & Structures'] ,
    'db/conf/frocos': ['FroCoS', 'FroCos'],
    'db/journals/jacic': ['JACIC', 'J. Aerospace Inf. Sys.'] ,
    'db/conf/ieaaie': ['IEA/AIE', 'IEA/AIE Vol. 1', 'IEA/AIE Vol. 2'] ,
    'db/conf/rfid': ['RFID', 'IEEE RFID'] ,
    'db/journals/jasis': ['JASIST', 'JASIS'] ,
    'db/journals/trob': ['IEEE Trans. Robotics and Automation', 'IEEE Trans. Robotics', 'IEEE J. Robotics and Automation'] ,
    'db/journals/ieeecc': ['IEEE Concurrency', 'IEEE P&DT'] ,
    'db/journals/ijksr': ['IJKSR', 'IJSEUS'] ,
    'db/journals/ras': ['Robotics and Autonomous Systems', 'Robotics'] ,
    'db/journals/taslp': ['IEEE Trans. Audio, Speech & Language Processing', 'IEEE/ACM Trans. Audio, Speech & Language Processing', 'IEEE Trans. Speech and Audio Processing'] ,
    'db/journals/jla': ['J. Logic & Analysis', 'Logic & Analysis'] ,
    'db/conf/nas': ['NAS', 'IEEE NAS'] ,
    'db/journals/cis': ['Control and Intelligent Systems', 'Mechatronic Systems and Control'] ,
    'db/journals/cai': ['Computing and Informatics', 'Computers and Artificial Intelligence'] ,
    'db/journals/cib': ['IEEE Intelligent Informatics Bulletin', 'IEEE Computational Intelligence Bulletin'] ,
    'db/journals/debu': ['IEEE Data Eng. Bull.', 'IEEE Database Eng. Bull.'] ,
    'db/journals/ijoe': ['Int. J. Online Eng.', 'Int. J. Online Biomed. Eng.'] ,
    'db/journals/zmp': ['J. Media Psychology', 'Zeitschrift für Medienpsychologie'],
    'db/conf/mcs': ['Multiple Classifier Systems', 'MCS'] ,
    'db/journals/gidr': ['GI Datenbank Rundbrief', 'Datenbank Rundbrief'] ,
    'db/journals/jods': ['J. Data Semantics', 'J. Data Semantics III', 'J. Data Semantics IV', 'J. Data Semantics V', 'J. Data Semantics VII', 'J. Data Semantics VI'] ,
    'db/conf/os': ['Symposium on Operating Systems', 'Conference on Operating Systems'] ,
    'db/conf/csac': ['Computer Supported Acitivity Coordination', 'Computer Supported Activity Coordination'] ,
    'db/conf/aaaifs': ['AAAI Fall Symposia', 'AAAI Fall Symposium: Artificial Intelligence for Prognostics', 'AAAI Fall Symposium: Biologically Inspired Cognitive Architectures', 'AAAI Fall Symposium: Semantic Web for Collaborative Knowledge Acquisition', 'AAAI Fall Symposium: Caring Machines', 'AAAI Fall Symposium: AI and Consciousness', 'AAAI Fall Symposium: AI in Eldercare: New Solutions to Old Problems', 'AAAI Fall Symposium: Artificial Intelligence for Gerontechnology', 'AAAI Fall Symposium: Intelligent Narrative Technologies', 'AAAI Fall Symposium: Capturing and Using Patterns for Evidence Detection', 'AAAI Fall Symposium: Naturally-Inspired Artificial Intelligence', 'AAAI Fall Symposium: Cognitive and Metacognitive Educational Systems', 'AAAI Fall Symposium: Advances in Cognitive Systems', 'AAAI Fall Symposium: Question Generation', 'AAAI Fall Symposium: Integrating Reasoning into Everyday Applications', 'AAAI Fall Symposium: Regarding the Intelligence in Distributed Intelligent Systems', 'AAAI Fall Symposium: Human Control of Bioinspired Swarms', 'AAAI Fall Symposium: Complex Adaptive Systems', 'AAAI Fall Symposium: Computational Approaches to Representation Change during Learning and Development', 'AAAI Fall Symposium: Interaction and Emergent Phenomena in Societies of Agents', 'AAAI Fall Symposium: Virtual Healthcare Interaction', 'AAAI Fall Symposium: Emergent Agents and Socialities', 'AAAI Fall Symposium: Information Retrieval and Knowledge Discovery in Biomedical Text', 'AAAI Fall Symposium: Building Representations of Common Ground with Intelligent Agents', 'AAAI Fall Symposium: Dialog with Robots', 'AAAI Fall Symposium: Proactive Assistant Agents', 'AAAI Fall Symposium: Quantum Informatics for Cognitive, Social, and Semantic Processes', 'AAAI Fall Symposium: Manifold Learning and Its Applications', 'AAAI Fall Symposium: Commonsense Knowledge', 'AAAI Fall Symposium: Multimedia Information Extraction', 'AAAI Fall Symposium: Robot-Human Teamwork in Dynamic Adverse Environment', 'AAAI Fall Symposium: Robots Learning Interactively from Human Teachers', 'AAAI Fall Symposium: Multi-Representational Architectures for Human-Level Intelligence', 'AAAI Fall Symposium: Automated Scientific Discovery', 'AAAI Fall Symposium: Developmental Systems', 'AAAI Fall Symposium: Artificial Intelligence of Humor', 'AAAI Fall Symposium: The Uses of Computational Argumentation', 'AAAI Fall Symposium: Computational Models of Narrative', 'AAAI Fall Symposium: Machine Aggregation of Human Judgment', 'AAAI Fall Symposium: Complex Adaptive Systems and the Threshold Effect', 'AAAI Fall Symposium: Coevolutionary and Coadaptive Systems', 'AAAI Fall Symposium: Aurally Informed Performance', 'AAAI Fall Symposium: Adaptive Agents in Cultural Contexts', 'AAAI Fall Symposium: Discovery Informatics', 'AAAI Fall Symposium: ALEC', 'AAAI Fall Symposium: Agents and the Semantic Web', 'AAAI Fall Symposium: Social Networks and Social Contagion', 'AAAI Fall Symposium: Spacecraft Autonomy'] ,
    'db/conf/aaaiss': ['AAAI Spring Symposia','AAAI Spring Symposium: Data Driven Wellness', 'AAAI Spring Symposium: Technosocial Predictive Analytics', 'AAAI Spring Symposium: Multidisciplinary Collaboration for Socially Assistive Robotics', 'AAAI Spring Symposium: To Boldly Go Where No Human-Robot Team Has Gone Before', 'AAAI Spring Symposium: Intelligent Narrative Technologies II', 'AAAI Spring Symposium: Using AI to Motivate Greater Participation in Computer Science',  'AAAI Spring Symposium: Artificial Intelligence and Sustainable Design', 'AAAI Spring Symposium: Persistent Assistants: Living and Working with AI', 'AAAI Spring Symposium: Cognitive Shape Processing', 'AAAI Spring Symposium: Intelligent Information Privacy Management', 'AAAI Spring Symposium: Symbiotic Relationships between Semantic Web and Knowledge Engineering', 'AAAI Spring Symposium: Interaction Challenges for Intelligent Assistants', 'AAAI Spring Symposium: Computational Approaches to Analyzing Weblogs', 'AAAI Spring Symposium: Self-Tracking and Collective Intelligence for Personal Wellness', 'AAAI Spring Symposium: Experimental Design for Real-World Systems', 'AAAI Spring Symposium: Logical Formalizations of Commonsense Reasoning', 'AAAI Spring Symposium: Semantic Scientific Knowledge Integration', 'AAAI Spring Symposium: Quantum Interaction', 'AAAI Spring Symposium: Modeling Complex Adaptive Systems as if They Were Voting Processes', 'AAAI Spring Symposium: Computational Physiology', 'AAAI Spring Symposium: Argumentation for Consumers of Healthcare', 'AAAI Spring Symposium: Emotion, Personality, and Social Behavior', 'AAAI Spring Symposium: Educational Robotics and Beyond', 'AAAI Spring Symposium: Benchmarking of Qualitative Spatial and Temporal Reasoning Systems', 'AAAI Spring Symposium: Creativity and Early Cognitive Development', 'AAAI Spring Symposium: Linked Data Meets Artificial Intelligence', 'AAAI Spring Symposium: Wisdom of the Crowd', 'AAAI Spring Symposium: Artificial Intelligence for Development', "AAAI Spring Symposium: It's All in the Timing", 'AAAI Spring Symposium: AI for Business Agility', 'AAAI Spring Symposium: Reasoning with Mental and External Diagrams: Computational Modeling and Spatial Assistance', 'AAAI Spring Symposium: AI Technologies for Homeland Security', 'AAAI Spring Symposium: Designing Intelligent Robots', 'AAAI Spring Symposium: Intelligent Web Services Meet Social Computing', 'AAAI Spring Symposium: Agents that Learn from Human Teachers', 'AAAI Spring Symposium: Between a Rock and a Hard Place: Cognitive Science Principles Meet AI-Hard Problems', 'AAAI Spring Symposium: Control Mechanisms for Spatial Knowledge Processing in Cognitive / Intelligent Systems', 'AAAI Spring Symposium: Social Information Processing', 'AAAI Spring Symposium: AI, The Fundamental Social Aggregation Challenge', 'AAAI Spring Symposium: Learning by Reading and Learning to Read', 'AAAI Spring Symposium: What Went Wrong and Why: Lessons from AI Research and Applications', 'AAAI Spring Symposium: Knowledge Collection from Volunteer Contributors', 'AAAI Spring Symposium: Embedded Reasoning', 'AAAI Spring Symposium: Lifelong Machine Learning', 'AAAI Spring Symposium: AI Meets Business Rules and Process Management', 'AAAI Spring Symposium: Towards Conscious AI Systems', 'AAAI Spring Symposium: Game Theory for Security, Sustainability, and Health', 'AAAI Spring Symposium: Challenges to Decision Support in a Changing World', 'AAAI Spring Symposium: Intelligent Event Processing', 'AAAI Spring Symposium: Distributed Plan and Schedule Management', 'AAAI Spring Symposium: Combining Machine Learning with Knowledge Engineering', 'AAAI Spring Symposium: Machine Reading', 'AAAI Spring Symposium: Semantic Web Meets eGovernment', 'AAAI Spring Symposium: Analyzing Microtext', 'AAAI Spring Symposium: Social Semantic Web: Where Web 2.0 Meets Web 3.0', 'AAAI Spring Symposium: Help Me Help You: Bridging the Gaps in Human-Agent Collaboration', 'AAAI Spring Symposium: Intentions in Intelligent Systems', 'AAAI Spring Symposium: Creative Intelligent Systems', 'AAAI Spring Symposium: Human Behavior Modeling', 'AAAI Spring Symposium: Multirobot Systems and Physical Data Structures', 'AAAI Spring Symposium: Formalizing and Compiling Background Knowledge and Its Applications to Knowledge Representation and Question Answering', 'AAAI Spring Symposium: AI and Health Communication', 'AAAI Spring Symposium: Trust and Autonomous Systems', 'AAAI Spring Symposium: Shikakeology', 'AAAI Spring Symposium: Game Theoretic and Decision Theoretic Agents'] ,
    'db/conf/coco': ['Conference on Computational Complexity','IEEE Conference on Computational Complexity', 'Structure in Complexity Theory Conference', 'Computational Complexity Conference', 'Complexity of Computer Computations', 'CCC'] ,
    # SIGOPS
    # - OSDI/SOSP alternate years, so are treated as one venue; USENIX ATC has two variants in DBLP
    # 'ops': ['SOSP', 'OSDI', 'EuroSys'], # 'USENIX Annual Technical Conference', 'USENIX Annual Technical Conference, General Track'],
    'sosp' : ['SOSP'],
    'osdi' : ['OSDI'],
    'eurosys' : ['EuroSys'], # next tier
    'fast' : ['FAST'], # next tier
    'db/conf/sbm': ['SBIM', 'SBM'] ,
    'usenixatc' : ['USENIX','USENIX Annual Technical Conference', 'USENIX Annual Technical Conference, General Track','USENIX Winter', 'USENIX Summer'], # next tier
    # SIGMETRICS
    # - Two variants for each, as in DBLP.
    # 'metrics': ['SIGMETRICS', 'SIGMETRICS/Performance', 'POMACS','IMC', 'Internet Measurement Conference'],
    'imc': ['IMC', 'Internet Measurement Conference'],
    'sigmetrics': ['SIGMETRICS', 'SIGMETRICS/Performance', 'POMACS'],
    'db/conf/csoc': ['CSOC', 'CSOS'] ,
    # SIGMOBILE
    # 'mobile': ['MobiSys', 'MobiCom', 'MOBICOM', 'SenSys'],
    'mobisys' : ['MobiSys'],
    'mobicom' : ['MobiCom', 'MOBICOM'],
    'sensys'  : ['SenSys'],
    'social': ['SocialCom','SocialCom/PASSAT'],
    # SIGHPC
    # 'hpc': ['SC', 'HPDC', 'ICS'],
    'sc': ['SC','SC Companion'],
    'hpdc': ['HPDC'],
    'ics': ['ICS'],
    # SIGBED
    # 'bed': ['RTSS', 'RTAS', 'IEEE Real-Time and Embedded Technology and Applications Symposium', 'EMSOFT'],
    'emsoft': ['EMSOFT', 'ACM Trans. Embedded Comput. Syst.'], # TECS: issue number & page numbers must be checked
    'rtss' : ['RTSS'],
    'rtas' : ['RTAS', 'IEEE Real-Time and Embedded Technology and Applications Symposium'],
    # SIGDA
    # 'da': ['ICCAD', 'DAC'],
    'iccad': ['ICCAD'],
    'dac' : ['DAC'],
    # SIGMOD
    # 'mod': ['VLDB', 'PVLDB', 'SIGMOD Conference'],
    'vldb' : ['VLDB', 'PVLDB'],
    'sigmod' : ['SIGMOD Conference'],
    'icde' : ['ICDE'], # next tier
    'pods' : ['PODS'], # next tier
    'assets': ['ASSETS','International ACM Conference on Assistive Technologies'],
    # SIGSAC
    # - USENIX Security listed twice to reflect variants in DBLP
    # 'sec': ['IEEE Symposium on Security and Privacy', 'ACM Conference on Computer and Communications Security', 'USENIX Security Symposium', 'USENIX Security', 'CCS'], # , 'NDSS'],
    'ccs': ['CCS', 'ACM Conference on Computer and Communications Security'],
    'oakland' : ['IEEE Symposium on Security and Privacy'],
    'usenixsec' : ['USENIX Security Symposium', 'USENIX Security'],
    'ndss' : ['NDSS'],
    'pets' : ['PoPETs', 'Privacy Enhancing Technologies'],
    'xp':  ['XP', 'XP Workshops','XP1 Workshop on Database Theory','XP2 Workshop on Relational Database Theory','XP4.5 Workshop on Database Theory', 'XP7.52 Workshop on Database Theory'],
    # SIGCOMM
    # 'comm': ['SIGCOMM', 'NSDI'], # INFOCOM
    'sigcomm': ['SIGCOMM'],
    'dmkd': ['DMKD','1999 ACM SIGMOD Workshop on Research Issues in Data Mining and Knowledge Discovery', 'ACM SIGMOD Workshop on Research Issues in Data Mining and Knowledge Discovery'],
    'nsdi': ['NSDI'], # INFOCOM
    # SIGARCH
    # 'arch': ['ISCA', 'MICRO', 'ASPLOS'],
    'asplos': ['ASPLOS'],
    'isca': ['ISCA'],
    'micro': ['MICRO'],
    'hpca': ['HPCA'], # next tier
    # SIGLOG
    # 'log': ['CAV', 'CAV (1)', 'CAV (2)', 'LICS', 'CSL-LICS'],
    'cav': ['CAV', 'CAV (1)', 'CAV (2)'],
    'lics' : ['LICS', 'CSL-LICS'],
    # SIGACT
    # 'act': ['STOC', 'FOCS', 'SODA'],
    'focs': ['FOCS','SWAT (FOCS)','SWCT'],
    'stoc': ['STOC'],
    'soda': ['SODA'],
    'IS':['IS','IEEE Conf. of Intelligent Systems','IEEE Conf. on Intelligent Systems'],
    # 'mlmining': ['NIPS', 'ICML', 'ICML (1)', 'ICML (2)', 'ICML (3)', 'KDD'],
    'nips': ['NIPS', 'NeurIPS'],
    'icml': ['ICML', 'ICML (1)', 'ICML (2)', 'ICML (3)','ML'],
    'kdd' : ['KDD'],
    # 'ai': ['AAAI', 'AAAI/IAAI', 'IJCAI'],
    'aaai': ['AAAI', 'AAAI/IAAI'],
    'ijcai': ['IJCAI'],
    # AAAI listed to account for AAAI/IAAI joint conference
    # SIGGRAPH
    # - special handling of TOG to select SIGGRAPH and SIGGRAPH Asia
    'siggraph': ['SIGGRAPH'],
#    'siggraph' : ['SIGGRAPH'],
    'siggraph-asia' : ['SIGGRAPH Asia'],
    # SIGIR
    # 'ir': ['WWW', 'SIGIR'],
    'sigir': ['SIGIR'],
    'www': ['WWW'],
    # SIGCHI
    # 'chi': ['CHI', 'UbiComp', 'Ubicomp', 'UIST', 'IMWUT', 'Pervasive'],
    'chiconf' : ['CHI'],
    'ubicomp' : ['UbiComp', 'Ubicomp', 'IMWUT', 'Pervasive'],
    'uist' : ['UIST','ACM Symposium on User Interface Software and Technology'],
#    'nlp': ['EMNLP', 'ACL', 'ACL (1)', 'ACL (2)', 'NAACL', 'HLT-NAACL', 'NAACL-HLT',
#            'ACL/IJCNLP',  # -- in 2009 was joint
#            'COLING-ACL',  # -- in 1998 was joint
#            'EMNLP-CoNLL',  # -- in 2012 was joint
#            'HLT/EMNLP',  # -- in 2005 was joint
#            ],
    'emnlp': ['EMNLP', 'EMNLP-CoNLL', 'HLT/EMNLP'],
    'acl' : ['ACL', 'ACL (1)', 'ACL (2)', 'ACL/IJCNLP', 'COLING-ACL'],
    'naacl' : ['NAACL', 'HLT-NAACL', 'NAACL-HLT', 'NAACL-HLT (1)','NAACL-HLT (2)'],
#    'vision': ['CVPR', 'CVPR (1)', 'CVPR (2)', 'ICCV', 'ECCV', 'ECCV (1)', 'ECCV (2)', 'ECCV (3)', 'ECCV (4)', 'ECCV (5)', 'ECCV (6)', 'ECCV (7)'],
    'cvpr': ['CVPR', 'CVPR (1)', 'CVPR (2)'],
    'iccv': ['ICCV'],
    'eccv': ['ECCV', 'ECCV (1)', 'ECCV (2)', 'ECCV (3)', 'ECCV (4)', 'ECCV (5)', 'ECCV (6)', 'ECCV (7)', 'ECCV (8)', 'ECCV (9)', 'ECCV (10)', 'ECCV (11)', 'ECCV (12)', 'ECCV (13)', 'ECCV (14)', 'ECCV (15)', 'ECCV (16)'],
    # 'robotics': ['ICRA', 'ICRA (1)', 'ICRA (2)', 'IROS', 'Robotics: Science and Systems'],
    'icra': ['ICRA', 'ICRA (1)', 'ICRA (2)'],
    'iros': ['IROS'],
    'icme': ['ICME','ICMCS'],
    'rss': ['Robotics: Science and Systems'],
    # 'crypt': ['CRYPTO', 'CRYPTO (1)', 'CRYPTO (2)', 'CRYPTO (3)', 'EUROCRYPT', 'EUROCRYPT (1)', 'EUROCRYPT (2)', 'EUROCRYPT (3)'],
    'crypto': ['CRYPTO', 'CRYPTO (1)', 'CRYPTO (2)', 'CRYPTO (3)'],
    'eurocrypt': ['EUROCRYPT', 'EUROCRYPT (1)', 'EUROCRYPT (2)', 'EUROCRYPT (3)'],
    # SIGBio
    # - special handling for ISMB proceedings in Bioinformatics special issues.
    # 'bio': ['RECOMB', 'ISMB', 'Bioinformatics', 'ISMB/ECCB (Supplement of Bioinformatics)', 'Bioinformatics [ISMB/ECCB]', 'ISMB (Supplement of Bioinformatics)'],
    'ismb': ['ISMB', 'Bioinformatics', 'ISMB/ECCB (Supplement of Bioinformatics)', 'Bioinformatics [ISMB/ECCB]', 'ISMB (Supplement of Bioinformatics)'],
    'recomb' : ['RECOMB'],
    # special handling of IEEE TVCG to select IEEE Vis and VR proceedings
    'vis': ['IEEE Visualization', 'IEEE Trans. Vis. Comput. Graph.'],
    'vr' : ['VR'],
    # 'ecom' : ['EC', 'WINE']
    'ec' : ['EC'],
    'wine' : ['WINE']
    # ,'cse' : ['SIGCSE']
}
inverse_area_dict = {}
for k,v in areadict.items():
    n = len(v)
    for i in range(1,n):
        inverse_area_dict[v[i]] = v[0]
# ISSTA/ECOOP Workshop  SpringSim (MSCIAAS) ICoMS CCKS
# EMSOFT is now published as a special issue of TECS, in a particular page range.
EMSOFT_TECS = { 2017: (16, 5) }
EMSOFT_TECS_PaperNumbers = { 2017: (163, 190) } # "pages" 163--190

# ISMB proceedings are published as special issues of Bioinformatics.
# Here is the list.
ISMB_Bioinformatics = {2018: (34, 13),
                       2017: (33, 14),
                       2016: (32, 12),
                       2015: (31, 12),
                       2014: (30, 12),
                       2013: (29, 13),
                       2012: (28, 12),
                       2011: (27, 13),
                       2010: (26, 12),
                       2009: (25, 12),
                       2008: (24, 13),
                       2007: (23, 13)
                       }

# TOG special handling to count only SIGGRAPH proceedings.
# Assuming all will be in the same issues through 2021.
TOG_SIGGRAPH_Volume = {2021: (40, 4),
                       2020: (39, 4),
                       2019: (38, 4),
                       2018: (37, 4),
                       2017: (36, 4),
                       2016: (35, 4),
                       2015: (34, 4),
                       2014: (33, 4),
                       2013: (32, 4),
                       2012: (31, 4),
                       2011: (30, 4),
                       2010: (29, 4),
                       2009: (28, 3),
                       2008: (27, 3),
                       2007: (26, 3),
                       2006: (25, 3),
                       2005: (24, 3),
                       2004: (23, 3)
                       }

# TOG special handling to count only SIGGRAPH Asia proceedings.
# Assuming all will be in the same issues through 2021.
TOG_SIGGRAPH_Asia_Volume = {2021: (40, 6),
                            2020: (39, 6),
                            2019: (38, 6),
                            2018: (37, 6),
                            2017: (36, 6),
                            2016: (35, 6),
                            2015: (34, 6),
                            2014: (33, 6),
                            2013: (32, 6),
                            2012: (31, 6),
                            2011: (30, 6),
                            2010: (29, 6),
                            2009: (28, 5),
                            2008: (27, 5)
                            }

# TVCG special handling to count only IEEE VIS
TVCG_Vis_Volume = {2021: (27, 1),
                   2020: (26, 1),
                   2019: (25, 1),
                   2018: (24, 1),
                   2017: (23, 1),
                   2016: (22, 1),
                   2014: (20, 12),
                   2013: (19, 12),
                   2012: (18, 12),
                   2011: (17, 12),
                   2010: (16, 6),
                   2009: (15, 6),
                   2008: (14, 6),
                   2007: (13, 6),
                   2006: (12, 5)
                   }

# TVCG special handling to count only IEEE VR
TVCG_VR_Volume = {2021: (27, 4),
                  2020: (26, 4),
                  2019: (25, 4),
                  2018: (24, 4),
                  2017: (23, 4),
                  2016: (22, 4),
                  2015: (21, 4),
                  2014: (20, 4),
                  2013: (19, 4),
                  2012: (18, 4)}

# ICSE special handling to omit short papers.
# Contributed by Zhendong Su, UC Davis.
# Short papers start at this page number for these proceedings of ICSE (and are thus omitted,
# as the acceptance criteria differ).
ICSE_ShortPaperStart = {2013: 851,
                        2012: 957,
                        2011: 620,
                        2010: 544,
                        2009: 550,
                        2007: 510,
                        2006: 411,
                        2005: 478,
                        2003: 477,
                        2002: 534,
                        2001: 502,
                        2000: 518,
                        1999: 582,
                        1998: 419,
                        1997: 535}

# SIGMOD special handling to avoid non-research papers.
# This and other SIGMOD data below contributed by Davide Martinenghi,
# Politecnico di Milano.
SIGMOD_NonResearchPaperStart = {2017: 1587,
                                2016: 2069,
                                2013: 917,
                                2012: 577,
                                2011: 1045,
                                2010: 963,
                                2009: 841,
                                2008: 1043,
                                2007: 873,
                                2006: 695,
                                2005: 778,
                                2004: 839,
                                2003: 635,
                                2002: 500,
                                2001: 521,
                                2000: 499,
                                1999: 503,
                                1998: 496,
                                1997: 498,
                                1996: 541,
                                1995: 423,
                                1994: 466,
                                1993: 388}

# SIGMOD recently has begun intermingling research and non-research
# track papers in their proceedings, requiring individual paper
# filtering.
SIGMOD_NonResearchPapersRange = { 2018 : [(177, 230), (583, 627), (789, 839), (1393, 1459),
                                          (1637, 1845)],
                                  2017: [(1, 3), (51, 63), (125, 138), (331, 343),
                                         (1041, 1052), (511, 526), (1587, 1782)],
                                  2016: [(1753, 1764), (1295, 1306), (795, 806),
                                        (227, 238), (999, 1010), (1923, 1934),
                                        (1307, 1318), (1951, 1960), (759, 771),
                                        (253, 265), (1405, 1416), (215, 226),
                                        (1105, 1117), (35, 46), (63, 75),
                                        (807, 819), (1099, 1104), (1087, 1098),
                                        (847, 859), (239, 251), (1393, 1404),
                                        (2069, 2243)],
                                 2015: [(227, 276), (607, 658), (1343, 1394),
                                        (1657, 1706), (1917, 1940),
                                        (859, 918), (1063, 1122), (1403, 1462)],
                                 2014: [(147, 188), (337, 384), (529, 573), (1223, 1258)]}



pageCounterNormal = re.compile('(\d+)-(\d+)')
# Match page number in the form volume:page (as in 12:140-12:150).
pageCounterColon = re.compile('[0-9]+:([1-9][0-9]*)-[0-9]+:([1-9][0-9]*)')
# Special regexp for extracting pseudo-volumes (paper number) from TECS.
TECSCounterColon = re.compile('([0-9]+):[1-9][0-9]*-([0-9]+):[1-9][0-9]*')
# Extract the ISMB proceedings page numbers.
ISMBpageCounter = re.compile('i(\d+)-i(\d+)')
def startpage(pageStr):
    """Compute the starting page number from a string representing page numbers."""
    global pageCounterNormal
    global pageCounterColon
    if pageStr is None:
        return 0
    pageCounterMatcher1 = pageCounterNormal.match(pageStr)
    pageCounterMatcher2 = pageCounterColon.match(pageStr)
    start = 0

    if not pageCounterMatcher1 is None:
        start = int(pageCounterMatcher1.group(1))
    else:
        if not pageCounterMatcher2 is None:
            start = int(pageCounterMatcher2.group(1))
    return start

#def pagecount(pageStr : str) : int:
def pagecount(pageStr):
    """Compute the number of pages in a string representing a range of page numbers."""
    if pageStr is None:
        return 0
    pageCounterMatcher1 = pageCounterNormal.match(pageStr)
    pageCounterMatcher2 = pageCounterColon.match(pageStr)
    start = 0
    end = 0
    count = 0

    if not pageCounterMatcher1 is None:
        start = int(pageCounterMatcher1.group(1))
        end = int(pageCounterMatcher1.group(2))
        count = end - start + 1
    else:
        if not pageCounterMatcher2 is None:
            start = int(pageCounterMatcher2.group(1))
            end = int(pageCounterMatcher2.group(2))
            count = end - start + 1
    return count

parser = etree.iterparse(source=gzip.GzipFile('download/dblp.xml.gz','rb'), dtd_validation=False, load_dtd=True)
counter = 0
main_log = []

existing_tags = {}
named_aliases = []
for event, elem in parser:
    title, authors, venue, pages, startPage,year, volume,number,url,publtype,eb_toofew,eb_skip= None, [], None, -1, -1, 0, '0', '0','',None,False,False
    insert_data = True
    if elem.tag == 'www': #and 'homepages' in elem.key:
        tag_info = [_ for _ in elem]
        author_names = [_.text for _ in tag_info if _.tag == 'author']
        is_homepage = sum(['Home Page' in _.text for _ in tag_info if _.tag == 'title']) > 0
        if is_homepage and len(author_names) > 1:
            named_aliases.append(author_names)

    #existing_tags[elem.tag] = 1 + existing_tags.get(elem.tag,0)
    if elem.tag in {"article", "inproceedings", "proceedings", "book", "incollection"}:
        for sub in elem:
            if sub.tag == 'title':
                title = re.sub("<.*?>", "", etree.tostring(sub).decode('utf-8')) if sub.text is None else sub.text
            elif sub.tag == 'booktitle':
                venue = re.sub("<.*?>", "", etree.tostring(sub).decode('utf-8')) if sub.text is None else sub.text
            elif sub.tag == 'journal':
                venue = re.sub("<.*?>", "", etree.tostring(sub).decode('utf-8')) if sub.text is None else sub.text
            elif sub.tag == 'pages':
                pageCount = sub.text
                pages = pagecount(sub.text)
                startPage = startpage(sub.text)
            elif sub.tag == 'author':
                authors.append(sub.text)
            elif sub.tag == 'year' and sub.text != None:
                year = int(sub.text)
            elif sub.tag == 'volume':
                volume = sub.text
            elif sub.tag == 'number':
                number = sub.text
            elif sub.tag == 'url':
                url = sub.text
        if elem.get('publtype') != None:
            publtype  = elem.get('publtype')

        if venue == 'ACM Trans. Embedded Comput. Syst.':
            if year in EMSOFT_TECS:
                pvmatcher = TECSCounterColon.match(pageCount)
                if not pvmatcher is None:
                    pseudovolume = int(pvmatcher.group(1))
                    (startpv, endpv) = EMSOFT_TECS_PaperNumbers[year]
                    if pseudovolume < int(startpv) or pseudovolume > int(endpv):
                        eb_skip = True
            else:
                eb_skip = True


        if venue == 'PACMPL':
            venue = number
        elif venue == 'ACM Trans. Graph.':
            if year in TOG_SIGGRAPH_Volume:
                (vol, num) = TOG_SIGGRAPH_Volume[year]
                if (volume == str(vol)) and (number == str(num)):
                    venue = 'SIGGRAPH'
            if year in TOG_SIGGRAPH_Asia_Volume:
                (vol, num) = TOG_SIGGRAPH_Asia_Volume[year]
                if (volume == str(vol)) and (number == str(num)):
                    venue = 'SIGGRAPH Asia'
        elif venue == 'IEEE Trans. Vis. Comput. Graph.':
            if year in TVCG_VR_Volume:
                (vol, num) = TVCG_VR_Volume[year]
                if (volume == str(vol)) and (number == str(num)):
                    venue = 'VR'
        elif venue == 'Int. J. Computer Assisted Radiology and Surgery':
            ipcai_lookup = {2015: [6], 2016: [6], 2017: [6,7], 2018:[5,6], 2019:[6,7]}
            if number.isdigit():
                number = int(number)
                if (year in ipcai_lookup) and (number in ipcai_lookup[year]):
                    #print(volume,number,year,title,authors)
                    venue = 'IPCAI'


        # Special handling for ISMB.
        if venue == 'Bioinformatics':
            if year in ISMB_Bioinformatics:
                (vol, num) = ISMB_Bioinformatics[year]
                if (volume != str(vol)) or (number != str(num)):
                    eb_skip = True
                else:
                    if (int(volume) >= 33): # Hopefully this works going forward.
                        pg = ISMBpageCounter.match(pageCount)
                        if pg == None:
                            eb_skip = True
                        else:
                            startPage = int(pg.group(1))
                            end = int(pg.group(2))
                            pages = end - startPage + 1
            else:
                eb_skip = True
        # Special handling for SIGMOD.
        elif venue == 'SIGMOD Conference':
            if year in SIGMOD_NonResearchPaperStart:
                pageno = SIGMOD_NonResearchPaperStart[year]
                if startPage >= pageno:
                    eb_skip = True
            if year in SIGMOD_NonResearchPapersRange:
                pageRange = SIGMOD_NonResearchPapersRange[year]
                for p in pageRange:
                    if startPage >= p[0] and startPage + pages - 1 <= p[1]:
                       eb_skip = True
        # Special handling for SIGGRAPH and SIGGRAPH Asia.
        elif venue in areadict['siggraph']: # == 'ACM Trans. Graph.':
            if year in TOG_SIGGRAPH_Volume:
                (vol, num) = TOG_SIGGRAPH_Volume[year]
                if not ((volume == str(vol)) and (number == str(num))):
                    eb_skip = True
        elif venue in areadict['siggraph-asia']: # == 'ACM Trans. Graph.':
            if year in TOG_SIGGRAPH_Asia_Volume:
                (vol, num) = TOG_SIGGRAPH_Asia_Volume[year]
                if not((volume == str(vol)) and (number == str(num))):
                    eb_skip = True

        # Special handling for IEEE Vis and VR
        elif venue == 'IEEE Trans. Vis. Comput. Graph.':
            Vis_Conf = False
            if year in TVCG_Vis_Volume:
                (vol, num) = TVCG_Vis_Volume[year]
                if (volume == str(vol)) and (number == str(num)):
                    Vis_Conf = True
            if year in TVCG_VR_Volume:
                (vol, num) = TVCG_VR_Volume[year]
                if (volume == str(vol)) and (number == str(num)):
                    Vis_Conf = True
            if not Vis_Conf:
                eb_skip = True

        # Disambiguate Innovations in (Theoretical) Computer Science from
        # International Conference on Supercomputing
        elif venue == 'ICS':
            if not url is None:
                if url.find('innovations') != -1:
                    eb_skip = True
        if pages == -1 and venue == 'ACM Conference on Computer and Communications Security':
            eb_toofew = True

        if ((pages != -1) and (pages < 6)):
            eb_toofew = True
            exceptionConference = False
            exceptionConference |= venue == 'SC' and year <= 2012
            exceptionConference |= venue == 'SIGSOFT FSE' and year == 2012
            exceptionConference |= venue == 'ACM Trans. Graph.' and int(volume) >= 26 and int(volume) <= 36
            exceptionConference |= venue == 'SIGGRAPH' and int(volume) >= 26 and int(volume) <= 36
            exceptionConference |= venue == 'CHI' and year == 2018 # FIXME - hopefully DBLP will fix
            exceptionConference |= venue == 'ICCAD' and year == 2018
            exceptionConference |= venue == 'CHI' and year == 2019
            exceptionConference |= venue == 'FAST' and year == 2012
            if exceptionConference:
                eb_toofew = False
        



        insert_data = False if (venue is None or year < 1970 or len(authors) == 0) else insert_data
        #if 'Jonathan T. Moon' in authors:
        #    print(title,authors,venue,pages,insert_data)
        if insert_data:
            venue = inverse_area_dict.get(venue,venue)
            split_venue = venue.split(' ')
            # turn CVPR (1) to CVPR
            if len(split_venue) > 0 and len(split_venue[-1]) > 2 and split_venue[-1][-1] == ')' and split_venue[-1][1:-1].isnumeric():
                venue = ' '.join(split_venue[:-1])

            if venue != None:
                venue = venue.replace('SIGGRAPH ASIA','SIGGRAPH Asia')
                venue = venue.replace('(','').replace(')','')

            data = (elem.tag,title, authors, venue, pages, startPage,year,volume,number,url,publtype,eb_toofew,eb_skip)
            main_log.append(data)
            if 'Angela Dai' in authors:
                print(data)
            if 'Leonid Keselman' in authors:
                print(data)
        #print(elem.tag,title, authors, venue, pages, startPage,year)
        #print(elem.text)
        #print([(s.tag,s.text, etree.tostring(sub)) for s in elem])
        elem.clear()
        for ancestor in elem.xpath('ancestor-or-self::*'):
            while ancestor.getprevious() is not None:
                del ancestor.getparent()[0]
    counter +=1
    if (counter % 100000) == 0:
        print('Parsed {} items'.format(counter))
        #print(existing_tags)
with gzip.open('dblp_aliases_auto.pkl.gz','wb') as fp:
    pickle.dump(named_aliases,fp, -1)
with gzip.open('parsed_files.pkl.gz','wb') as fp:
    pickle.dump(main_log,fp, -1)
