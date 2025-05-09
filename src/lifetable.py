import os
from collections import namedtuple
from jinja2 import Template


TABLE_TEMPLATE = '''
<div class="custom-table">
<table>
{% for row in rows -%}
<tr>
{% for cell in row -%}
<td {% if cell.color %}style="background: linear-gradient(30deg, {{ cell.color }}, #000000 70%, #FFFFFF77); box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2); border-radius: 0px;"{% endif %}>{{ cell.date }}</td>
{% endfor -%}
</tr>
{% endfor -%}
</table>
</div>
'''


class LifeA4TableGenerator:

    LifeStage = namedtuple('LifeStage', ['startYear', 'startMonth', 'endYear', 'endMonth', 'color'])
    CellAlpha = 0.95
    BirthYear, BirthMonth = 1990, 3
    DeathYear, DeathMonth = 2064, 2  # expected

    Stages = [
        LifeStage(1990, 3,  1997, 11, f'rgba(152, 255, 152, {CellAlpha})'),
        LifeStage(1997, 12, 2006, 1,  f'rgba(255, 255, 0,   {CellAlpha})'),
        LifeStage(2006, 2,  2008, 6,  f'rgba(197, 119, 255, {CellAlpha})'),
        LifeStage(2008, 7,  2012, 7,  f'rgba(255, 255, 194, {CellAlpha})'),
        LifeStage(2012, 8,  2014, 7,  f'rgba(59, 185, 255,  {CellAlpha})'),
        LifeStage(2014, 8,  2015, 7,  f'rgba(224, 224, 224, {CellAlpha})'),
        LifeStage(2015, 8,  2016, 2,  f'rgba(224, 176, 255, {CellAlpha})'),
        LifeStage(2016, 3,  2016, 4,  f'rgba(224, 224, 224, {CellAlpha})'),
        LifeStage(2016, 5,  2018, 4,  f'rgba(84, 197, 113,  {CellAlpha})'),
        LifeStage(2018, 5,  2018, 7,  f'rgba(255, 36, 0,    {CellAlpha})'),
        LifeStage(2018, 8,  2019, 9,  f'rgba(84, 197, 113,  {CellAlpha})'),
        LifeStage(2019, 10, 2022, 7,  f'rgba(137, 59, 255,  {CellAlpha})'),
        LifeStage(2022, 8,  2023, 6,  f'rgba(142, 173, 161, {CellAlpha})'),
        LifeStage(2023, 7,  2024, 3,  f'rgba(55, 94, 237,   {CellAlpha})'),
        LifeStage(2024, 4,  2024, 5,  f'rgba(119, 120, 128, {CellAlpha})'),
        LifeStage(2024, 6,  2024, 12, f'rgba(2, 119, 255,   {CellAlpha})'),
    ]

    @staticmethod
    def incrementYearMonth(year, month):
        month += 1
        if month > 12:
            month = 1
            year += 1
        return year, month

    def inStage(self, year, month, stage):
        """Check if a given month year is within a specific life stage."""
        if stage.startYear < year < stage.endYear:
            return True
        elif year == stage.startYear == stage.endYear:
            return stage.startMonth <= month <= stage.endMonth
        elif year == stage.startYear:
            return month >= stage.startMonth
        elif year == stage.endYear:
            return month <= stage.endMonth
        else:
            return False

    def isAlive(self, year, month):
        return (year < self.DeathYear) or \
               (year == self.DeathYear and month <= self.DeathMonth)

    def cellColor(self, year, month):
        """Determine the background color for a month/year table cell"""
        for stage in self.Stages:
            if self.inStage(year, month, stage):
                return stage.color
        return None

    def populate(self):
        thisYear, thisMonth = self.BirthYear, self.BirthMonth
        data = []

        while self.isAlive(thisYear, thisMonth):
            row = []
            # 21 months per row
            for _ in range(21):
                if self.isAlive(thisYear, thisMonth):
                    row.append({
                        'date': f"{str(thisYear)[-2:]}/{thisMonth:02}",
                        'color': self.cellColor(thisYear, thisMonth)
                    })
                    thisYear, thisMonth = self.incrementYearMonth(thisYear, thisMonth)
                else:
                    row.append({'date': '', 'color': None})
            data.append(row)

        return data

    def render2Html(self):
        rows = self.populate()
        template = Template(TABLE_TEMPLATE)
        return template.render(rows=rows)

    def append2Markdown(self, mdFile):
        html = self.render2Html()
        with open(mdFile, 'a') as file:
            file.write('\n\n\n')
            file.write(html)
            file.write('\n\n\n')


if __name__ == "__main__":

    thisPath = os.path.dirname(os.path.abspath(__file__))
    markdown = os.path.join(thisPath, '../docs/docs/home/life-a4.md')

    generator = LifeA4TableGenerator()
    generator.append2Markdown(markdown)

