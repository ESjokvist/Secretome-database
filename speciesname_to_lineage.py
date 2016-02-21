from __future__ import division
RANKS = ['no rank', 'varietas', 'species', 'genus', 'family', 'order', 'class', 'phylum', 'superkingdom']

import sys

def getTreeList(taxIds, nodesDB):
    known_tree_lists = {}
    for taxId in taxIds: 
    	if not taxId in known_tree_lists:
    		tree_list = []
    		nextTaxId = [taxId]
    		while nextTaxId:
        		thisTaxId = nextTaxId.pop(0)
        		if (not thisTaxId == '1') and (thisTaxId in nodesDB):
        			parent = nodesDB[thisTaxId]['parent']
        			nextTaxId.append(parent)
        			tree_list.append(thisTaxId)
        		else:
    				tree_list.append('1')
    		known_tree_lists[taxId] = tree_list
    return known_tree_lists

def getLineages(tree_lists, nodesDB):
	lineage = {}
	for tree_list_id, tree_list in tree_lists.items():
		lineage[tree_list_id] = {rank : 'undef' for rank in RANKS}
		for taxId in tree_list:
			node = nodesDB[taxId]
			if node['rank'] in RANKS:
				lineage[tree_list_id][node['rank']] = node['name']
		# traverse ranks again so that undef is "higher_def_rank" + "-" + undef
		def_rank = ''
		for rank in reversed(list(RANKS)):
			if not lineage[tree_list_id][rank] == 'undef':
				def_rank = lineage[tree_list_id][rank]
			else:
				if (def_rank):
					lineage[tree_list_id][rank] = def_rank + "-" + lineage[tree_list_id][rank]
	return lineage

def readNodesDB(nodesDB_f):
    nodesDB = {}
    nodes_count = 0
    i = 0
    with open(nodesDB_f) as fh:
        for line in fh:
            if line.startswith("#"):
                nodes_count = int(line.lstrip("# nodes_count = ").rstrip("\n"))
            else:
                i += 1
                node, rank, name, parent = line.rstrip("\n").split("\t")
                nodesDB[node] = {'rank' : rank, 'name' : name, 'parent' : parent}
    return nodesDB

def parse_names(list_of_unique_names_f):
	species_names_l = []
	with open(list_of_unique_names_f) as fh:
		for l in fh:
			species_name = l.rstrip("\n")
			species_names_l.append(species_name)
	return species_names_l

def getTaxId(species_names, nodesDB):
    taxIds = []
    species_taxid = {}
    for key, value in nodesDB.items():
        if value["name"] in species_names:
            species_taxid[value["name"]]=key
            taxIds.append(key)
#            print value["name"]
#    print species_taxid
    return taxIds
    
if __name__ == "__main__":
	nodesDB_f = sys.argv[1]
	list_of_unique_names_f = sys.argv[2]

	species_names_l = parse_names(list_of_unique_names_f) 
#        print species_names_l
	nodesDB = readNodesDB(nodesDB_f)
#        print len(nodesDB)
	# set of taxids : set of all taxids you want to find
        set_of_taxIds = getTaxId(species_names_l, nodesDB)
#        print set_of_taxIds
	tree_lists = getTreeList(set_of_taxIds, nodesDB)
	lineages = getLineages(tree_lists, nodesDB)

print lineages
