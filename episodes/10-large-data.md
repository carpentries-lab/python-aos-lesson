---
title: "Using dask to handle larger data"
teaching: 30
exercises: 30
questions:
- "How do I work with multiple CMIP files that won't fit in memory?"
objectives:
- "Import the dask library and start a client with parallel workers."
- "Inspect netCDF chunking."
- "Calculate and plot an ocean temperature climatology."
keypoints:
- "Libraries such as dask and xarray can make loading, processing and visualising netCDF data much easier."
- "Dask can massively speed up processing through parallelism but care may be needed particularly with data chunking."
---

When working with climate data, it is common to find we want to analyse more data than can fit in memory at one time, or that calculations take a long time. We may be able to parallelise our operations with the `dask` library, which is built on `xarray` and enables calculations to make use of multiple "cores" in our computer.

> ## Additional libraries
>
> For this section we'll also need to install the `dask` and
> `siphon` libraries into our conda environment.
> There may be many dependencies.
>
{: .callout}

> ## Data used
> If teaching this lesson in a classroom, a copy of the dataset
> should be on hand on external media in case of wifi limitations.
> For remote teaching, please note the data being used is quite
> large, if network issues arise, the participant should instead use
> the smaller provided `pr` data files and utilise `%%time` magic
> to investigate speed-up.
{: .callout}

Let's take a look at a dataset with many files, for example daily ocean surface temperature data.

`OPeNDAP` is a protocol to remotely access netCDF data over a network as though it were a local file. OPeNDAP is provided commonly by "THREDDS" or "TDS" servers. We can use OPeNDAP to query CMIP6 data remotely where it is hosted (in this case, the NCI Earth Ssytem Grid node in Canberra). In python, we use the `siphon` library to query THREDDS catalogues to find available files.

~~~
from siphon.catalog import TDSCatalog

cat = TDSCatalog("http://dapds00.nci.org.au/thredds/catalog/fs38/publications/CMIP6/CMIP/CSIRO-ARCCSS/ACCESS-CM2/historical/r1i1p1f1/Oday/tos/gn/latest/catalog.xml")
print("\n".join(cat.datasets.keys()))

filelist=list(cat.datasets.keys())
DAProot='https://esgf.nci.org.au/thredds/dodsC/master/CMIP6/CMIP/CSIRO-ARCCSS/ACCESS-CM2/historical/r1i1p1f1/Oday/tos/gn/v20191108/'
path = [ DAProot+f for f in filelist ]
~~~
{: .language-python}

We can use `xarray` to open a "multifile" dataset as though it were a single file. We'll load a few libraries we might need here.
~~~
import xarray as xr
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import numpy as np
~~~
{: .language-python}

Recall that when we first open data in xarray it simply ("lazily") loads the metadata associated with the data and shows summary information about the contents of the dataset.
**This may take a little time for a large multifile dataset!**

~~~
dset = xr.open_mfdataset(path, combine='by_coords')
print(dset)
~~~
{: .language-python}

~~~
<xarray.Dataset>
Dimensions:             (bnds: 2, i: 360, j: 300, time: 60265, vertices: 4)
Coordinates:
    longitude           (j, i) float64 dask.array<chunksize=(300, 360), meta=np.ndarray>
    latitude            (j, i) float64 dask.array<chunksize=(300, 360), meta=np.ndarray>
  * i                   (i) int32 0 1 2 3 4 5 6 ... 353 354 355 356 357 358 359
  * j                   (j) int32 0 1 2 3 4 5 6 ... 293 294 295 296 297 298 299
  * time                (time) datetime64[ns] 1850-01-01T12:00:00 ... 2014-12-31T12:00:00
Dimensions without coordinates: bnds, vertices
Data variables:
    time_bnds           (time, bnds) datetime64[ns] dask.array<chunksize=(3652, 2), meta=np.ndarray>
    vertices_latitude   (time, j, i, vertices) float64 dask.array<chunksize=(3652, 300, 360, 4), meta=np.ndarray>
    vertices_longitude  (time, j, i, vertices) float64 dask.array<chunksize=(3652, 300, 360, 4), meta=np.ndarray>
    tos                 (time, j, i) float32 dask.array<chunksize=(3652, 300, 360), meta=np.ndarray>
