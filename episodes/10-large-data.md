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
<xarray.DataArray 'tos' (time: 60265, j: 300, i: 360)>
dask.array<concatenate, shape=(60265, 300, 360), dtype=float32, chunksize=(3653, 300, 360), chunktype=numpy.ndarray>
Coordinates:
    longitude  (j, i) float64 dask.array<chunksize=(300, 360), meta=np.ndarray>
    latitude   (j, i) float64 dask.array<chunksize=(300, 360), meta=np.ndarray>
  * i          (i) int32 0 1 2 3 4 5 6 7 8 ... 352 353 354 355 356 357 358 359
  * j          (j) int32 0 1 2 3 4 5 6 7 8 ... 292 293 294 295 296 297 298 299
  * time       (time) datetime64[ns] 1850-01-01T12:00:00 ... 2014-12-31T12:00:00
Attributes:
    standard_name:  sea_surface_temperature
    long_name:      Sea Surface Temperature
    comment:        Temperature of upper boundary of the liquid ocean, includ...
    units:          degC
    cell_methods:   area: mean where sea time: mean
    cell_measures:  area: areacello
    history:        2019-11-08T18:23:54Z altered by CMOR: replaced missing va...
    _ChunkSizes:    [  1 300 360]
~~~
{: .output}

Notice that we now have an attribute `_ChunkSizes` listed. This has shape `[1 300 360]`, while the `dask.array` itself has shape (60265, 300, 360), and chunksize (3653, 300, 360). 
This means that the underlying data is structured to be most efficiently accessed for the whole lat/lon range at each time step, but dask will load up 3653 of these "slices" at once, for a combined dataset size of 60265 timesteps.

So far we have not loaded any data, only metadata. Operating on this data is likely to be slow! But let's try making a sea surface temperature climatology, similar to the precipitation climatology we made in the Visualisation episode.

~~~
clim = dset['tos'].mean('time', keep_attrs=True)
print(clim)
~~~
{: .language-python}

~~~
<xarray.DataArray 'tos' (j: 300, i: 360)>
dask.array<mean_agg-aggregate, shape=(300, 360), dtype=float32, chunksize=(300, 360), chunktype=numpy.ndarray>
Coordinates:
    longitude  (j, i) float64 dask.array<chunksize=(300, 360), meta=np.ndarray>
    latitude   (j, i) float64 dask.array<chunksize=(300, 360), meta=np.ndarray>
  * i          (i) int32 0 1 2 3 4 5 6 7 8 ... 352 353 354 355 356 357 358 359
  * j          (j) int32 0 1 2 3 4 5 6 7 8 ... 292 293 294 295 296 297 298 299
Attributes:
    standard_name:  sea_surface_temperature
    long_name:      Sea Surface Temperature
    comment:        Temperature of upper boundary of the liquid ocean, includ...
    units:          degC
    cell_methods:   area: mean where sea time: mean
    cell_measures:  area: areacello
    history:        2019-11-08T18:23:54Z altered by CMOR: replaced missing va...
    _ChunkSizes:    [  1 300 360]
~~~
{: output}

But wait! That was very fast! Why is that?
(**hint**, consider lazy loading and xarray operations, what have we done in the above step?)

We can investigate how chunks affect how quickly we can actually read the data. To move from metadata objects to actual data, we use the `.load()` or `.compute()` calls to dask.

> ## Changing chunks
> If we decide to change chunking to improve performance, note we
> can control the size of dask chunks used, but they *must* align
> with the netCDF file chunks or we will certainly make performance worse!
{: .callout}

> ## Investigating chunks
>
> Time how long it takes to load the ocean temperature data for `'2014-01-01T12:00:00`
> and then time how long it takes to load the data at `i=136` and `j=100` (-0.1662N, 180.5E).
> How much difference in time is there when using these different
> (time slice vs time series) access methods?
> **Hint:** Use the `%%time` magic to get a single timing, or `%%timeit`
> to get an average time -
> but note that an initial load will be much slower than subsequent calls!
>
> > ## Solution
> > ~~~
> > import time
> > 
> > %%time
> > dset.tos.sel(time='2014-01-01T12:00:00').load()
> > 
> > %%time
> > dset.tos.sel(i=100,j=136).load()
> > ~~~
> > We see that the first call (all lat/lon at a single time step)
> > is orders of magnitude faster than extracting all time steps at
> > a single point location with the current dataset chunking
> > (for me it was ~1 sec vs ~5 min using a single core).
> > {: .language-python}
> {: .solution}
{: .challenge}

