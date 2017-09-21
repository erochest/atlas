
from lap.web.templates import PopUpTemplate
from lap.web.templates.browse import CommunityCode

class main(PopUpTemplate):
    title = 'Community Information'
    project = 'lamsas'

    class page(CommunityCode):
        pass

