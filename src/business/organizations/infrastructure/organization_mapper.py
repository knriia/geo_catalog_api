import uuid6

from src.business.organizations.domain.organization_entity import OrganizationEntity
from src.business.organizations.infrastructure.organization_model import (
    OrganizationActivityModel,
    OrganizationModel,
    OrganizationPhoneModel,
)
from src.catalogs.activities.infrastructure.activity_mapper import ActivityMapper
from src.catalogs.buildings.infrastructure.building_mapper import BuildingMapper


class OrganizationMapper:
    @staticmethod
    def to_domain(model: OrganizationModel) -> OrganizationEntity:
        building_entity = None
        if "building" in model.__dict__ and model.building:
            building_entity = BuildingMapper.to_domain(model.building)

        activity_entities = []
        activity_ids = []
        if "activities" in model.__dict__ and model.activities:
            activity_entities = [ActivityMapper.to_domain(a) for a in model.activities]
            activity_ids = [a.id for a in model.activities]

        phone_numbers = []
        if "phone_numbers" in model.__dict__ and model.phone_numbers:
            phone_numbers = [p.phone_number for p in model.phone_numbers]

        return OrganizationEntity(
            id=model.id,
            name=model.name,
            building_id=model.building_id,
            activity_ids=activity_ids,
            phone_numbers=phone_numbers,
            building=building_entity,
            activities=activity_entities,
        )

    @staticmethod
    def to_model(entity: OrganizationEntity) -> OrganizationModel:
        phone_models = [
            OrganizationPhoneModel(id=uuid6.uuid7(), phone_number=num, organization_id=entity.id)
            for num in entity.phone_numbers
        ]
        activity_links = [
            OrganizationActivityModel(organization_id=entity.id, activity_id=act_id) for act_id in entity.activity_ids
        ]

        return OrganizationModel(
            id=entity.id,
            name=entity.name,
            building_id=entity.building_id,
            phone_numbers=phone_models,
            activity_links=activity_links,
        )
