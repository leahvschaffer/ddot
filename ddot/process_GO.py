import os, requests, gzip, sys
from ddot import *
import mygene
import pandas as pd

ndex_server = raw_input('http://www.ndexbio.org or http://test.ndexbio.org:')
ndex_user = raw_input('Enter your username:')
ndex_pass = raw_input('Enter your password:')

now = datetime.now().strftime("%Y%m%d")

dirname = 'GeneOntology_{}'.format(now)
if os.path.isdir(dirname)==False:
    os.makedirs(dirname)
    os.chdir(dirname)

# Download GO obo file
r = requests.get('http://purl.obolibrary.org/obo/go/go-basic.obo')
with open('go-basic.obo', 'wb') as f:
    f.write(r.content)

# Parse OBO file
parse_obo('go-basic.obo', 'go.tab', 'goID_2_name.tab', 'goID_2_namespace.tab', 'goID_2_alt_id.tab')

# Download gene-term annotations for human
r = requests.get('http://geneontology.org/gene-associations/goa_human.gaf.gz')
with open('goa_human.gaf.gz', 'wb') as f:
    f.write(r.content)

hierarchy = pd.read_table('go.tab',
                          sep='\t',
                          header=None,
                          names=['Parent', 'Child', 'Relation', 'Namespace'])
with gzip.open('goa_human.gaf.gz', 'rb') as f:
    mapping = parse_gaf(f)

if len(sys.argv) == 1:
    go_human = Ontology.from_table(
        table=hierarchy,
        parent='Parent',
        child='Child',
        mapping=mapping,
        mapping_child='DB Object ID',
        mapping_parent='GO ID',
        add_root_name='GO:00SUPER',
        ignore_orphan_terms=True, clixo_format=False)
    go_human.clear_node_attr()
    go_human.clear_edge_attr()
    aspect = ''
else:
    aspect= sys.argv[1]
    if not aspect in ['P', 'C', 'F']:
        raise Exception("aspect needs to be one of P(BP), C(CC), F(MF)")
    go_human = Ontology.from_table(
        table=hierarchy,
        parent='Parent',
        child='Child',
        mapping=mapping.loc[mapping['Aspect'] == aspect, :],
        #         mapping=mapping.loc[mapping['DB'] == 'UniProtKB', :],
        mapping_child='DB Object ID',
        mapping_parent='GO ID',
        ignore_orphan_terms=False, clixo_format=False)  # if true, bug, can't proceed
    go_human.clear_node_attr()
    go_human.clear_edge_attr()

# convert Uniprot IDs to Hugo Symbols
mg = mygene.MyGeneInfo()
uniprot_2_symbol_df = mg.querymany(go_human.genes, scopes='uniprot', fields='symbol', species='human', as_dataframe=True)

def f(x):
    x = x['symbol']
    if len(x)==1:
        return x[0]
    else:
        return x.tolist()
uniprot_2_symbol = uniprot_2_symbol_df.dropna(subset=['symbol']).groupby('query').apply(f)

go_human_symbol = go_human.delete(to_delete=set(go_human.genes) - set(uniprot_2_symbol.keys()))
go_human_symbol = go_human_symbol.collapse_ontology(method='python')
# if 'GO:00SUPER' not in go_human.terms: go_human.add_root('GO:00SUPER', inplace=True)

# get those terms with only 1 gene (not needed; handled by collapse_ontology
# lonely_terms = [go_human_symbol.terms[i] for i in range(len(go_human_symbol.terms)) if go_human_symbol.term_sizes[i] <= 1]
# go_human_symbol = go_human_symbol.delete(to_delete = lonely_terms,
#                                          preserve_transitivity=True)

# need re-route of edges (why not handled by collapseOntology?)


# remove indirect connection
graph = go_human_symbol.to_igraph()
graph.es['weight'] = -1
for p in go_human_symbol.parent_2_child:
    children =[c for c in go_human_symbol.parent_2_child[p]]
    for c in children: # cannot do this ! pointer leaked
        long_path = graph.shortest_paths(c, p, weights='weight')
        if long_path[0][0] != -1:
            go_human_symbol.parent_2_child[p].remove(c)
            go_human_symbol.child_2_parent[c].remove(p)

go_human_symbol.propagate('reverse', inplace=True)


go_human_symbol = go_human_symbol.rename(genes=uniprot_2_symbol.to_dict())
print(go_human_symbol)
# Write GO to file
_ = go_human_symbol.to_table('processed_go_{}.symbol'.format(aspect), clixo_format=True)

dict_term_name = pd.read_table('goID_2_name.tab', index_col=0, header=None)[1].to_dict()
go_human_symbol.node_attr['Label'] = pd.Series(dict_term_name)
# upload to NDEx
# ndex_server = input()

url, ont_ndexgraph = go_human_symbol.to_ndex(name=dirname + '_' + aspect,
                                 ndex_server=ndex_server, ndex_user=ndex_user, ndex_pass=ndex_pass,
                                 layout='bubble-collect', style='passthrough',
                                 visible_term_attr=['Size'],
                                 verbose=True)
print(url)