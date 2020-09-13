from spacy.matcher import Matcher
from tqdm import tqdm
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import spacy

nlp = spacy.load('en_core_web_sm')


# From Analytics Vidhya
def get_entities(sent):

    ent1 = ""
    ent2 = ""
    prv_tok_dep = ""
    prv_tok_text = ""
    prefix = ""
    modifier = ""
    for tok in nlp(sent):
        if tok.dep_ != "punct":
            if tok.dep_ == "compound":
                prefix = tok.text
                if prv_tok_dep == "compound":
                    prefix = prv_tok_text + " " + tok.text

            if tok.dep_.endswith("mod") == True:
                modifier = tok.text
                if prv_tok_dep == "compound":
                    modifier = prv_tok_text + " " + tok.text

            if tok.dep_.find("subj") == True:
                ent1 = modifier + " " + prefix + " " + tok.text
                prefix = ""
                modifier = ""
                prv_tok_dep = ""
                prv_tok_text = ""

            if tok.dep_.find("obj") == True:
                ent2 = modifier + " " + prefix + " " + tok.text

            prv_tok_dep = tok.dep_
            prv_tok_text = tok.text

    return [ent1.strip(), ent2.strip()]


# From Analytics Vidhya
def get_relation(sent):

    doc = nlp(sent)
    matcher = Matcher(nlp.vocab)
    pattern = [{'DEP': 'ROOT'},
               {'DEP': 'prep', 'OP': "?"},
               {'DEP': 'agent', 'OP': "?"},
               {'POS': 'ADJ', 'OP': "?"}]
    matcher.add("matching_1", None, pattern)
    matches = matcher(doc)
    k = len(matches) - 1
    span = doc[matches[k][1]:matches[k][2]]
    return(span.text)


def main():

    candidate_sentences = pd.read_csv("wiki_sentences_v2.csv")

    entity_pairs = []
    relations = []
    locations = []
    persons = []
    persons_centrality = []
    locations_cetrality = []

    for i in tqdm(candidate_sentences["sentence"]):
        entity_pairs.append(get_entities(i))
        relations.append(get_relation(i))
        doc = nlp(i)
        for ent in doc.ents:
            if(ent.label_ is 'GPE'):
                locations.append(ent.text.strip())
            if(ent.label_ is 'PERSON'):
                persons.append(ent.text.strip())

    source = [i[0] for i in entity_pairs]
    target = [i[1] for i in entity_pairs]

    # Removing mutliple occurances
    locations = set(locations)
    persons = set(persons)

    kg_df = pd.DataFrame(
        {'source': source, 'target': target, 'edge': relations})
    G = nx.from_pandas_edgelist(
        kg_df, "source", "target", edge_attr=True, create_using=nx.MultiDiGraph())

    # Centrality for all nodes
    centrality = nx.closeness_centrality(G)

    # Extracting Person centralities
    for x in persons:
        if x in centrality.keys():
            persons_centrality.append([centrality[x], x])

    # Extracting location centralities
    for x in locations:
        if x in centrality.keys():
            locations_cetrality.append([centrality[x], x])

    # Sorting
    persons_centrality.sort(reverse=True)
    locations_cetrality.sort(reverse=True)

    # Printing
    print("\n\nImportant personalities\n")
    for x in persons_centrality[:10]:
        print(x[1])

    print("\n\nImportant locations\n")
    for x in locations_cetrality[:10]:
        print(x[1])

    # Code for ploting -------------------------------------------------------------------------------------------------------

    # kg_df.to_csv('graph.csv')
    # plt.figure(figsize=(12, 12))
    # pos = nx.spring_layout(G)
    # nx.draw(G, with_labels=True, node_color='skyblue',
    #         edge_cmap=plt.cm.Blues, pos=pos)
    # plt.show()

    # G = nx.from_pandas_edgelist(kg_df[kg_df['edge'] == "became"],
    #                             "source", "target", edge_attr=True, create_using=nx.MultiDiGraph())
    # plt.figure(figsize=(12, 12))
    # pos = nx.spring_layout(G, k=0.5)
    # nx.draw(G, with_labels=True, node_color='skyblue',
    #         node_size=1500, edge_cmap=plt.cm.Blues, pos=pos)
    # plt.show()

    # -----------------------------------------------------------------------------------------------------------------------


if __name__ == "__main__":
    main()
