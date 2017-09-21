
from lap import settings
from lap.web.templates import GlobalTemplate, SubtemplateCode

class main(GlobalTemplate):
    title = 'About the Projects'
    _links = settings.links.info

    class page(SubtemplateCode):
        pass

