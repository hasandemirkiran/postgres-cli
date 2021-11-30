import datetime


def return_tree_of_specific_type(tree_class: int):
    """
    This query return Feature ID, Feature coordinates, Label ID, Session ID and Raster url
    """
    query = """WITH FinalData(feature_id, feature_area, label_id, session_id) AS ( 
            SELECT	F.id, ST_AsText(F.feature_area), L.id,	L.session_id 
	        FROM public.label_feature F 
            JOIN public.label L ON F.label_id = L.id 
	        WHERE L.id = F.label_id AND F.class_id = {0}), 
	        SessionRaster(session_id, raster_url) AS ( 
            SELECT	S.id, R.url 
            FROM public.label_session S 
            JOIN public.raster_info R ON S.raster_info_id = R.id) 
            SELECT  FD.feature_id, FD.feature_area, FD.label_id, SR.session_id, SR.raster_url 
            FROM FinalData AS FD 
            JOIN SessionRaster AS SR ON FD.session_id = SR.session_id ;""".format(
        tree_class
    )
    return query


def return_all_region_for_a_tree_type(tree_class: int):
    """
    This query return Feature ID, Feature tree class, Feature coordinates, Label ID, Session ID and Raster url
    """
    query = """WITH LabelData(label_id, session_id) AS ( 
            SELECT	L.id,L.session_id   
	        FROM public.label_feature F 
		    JOIN public.label L ON F.label_id = L.id 
	        WHERE L.id = F.label_id AND F.class_id = {}), 
	        SessionRaster(session_id, raster_url) AS ( 
            SELECT	S.id, R.url 
	        FROM public.label_session S 
            JOIN public.raster_info R ON S.raster_info_id = R.id)  
            SELECT  F.id, F.class_id AS tree_type, F.feature_area, LD.label_id,	SR.session_id,SR.raster_url 
            FROM LabelData AS LD 
	        JOIN SessionRaster AS SR ON LD.session_id = SR.session_id  
	        JOIN public.label_feature AS F ON F.label_id = LD.label_id ;""".format(
        tree_class
    )
    return query


def return_all_region_by_tree_type_percentage(tree_class: str, min=0, max=100):
    """
    Starting from a specific type of tree and its minimum and maximum presence (in percentage) return the labels with that conditions (and all the trees inside)
    Feature ID, Feature coordinates, tree class, lable ID, Session ID, the raster url and the tree presence percentage
    """

    query = """WITH SessionRaster(session_id, raster_url, area_name) AS ( 
            SELECT	S.id, R.url, S.name
	        FROM public.label_session AS S JOIN public.raster_info R ON S.raster_info_id = R.id  
            WHERE S.classification = true)
	        , PartialCount(label_id, session_id, label_area ,counter) as ( 
            SELECT	L.id, L.session_id, L.label_area, COUNT(*) 
	        FROM public.label_feature AS F 
		    JOIN public.label L ON F.label_id = L.id 
            WHERE L.id = F.label_id AND F.class_id = {0}
            GROUP BY L.id) 
            , TotalCount (label_id, counter) as (
            SELECT	L.id, COUNT(*) 
            FROM public.label_feature F 
            JOIN public.label L ON F.label_id = L.id 
            WHERE L.id = F.label_id 
            GROUP BY L.id ) 
            , SelectedLabel (label_id, session_id, label_area, percentage) as ( 
            SELECT	PC.label_id, PC.session_id, PC.label_area,(PC.counter::float/TC.counter::float)*100.0 
            FROM PartialCount AS PC 
            JOIN TotalCount AS TC ON TC.label_id = PC.label_id 
            JOIN SessionRaster AS SR ON SR.session_id = PC.session_id 
            WHERE (PC.counter::float/TC.counter::float)*100.0 > {1} AND (PC.counter::float/TC.counter::float)*100.0 < {2}) 
            SELECT  F.id AS feature_id, ST_x(F.feature_area) AS feature_coordinate_x ,ST_y(F.feature_area) AS feature_coordinate_y, TR.name AS tree_type, 
                SL.label_id AS label_id, ST_AsGeoJSON(SL.label_area) AS label_area, SL.session_id AS session_id, SR.raster_url AS raster_url, SL.percentage AS percentage, SR.area_name AS region_name
            FROM SelectedLabel AS SL 
            JOIN SessionRaster AS SR ON SR.session_id = SL.session_id 
            JOIN public.label_feature AS F ON F.label_id = SL.label_id 
            JOIN public.tree_class AS TR ON TR.id = F.class_id 
            ORDER BY region_name ASC""".format(
        tree_class, min, max
    )
    # ORDER BY label_id".format(tree_class, min, max)
    return query


