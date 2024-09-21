def map_object_attributes(obj, mapping):
    mapped_kwargs = {}
    for obj_attr, kwargs_key in mapping.items():
        if hasattr(obj, obj_attr):
            mapped_kwargs[kwargs_key] = getattr(obj, obj_attr)
    return mapped_kwargs
