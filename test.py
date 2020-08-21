
def unit_conversion(source, target, value):
    """

    >>> unit_conversion('km', 'm', 10)
    (10000.0, 'm')

    >>> unit_conversion('m', 'km', 10)
    (0.01, 'km')

    >>> unit_conversion('kHz', 'Hz', 10)
    (10000.0, 'Hz')

    >>> unit_conversion('Hz', 'kHz', 10)
    (0.01, 'kHz')

    >>> unit_conversion('km', 'l', 10)
    Traceback (most recent call last):
        ...
    ValueError



    :param source:
    :param target:
    :param value:
    :return:
    """
    si_prefix = {
        'm': 1,
        ' ': 1000,
        'k': 1000000,
        'M': 1000000000,
    }
    if source == 'pcs' or target == 'pcs':
        return value, 'pcs'
    elif source == target:
        return value, target
    else:
        source_prefix = ' '
        source_base = ''
        target_prefix = ' '
        target_base = ''
        if len(source) == 1:
            source_prefix = ' '
            source_base = source
        else:
            source_prefix = source[0]
            source_base = source[1:]

        if len(target) == 1:
            target_prefix = ' '
            target_base = target
        else:
            target_prefix = target[0]
            target_base = target[1:]

        if source_base == target_base:
            ratio = si_prefix[source_prefix] / si_prefix[target_prefix]
            return value*ratio, target
        else:
            raise ValueError()