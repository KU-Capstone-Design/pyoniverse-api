from chalice import BadRequestError
from overrides import override

from chalicelib.common.model.converter import IdConverter
from chalicelib.interface.service import Service


class HomeService(Service):
    @override
    def get_list(self, **kwargs) -> list:
        match kwargs["type"]:
            case "stores":
                res = self._repository.find(type="brand")
                for brand in res:
                    brand["brand"] = brand["name"].upper()
                    brand["image-alt"] = f"{brand['brand']} Logo"

            case "events":
                res = self._repository.find(type="event")
                for event in res:
                    event["brand"] = IdConverter.convert_brand_id(event["brand"])[
                        "name"
                    ].upper()
                    event["image"] = event["image"]["thumb"]
                    event["image-alt"] = f"({event['brand']}) {event['name']}"
                    # TODO : DB 연동
                    event["start_at"] = "2023-10-01"
                    event["end_at"] = "2023-10-31"
                return res
            case "products":
                res = self._repository.find(type="product")
                for product in res:
                    product["events"] = [
                        IdConverter.convert_event_id(e)["name"]
                        for e in product["best"]["events"]
                    ]
                    product["event_brand"] = IdConverter.convert_brand_id(
                        product["best"]["brand"]
                    )["name"].upper()
                    product["event_price"] = (
                        product["best"]["price"]
                        if product["best"]["price"] < product["price"]
                        else None
                    )
                    product["image-alt"] = f"{product['name']} thumbnail"
                    del product["best"]
                return res
            case _:
                raise BadRequestError(
                    f"Invalid type: {type}. Valid types are: stores, events, products"
                )
        return res