def return_all_labels_for_region(region: str):
    """
    Starting from the name of a region return all the avaiable labels for that region
    Feature ID, Feature coordinates, tree class, lable ID, Session ID, the raster url and the tree presence percentage
    """
    query = """SELECT	F.id AS feature_id, ST_x(F.feature_area) AS feature_coordinate_x, ST_y(F.feature_area) AS feature_coordinate_y,	ST_AsGeoJSON(L.label_area) AS label_area, 
		    TR.name AS tree_type, L.id AS label_id,	S.id AS session_id,	R.url AS raster_url, S.name AS region_name 
            FROM public.label_feature AS F 
	        JOIN public.label AS L ON L.id = F.label_id 
	        JOIN public.label_session AS S ON S.id = L.session_id 
	        JOIN public.raster_info AS R ON R.id = S.raster_info_id 
	        JOIN public.tree_class AS TR ON TR.id = F.class_id 
            WHERE S.name= '{}' 
            ORDER BY S.name ASC;""".format(
        region
    )
    return query


def return_all_region_for_temporal_interval(
    start_date: datetime.date.fromisoformat, end_date: datetime.date.fromisoformat
):
    """
    Starting from a specific type of tree and its minimum and maximum presence (in percentage) return the labels with that conditions (and all the trees inside)
    Feature ID, Feature coordinates, tree class, lable ID, Session ID, the raster url and the tree presence percentage
    """
    query = """SELECT	F.id AS feature_id, ST_x(F.feature_area) AS feature_coordinate_x, ST_y(F.feature_area) AS feature_coordinate_y,	ST_AsGeoJSON(L.label_area) AS label_area, 
		    TR.name AS tree_type, L.id AS label_id,	S.id AS session_id,	R.url AS raster_url, S.name AS region_name 
            FROM public.label_feature AS F 
	        JOIN public.label AS L ON L.id = F.label_id 
	        JOIN public.label_session AS S ON S.id = L.session_id 
	        JOIN public.raster_info AS R ON R.id = S.raster_info_id 
	        JOIN public.tree_class AS TR ON TR.id = F.class_id 
            WHERE R.recording_start_date between '{} 00:00:00' and '{} 23:59:59'
            ORDER BY S.name ASC; """.format(
        start_date, end_date
    )
    return query


def return_all_region_for_same_months(first_month: int, last_month: int):
    """
    Starting from a specific type of tree and its minimum and maximum presence (in percentage) return the labels with that conditions (and all the trees inside)
    Feature ID, Feature coordinates, tree class, lable ID, Session ID, the raster url and the tree presence percentage
    """
    query = """SELECT  F.id AS feature_id, ST_x(F.feature_area) AS feature_coordinate_x, ST_y(F.feature_area) AS feature_coordinate_y,	
		        ST_AsGeoJSON(L.label_area) AS label_area, TR.name AS tree_type, L.id AS label_id, S.id AS session_id,	
		        R.url AS raster_url, S.name AS region_name, R.recording_start_date AS acquisition_date
                FROM public.label_feature AS F 
                JOIN public.label AS L ON L.id = F.label_id 
                JOIN public.label_session AS S ON S.id = L.session_id 
                JOIN public.raster_info AS R ON R.id = S.raster_info_id 
                JOIN public.tree_class AS TR ON TR.id = F.class_id 
                WHERE EXTRACT(MONTH FROM R.recording_start_date) BETWEEN {} AND {}
                ORDER BY S.name ASC; """.format(
        first_month, last_month
    )
    return query
