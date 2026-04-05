from enum import Enum

class ProductCategory(str, Enum):
    ELECTRONICS = "electronics"
    FASHION = "fashion"
    HOME_GARDEN = "home_garden"
    BEAUTY = "beauty"
    AUTOMOTIVE = "automotive"
    OTHER = "other"

class Currency(str, Enum):
    MAD = "MAD"
    USD = "USD"
    EUR = "EUR"

class ProductCondition(str, Enum):
    NEW = "new"
    USED = "used"
    REFURBISHED = "refurbished"
    OPEN_BOX = "open_box"