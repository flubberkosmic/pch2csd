from enum import Enum
from typing import List

from pch2csd.data import ProjectData
from pch2csd.parsing.util import AttrEqMixin, ReprStrMixin


class Location(Enum):
    FX_AREA = 0
    VOICE_AREA = 1

    @staticmethod
    def from_int(i: int):
        if i == 0:
            return Location.FX_AREA
        elif i == 1:
            return Location.VOICE_AREA
        else:
            raise ValueError(f'Wrong location code: {i}')


class Patch(ReprStrMixin):
    __slots__ = ['data', 'ver', 'type', 'modules', 'cables', 'mod_params']

    def __init__(self, data: ProjectData):
        self.data = data
        self.description = PatchDescription()
        self.modules: List[Module] = []
        self.cables: List[Cable] = []
        self.mod_params: List[ModuleParameters] = []

    def find_module(self, id: int, loc=Location.VOICE_AREA):
        for m in self.modules:
            if m.id == id and m.location == loc:
                return m


class PatchDescription(ReprStrMixin):
    def __init__(self):
        self.active_variation = 0  # TODO support variations


class Module(AttrEqMixin, ReprStrMixin):
    def __init__(self, data: ProjectData, loc: Location, mod_type: int, id: int):
        self.type = mod_type
        self.type_name = data.mod_type_name[mod_type]
        self.id = id
        self.location = loc
        io = data.mod_type_connections[self.type]
        self.inlet_types = io['inputs']
        self.outlet_types = io['outputs']
        # Default buses
        self.inlet_conn = [0 for _ in self.inlet_types]
        self.outlet_conn = [1 for _ in self.outlet_types]

    def __eq__(self, other):
        return self.attrs_equal(other)


class CableType(Enum):
    IN_TO_IN = 0
    OUT_TO_IN = 1

    @staticmethod
    def from_int(i: int):
        if i == 0:
            return CableType.IN_TO_IN
        elif i == 1:
            return CableType.OUT_TO_IN
        else:
            raise ValueError(f'Wrong cable type code: {i}')


class CableColor(Enum):
    RED = 0
    BLUE = 1
    YELLOW = 2
    ORANGE = 3
    GREEN = 4
    PURPLE = 5
    WHITE = 6

    @staticmethod
    def from_int(i: int):
        if i == 0:
            return CableColor.RED
        elif i == 1:
            return CableColor.BLUE
        elif i == 2:
            return CableColor.YELLOW
        elif i == 3:
            return CableColor.ORANGE
        elif i == 4:
            return CableColor.GREEN
        elif i == 5:
            return CableColor.PURPLE
        elif i == 6:
            return CableColor.WHITE
        else:
            raise ValueError(f'Wrong cable color code {i}')


class Cable(AttrEqMixin, ReprStrMixin):
    def __init__(self, loc: Location, type: CableType, color: CableColor, module_from: int,
                 jack_from: int, module_to: int, jack_to: int):
        self.loc = loc
        self.type = type
        self.color = color
        self.module_from = module_from
        self.jack_from = jack_from
        self.module_to = module_to
        self.jack_to = jack_to

    def __eq__(self, other):
        return self.attrs_equal(other)


class ModuleParameters(AttrEqMixin, ReprStrMixin):
    def __init__(self, loc: Location, module_id: int, num_params: int, values=None):
        if values is None:
            values = []
        self.loc = loc
        self.module_id = module_id
        self.num_params = num_params
        self.values = values

    def __eq__(self, other):
        return self.attrs_equal(other)
