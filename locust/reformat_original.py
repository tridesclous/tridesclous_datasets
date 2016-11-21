import os
import numpy as np
from urllib.request import urlretrieve
import h5py
import json

"""
Reformat hdf5 to simple raw for easy testing.
"""



name = 'locust20010201.hdf5'
distantfile = 'https://zenodo.org/record/21589/files/'+name

localdir = os.path.dirname(os.path.abspath(__file__))

if not os.access(localdir, os.W_OK):
    localdir = tempfile.gettempdir()
localfile = os.path.join(os.path.dirname(__file__), name)

if not os.path.exists(localfile):
    urlretrieve(distantfile, localfile)
hdf = h5py.File(localfile,'r')

ch_names = ['ch09','ch11','ch13','ch16']
trial_names = ['trial_01', 'trial_02']


for trial_name in trial_names:
    sigs = np.array([hdf['Continuous_1'][trial_name][name][...] for name in ch_names]).transpose().copy()
    with open('locust_'+trial_name+'.raw', mode='wb') as f:
        f.write(sigs.tobytes())
    


with open('info.json', mode='w', encoding='utf8') as f:
    info = {'sample_rate': 15000., 'shape': (-1,4), 'dtype': sigs.dtype.name}
    json.dump(info, f, indent=4)

