from chalice import BadRequestError

from chalicelib.interface.service import Service


class EventService(Service):
    def get_single(cls, **kwargs) -> object:
        """
        _type: Literal[detail, list]
        id: int
        """
        # dao = cls.repository.find_by_id(id)
        # TODO : dao -> dto converter
        match kwargs["_type"]:
            case "detail":
                return {
                    "id": 0,
                    "name": "cu 와인 라벨 패키지 공모전",
                    "start_at": "2023-10-01",
                    "end_at": "2023-10-31",
                    "brand_slug": "cu",
                    "brand_name": "CU Store",
                    "images": [
                        "https://pyoniverse-image.s3.ap-northeast-2.amazonaws.com/events/"
                        "18ae49979b0050484fb8a0a86415ac3f248284fb.webp",
                    ],
                    "image_alt": "alt tag",
                    "view_count": 222,
                    "good_count": 222,
                    "link": "https://cu.bgfretail.com/brand_info/news_view.do?category=brand_info&depth2=5&idx=946",
                }
            case "list":
                return {
                    "brands": [
                        {
                            "slug": "cu",
                            "name": "CU Store",
                            "image": "https://pyoniverse-image.s3.ap-northeast-2.amazonaws.com/brands/cu-logo.webp",
                        },
                        {
                            "slug": "seven-eleven",
                            "name": "Seven Eleven",
                            "image": "https://pyoniverse-image.s3.ap-northeast-2.amazonaws.com/"
                            "brands/seveneleven-logo.webp",
                        },
                        {
                            "slug": "gs25",
                            "name": "GS25",
                            "image": "https://pyoniverse-image.s3.ap-northeast-2.amazonaws.com/brands/gs25-logo.webp",
                        },
                        {
                            "slug": "emart24",
                            "name": "Emart24",
                            "image": "https://pyoniverse-image.s3.ap-northeast-2.amazonaws.com/"
                            "brands/emart24-logo.webp",
                        },
                        {
                            "slug": "c-space",
                            "name": "CSpace",
                            "image": "https://pyoniverse-image.s3.ap-northeast-2.amazonaws.com/brands/cspace-logo.webp",
                        },
                    ],
                    "brand_slug": "cu",
                    "brand_name": "CU Store",
                    "events": [
                        {
                            "id": 0,
                            "name": "cu event",
                            "start_at": "2023-10-01",
                            "end_at": "2023-10-31",
                            "image": "https://pyoniverse-image.s3.ap-northeast-2.amazonaws.com/events/"
                            "18ae49979b0050484fb8a0a86415ac3f248284fb.webp",
                            "image_alt": "cu event alt",
                            "view_count": 222,
                            "good_count": 222,
                        },
                        {
                            "id": 0,
                            "name": "cu event",
                            "start_at": "2023-10-01",
                            "end_at": "2023-10-31",
                            "image": "https://pyoniverse-image.s3.ap-northeast-2.amazonaws.com/events/"
                            "18ae49979b0050484fb8a0a86415ac3f248284fb.webp",
                            "image_alt": "cu event alt",
                            "view_count": 222,
                            "good_count": 222,
                        },
                        {
                            "id": 0,
                            "name": "cu event",
                            "start_at": "2023-10-01",
                            "end_at": "2023-10-31",
                            "image": "https://pyoniverse-image.s3.ap-northeast-2.amazonaws.com/events/"
                            "18ae49979b0050484fb8a0a86415ac3f248284fb.webp",
                            "image_alt": "cu event alt",
                            "view_count": 222,
                            "good_count": 222,
                        },
                        {
                            "id": 0,
                            "name": "cu event",
                            "start_at": "2023-10-01",
                            "end_at": "2023-10-31",
                            "image": "https://pyoniverse-image.s3.ap-northeast-2.amazonaws.com/events/"
                            "18ae49979b0050484fb8a0a86415ac3f248284fb.webp",
                            "image_alt": "cu event alt",
                            "view_count": 222,
                            "good_count": 222,
                        },
                    ],
                }
            case _:
                raise BadRequestError(f"{kwargs['_type']} not in [list, detail]")
