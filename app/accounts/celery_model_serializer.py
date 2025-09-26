from celery import Task
import logging
from django.apps import apps
from django.db import models

db_logger = logging.getLogger('db')

MODEL_MARKER = '__model_instance__'

def wrap_model(arg):
    if isinstance(arg, models.Model):
        # Wrap the model instance into a tuple of model metadata (exactly 4 elements)
        wrapped = (MODEL_MARKER, arg._meta.app_label, arg._meta.model_name, str(arg.pk))
        return wrapped
    elif isinstance(arg, list):
        # Recursively wrap items in the list
        return [wrap_model(item) for item in arg]
    elif isinstance(arg, dict):
        # Recursively wrap values in the dictionary
        return {k: wrap_model(v) for k, v in arg.items()}
    elif isinstance(arg, tuple):
        # Recursively wrap items in the tuple
        return tuple(wrap_model(item) for item in arg)
    return arg


def unwrap_model(arg):
    if isinstance(arg, tuple):
        empty_tuple = ()
        for i in arg :
            if isinstance(i, list):
                ## if its a list and wrapped model instant 
                if len(i) > 0 and i[0] == MODEL_MARKER and len(i) == 4:
                    app_label, model_name, pk = i[1], i[2], i[3]
                    model_class = apps.get_model(app_label, model_name)
                    main_object = model_class.objects.get(pk=pk)
                    empty_tuple = empty_tuple + (main_object,)
                else:
                    empty_tuple = empty_tuple + (i,)
            elif isinstance(i, dict):
                ## if its a dict and wrapped model instant 
                dict_wrapped_data = {}
                for dict_key,dict_value in i.items():
                    if isinstance(dict_value, list):
                        ## if its a list and wrapped model instant 
                        if len(dict_value) > 0 and dict_value[0] == MODEL_MARKER and len(dict_value) == 4:
                            app_label, model_name, pk = dict_value[1], dict_value[2], dict_value[3]
                            model_class = apps.get_model(app_label, model_name)
                            main_object = model_class.objects.get(pk=pk)
                            dict_wrapped_data[dict_key] = main_object
                        else:
                            dict_wrapped_data[dict_key] = dict_value
                    else:
                        dict_wrapped_data[dict_key] = dict_value

                empty_tuple = empty_tuple + (dict_wrapped_data,)
            else:
                empty_tuple = empty_tuple + (i,)
        return empty_tuple
    
    elif isinstance(arg, list):
        return [unwrap_model(item) for item in arg]
    elif isinstance(arg, dict):
        return {k: unwrap_model(v) for k, v in arg.items()}
    return arg


class CustomModelTask(Task):
    """
    Custom Celery Task that automatically wraps model instances into primary keys 
    when calling the task, and automatically unwraps them when executing the task.
    """

    def apply_async(self, args=None, kwargs=None, **options):
        # Wrap args and kwargs before sending to Celery
        wrapped_args = wrap_model(args or [])
        wrapped_kwargs = wrap_model(kwargs or {})
        return super().apply_async(args=wrapped_args, kwargs=wrapped_kwargs, **options)

    def __call__(self, *args, **kwargs):
        # Unwrap args and kwargs before calling the actual task
        unwrapped_args = unwrap_model(args)
        unwrapped_kwargs = unwrap_model(kwargs)
        return self.run(*unwrapped_args, **unwrapped_kwargs)
