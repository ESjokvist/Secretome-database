import json

single_phylum_clusters = {}
with open("cluster_by_phylum.json") as f:
    fylum_annotated_clusters = json.load(f)
    for key, value in fylum_annotated_clusters.items():
        if len(value)==1:
            for phylum, nr in value.items():
                if nr > 1:
                    phyla = single_phylum_clusters.get(phylum, 0)
                    single_phylum_clusters[phylum] = phyla+1
with open("single_phylum_clusters.json", "w") as f:
    json.dump(single_phylum_clusters, f)
    
