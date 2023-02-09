import sys
import argparse
import pandas as pd
from time import sleep
from ddot import *
import ndex2.client as nc2

def geneset2pairs(genelist):
    genelist.sort()
    pairlist = []
    for c in itertools.combinations(genelist, 2):
        pair = [c[0], c[1]]
        pair.sort()
        pairlist.append(pair)
    return pairlist

def ont_2_genepairs(ont, max_tsize):
    # ont = ont.propagate(direction='forward')
    pairs_seen = {}
    pairs = []
    for t,s in zip(ont.terms, ont.term_sizes):
        if s > max_tsize:
            continue
        else:
            genelist = [ont.genes[g] for g in ont.term_2_gene[t]]
            pairlist = geneset2pairs(genelist)
            for p in pairlist:
                if p[0] + ' ' + p[1] in pairs_seen:
                    continue
                else:
                    pairs.append([p[0], p[1]])
                    pairs_seen[p[0] + ' ' + p[1]] = 1
            # print(t)
    return pairs

def support_data_focus(pairs, rf_score, netlinks=None):
    gene1, gene2 = [], []
    for p in pairs:
        g1, g2 = p[0], p[1]
        gene1.append(g1)
        gene2.append(g2)

    df = pd.DataFrame.from_dict(dict([('Gene1', gene1), ('Gene2', gene2)]))
    df_rf = pd.read_table(rf_score, sep='\t', header=None)
    if df_rf.shape[1] < 3:
        df_rf[2] = 1.0
    df_rf.rename(columns = {0:'Gene1', 1:'Gene2', 2:'Score'}, inplace=True)
    df_rf[['Gene1', 'Gene2']] = np.sort(df_rf[['Gene1', 'Gene2']], axis=1)
    df = df_rf.merge(df, how='left', on=['Gene1', 'Gene2'])

    data_categories = {}

    if netlinks != None:
        for l in open(netlinks).readlines():
            if l.startswith('#'):
                continue
            info = l.strip().split('\t')
            name, loc = info[0], info[1]
            if len(info) == 3:
                data_categories[name] = info[2]
            df_net = pd.read_table(loc, sep='\t', header=None)
            if df_net.shape[1] < 3:
                df_net[2] = 1.0 #fixes columns for unweighted network
            df_net.rename(columns = {0:'Gene1', 1:'Gene2', 2:name}, inplace=True)
            df_net[['Gene1', 'Gene2']] = np.sort(df_net[['Gene1', 'Gene2']], axis=1)
            df = df.merge(df_net, how='left', on = ['Gene1', 'Gene2'])
            if df_net[name].dtype == bool:
                df[name].fillna(False, inplace=True)
            # else:
            #     df[name].fillna(0, inplace=True)
            # print name

    # TODO: return dataset grouping labels

    return df, data_categories

def rename(ont, node_attr, col=None):
    term_names = sorted(ont.terms, key=lambda x: ont.term_sizes[ont.terms_index[x]])
    term_names = [str(t) for t in term_names]
    term_rename = {t: t for t in term_names}
    # term_rename = {t: 'S:' + t for t in
    #                term_names}  ##IMPORTANT: should always start with S:, bad assumption, but the current status

    # if reindex:
    #     term_rename = {t: 'S:' + str(len(term_names) - term_names.index(t) - 1).zfill(5) for t in term_names}
    if col != None:
        dict_rename = node_attr[col].to_dict()
        term_rename = {t: dict_rename[t].split()[0] for t in term_names if t in dict_rename}

    ont.rename(terms=term_rename, inplace=True)
    node_attr.rename(index=term_rename, inplace=True)
    node_attr = node_attr.round(3)
    ont.update_node_attr(node_attr)  # this order somehow matters
    return ont, node_attr, term_rename

def addLabel(ont, node_attr, colname):
    for i in node_attr[node_attr[colname].isnull() == False].index:
        # ont.node_attr.loc[i, 'Label'] = i + ' ' + node_attr.loc[i, colname]
        ont.node_attr.loc[i, 'Label'] = node_attr.loc[i, colname]
    return ont


def create_term_to_uuid(ont, hname, terms, subnet_links, subnet_size, rf_score, uuid_file=None):
    if uuid_file != None:
        df_term_2_uuid = pd.read_table(uuid_file, sep='\t', index_col=0, header=None)
        df_term_2_uuid.index = df_term_2_uuid.index.astype(str)
        term_uuid = df_term_2_uuid[2].to_dict()
    else:
        pairs = ont_2_genepairs(ont, max_tsize=subnet_size[1])
        net_data, data_categories = support_data_focus(pairs, rf_score, subnet_links)  ## need some work on the input networks
        dict_edge_group = {v:[] for v in data_categories.values()}
        for d in data_categories:
            dict_edge_group[data_categories[d]].append(d)

        term_uuid = ont.upload_subnets_ndex(network=net_data, main_feature='Score',
                                            name=hname, terms=terms,
        ndex_server=ndex_server, ndex_user=ndex_user, ndex_pass=ndex_pass,
                                            spring_feature='Score', spring_weight = 1.0,
                                            edge_groups = dict_edge_group, max_num_edges = args.max_num_edges,
                                            verbose=False)  ## by default is public

        # save the UUID for future use
        with open('term_2_uuid.' + hname, 'a') as fh:
            # fh.write('Name\tOld_name\tUUID\n')
            ks = list(term_uuid.keys())
            term_rename_rev = {v: k for k, v in term_rename.items()}
            ks.sort()
            for k in ks:
                fh.write('{}\t{}\t{}\n'.format(k, term_rename_rev[k], term_uuid[k]))
    return term_uuid

