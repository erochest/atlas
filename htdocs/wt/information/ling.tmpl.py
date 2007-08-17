
from lap import settings
from lap.web.templates import GlobalTemplate, SubtemplateCode

class main(GlobalTemplate):
    title = 'About Linguistics'
    _links = settings.links.info

    class page(SubtemplateCode):
        pass

