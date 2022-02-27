from everycache_api.extensions import db, ma


class BaseSchema(ma.SQLAlchemyAutoSchema):
    id = ma.String(attribute="ext_id", dump_only=True)

    class Meta:
        sqla_session = db.session
        load_instance = True
        ordered = True
        exclude = ["id_", "deleted"]
