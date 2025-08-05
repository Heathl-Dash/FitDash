MV_REGISTRY={}


class MaterializedView:
    view_name=None
    sql=None
    frequency=None

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if cls.view_name and cls.sql:
            if cls.frequency not in {'daily', 'weekly', 'monthly'}:
                raise ValueError(f"MaterializedView '{cls.__name__}' precisa ter frequency válido.")
            MV_REGISTRY[cls.view_name]=cls()