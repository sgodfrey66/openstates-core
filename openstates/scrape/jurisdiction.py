from .base import BaseModel, Scraper
from .schemas.jurisdiction import schema


class Jurisdiction(BaseModel):
    """ Base class for a jurisdiction """

    _type = "jurisdiction"
    _schema = schema

    # schema objects
    classification = None
    name = None
    url = None
    legislative_sessions = []
    feature_flags = []
    extras = {}

    # non-db properties
    scrapers = {}
    default_scrapers = None
    parties = []
    ignored_scraped_sessions = []

    def __init__(self):
        super(BaseModel, self).__init__()
        self._related = []
        self.extras = {}

    @property
    def jurisdiction_id(self):
        return "{}/{}".format(
            self.division_id.replace("ocd-division", "ocd-jurisdiction"),
            self.classification,
        )

    _id = jurisdiction_id

    def as_dict(self):
        return {
            "_id": self.jurisdiction_id,
            "id": self.jurisdiction_id,
            "name": self.name,
            "url": self.url,
            "division_id": self.division_id,
            "classification": self.classification,
            "legislative_sessions": self.legislative_sessions,
            "feature_flags": self.feature_flags,
            "extras": self.extras,
        }

    def __str__(self):
        return self.name

    def get_organizations(self):
        raise NotImplementedError(
            "get_organizations is not implemented"
        )  # pragma: no cover


class JurisdictionScraper(Scraper):
    def scrape(self):
        # yield a single Jurisdiction object
        yield self.jurisdiction

        # yield all organizations
        for org in self.jurisdiction.get_organizations():
            yield org

        if self.jurisdiction.parties:
            raise ValueError("including parties on Jurisdiction is no longer supported")
