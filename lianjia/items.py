from scrapy.item import Item, Field


class LianjiaItem(Item):
    city = Field()
    district = Field()
    realEstateAgent = Field()
    age = Field()
    houseType = Field()
    unitPrice = Field()
    price = Field()
    residentialName = Field()
    publicTime = Field()
    acreage = Field()
    title = Field()

    imageUrl = Field()
    imagePath = Field()
