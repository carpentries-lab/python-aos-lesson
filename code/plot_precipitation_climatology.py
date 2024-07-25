import xarray as xr
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import numpy as np
import cmocean
import argparse


def convert_pr_units(da):
    """Convert kg m-2 s-1 to mm day-1.
    
    Args:
      da (xarray.DataArray): Precipitation data
    
    """
    
    da.data = da.data * 86400
    da.attrs["units"] = "mm/day"
    
    return da


def create_plot(clim, model, season, gridlines=False):
    """Plot the precipitation climatology.
    
    Args:
      clim (xarray.DataArray): Precipitation climatology data
      model (str): Name of the climate model
      season (str): Season
      
    Kwargs:
      gridlines (bool): Select whether to plot gridlines    
    
    """
        
    fig = plt.figure(figsize=[12,5])
    ax = fig.add_subplot(111, projection=ccrs.PlateCarree(central_longitude=180))
    clim.sel(season=season).plot.contourf(
        ax=ax,
        levels=np.arange(0, 13.5, 1.5),
        extend="max",
        transform=ccrs.PlateCarree(),
        cbar_kwargs={"label": clim.units},
        cmap=cmocean.cm.haline_r,
    )
    ax.coastlines()
    if gridlines:
        plt.gca().gridlines()
    
    title = f"{model} precipitation climatology ({season})"
    plt.title(title)


def main(inargs):
    """Run the program."""

    ds = xr.open_dataset(inargs.pr_file)
    
    clim = ds["pr"].groupby("time.season").mean("time", keep_attrs=True)
    clim = convert_pr_units(clim)

    create_plot(clim, dset.attrs["source_id"], inargs.season)
    plt.savefig(
        inargs.output_file,
        dpi=200,
        bbox_inches="tight",
        facecolor="white",    
    )


if __name__ == "__main__":
    description = "Plot the precipitation climatology."
    parser = argparse.ArgumentParser(description=description)
    
    parser.add_argument("pr_file", type=str, help="Precipitation data file")
    parser.add_argument("season", type=str, help="Season to plot")
    parser.add_argument("output_file", type=str, help="Output file name")

    args = parser.parse_args()
    main(args)
