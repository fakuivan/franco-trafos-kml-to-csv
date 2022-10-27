#!/usr/bin/env python3.10
from typing import NamedTuple
from pykml import parser
from pykml.factory import nsmap
from lxml import objectify
import typer
import csv
from sys import stdout

class Trafo(NamedTuple):
    nombre_pot: str
    id_trafo: str
    id_monohilo: str
    lat: float
    long: float

    @classmethod
    def from_xml(cls, xml: objectify.ObjectifiedElement):
        long, lat, _ = map(float, str(xml.Point.coordinates).split(","))
        return cls(
            getattr(xml, "name", ""),
            getattr(xml, "ID_Trafo", ""),
            getattr(xml, "ID_Monohilo", ""),
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