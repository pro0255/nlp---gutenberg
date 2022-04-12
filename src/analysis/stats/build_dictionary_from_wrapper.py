import typing
import json

from src.statistic.metric_wrapper import MetricWrapper
from src.statistic.types.metric_type import translate_instance_to_type


def build_dictionary_from_wrapper(
    current_stats: typing.Type[MetricWrapper],
) -> typing.Dict:
    res = {}

    for m_instance in current_stats.metric_instances:
        name = translate_instance_to_type(m_instance)
        current_df = m_instance.get_dataframe()
        current_dic = current_df.to_dict()
        res[name] = json.dumps(current_dic)

    return res