Now let's look at that climatology, what type of data is it?
~~~
type(clim.data)
~~~
{: .language-python}
~~~
dask.array.core.Array
~~~
{: .output}

Let's start a `dask` "client" to allow the next calculation to be handled in parallel.

~~~
from dask.distributed import Client
client = Client()
print(client)
~~~
{: .language-python}
This starts a parallel cluster client, and gives us a `bokeh` port to view the dask dashboard.

This is where it all gets messy. We are relying both on local parallel compute, and also streaming data from a remote server which has a size limit on individual requests. We can scale to more interesting levels if working on the local filesystem at NCI. For the remainder of this task we may need to switch to a simpler precipitation dataset. e.g.

Try the `tos` data:
~~~
%%time
clim.compute()
~~~
{: .language=python}

If the previous climatology calculation fails with a NetCDF error and you don't have access to jupyter notebooks at NCI (instead specify the actual path to data, e.g. `/g/data/fs38/publications/CMIP6/`), try this:

~~~
cat = TDSCatalog("http://dapds00.nci.org.au/thredds/catalog/fs38/publications/CMIP6/ScenarioMIP/CSIRO-ARCCSS/ACCESS-CM2/ssp585/r1i1p1f1/day/pr/gn/latest/catalog.xml")
print("\n".join(cat.datasets.keys()))

filelist=list(cat.datasets.keys())
DAProot='https://esgf.nci.org.au/thredds/dodsC/master/CMIP6/ScenarioMIP/CSIRO-ARCCSS/ACCESS-CM2/ssp585/r1i1p1f1/day/pr/gn/v20191108/'
path = [ DAProot+f for f in filelist ]

dset2 = xr.open_mfdataset(path, combine='by_coords',chunks={'time':'100MB'}) #Limit chunk size to be less than a THREDDS request limit

clim = dset2['pr'].mean('time', keep_attrs=True)
print(clim)
~~~
{: .language-python}

~~~
%%time
clim.compute()
~~~
~~~
CPU times: user 3.79 s, sys: 801 ms, total: 4.59 s
Wall time: 40.1 s

xarray.DataArray
'pr'

    lat: 144lon: 192

    array([[2.4257924e-06, 2.4922954e-06, 2.5074639e-06, ..., 2.5419881e-06,
            2.5584206e-06, 2.5209411e-06],
           [2.4357266e-06, 2.3995908e-06, 2.3777325e-06, ..., 2.4783983e-06,
            2.4712863e-06, 2.4676210e-06],
           [2.5555057e-06, 2.4873918e-06, 2.4325188e-06, ..., 2.7541412e-06,
            2.6866162e-06, 2.6368391e-06],
           ...,
           [1.0240185e-05, 1.0276052e-05, 1.0309918e-05, ..., 1.0122936e-05,
            1.0167766e-05, 1.0204100e-05],
           [9.9295821e-06, 9.9560648e-06, 9.9702647e-06, ..., 9.8695555e-06,
            9.8934788e-06, 9.9096997e-06],
           [9.5022224e-06, 9.5112646e-06, 9.5121368e-06, ..., 9.5095284e-06,
            9.5050536e-06, 9.5094583e-06]], dtype=float32)

    Coordinates:
        lat
        (lat)
        float64
        -89.38 -88.12 ... 88.12 89.38
        lon
        (lon)
        float64
        0.9375 2.812 4.688 ... 357.2 359.1
    Attributes:

    standard_name :
        precipitation_flux
    long_name :
        Precipitation
    comment :
        includes both liquid and solid phases
    units :
        kg m-2 s-1
    cell_methods :
        area: time: mean
    cell_measures :
        area: areacella
    history :
        2019-11-08T10:45:49Z altered by CMOR: replaced missing value flag (-1.07374e+09) with standard missing value (1e+20).
    _ChunkSizes :
        [  1 144 192]
~~~
{: .output}

*The above timing was from a VDI node. Run on my local laptop it took 15minutes!*
We can now plot our climatology as we did in the Visualisation episode.

While `dask` gives us the capacity to better handle big data, it is still better to "take the compute to the data" whenever possible, as such, working with CMIP data will always be most effective when working on a local high performance filesystem with the data available alongside your Python notebook.
