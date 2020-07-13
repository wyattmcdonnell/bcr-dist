import sklearn.decomposition as skdecomp
import sklearn.manifold as skmanifold
from cmodule.build import bcrdist
import matplotlib.pyplot as plot
import numpy as np
import sys

class dsarray(bcrdist.dsbcellarray):
    '''
    An array of double stranded bcells, with  a light and heavy chain.
    This python subclass of the pure c class bcrdist.dsbcellarray implements
    new plotting functions like generate kpca data, which invoke python
    libraries and functions
    '''
    
    def __init__(self, *args):
        bcrdist.dsbcellarray.__init__(self, *args)
    
    def generate_kpca_data(self):
        dist, ids = self.dist_matrix()
        
        pcafunc = skdecomp.KernelPCA(75, kernel='precomputed')
        tsnefunc = skmanifold.TSNE(n_components = 2, metric = 'precomputed')
        tsne1dfunc = skmanifold.TSNE(n_components = 1, metric = 'precomputed')
        kernel = 1 - (dist / dist.max())
        kernel = np.exp(-dist**2 / dist.max()**2)
        pcs = pcafunc.fit_transform(kernel)
        tsne = tsnefunc.fit_transform(dist)
        tsne1d = tsne1dfunc.fit_transform(dist)
        
        
        plot.scatter(pcs[:,0], pcs[:,1], s=1)
        plot.savefig(self.name() + "-pca-plot.png")
        plot.clf()
        plot.scatter(tsne[:,0], tsne[:,1], s=1)
        plot.savefig(self.name() + "-tsne-plot.png")
        
        
        
        pcstxt = np.concatenate((np.array(ids).reshape(-1,1), pcs.astype(str)), axis=1)
        np.savetxt(self.name() + "-pcs.csv", pcstxt, delimiter=',', fmt='%s', comments='', header = "cell_index," + ','.join(["pc" + str(i) for i in range(75)]))
        
        tsnetxt = np.concatenate((np.array(ids).reshape(-1,1), tsne.astype(str), tsne1d.astype(str)), axis=1)
        np.savetxt(self.name() + "-tsne.csv", tsnetxt, delimiter=',', fmt='%s', comments='', header = "cell_index,pre_tSNEx,pre_tSNEy,bcr_metric_tSNE")
        
        alltxt = np.concatenate((np.array(ids).reshape(-1,1), pcs.astype(str), tsne.astype(str), tsne1d.astype(str)), axis=1)
        np.savetxt(self.name() + "-all-pcs-tsne-w1d.csv", alltxt, delimiter=',', fmt='%s', comments='', header = "cell_index," + ','.join(["pc" + str(i) for i in range(75)]) + ",pre_tSNEx,pre_tSNEy,bcr_metric_tSNE")

        print( "sucessfully saved tsne and kpca data to file " + self.name() + "-all-pcs-tsne-w1d.csv" )