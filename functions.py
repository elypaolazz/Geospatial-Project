import os
import geopandas as gpd


# Function to download and extract zip folders
def download_extract(path_name, zip_url):
    if not os.path.exists(path_name):
        # download the data
        import requests, zipfile, io
        zip_file_url = zip_url
        # request the file
        r = requests.get(zip_file_url, verify=False)
        z = zipfile.ZipFile(io.BytesIO(r.content))
        # unzip the file
        z.extractall('data')

# Function to load Dolomiti data as GeoDataFrame and add systems area
def load_geodf_dolomities(path):
    gpd.io.file.fiona.drvsupport.supported_drivers['KML'] = 'rw'
    geodf_dolomities = gpd.read_file(path, driver='KML')
    geodf_dolomities["area"] = geodf_dolomities.to_crs(epsg=32632).geometry.area
    return geodf_dolomities

# Function to calculate representative point for the region labels
def representative_points_for_labels(geodf, labels_column):
    representative_points = gpd.GeoDataFrame(geodf.representative_point()).reset_index()
    representative_points = representative_points.rename(columns={0:'geometry'}).set_geometry('geometry')
    labels = geodf[labels_column].to_frame().reset_index()
    representative_points = representative_points.merge(labels,on="index")
    representative_points = representative_points.rename(columns={labels_column :'names'})
    representative_points = representative_points.rename(columns={0:'geometry'})
    representative_points = gpd.GeoDataFrame(representative_points,geometry=representative_points['geometry'],crs=4326)
    return representative_points

# Function to get cities coordinates labels
def city_coordinates_label(geodf, city_type_col):
    cols = ['cities']
    names = list(geodf[city_type_col].unique())
    capoluoghi = gpd.GeoDataFrame(names,columns=cols)
    geo_capoluighi = gpd.tools.geocode(capoluoghi.cities, provider="arcgis")
    geo_capoluighi = geo_capoluighi.rename(columns={0:'geometry'}).set_geometry('geometry')
    labels = geodf.DEN_PROV.to_frame()
    geo_capoluighi = geo_capoluighi.rename(columns={'address': city_type_col})
    geo_capoluighi = geo_capoluighi.merge(labels,on= city_type_col)
    geo_capoluighi = geo_capoluighi.rename(columns={0:'geometry'})
    geo_capoluighi = gpd.GeoDataFrame(geo_capoluighi,geometry=geo_capoluighi['geometry'],crs=4326)
    return geo_capoluighi

# Function to obtain the percentage of each Dolomitic system in the province
# def province_systems_percentage(province, system, geodf_dolomities):
    
#     geodf_dolomities = geodf_dolomities
#     load_province(province, 'data\Limiti01012021_g\ProvCM01012021_g')
    
#     system_geodf = geodf_dolomities[geodf_dolomities.Name == system]
#     system_area = geodf_dolomities[geodf_dolomities.Name == system]['area'].values[0]
    
#     system_area_clipped = system_geodf.to_crs(epsg=32632).clip(province_geodf.to_crs(epsg=32632)).area/10**6
    
#     percentage_of_system = (system_area_clipped.values[0]/system_area)*100

#     print(round(percentage_of_system, 2), "% of the", " '",system,"' ", "is in province of ", province, sep="")
    
# Function to obtain the percentage of each Dolomitic system in the Dolomiti's municipalities of the province
def mun_systems_area(mun):
    
    mun_geodf = municipalities[municipalities.COMUNE == mun]
    
    system_geodf = geodf_dolomities
    systems_area = sum(geodf_dolomities['area'])
    
    system_area_clipped = overal_dolomiti.to_crs(epsg=32632).clip(mun_geodf.to_crs(epsg=32632)).area/10**6
    
    percentage_dolomiti = (system_area_clipped/systems_area)*100

    print("'", mun, "'", " contains ", round(system_area_clipped.values[0], 3), " km\u00b2 of Dolomities.", "and the ", round(percentage_dolomiti.values[0], 3), "% of the overall Dolomities territory", sep="")
    
    return [mun, system_area_clipped.values[0], percentage_dolomiti.values[0]]

# Function to get province GeoDataFrame
def load_province(province_capital, path):
    provinces_path = path
    provinces = gpd.read_file(provinces_path)
    provinces = provinces.to_crs(epsg=4326)[['COD_REG', 'COD_PROV', 'DEN_PROV', 'Shape_Area', 'geometry']]
    province = provinces[provinces.DEN_PROV == province_capital]
    return province


