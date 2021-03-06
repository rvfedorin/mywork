from django.db import models

# Create your models here.

REGIONS = (
	(1, 'Spb'),
	(2, 'Region2'),
	(3, 'Region3'),
	(4, 'Region4'),
	(5, 'Region5'),
	)


class Cities(models.Model):

    city = models.CharField(max_length=30, help_text='Город')
    city_prefix = models.CharField(max_length=10, help_text='Префикс в мнемокоде')
    region = models.IntegerField(choices=REGIONS)
    comment = models.TextField(blank=True)


    def __str__(self):
        _text = f"{REGIONS[self.region-1][1]} {self.city} ({self.city_prefix});  {self.comment}"
        return _text

    def get_reg_id(region: str):
        for _id, _reg in REGIONS:
            if _reg == region:
                return _id

    def all_regions():
        regions = []
        for _reg in REGIONS:
            regions.append(_reg[1])
        return regions


    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'