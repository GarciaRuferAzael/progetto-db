from sqlalchemy.inspection import inspect

class Serializer(object):

    def serialize(self):
        return {c: getattr(self, c) for c in inspect(self).attrs.keys()} # type: ignore

    @staticmethod
    def serialize_list(l):
        return [m.serialize() for m in l]