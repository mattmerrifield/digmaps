
import enum


class ChoiceEnum(enum.Enum):
    @classmethod
    def choices(cls):
        """
        Choices for a django model
        """
        return [(tag.value, tag.name.replace("_", " ").title()) for tag in cls]


class Evidence(enum.IntEnum, ChoiceEnum):
    """
    Constants to quantitatively describe how certain we are that a site
    contains evidence for a certain tag.

    Internally represented as integers from a scale of 0-100, so they sort.
    """

    VERY_CLEAR = 100
    CLEAR = 75
    TYPICAL = 50
    UNCLEAR = 25
    VERY_UNCLEAR = 0


class BurialTypes(ChoiceEnum):
    """
    Types of burial hardware
    """
    TOMB = "tomb"
    CARIN = "carin"
    CEMETARY = "cemetary"


class Survey(ChoiceEnum):
    """
    Types of archaeological survey. Looking around on the ground, vs. digging in it
    """
    SURFACE_SURVEY = 'surface'
    EXCAVATION = 'excavation'
