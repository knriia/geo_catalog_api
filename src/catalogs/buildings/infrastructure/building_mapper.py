from typing import cast

from geoalchemy2 import WKTElement
from geoalchemy2.shape import to_shape
from shapely.geometry import Point

from src.catalogs.buildings.domain.building_entity import BuildingEntity
from src.catalogs.buildings.infrastructure.building_model import BuildingModel


class BuildingMapper:
    @staticmethod
    def to_domain(model: BuildingModel) -> BuildingEntity:
        point = cast(Point, to_shape(model.coordinates))
        return BuildingEntity(id=model.id, address=model.address, latitude=point.y, longitude=point.x)

    @staticmethod
    def to_model(building_param: BuildingEntity) -> BuildingModel:
        point_wkt = f"POINT({building_param.longitude} {building_param.latitude})"

        return BuildingModel(
            id=building_param.id,
            address=building_param.address,
            coordinates=WKTElement(point_wkt, srid=4326),
        )
