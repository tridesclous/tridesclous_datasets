import os
import numpy as np
from urllib.request import urlretrieve
import h5py
import json

"""
Reformat hdf5 to simple raw for easy testing.
"""



name = 'DelesclusePouzatDataJNM2006.hdf5'
distantfile = 'https://zenodo.org/record/15228/files/'+name

localdir = os.path.dirname(os.path.abspath(__file__))

if not os.access(localdir, os.W_OK):
    localdir = tempfile.gettempdir()
localfile = os.path.join(os.path.dirname(__file__), name)

if not os.path.exists(localfile):
    urlretrieve(distantfile, localfile)
hdf = h5py.File(localfile,'r')


ch_names = ['Channel_0','Channel_1','Channel_2','Channel_3']

sigs_Extracellular = np.array([hdf['ExtracellularData'][name][...] for name in ch_names]).transpose().copy()

sigs_CellAttached = np.array(hdf['CellAttached']['Reference'][...]).transpose().copy()



with open('purkinje_extra_cellular.raw', mode='wb') as f:
    f.write(sigs_Extracellular.tobytes())

with open('purkinje_cell_attached.raw', mode='wb') as f:
    f.write(sigs_CellAttached.tobytes())



with open('info.json', mode='w', encoding='utf8') as f:
    info = {'sample_rate': 15000., 'shape': (-1,4), 'dtype': sigs_Extracellular.dtype.name}
    json.dump(info, f, indent=4)


