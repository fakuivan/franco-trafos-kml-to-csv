#!/usr/bin/env python3.10
from typing import NamedTuple, TypeVar, Any
from pykml import parser
from pykml.factory import nsmap
from lxml import objectify
import typer
import csv
from sys import stdout

T = TypeVar("T")
def getattr_chain(obj, default: T, attr_name: str, *rest_attr: str) -> T | Any:
    if not (hasattr(obj, attr_name)):
        return default
    attr = getattr(obj, attr_name)
    if len(rest_attr) > 0:
        getattr_chain(attr, default, *rest_attr)
    return attr


class Trafo(NamedTuple):
    nombre_pot: str
    id_trafo: str
    id_monohilo: str
    lat: float
    long: float

    @classmethod
    def from_xml(cls, xml: objectify.ObjectifiedElement):
        long, lat, _ = map(float, str(xml.Point.coordinates).split(","))
        schema_data = getattr_chain(xml, None, "ExtendedData", "SchemaData")
        trafo, monohilo = ("", "") if schema_data is None else [*schema_data.getiterator()][2:4]
        return cls(
            getattr(xml, "name", ""),
            trafo,
            monohilo,
            lat,
            long
        )


def main(kml_file: typer.FileText):
    root = parser.parse(kml_file).getroot()
    placemarks = root.findall(".//ns:Placemark", namespaces={"ns": nsmap[None]})

    writer = csv.writer(stdout)
    writer.writerow(Trafo._fields)
    writer.writerows(map(Trafo.from_xml, placemarks))

if __name__ == "__main__":
    typer.run(main)