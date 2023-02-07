import pandas as pd
from ocpa.objects.log.ocel import OCEL
from ocpa.objects.log.variants.table import Table
from ocpa.objects.log.variants.graph import EventGraph
import ocpa.objects.log.converter.versions.df_to_ocel as obj_converter
import ocpa.objects.log.importer.csv.versions.to_df as df_importer
import ocpa.objects.log.variants.util.table as table_utils
from typing import Dict


def apply(filepath, parameters: Dict, file_path_object_attribute_table=None) -> OCEL:
    df = df_importer.apply(filepath, parameters)
    obj_df = None

    if parameters["take_sample"]:
        df = df.iloc[:, 0:parameters["take_sample"]]

    if file_path_object_attribute_table:
        obj_df = pd.read_csv(file_path_object_attribute_table)

    log = Table(df, parameters=parameters, object_attributes=obj_df)
    obj = obj_converter.apply(df)
    graph = EventGraph(table_utils.eog_from_log(log))
    ocel = OCEL(log, obj, graph, parameters)
    return ocel
