from dataclasses import dataclass, field


@dataclass
class DimensionsService:
    """Рассчёт габаритных размеров"""
    width: float
    height: float
    streamline_coefficient: float

    @property
    def midelev_cross_sectional_area(self):
        """площадь Миделева сечения"""
        return self.width * self.height * 0.79
