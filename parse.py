#!/usr/bin/env python3.10
from typing import NamedTuple, TypeVar, Any
from pykml import parser
from pykml.factory import nsmap
from lxml import objectify
import typer
import csv
from sys import stdout

def process_schema_data(xml: objectify.ObjectifiedElement) -> tuple[str, str]:
    extended_data = getattr(xml, "ExtendedData")
    if extended_data is None:
        return ("", "")
    schema_data: objectify.ObjectifiedDataElement | None = getattr(
        extended_data, "SchemaData")
    if schema_data is None:
        return ("", "")
    schema_data, = schema_data.iterchildren(None)
    if schema_data is None:
        return ("", "")
    trafo, monohilo, _, _ = schema_data.iterchildren(None)
    return tuple(map(str, [trafo, monohilo]))

class Trafo(NamedTuple):
    nombre_pot: str
    id_trafo: str
    id_monohilo: str
    lat: float
    long: float

    @classmethod
    def from_xml(cls, xml: objectify.ObjectifiedElement):
        long, lat, _ = map(float, str(xml.Point.coordinates).split(","))
        trafo, monohilo = process_schema_data(xml)
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