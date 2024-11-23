from wroblewshop.domain.cupboard import Cupboard
from wroblewshop.views.home import HomeContext


class TestHomeContext:
    def test_from_domain(self) -> None:
        cupboard = Cupboard(id_=1, name="Palace")

        context = HomeContext.from_domain(cupboard)

        assert context.cupboard_name == "Palace"
