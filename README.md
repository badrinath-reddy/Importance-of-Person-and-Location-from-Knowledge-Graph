# Importance of Persons And Locations Using Knowledge Graph

## Procedure

- By following all the steps in the [Analytics Vidhya](https://www.analyticsvidhya.com/blog/2019/10/how-to-build-knowledge-graph-text-using-spacy/), I built the KG.
- Using spacy NER I found persons and location nodes.
- I used closeness centrality to find importance of node.
- I sorted the persons and locations nodes WRT centrality and printed top 10 occurances.

## Instructions

### Setup in windows

- Download the data and place in the main folder

### Run

- virtualenv venv
- venv\Scripts\activate
- pip install -r requirements.txt
- python -m spacy download en_core_web_sm
- python main.py

## Note

- There are some outliers due to incorrect spacy NER.
- We can use many other centralities, I choose closeness centrality.
- We can use other NER like DBpedia Spotlight.

## Refrences

- [Knowledge Graph](https://www.analyticsvidhya.com/blog/2019/10/how-to-build-knowledge-graph-text-using-spacy/)
- [Data](https://drive.google.com/file/d/1yuEUhkVFIYfMVfpA_crFGfSeJLgbPUxu/view)
- [Centrality](https://www.geeksforgeeks.org/network-centrality-measures-in-a-graph-using-networkx-python/)
