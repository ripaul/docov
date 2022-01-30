"""
docov

Light-weight, recursive docstring coverage analysis for python modules.
"""

class _submodules:
    import anybadge
    import inspect
    import builtins

builtin_types = [getattr(_submodules.builtins, d) for d in dir(_submodules.builtins) if isinstance(getattr(_submodules.builtins, d), type)]


def fetch(module, depth = 3, ignore_hidden = True, ignore = set()):
    """
        Fetch symbols from module by recursively inspecting its members.

        Parameters:
            module:         Module which is to be analyzed
            depth:          Recursion depth
            ignore_hidden:  Ignore members starting with underscores
            ignore:         Set of members (identified by strings) which are to be ignored
    """
    NAME = 0
    HANDLE = 1

    seen = set()

    items = [item for item in _submodules.inspect.getmembers(module) if not ignore_hidden or not item[NAME].startswith('_')]

    for i in range(len(items)):
        seen.add(id(items[i][HANDLE]))
        items[i] = (module.__name__ + "." + items[i][NAME], items[i][HANDLE])

    i = 0
    while i < len(items):
        item = items[i][HANDLE]
        name = items[i][NAME]

        if not ( \
                name in ignore or \
                name.count('.') >= depth or \
                type(item) in builtin_types):
            _items = [_item for _item in _submodules.inspect.getmembers(item) if not ignore_hidden or not _item[NAME].startswith('_') and not id(_item[HANDLE]) in seen]

            for j in range(len(_items)):
                seen.add(id(items[i][HANDLE]))
                _items[j] = (name + "." + _items[j][NAME], _items[j][HANDLE])

            items += _items

        i += 1

    return items


class SufficientDocstring:
    """
        Wrapper class containing the condition for what is regarded a sufficient docstring and some meta data.
    """

    target = "docstring"
    name = "docov"
    unit = "%"
    thresholds = {50: 'red',
                  65: 'orange',
                  75: 'yellow',
                  90: 'green'}
    
    def __call__(self, item):
        return item.__doc__ is not None and len(item.__doc__) >= 20


def analyze(module, condition = SufficientDocstring(), **kwargs):
    """
        Check the passed condition on the module's symbols.

        Parameters:
            module:     Module which is to be analyzed
            condition:  Condition which is to be checked on the members
            kwargs:     Key-word arguments for underlying function calls (e.g. docov.fetch)

        Returns:
            sufficient_items:   List of (name, object)-tuples that passed the condition
            insufficient_items: List of (name, object)-tuples that did not pass the condition
            condition:          Condition that was checked
    """
    items = fetch(module, **kwargs)

    sufficient_items = []
    insufficient_items = []
    for name, item in items:
        if not condition(item):
            insufficient_items.append((name, item))
        else:
            sufficient_items.append((name, item))

    return sufficient_items, insufficient_items, condition


def create_report(sufficient_items, insufficient_items, condition, output = ".", **kwargs):
    """
        Report the symbols which did not pass the condition.

        Parameters:
            sufficient_items:   List of (name, object)-tuples that passed the condition
            insufficient_items: List of (name, object)-tuples that did not pass the condition
            condition:          Condition that was checked
            output:             Output directory
            kwargs:             Key-word arguments for underlying function calls (e.g. docov.analyze)
    """
    n_all = len(sufficient_items) + len(insufficient_items)

    text = "Found insufficient " + condition.target + " for the following items:\n"

    names = [name for name, _ in insufficient_items]

    for name in sorted(names):
        text += "  -- " + name + "\n"

    coverage = int(1000 * round(len(sufficient_items) / n_all, 3)) / 10.

    text += "Found " + str(n_all) + " items of which " + str(len(sufficient_items)) + " have suffcient "
    text += condition.target + ".\n"
    text += "Coverage: " + str(coverage) + condition.unit + "\n"

    with open(output + "/" + condition.name + ".txt", "w") as f:
        f.write(text)


def create_badge(sufficient_items, insufficient_items, condition, output = ".", thresholds = None, **kwargs):
    """
        Create a badge with the fraction of symbols which did pass the condition.

        Parameters:
            sufficient_items:   List of (name, object)-tuples that passed the condition
            insufficient_items: List of (name, object)-tuples that did not pass the condition
            condition:          Condition that was checked
            output:             Output directory
            thresholds:         Color-coding thresholds for the resulting fraction of passing symbols
            kwargs:             Key-word arguments for underlying function calls (e.g. docov.analyze)
    """
    n_all = len(sufficient_items) + len(insufficient_items)

    coverage = int(1000 * round(len(sufficient_items) / n_all, 3)) / 10.

    thresholds = condition.thresholds if thresholds is None else condition.thresholds
    badge = _submodules.anybadge.Badge(condition.name, coverage, value_suffix=condition.unit, thresholds=thresholds)
    badge.write_badge(output + "/" + condition.name + ".svg", overwrite=True)
