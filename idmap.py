"""
Bidirectional map from object to unique ID.
Useful, for example, when making a map of feature names <=> IDs.
"""

class KeyError(Exception):
    """
    Exception raised for keys missing from a readonly FeatureMap
    Attributes:
        key -- Key not present.
    """
    def __init__(self, key):
        self.key = key

class IDmap:
    """
    Map from an objection to a unique numerial ID.
    The IDs are sequential, starting from 0.
    If allow_unknown=True (False by default), then all unknown words get mapped
    to one OOV token id.
    """
    def __init__(self, keys=[], allow_unknown=False, unknown_key="*UNKNOWN*"):
        self.unknown_key = unknown_key
        self.map = {}
        self.reverse_map = []
        self.allow_unknown = False      # We'll set this to allow_unknown AFTER running add on all the keys
        if allow_unknown:
            self.add(self.unknown_key)
        for key in keys:
            self.add(key)
        self.allow_unknown = allow_unknown

    def add(self, key):
        """ Add key to map. """
        if key != self.unknown_key:
            assert not self.exists(key)
        assert key not in self.map
        self.map[key] = len(self.reverse_map)
        self.reverse_map.append(key)
        assert self.exists(key) and self.key(self.id(key)) == key

    def exists(self, key):
        """ Return True iff this key is in the map, or if self.allow_unknown is True """
        return key in self.map or self.allow_unknown

    def id(self, key, add_if_key_doesnt_exist=False):
        """
        Get the ID for this string.
        """
        if add_if_key_doesnt_exist and key not in self.map:
            self.add(key)
            assert key in self.map

        if key in self.map: return self.map[key]
        if self.allow_unknown:
#            import sys
#            print >> sys.stderr, self.__dict__.keys() # REMOVEME
            return self.map[self.unknown_key]
        raise KeyError(key)

    def key(self, id):
        """ Get the key for this ID. """
        return self.reverse_map[id]

    def __getitem__(self, k):
        if type(k) == int: return self.key(k)
        else: return self.id(k)

    @property
    def all(self):
        """ All keys. """
        return self.reverse_map

    @property
    def len(self):
        assert len(self.map) == len(self.reverse_map)
        return len(self.map)
