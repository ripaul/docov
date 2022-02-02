"""
docov

Light-weight, recursive docstring coverage analysis for python modules.
"""

class _submodules:
    import anybadge
    import inspect
    import builtins
    import importlib

#from pprint import pprint as _pprint

builtin_types = [getattr(_submodules.builtins, d) for d in dir(_submodules.builtins) if isinstance(getattr(_submodules.builtins, d), type)]


def is_module(item):
    """
        Checks if the passed item can be imported as a module.
    """
    try:
        _submodules.importlib.import_module(item)
        return True
    except:
        return False


def collect_ignores(items):
    """
        Collect items that are supposed to be ignored. This consists of symbols, types and modules.

        Parameters:
            items: A list of items which are supposed to be ignored.
    """
    ignored_types = builtin_types
    ignored_modules = set()
    ignored_symbols = set()
    for item in items:
        if is_module(item):
            ignored_modules.add(item)
            module = _submodules.importlib.import_module(item)
            ignored_types += set([getattr(module, d) for d in dir(module) if isinstance(getattr(module, d), type)])
        else:
            ignored_symbols.add(item)

    return set(ignored_types), ignored_modules, ignored_symbols



def fetch(module, depth = 3, ignore_hidden = True, ignore = []):
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

    ignored_types, ignored_modules, ignored_symbols = collect_ignores(ignore)
    seen = set()

    def skip_analysis(name, item):
        try:
            return (ignore_hidden and name.startswith('_')) or id(item) in seen or name.split('.')[-1] in ignored_symbols or name in ignored_symbols
        except:
            return False

    def skip_recursion(name, item):
        try:
            return (name in ignored_symbols or \
                 name.split('.')[-1] in ignored_symbols or \
                 name.count('.') >= depth or \
                 name.split('.')[0] in ignored_modules or \
                 type(item) in ignored_types or \
                 item in ignored_types)
        except:
            return False

    items = [(module.__name__ + "." + item[NAME], item[HANDLE]) for item in _submodules.inspect.getmembers(module) if not skip_analysis(*item)]

    for i in range(len(items)):
        seen.add(id(items[i][HANDLE]))

    i = 0
    while i < len(items):
        item = items[i][HANDLE]
        name = items[i][NAME]

        if not skip_recursion(name, item):
            _items = [_item for _item in _submodules.inspect.getmembers(item) if not skip_analysis(*_item)]

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


def report(sufficient_items, insufficient_items, condition, output = ".", prefix = None, **kwargs):
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

    if n_all == 0:
        raise RuntimeError("No items were analyzed!")

    text = "Found insufficient " + condition.target + " for the following items:\n"

    names = [name for name, _ in insufficient_items]

    for name in sorted(names):
        text += "  -- " + name + "\n"

    coverage = int(1000 * round(len(sufficient_items) / n_all, 3)) / 10.

    text += "Found " + str(n_all) + " items of which " + str(len(sufficient_items)) + " have suffcient "
    text += condition.target + ".\n"
    text += "Coverage: " + str(coverage) + condition.unit + "\n"

    prefix = prefix + "_" if prefix is not None else ""

    return output + "/" + prefix + condition.name + ".txt", text

    #with open(output + "/" + prefix + condition.name + ".txt", "w") as f:
    #    f.write(text)


def badge(sufficient_items, insufficient_items, condition, output = ".", prefix = None, thresholds = None, **kwargs):
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

    if n_all == 0:
        raise RuntimeError("No items were analyzed!")

    coverage = int(1000 * round(len(sufficient_items) / n_all, 3)) / 10.

    thresholds = condition.thresholds if thresholds is None else condition.thresholds
    badge = _submodules.anybadge.Badge(condition.name, coverage, value_suffix=condition.unit, thresholds=thresholds)

    prefix = prefix + "_" if prefix is not None else ""

    return output + "/" + prefix + condition.name + ".svg", badge

    #badge.write_badge(output + "/" + prefix + condition.name + ".svg", overwrite=True)