Attributes:
    Conventions:                     CF-1.7 CMIP-6.2
    activity_id:                     CMIP
    branch_method:                   standard
    branch_time_in_child:            0.0
    branch_time_in_parent:           0.0
    creation_date:                   2019-11-08T18:23:57Z
    data_specs_version:              01.00.30
    experiment:                      all-forcing simulation of the recent past
    experiment_id:                   historical
    external_variables:              areacello
    forcing_index:                   1
    frequency:                       day
    further_info_url:                https://furtherinfo.es-doc.org/CMIP6.CSI...
    grid:                            native atmosphere N96 grid (144x192 latx...
    grid_label:                      gn
    history:                         2019-11-08T18:23:57Z ; CMOR rewrote data...
    initialization_index:            1
    institution:                     CSIRO (Commonwealth Scientific and Indus...
    institution_id:                  CSIRO-ARCCSS
    mip_era:                         CMIP6
    nominal_resolution:              250 km
    notes:                           Exp: CM2-historical; Local ID: bj594; Va...
    parent_activity_id:              CMIP
    parent_experiment_id:            piControl
    parent_mip_era:                  CMIP6
    parent_source_id:                ACCESS-CM2
    parent_time_units:               days since 0950-01-01
    parent_variant_label:            r1i1p1f1
    physics_index:                   1
    product:                         model-output
    realization_index:               1
    realm:                           ocean
    run_variant:                     forcing: GHG, Oz, SA, Sl, Vl, BC, OC, (G...
    source:                          ACCESS-CM2 (2019): \naerosol: UKCA-GLOMA...
    source_id:                       ACCESS-CM2
    source_type:                     AOGCM
    sub_experiment:                  none
    sub_experiment_id:               none
    table_id:                        Oday
    table_info:                      Creation Date:(30 April 2019) MD5:e14f55...
    title:                           ACCESS-CM2 output prepared for CMIP6
    variable_id:                     tos
    variant_label:                   r1i1p1f1
    version:                         v20191108
    cmor_version:                    3.4.0
    _NCProperties:                   version=2,netcdf=4.6.2,hdf5=1.10.5
    tracking_id:                     hdl:21.14100/45e464ff-5f78-4b7b-8924-f3b...
    license:                         CMIP6 model data produced by CSIRO is li...
    DODS_EXTRA.Unlimited_Dimension:  time
~~~
{: .output}

We can see that our `dset` object is an `xarray.Dataset`, but notice now that each variable has type `dask.array`, meaning that xarray is aware of the netCDF "chunks" (how the data is packed in the files), and we'll be able to parallelise across these if we need/want to.

In this case, we are interested in the ocean surface temperature (`tos`) variable contained within that xarray Dataset:

~~~
print(dset['tos'])
~~~
{: .language-python}

~~~
<xarray.DataArray 'pr' (time: 60, lat: 144, lon: 192)>
[1658880 values with dtype=float32]
Coordinates:
  * time     (time) datetime64[ns] 2010-01-16T12:00:00 ... 2014-12-16T12:00:00
  * lon      (lon) float64 0.9375 2.812 4.688 6.562 ... 353.4 355.3 357.2 359.1
  * lat      (lat) float64 -89.38 -88.12 -86.88 -85.62 ... 86.88 88.12 89.38
Attributes:
    standard_name:  precipitation_flux
    long_name:      Precipitation
    units:          kg m-2 s-1
    comment:        includes both liquid and solid phases
    cell_methods:   area: time: mean
    cell_measures:  area: areacella
~~~
{: .output}

We can actually use either the `dset['pr']` or `dset.pr` syntax to access the precipitation
`xarray.DataArray`.

To calculate the precipitation climatology,
we can make use of the fact that xarray DataArrays have built in functionality
for averaging over their dimensions.

~~~
clim = dset['pr'].mean('time', keep_attrs=True)
print(clim)
~~~
{: .language-python}

~~~
<xarray.DataArray 'pr' (lat: 144, lon: 192)>
array([[1.8461452e-06, 1.9054805e-06, 1.9228980e-06, ..., 1.9869783e-06,
        2.0026005e-06, 1.9683730e-06],
       [1.9064508e-06, 1.9021350e-06, 1.8931637e-06, ..., 1.9433096e-06,
        1.9182237e-06, 1.9072245e-06],
       [2.1003202e-06, 2.0477617e-06, 2.0348527e-06, ..., 2.2391034e-06,
        2.1970161e-06, 2.1641599e-06],
       ...,
       [7.5109556e-06, 7.4777777e-06, 7.4689174e-06, ..., 7.3359679e-06,
        7.3987890e-06, 7.3978440e-06],
       [7.1837171e-06, 7.1722038e-06, 7.1926393e-06, ..., 7.1552149e-06,
        7.1576678e-06, 7.1592167e-06],
       [7.0353467e-06, 7.0403985e-06, 7.0326828e-06, ..., 7.0392648e-06,
        7.0387587e-06, 7.0304386e-06]], dtype=float32)
Coordinates:
  * lon      (lon) float64 0.9375 2.812 4.688 6.562 ... 353.4 355.3 357.2 359.1
  * lat      (lat) float64 -89.38 -88.12 -86.88 -85.62 ... 86.88 88.12 89.38
Attributes:
    standard_name:  precipitation_flux
    long_name:      Precipitation
    units:          kg m-2 s-1
    comment:        includes both liquid and solid phases
    cell_methods:   area: time: mean
    cell_measures:  area: areacella
~~~
{: output}

> ## Dask
>
> Rather than read the entire three dimensional (time, lat, lon)
> data array into memory and then calculate the climatology,
> xarray lazy loading has allowed us to only load the
> two dimensional (lat, lon) climatology.
> If the original 3D data array was much larger than the one we are analysing here
> (i.e. so large that we'd get a memory error if we attempted to calculate the climatology)
> xarray can make use of a library called [Dask](http://xarray.pydata.org/en/stable/dask.html)
> to break the task down into chunks and distribute it to multiple cores if needed.
>
{: .callout}

Now that we've calculated the climatology, 
we want to convert the units from kg m-2 s-1
to something that we are a little more familiar with like mm day-1.

To do this, consider that
1 kg of rain water spread over 1 m2 of surface is 1 mm in thickness
and that there are 86400 seconds in one day.
Therefore, 1 kg m-2 s-1 = 86400 mm day-1.

The data associated with our xarray DataArray is simply a numpy array,

~~~
type(clim.data)
~~~
{: .language-python}

~~~
numpy.ndarray
~~~
{: .output}

so we can go ahead and multiply that array by 86400 and update the units attribute accordingly:

~~~
clim.data = clim.data * 86400
clim.attrs['units'] = 'mm/day' 

print(clim)
~~~
{: .language-python}

~~~
<xarray.DataArray 'pr' (lat: 144, lon: 192)>
array([[0.15950695, 0.16463352, 0.16613839, ..., 0.17167493, 0.17302468,
        0.17006743],
       [0.16471735, 0.16434446, 0.16356934, ..., 0.16790195, 0.16573453,
        0.1647842 ],
       [0.18146767, 0.17692661, 0.17581128, ..., 0.19345854, 0.18982219,
        0.18698342],
       ...,
       [0.64894656, 0.64607999, 0.64531446, ..., 0.63382763, 0.63925537,
        0.63917372],
       [0.62067316, 0.61967841, 0.62144403, ..., 0.61821057, 0.6184225 ,
        0.61855632],
       [0.60785395, 0.60829043, 0.60762379, ..., 0.60819248, 0.60814875,
        0.6074299 ]])
Coordinates:
  * lon      (lon) float64 0.9375 2.812 4.688 6.562 ... 353.4 355.3 357.2 359.1
  * lat      (lat) float64 -89.38 -88.12 -86.88 -85.62 ... 86.88 88.12 89.38
Attributes:
    standard_name:  precipitation_flux
    long_name:      Precipitation
    units:          mm/day
    comment:        includes both liquid and solid phases
    cell_methods:   area: time: mean
    cell_measures:  area: areacella
~~~
{: .output}

We could now go ahead and plot our climatology using matplotlib,
but it would take many lines of code to extract all the latitude and longitude information
and to setup all the plot characteristics.
Recognising this burden,
the xarray developers have built on top of `matplotlib.pyplot` to make the visualisation
of xarray DataArrays much easier.
~~~
fig = plt.figure(figsize=[12,5])

ax = fig.add_subplot(111, projection=ccrs.PlateCarree(central_longitude=180))

clim.plot.contourf(ax=ax,
                   levels=np.arange(0, 13.5, 1.5),
                   extend='max',
                   transform=ccrs.PlateCarree(),
                   cbar_kwargs={'label': clim.units})
ax.coastlines()

plt.show()
~~~
{: .language-python}

![Precipitation climatology](../fig/02-visualisation-viridis.png)

The default colorbar used by matplotlib is `viridis`.
It used to be `jet`,
but that was changed a couple of years ago in response to the 
[#endtherainbow](https://www.climate-lab-book.ac.uk/2014/end-of-the-rainbow/) campaign.

Putting all the code together
(and reversing viridis so that wet is purple and dry is yellow)...

~~~
import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import numpy as np

access_pr_file = 'data/pr_Amon_ACCESS1-3_historical_r1i1p1_200101-200512.nc'

dset = xr.open_dataset(access_pr_file)

clim = dset['pr'].mean('time', keep_attrs=True)

clim.data = clim.data * 86400
clim.attrs['units'] = 'mm/day'

fig = plt.figure(figsize=[12,5])
ax = fig.add_subplot(111, projection=ccrs.PlateCarree(central_longitude=180))
clim.plot.contourf(ax=ax,
                   levels=np.arange(0, 13.5, 1.5),
                   extend='max',
                   transform=ccrs.PlateCarree(),
                   cbar_kwargs={'label': clim.units},
                   cmap='viridis_r')
ax.coastlines()
plt.show()
~~~
{: .language-python}

![Precipitation climatology](../fig/02-visualisation-viridis_r.png)

> ## Color palette
>
> Copy and paste the final slab of code above into your own Jupyter notebook.
>
> The viridis color palette doesn't seem quite right for rainfall.
> Change it to the "haline" [cmocean](http://matplotlib.org/cmocean/) palette
> used for ocean salinity data.
>
> > ## Solution
> > ~~~
> > import cmocean
> >
> > ...
> > clim.plot.contourf(ax=ax,
                       ...
                       cmap=cmocean.cm.haline_r)
> > ~~~
> > {: .language-python}
> {: .solution}
{: .challenge} 

> ## Season selection
>
> Rather than plot the annual climatology,
> edit the code so that it plots the June-August (JJA) season.
>
> (Hint: the [groupby]() functionality can be used to
> group all the data into seasons prior to averaging over the time axis) 
>
> > ## Solution
> > ~~~
> > clim = dset['pr'].groupby('time.season').mean('time', keep_attrs=True) 
> > 
> > clim.sel(season='JJA').plot.contourf(ax=ax,
> > ~~~
> > {: .language-python}
> {: .solution}
{: .challenge}

> ## Add a title
>
> Add a title to the plot which gives the name of the model
> (taken from the `dset` attributes)
> followed by the words "precipitation climatology (JJA)"
>
> > ## Solution
> > ~~~
> > title = '%s precipitation climatology (JJA)' %(dset.attrs['model_id'])
> > plt.title(title)
> > ~~~
> > {: .language-python}
> {: .solution}
{: .challenge}
