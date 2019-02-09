import logging
from banal import ensure_list
from marshmallow import pre_dump
from marshmallow.fields import Raw, String, Nested, Field

from aleph.model import Alert, Role, Entity, Collection
from aleph.serializers.roles import RoleSchema
from aleph.serializers.alerts import AlertSchema
from aleph.serializers.entities import CombinedSchema
from aleph.serializers.collections import CollectionSchema
from aleph.serializers.common import BaseSchema

log = logging.getLogger(__name__)


class ParamTypes(Field):
    def _serialize(self, value, attr, obj):
        return {p: c.__name__.lower() for (p, c) in value.items()}


class EventSchema(BaseSchema):
    name = String()
    template = String()
    params = ParamTypes()


class NotificationSchema(BaseSchema):
    SCHEMATA = {
        Alert: AlertSchema,
        Role: RoleSchema,
        Entity: CombinedSchema,
        Collection: CollectionSchema
    }

    actor_id = String()
    event = Nested(EventSchema(), dump_only=True)
    params = Raw()

    @pre_dump(pass_many=True)
    def expand(self, objs, many=False):
        results = []
        for obj in ensure_list(objs):
            params = {}
            for name, clazz, value in obj.iterparams():
                schema = self.SCHEMATA.get(clazz)
                data = self._get_object(clazz, value)
                if data is not None:
                    params[name], _ = schema().dump(data)
            results.append({
                'id': obj.id,
                'created_at': obj.created_at,
                'actor_id': obj.actor_id,
                'event': obj.event,
                'params': params
            })
        return results
