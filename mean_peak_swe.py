
# coding: utf-8

# ## Script to calculate the long term and shorter term runoff ratio from the VIC 

# In[1]:

import numpy as np
import pandas as pd
import ipyparallel as pr
import livneh.tools as lt
import rhessys.utilities as rt
import time


# In[2]:

c = pr.Client() # start the parallel environment


# In[3]:

view = c.load_balanced_view() # access the first 4 engines


# In[4]:

get_ipython().run_cell_magic(u'px', u'', u"import pandas as pd\nimport numpy as np\nimport rhessys.utilities as rt\ndates = pd.read_pickle('/Volumes/data/projects/Budyko_vic/timecode.pcl')\nfluxes_columns = ['y','m','d','ET','R','BF','sm1','sm2','sm3','SWE','Cs','Qs','Ql','Qg','NR','PEText','PETtrc','PETsrc']\ntmp = pd.read_table('/Volumes/data/vic/fluxes/ascii/latitude.46.15625/flux_snow_46.15625_-120.40625', sep='\\t',names=fluxes_columns)\ntmp.index = dates\nwateryears = tmp.index.map(rt.wateryear)\nwyears = np.load('/Volumes/data/projects/Budyko_vic/wyears.npy')")


# In[5]:

def fluxproc(idx,fl):
    flux = pd.read_table(fl, sep='\t', names = fluxes_columns) # read fluxes
    flux.index = pd.DatetimeIndex(dates)
    flux['wateryear'] = wateryears # add water years to the data frame
    flux = flux.loc[(flux.wateryear>=wyears[0])&(flux.wateryear<=wyears[-1])] # subset to complete water years
    
    return idx,flux.groupby(by='wateryear').SWE.max().mean()


# In[6]:

files = pd.read_pickle('/Volumes/data/projects/Budyko_vic/forcing_fluxes_filenames_lat_lon_index.df')


# In[8]:

res = view.map(fluxproc,files.indexer,files.flux)


# In[10]:

while res.ready() == False:
    perc = round(float(res.progress)/float(len(files))*100.,2)
    print '#'*int(perc/4) # print a simple progress bar
    print str(perc)+'% Completed'
    time.sleep(60) # wait 60 seconds


# In[12]:

idx,meanpeakswe = zip(*res.result)


# In[13]:

mps = pd.DataFrame({'idx':idx,'meanpeakswe':meanpeakswe}) # generate data frame
mps.to_pickle('./data/meanpeakswe.pcl') # save as df for conus forest snow analyses

# dev scratch
#fluxes_columns = ['y','m','d','ET','R','BF','sm1','sm2','sm3','SWE','Cs','Qs','Ql','Qg','NR','PEText','PETtrc','PETsrc']
#tmp = pd.read_table('/Volumes/data/vic/fluxes/ascii/latitude.46.15625/flux_snow_46.15625_-120.40625', #sep='\t',names=fluxes_columns)
#dates = pd.read_pickle('/Volumes/data/projects/Budyko_vic/timecode.pcl')
#wyears = np.load('/Volumes/data/projects/Budyko_vic/wyears.npy')
#tmp.index = dates
#wateryears = tmp.index.map(rt.wateryear)
#tmp['wateryear'] = wateryears#tmp = tmp.loc[(tmp.wateryear>=wyears[0])&(tmp.wateryear<=wyears[-1])]#tmp.loc[tmp.wateryear==1951,'SWE'].max()#tmp.groupby(by='wateryear').SWE.max().mean()
