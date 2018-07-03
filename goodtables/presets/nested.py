# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

from copy import deepcopy
from ..registry import preset
from .. import exceptions


# Module API

@preset('nested')
def nested(source, **options):
    warnings = []
    tables = []
    presets = options.pop('presets')

    # Add warnings, tables
    source = deepcopy(source)
    for item in source:
        preset = item.pop('preset', 'table')
        checks = item.pop('checks', [])
        if preset == 'nested':
            message = 'Preset "nested" supports only one level depth'
            raise exceptions.GoodtablesException(message)
        try:
            preset_func = presets[preset]['func']
        except KeyError:
            message = 'Preset "%s" is not registered' % preset
            raise exceptions.GoodtablesException(message)
        item.update(options)
        item_warnings, item_tables = preset_func(**item)
        if checks:
            for item_table in item_tables:
                item_table['checks'] = checks
        warnings.extend(item_warnings)
        tables.extend(item_tables)

    return warnings, tables
