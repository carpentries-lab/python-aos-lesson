import argparse
import xarray
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import numpy
import cmocean


def convert_pr_units(darray):
    """Convert kg m-2 s-1 to mm day-1.
    
    Args:
      darray (xarray.core.dataarray.DataArray): Precipitation data
    
    """
    
    darray.data = darray.data * 86400
    darray.attrs['units'] = 'mm/day'
    
    return darray


def plot_climatology(clim_darray, model_name, season, gridlines=False):
    """Plot the precipitation climatology.
    
    Args:
      clim_darray (xarray.core.dataarray.DataArray): Precipitation climatology data
      season (str): Season    
    
    """
        
    fig = plt.figure(figsize=[12,5])
    ax = fig.add_subplot(111, projection=ccrs.PlateCarree(central_longitude=180))
    clim_darray.sel(season=season).plot.contourf(ax=ax,
                                                 levels=numpy.arange(0, 15, 1.5),
                                                 extend='max',
                                                 transform=ccrs.PlateCarree(),
                                                 cbar_kwargs={'label': clim_darray.units},
                                                 cmap=cmocean.cm.haline_r)
    ax.coastlines()
    if gridlines:
        plt.gca().gridlines()
    
    title = '%s precipitation climatology (%s)' %(model_name, season)
    plt.title(title)


def main(inargs):
    """Run the program."""

    dset = xarray.open_dataset(inargs.pr_file)
    pr_darray = dset['pr']
    
    clim_darray = pr_darray.groupby('time.season').mean(dim='time')
    clim_darray = convert_pr_units(clim_darray)

    plot_climatology(clim_darray, dset.attrs['model_id'], inargs.season)
    plt.savefig(inargs.output_file, dpi=200)


if __name__ == '__main__':
    description='Plot the precipitation climatology.'
    parser = argparse.ArgumentParser(description=description)
    
    parser.add_argument("pr_file", type=str, help="Precipitation data file")
    parser.add_argument("season", type=str, help="Season to plot")
    parser.add_argument("output_file", type=str, help="Output file name")

    args = parser.parse_args()
    
    main(args)
