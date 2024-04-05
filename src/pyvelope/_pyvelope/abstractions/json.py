from typing import Union

Json = Union[bool, float, int, str, None, list["Json"], dict[str, "Json"]]
JsonDict = dict[str, Json]

