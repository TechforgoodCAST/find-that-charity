import datetime
import re
from collections import defaultdict

from django.contrib.postgres.indexes import GinIndex
from django.db import models
from django.urls import reverse
from django_better_admin_arrayfield.models.fields import ArrayField

from .organisation_link import OrganisationLink
from .orgid import OrgidField
from .orgid_scheme import OrgidScheme
from .organisation_location import OrganisationLocation

EXTERNAL_LINKS = {
    "GB-CHC": [
        [
            "https://register-of-charities.charitycommission.gov.uk/charity-details/?regId={}&subId=0",
            "Charity Commission England and Wales",
        ],
        ["https://charitybase.uk/charities/{}", "CharityBase"],
        ["http://opencharities.org/charities/{}", "OpenCharities"],
        ["https://givingisgreat.org/charitydetail/?regNo={}", "Giving is Great"],
        [
            "http://www.charitychoice.co.uk/charities/search?t=qsearch&q={}",
            "Charities Direct",
        ],
    ],
    "GB-COH": [
        ["https://beta.companieshouse.gov.uk/company/{}", "Companies House"],
        ["https://opencorporates.com/companies/gb/{}", "Opencorporates"],
    ],
    "GB-NIC": [
        [
            "http://www.charitycommissionni.org.uk/charity-details/?regid={}&subid=0",
            "Charity Commission Northern Ireland",
        ],
        ["https://givingisgreat.org/charitydetail/?regNo={}", "Giving is Great"],
    ],
    "GB-SC": [
        [
            "https://www.oscr.org.uk/about-charities/search-the-register/charity-details?number={}",
            "Office of Scottish Charity Regulator",
        ],
        ["https://givingisgreat.org/charitydetail/?regNo={}", "Giving is Great"],
    ],
    "GB-EDU": [
        [
            "https://get-information-schools.service.gov.uk/Establishments/Establishment/Details/{}",
            "Get information about schools",
        ],
    ],
    "GB-UKPRN": [
        [
            "https://www.ukrlp.co.uk/ukrlp/ukrlp_provider.page_pls_provDetails?x=&pn_p_id={}&pv_status=VERIFIED&pv_vis_code=L",
            "UK Register of Learning Providers",
        ],
    ],
    "GB-NHS": [
        ["https://odsportal.hscic.gov.uk/Organisation/Details/{}", "NHS Digital"],
    ],
    "GB-LAE": [
        [
            "https://www.registers.service.gov.uk/registers/local-authority-eng/records/{}",
            "Local authorities in England",
        ],
    ],
    "GB-LAN": [
        [
            "https://www.registers.service.gov.uk/registers/local-authority-nir/records/{}",
            "Local authorities in Northern Ireland",
        ],
    ],
    "GB-LAS": [
        [
            "https://www.registers.service.gov.uk/registers/local-authority-sct/records/{}",
            "Local authorities in Scotland",
        ],
    ],
    "GB-PLA": [
        [
            "https://www.registers.service.gov.uk/registers/principal-local-authority/records/{}",
            "Principal Local authorities in Wales",
        ],
    ],
    "GB-GOR": [
        [
            "https://www.registers.service.gov.uk/registers/government-organisation/records/{}",
            "Government organisations on GOV.UK",
        ],
    ],
    "XI-GRID": [
        ["https://www.grid.ac/institutes/{}", "Global Research Identifier Database"],
    ],
}


