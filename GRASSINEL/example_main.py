from GRASSINEL.grass_functionality import *
from GRASSINEL.grass_setup import *
from GRASSINEL.S1_preprocessing import *
from datetime import datetime


def main():
    # ######### GRASS SETUP FUNCTION(S) #############
    grass_setup()
    import_shapefile(path_to_shape=Paths.boundary_path, shapename="jena_boundary@PERMANENT", overwrite_bool=True)

    # ######## SENTINEL DOWNLOAD FUNCTION(S) #############
    sen_download(start_time="2020-05-01", end_time="2020-05-07", sort_by="ingestiondate")
    # sen_download_extended(start_time="2020-05-01", end_time="2020-05-07", sort_by="ingestiondate",
    #                       relative_orbit_number=172)

    # ########## SENTINEL PREPROCESSING FUNCTION(S) #############
    pyroSAR_processing(down_path=Paths.sen_down_path, processed_path=Paths.sen_processed_path, target_resolution=50,
                       target_CRS=32632, terrain_flat_bool=False, remove_therm_noise_bool=False)
    subset_import(overwrite_bool=True, output="raster", polarization_type=["VH", "VV"])

    ########## GRASS SPACE TIME CUBE FUNCTION(S) #############
    create_stc(overwrite_bool=True, output="stcube", polarization_type=["VH", "VV"], stc_info_bool=True,
               stc_statistics_bool=True)
    visualize_stc(output="stcube", polarization_type=["VH", "VV"], stc_animation_bool=True, stc_timeline_bool=True)
    # raster_comparison(raster1_name="rasterVH0@PERMANENT", raster2_name="rasterVH1@PERMANENT", mode="swipe")

    # ########## GRASS ANALYSIS FUNCTION(S) #############
    raster_algebra(basename="product", layername="result", expression=" = stcubeVH*stcubeVV", overwrite_bool=True)
    # temporal_mapcalc(layername="diff", expression=" = rasterVH0@PERMANENT - rasterVH1@PERMANENT")
    # rvi_mapcalc(layername="rvi", overwrite_bool=True)


if __name__ == "__main__":
    start_time = datetime.now()
    main()
    end_time = datetime.now()
    print("processing-time = ", end_time - start_time, "Hr:min:sec")
