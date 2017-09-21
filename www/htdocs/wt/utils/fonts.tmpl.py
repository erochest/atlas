
from lap import settings
from lap.web.templates import GlobalTemplate, SubtemplateCode

class main(GlobalTemplate):
    title = 'Fonts'
    _links = settings.links.util

    class page(SubtemplateCode):
        pass