class Organisation(models.Model):
    org_id = OrgidField(db_index=True, verbose_name="Organisation Identifier")
    orgIDs = ArrayField(
        OrgidField(blank=True),
        verbose_name="Other organisation identifiers",
    )
    linked_orgs = ArrayField(
        models.CharField(max_length=100, blank=True),
        blank=True,
        null=True,
        verbose_name="Linked organisations",
    )
    name = models.CharField(max_length=255, verbose_name="Name")
    alternateName = ArrayField(
        models.CharField(max_length=255, blank=True),
        blank=True,
        null=True,
        verbose_name="Other names",
    )
    charityNumber = models.CharField(
        max_length=255, null=True, blank=True, verbose_name="Charity number"
    )
    companyNumber = models.CharField(
        max_length=255, null=True, blank=True, verbose_name="Company number"
    )
    streetAddress = models.CharField(
        max_length=255, null=True, blank=True, verbose_name="Address: street"
    )
    addressLocality = models.CharField(
        max_length=255, null=True, blank=True, verbose_name="Address: locality"
    )
    addressRegion = models.CharField(
        max_length=255, null=True, blank=True, verbose_name="Address: region"
    )
    addressCountry = models.CharField(
        max_length=255, null=True, blank=True, verbose_name="Address: country"
    )
    postalCode = models.CharField(
        max_length=255, null=True, blank=True, verbose_name="Postcode", db_index=True
    )
    telephone = models.CharField(
        max_length=255, null=True, blank=True, verbose_name="Telephone"
    )
    email = models.CharField(
        max_length=255, null=True, blank=True, verbose_name="Email address"
    )
    description = models.TextField(null=True, blank=True, verbose_name="Description")
    url = models.URLField(null=True, blank=True, verbose_name="Website address")
    domain = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        db_index=True,
        verbose_name="Website domain",
    )
    latestIncome = models.BigIntegerField(
        null=True, blank=True, verbose_name="Latest income"
    )
    latestIncomeDate = models.DateField(
        null=True, blank=True, verbose_name="Latest financial year end"
    )
    dateRegistered = models.DateField(
        null=True, blank=True, verbose_name="Date registered"
    )
    dateRemoved = models.DateField(null=True, blank=True, verbose_name="Date removed")
    active = models.BooleanField(null=True, blank=True, verbose_name="Active")
    status = models.CharField(
        max_length=200, null=True, blank=True, verbose_name="Status"
    )
    parent = models.CharField(
        max_length=200, null=True, blank=True, verbose_name="Parent organisation"
    )
    dateModified = models.DateTimeField(
        auto_now=True, verbose_name="Date record was last modified"
    )
    source = models.ForeignKey(
        "Source",
        related_name="organisations",
        on_delete=models.CASCADE,
    )
    organisationType = ArrayField(
        models.CharField(max_length=255, blank=True),
        blank=True,
        null=True,
        verbose_name="Other organisation types",
    )
    organisationTypePrimary = models.ForeignKey(
        "OrganisationType",
        on_delete=models.CASCADE,
        related_name="organisations",
        verbose_name="Primary organisation type",
    )
    scrape = models.ForeignKey(
        "Scrape",
        related_name="organisations",
        on_delete=models.CASCADE,
    )
    spider = models.CharField(max_length=200, db_index=True)
    org_id_scheme = models.ForeignKey(
        "OrgidScheme",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    class Meta:
        unique_together = (
            "org_id",
            "scrape",
        )
        indexes = [
            GinIndex(fields=["orgIDs"]),
            GinIndex(fields=["linked_orgs"]),
            GinIndex(fields=["alternateName"]),
            GinIndex(fields=["organisationType"]),
        ]

    def __str__(self):
        return "%s %s" % (self.organisationTypePrimary.title, self.org_id)

    @property
    def org_links(self):
        return OrganisationLink.objects.filter(
            models.Q(org_id_a=self.org_id) | models.Q(org_id_b=self.org_id)
        )

    def get_priority(self):
        if self.org_id.scheme in OrgidScheme.PRIORITIES:
            prefix_order = OrgidScheme.PRIORITIES.index(self.org_id.scheme)
        else:
            prefix_order = len(OrgidScheme.PRIORITIES) + 1
        return (
            0 if self.active else 1,
            prefix_order,
            self.dateRegistered if self.dateRegistered else datetime.date.min,
        )

    @property
    def all_names(self):
        if self.name is None:
            return self.alternateName
        if self.alternateName is None:
            return [self.name]
        return [self.name] + self.alternateName

    @classmethod
    def get_fields_as_properties(cls):
        internal_fields = ["scrape", "spider", "id"]
        return [
            {"id": f.name, "name": f.verbose_name}
            for f in cls._meta.get_fields()
            if f.name not in internal_fields
        ]

    def schema_dot_org(self, request=None):
        """Return a schema.org Organisation object representing this organisation"""

        obj = {
            "@context": "https://schema.org",
            "@type": "Organization",
            "name": self.name,
            "identifier": self.org_id,
        }

        if self.url:
            obj["url"] = self.url
        if self.description:
            obj["description"] = self.description
        if self.alternateName:
            obj["alternateName"] = self.alternateName
        if self.dateRegistered:
            obj["foundingDate"] = self.dateRegistered.isoformat()
        if not self.active and self.dateRemoved:
            obj["dissolutionDate"] = self.dateRemoved.isoformat()
        if self.orgIDs and len(self.orgIDs) > 1:
            if request:
                obj["sameAs"] = [request.build_absolute_uri(id) for id in self.sameAs]
            else:
                obj["sameAs"] = self.sameAs
        return obj

    def get_links(self):
        if self.url:
            yield (self.cleanUrl, self.displayUrl, self.org_id)
        if not self.orgIDs:
            return
        for o in self.orgIDs:
            links = EXTERNAL_LINKS.get(o.scheme, [])
            for link in links:
                yield (link[0].format(o.id), link[1], o)

    @property
    def sameAs(self):
        return [
            reverse("orgid_html", kwargs=dict(org_id=o))
            for o in self.orgIDs
            if o != self.org_id
        ]

    @property
    def cleanUrl(self):
        if not self.url:
            return None
        if not self.url.startswith("http") and not self.url.startswith("//"):
            return "http://" + self.url
        return self.url

    @property
    def displayUrl(self):
        if not self.url:
            return None
        url = re.sub(r"(https?:)?//", "", self.url)
        if url.startswith("www."):
            url = url[4:]
        if url.endswith("/"):
            url = url[:-1]
        return url

    @property
    def sortedAlternateName(self):
        if not self.alternateName:
            return []
        return sorted(
            self.alternateName,
            key=lambda x: x[4:] if x.lower().startswith("the ") else x,
        )

    def geoCodes(self):

        special_cases = {
            "K02000001": [
                "E92000001",
                "N92000002",
                "S92000003",
                "W92000004",
            ],  # United Kingdom
            # Great Britain
            "K03000001": ["E92000001", "S92000003", "W92000004"],
            "K04000001": ["E92000001", "W92000004"],  # England and Wales
        }

        for v in self.locations.all():
            if re.match("[ENWSK][0-9]{8}", v.geoCode):
                # special case for combinations of countries
                if v.geoCode in special_cases:
                    for a in special_cases[v.geoCode]:
                        yield a
                    continue
                yield v.geoCode

    def locations_group(self):
        locations = defaultdict(lambda: defaultdict(set))

        for v in self.locations.all():
            print(OrganisationLocation.LocationTypes)
            location_type = OrganisationLocation.LocationTypes(v.locationType).label
            if v.geo_laua:
                locations[v.geo_iso][v.geo_laua].add(location_type)
            else:
                locations[v.geo_iso][v.geo_iso].add(location_type)
        return locations