def upload_main_hierarchy(ont, name, term_uuid, visible_cols):
    url, ont_ndexgraph = ont.to_ndex(name=name,
                                     ndex_server=ndex_server, ndex_user=ndex_user, ndex_pass=ndex_pass,
                                     term_2_uuid=term_uuid,
                                     layout='bubble-collect', style='passthrough',
                                     visible_term_attr=visible_cols,
                                     verbose=False)
    # print(url)

    print('http://hiview.ucsd.edu/{}?type=test&server=http://test.ndexbio.org'.format(url.split('/')[-1]))
    return url.split('/')[-1]

if __name__ == "__main__":
    par = argparse.ArgumentParser()
    par.add_argument('--ont', required=True, help = 'ontology file, 3 col table')
    par.add_argument('--hier_name', required=True, help='name of the hierarchy')
    par.add_argument('--ndex_account', nargs=3)
    par.add_argument('--score', help = 'integrated edge score')
    par.add_argument('--subnet_size', nargs = 2, default=[2, 500], type=int, help='minimum and maximum term size to show network support')
    par.add_argument('--node_attr', help='table file for attributes on systems')
    par.add_argument('--evinet_links',  help='data frame for network support')
    par.add_argument('--evinet_size', default=100, help='data frame for network support')
    par.add_argument('--gene_attr', help='table file for attributes on genes')
    par.add_argument('--term_2_uuid', help='if available, reuse networks that are already on NDEX')
    par.add_argument('--visible_cols', nargs='*', help='a list, specified column names in the ode attribute file will be shown as subsystem information')
    par.add_argument('--max_num_edges', type=int, default=-1, help='maximum number of edges uploaded; default (-1) is no limit')
    par.add_argument('--col_label', help = 'a column name in the node attribute file, add as the term label on the map')
    par.add_argument('--rename', help = 'if not None, rename name of subsystems specified by this column in the node_attr file')
    par.add_argument('--skip_main', action='store_true', help ='if true, do not update the main hierarchy')

    args = par.parse_args()

    ndex_server, ndex_user, ndex_pass = args.ndex_account # global

    ont = Ontology.from_table(args.ont, clixo_format=True, is_mapping = lambda x :x[2] =='gene')
    ont.propagate('forward', inplace=True)
        # if there is multiple root, add root
    if len(ont.get_roots()) > 1:
        ont.add_root('ROOT', inplace=True)

    if args.node_attr != None:
        node_attr = pd.read_table(args.node_attr, sep='\t', index_col=0)
        node_attr.index = node_attr.index.astype(str)
        node_attr = node_attr.loc[node_attr.index.isin(ont.terms) | node_attr.index.isin(ont.genes), :]
    else:
        nodes = ont.terms + ont.genes
        node_attr = pd.DataFrame(index = nodes)

    if args.gene_attr != None:
        # combine gene attribute to term attribute
        gene_attr = pd.read_table(args.gene_attr, sep='\t', index_col=0)
        node_attr = pd.concat([node_attr, gene_attr])


    df_ont = pd.read_table(args.ont, sep='\t', header=None, comment='#')
    if df_ont.shape[1] > 3:
        df_weight = df_ont.loc[df_ont[3].notnull(), [0,3]]
        df_weight.drop_duplicates(inplace=True)
        df_weight.rename(columns = {3:'Parent weight'}, inplace=True)
        df_weight.set_index(keys = 0, inplace=True)
        df_weight.index = df_weight.index.astype(str)
        node_attr = node_attr.merge(df_weight, how='left', left_index=True, right_index=True)

        if not ('ROOT' in df_weight.index.tolist()):
            node_attr.loc['ROOT', 'Parent weight'] = 0.0
    else:
        node_attr['Parent weight'] = 0.01 # since

    ont, node_attr, term_rename = rename(ont, node_attr, args.rename)

    if args.col_label != None:
        ont = addLabel(ont, node_attr, args.col_label)

    terms = [t for t,s in zip(ont.terms, ont.term_sizes) if (s >= args.subnet_size[0]) and (s<=args.subnet_size[1])]

    # this is to control whether uploading multigraph networks (for different edge types), by default only upload integrated score when size is larger than 100
    terms_small = [t for t,s in zip(ont.terms, ont.term_sizes) if (s >= args.subnet_size[0]) and (s<args.evinet_size)]
    terms_big = [t for t,s in zip(ont.terms, ont.term_sizes) if (s >= args.evinet_size) and (s<=args.subnet_size[1])]

    # upload/reuse subnetworks
    all_uuid = []
    term_uuid = {}
    if args.score != None:
        term_uuid.update(create_term_to_uuid(ont, args.hier_name, terms_big, None, args.subnet_size, args.score, uuid_file=args.term_2_uuid))
        term_uuid.update(create_term_to_uuid(ont, args.hier_name, terms_small, args.evinet_links, args.subnet_size, args.score, uuid_file=args.term_2_uuid))
        for u in term_uuid.values():
            all_uuid.append(u)

    # upload the main hierarchy
    if not args.skip_main:
        # now if visible cols not specified, visualize all the columns in node attribute
        vis_cols = []
        if args.visible_cols == None:
            vis_cols = node_attr.columns.tolist()
        else:
            vis_cols = args.visible_cols

        main_uuid = upload_main_hierarchy(ont, args.hier_name, term_uuid, vis_cols)
        all_uuid.append(main_uuid)

    # create a network set containing everything uploaded for this hierarchy
    my_ndex = nc2.Ndex2(args.ndex_account[0], args.ndex_account[1], args.ndex_account[2])
    my_ndex.update_status()
    url = my_ndex.create_networkset(args.hier_name, '')
    set_uuid = url.split('/')[-1]
    my_ndex.add_networks_to_networkset(set_uuid, all_uuid) # this function is only available in Ndex2
    # TODO: cannot have duplicated set name
