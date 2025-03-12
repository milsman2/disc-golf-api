"""
Generate a URL for a UDisc course map based on coordinates.
"""

from pydantic import BaseModel


class UDiscCoords(BaseModel):
    lat: float
    lon: float
    sw_lat: float
    sw_lon: float
    ne_lat: float
    ne_lon: float

    def generate_url(self) -> str:
        return (
            f"https://udisc.com/courses?zoom=10&lat={self.lat}&lng={self.lon}"
            f"&swLat={self.sw_lat}&swLng={self.sw_lon}"
            f"&neLat={self.ne_lat}&neLng={self.ne_lon}"
        )


coords = UDiscCoords(
    lat=29.76328,
    lon=-95.36327,
    sw_lat=29.6319106,
    sw_lon=-95.6599009,
    ne_lat=29.8944774,
    ne_lon=-95.0666391,
)

generated_url = coords.generate_url()
