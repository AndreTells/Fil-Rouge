from enum import Enum

class ColaborationTypes(Enum):
    NONE = 0
    FRIENDS = 1
    ENEMIES = 2

    def __str__(self):
        match(self):
            case(ColaborationTypes.NONE):
                return 'NONE'
            case(ColaborationTypes.FRIENDS):
                return 'FRIENDS'
            case(ColaborationTypes.ENEMIES):
                return 'ENEMIES'
