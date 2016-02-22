from matplotlib import pyplot as plt
import json

with open("number_of_clusters_for_random_species.json") as f:
    n_cluster_vs_n_species = json.load(f)

x = [d['n_species'] for d in n_cluster_vs_n_species]
y = [d['mean'] for d in n_cluster_vs_n_species]
error = [d['std'] for d in n_cluster_vs_n_species]

plt.errorbar(x,y,yerr=error)
#plt.show()
plt.savefig('gene_families_plotted.pdf', bbox_inches='tight')
plt.close()