def lead_province_clipped_dolomiti(province_capital, path):
    geodf_dolomities = load_geodf_dolomities('data\I nove Sistemi delle Dolomiti UNESCO.kml')
    
    regions_path = path + '\Reg01012021_g'
    regions = gpd.read_file(regions_path)
    regions = regions.to_crs(epsg=4326)[['COD_REG', 'DEN_REG', 'Shape_Area', 'geometry']]

    provinces_path = path + '\ProvCM01012021_g'
    provinces = gpd.read_file(provinces_path)
    provinces = provinces.to_crs(epsg=4326)[['COD_REG', 'COD_PROV', 'DEN_PROV', 'Shape_Area', 'geometry']]

    prov_reg = gpd.sjoin(provinces, regions, how='left', predicate='within', lsuffix='', rsuffix='reg')
    
    geodf_dolomities_provices = gpd.sjoin(geodf_dolomities, prov_reg, how='left', predicate='intersects', lsuffix='dolomities', rsuffix='provinces')
    geodf_dolomities_provices = geodf_dolomities_provices[['Name', 'Description', 'geometry', 'area', 'COD_REG_', 'COD_PROV', 'DEN_PROV', 'Shape_Area_', 'DEN_REG', 'Shape_Area_reg']]
    
    dolomities_prov = geodf_dolomities_provices[geodf_dolomities_provices.DEN_PROV == 'Bolzano']
    
    province = load_province(province_capital, 'data\Limiti01012021_g\ProvCM01012021_g')
    dolomities_clipped = dolomities_prov.clip(province)
    
    return dolomities_clipped

# Function to load Dolomiti's municipalities of a province
def load_province_dolomiti_mun(code_prov, path):
    municipalities_path = path + '\Com01012021_g'
    municipalities = gpd.read_file(municipalities_path)
    municipalities = municipalities.to_crs(epsg=4326)[['COD_REG', 'COD_PROV', 'PRO_COM_T', 'COMUNE', 'Shape_Area', 'geometry']]
    municipalities_BZ = municipalities[municipalities.COD_PROV == code_prov]

    regions_path = path + '\Reg01012021_g'
    regions = gpd.read_file(regions_path)
    regions = regions.to_crs(epsg=4326)[['COD_REG', 'DEN_REG', 'Shape_Area', 'geometry']]

    provinces_path = path + '\ProvCM01012021_g'
    provinces = gpd.read_file(provinces_path)
    provinces = provinces.to_crs(epsg=4326)[['COD_REG', 'COD_PROV', 'DEN_PROV', 'Shape_Area', 'geometry']]

    prov_reg = gpd.sjoin(provinces, regions, how='left', predicate='within', lsuffix='', rsuffix='reg')
    prov_reg_mun = gpd.sjoin(municipalities, prov_reg, how='left', predicate='within', lsuffix='', rsuffix='prov')

    geodf_dolomities = load_geodf_dolomities('data\I nove Sistemi delle Dolomiti UNESCO.kml')
    geodf_dolomities_municipalities = gpd.sjoin(geodf_dolomities, prov_reg_mun, how='left', predicate='intersects', lsuffix='dolomities', rsuffix='mun')
    geodf_dolomities_municipalities = geodf_dolomities_municipalities[['Name', 'Description', 'geometry', 'area', 'COD_REG', 'COD_PROV_', 'PRO_COM_T', 'COMUNE', 'Shape_Area', 'DEN_PROV', 'DEN_REG']]

    dolomiti_mun = geodf_dolomities_municipalities.COMUNE.unique()
    geo_dolomiti_mun = municipalities_BZ[municipalities_BZ.COMUNE.isin(dolomiti_mun)]
    return geo_dolomiti_mun


def regions_systems_percentage(region, geodf_dolomities):
    
    regions_path = "data\Limiti01012021_g\Reg01012021_g"
    regions = gpd.read_file(regions_path)
    regions = regions.to_crs(epsg=4326)[['COD_REG', 'DEN_REG', 'Shape_Area', 'geometry']]
    
    region_geodf = regions[regions.DEN_REG == region]
    
    total_dolomiti_area = sum(geodf_dolomities.to_crs(epsg=32632).area)
    
    dolomiti_area_clipped = sum(geodf_dolomities.to_crs(epsg=32632).clip(region_geodf.to_crs(epsg=32632)).area)
    
    percentage_of_system = (dolomiti_area_clipped/total_dolomiti_area)*100

    print(round(percentage_of_system, 2), "% of the Dolomiti's peaks is in ", region, " with ", round(dolomiti_area_clipped/10**6, 2), " km\u00b2", sep="")
    
    return [region_geodf.DEN_REG.values[0], round(dolomiti_area_clipped/10**6, 2), round(percentage_of_system, 2)]


def dissolve_province_dolomiti_area(code_prov):
    geo_dolomiti_mun = load_province_dolomiti_mun(code_prov, 'data\Limiti01012021_g')
    geo_dolomiti_mun["territory"] = 'dolomiti'
    area_dolomiti = geo_dolomiti_mun[['territory', 'geometry']]
    area_dolomiti = area_dolomiti.to_crs(epsg=4326).dissolve(by='territory')
    return area_dolomiti
    
    
def load_BZ_dolomiti_ski_lift_data(path):
    ski_lifts_path = path
    ski_lifts_BZ = gpd.read_file(ski_lifts_path)
    ski_lifts_BZ = ski_lifts_BZ.to_crs(epsg=4326)
    ski_lifts_BZ_clipped = ski_lifts_BZ.clip(load_province_dolomiti_mun(21, 'data\Limiti01012021_g'))
    return ski_lifts_BZ_clipped