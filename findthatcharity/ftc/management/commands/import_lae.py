import datetime

from ftc.management.commands._base_scraper import AREA_TYPES, CSVScraper
from ftc.models import Organisation


class Command(CSVScraper):
    name = 'lae'
    allowed_domains = ['register.gov.uk']
    start_urls = [
        "https://local-authority-eng.register.gov.uk/records.csv?page-size=5000"
    ]
    org_id_prefix = "GB-LAE"
    id_field = "key"
    date_fields = ["entry-timestamp", "start-date", "end-date"]
    date_format = {
        "entry-timestamp": "%Y-%m-%dT%H:%M:%SZ",
        "start-date": "%Y-%m-%d",
        "end-date": "%Y-%m-%d",
    }
    source = {
        "title": "Local authorities in England register",
        "description": "Local authorities in England",
        "identifier": "lae",
        "license": "http://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/",
        "license_name": "Open Government Licence v3.0",
        "issued": "",
        "modified": "",
        "publisher": {
            "name": "Ministry of Housing, Communities and Local Government",
            "website": "https://www.gov.uk/government/organisations/ministry-of-housing-communities-and-local-government",
        },
        "distribution": [
            {
                "downloadURL": "",
                "accessURL": "https://www.registers.service.gov.uk/registers/local-authority-eng/",
                "title": "Local authorities in England register"
            }
        ],
    }
    orgtypes = ['Local Authority']

    def parse_row(self, record):

        record = self.clean_fields(record)
        org_types = [
            self.orgtype_cache["local-authority"],
        ]

        if record.get('local-authority-type'):
            org_types.append(
                self.add_org_type(LA_TYPES.get(record.get(
                "local-authority-type"), record.get("local-authority-type")))
            )
        org_ids = [self.get_org_id(record)]

        locations = []
        gss = LA_LOOKUP.get(record.get(self.id_field))
        if gss:
            locations.append({
                "id": gss,
                "name": record.get("name"),
                "geoCode": gss,
                "geoCodeType": AREA_TYPES.get(gss[0:3], "Local Authority"),
            })

        self.records.append(
            Organisation(**{
                "org_id": self.get_org_id(record),
                "name": record.get("official-name"),
                "charityNumber": None,
                "companyNumber": None,
                "streetAddress": None,
                "addressLocality": None,
                "addressRegion": None,
                "addressCountry": "England",
                "postalCode": None,
                "telephone": None,
                "alternateName": [],
                "email": None,
                "description": None,
                "organisationType": [o.slug for o in org_types],
                "organisationTypePrimary": org_types[0],
                "url": None,
                "location": locations,
                "latestIncome": None,
                "dateModified": datetime.datetime.now(),
                "dateRegistered": record.get("start-date"),
                "dateRemoved": record.get("end-date"),
                "active": record.get("end-date") is None,
                "parent": None,
                "orgIDs": org_ids,
                "scrape": self.scrape,
                "source": self.source,
                "spider": self.name,
                "org_id_scheme": self.orgid_scheme,
            })
        )

LA_TYPES = {
    "BGH": "Borough",
    "CIT": "City",
    "CC": "City corporation",
    "CA": "Council area",
    "CTY": "County",
    "DIS": "District",
    "LBO": "London borough",
    "MD": "Metropolitan district",
    "NMD": "Non-metropolitan district",
    "SRA": "Strategic Regional Authority",
    "UA": "Unitary authority",
    "COMB": "Combined authority",
}

# @TODO: I don't think this list is up to date
LA_LOOKUP = {
    'ADU': 'E07000223',
    'ARU': 'E07000224',
    'ASH': 'E07000170',
    'ASF': 'E07000105',
    'BAB': 'E07000200',
    'BNS': 'E08000016',
    'BAR': 'E07000027',
    'BAI': 'E07000066',
    'BAE': 'E07000171',
    'BIR': 'E08000025',
    'BPL': 'E06000009',
    'BOS': 'E07000033',
    'BOL': 'E08000001',
    'POL': 'E06000029',
    'BMH': 'E06000028',
    'BRC': 'E06000036',
    'BRW': 'E07000068',
    'BNH': 'E06000043',
    'BST': 'E06000023',
    'BRT': 'E07000172',
    'BUR': 'E08000002',
    'CAB': 'E07000008',
    'CAN': 'E07000192',
    'CAT': 'E07000106',
    'CAS': 'E07000069',
    'CBF': 'E06000056',
    'CHA': 'E07000130',
    'CHT': 'E07000078',
    'CHR': 'E07000177',
    'CHW': 'E06000050',
    'CHS': 'E07000034',
    'CHO': 'E07000118',
    'BRD': 'E08000032',
    'LIC': 'E07000138',
    'LND': 'E09000001',
    'WKF': 'E08000036',
    'WSM': 'E09000033',
    'YOR': 'E06000014',
    'COL': 'E07000071',
    'COR': 'E07000150',
    'CON': 'E06000052',
    'IOS': 'E06000053',
    'CRA': 'E07000163',
    'CRW': 'E07000226',
    'DAC': 'E07000096',
    'DAL': 'E06000005',
    'DAR': 'E07000107',
    'DER': 'E06000015',
    'DNC': 'E08000017',
    'DOV': 'E07000108',
    'DUD': 'E08000027',
    'DUR': 'E06000047',
    'EDE': 'E07000040',
    'EHE': 'E07000097',
    'ERY': 'E06000011',
    'EAS': 'E07000061',
    'EPP': 'E07000072',
    'EXE': 'E07000041',
    'FAR': 'E07000087',
    'FOR': 'E07000201',
    'GAT': 'E08000037',
    'GLO': 'E07000081',
    'GOS': 'E07000088',
    'GRA': 'E07000109',
    'GRY': 'E07000145',
    'GRT': 'E07000209',
    'HRY': 'E09000014',
    'HAR': 'E07000073',
    'HAG': 'E07000165',
    'HPL': 'E06000001',
    'HIG': 'E07000037',
    'HIN': 'E07000132',
    'IPS': 'E07000202',
    'KET': 'E07000153',
    'KHL': 'E06000010',
    'KIR': 'E08000034',
    'LAC': 'E07000121',
    'LDS': 'E08000035',
    'LCE': 'E06000016',
    'LEE': 'E07000063',
    'BDG': 'E09000002',
    'BNE': 'E09000003',
    'BEX': 'E09000004',
    'BEN': 'E09000005',
    'CMD': 'E09000007',
    'CRY': 'E09000008',
    'EAL': 'E09000009',
    'ENF': 'E09000010',
    'GRE': 'E09000011',
    'HCK': 'E09000012',
    'HMF': 'E09000013',
    'HRW': 'E09000015',
    'HAV': 'E09000016',
    'HIL': 'E09000017',
    'HNS': 'E09000018',
    'ISL': 'E09000019',
    'LBH': 'E09000022',
    'LEW': 'E09000023',
    'MRT': 'E09000024',
    'NWM': 'E09000025',
    'RDB': 'E09000026',
    'STN': 'E09000029',
    'TWH': 'E09000030',
    'WFT': 'E09000031',
    'WND': 'E09000032',
    'LUT': 'E06000032',
    'MAI': 'E07000110',
    'MAN': 'E08000003',
    'MAS': 'E07000174',
    'MDW': 'E06000035',
    'MEL': 'E07000133',
    'MDE': 'E07000042',
    'MSU': 'E07000203',
    'MDB': 'E06000002',
    'MIK': 'E06000042',
    'MOL': 'E07000210',
    'NEW': 'E07000091',
    'NEA': 'E07000175',
    'NET': 'E08000021',
    'NED': 'E07000038',
    'NKE': 'E07000139',
    'NSM': 'E06000024',
    'NTY': 'E08000022',
    'NWA': 'E07000218',
    'NWL': 'E07000134',
    'NOR': 'E07000154',
    'NBL': 'E06000057',
    'NOW': 'E07000148',
    'NGM': 'E06000018',
    'NUN': 'E07000219',
    'OAD': 'E07000135',
    'OLD': 'E08000004',
    'OXO': 'E07000178',
    'POR': 'E06000044',
    'RDG': 'E06000038',
    'RED': 'E07000236',
    'RIB': 'E07000124',
    'RIH': 'E07000166',
    'RCH': 'E08000005',
    'ROS': 'E07000125',
    'ROT': 'E08000018',
    'KEC': 'E09000020',
    'KTT': 'E09000021',
    'RUG': 'E07000220',
    'RUN': 'E07000212',
    'RYE': 'E07000167',
    'SLF': 'E08000006',
    'SAW': 'E08000028',
    'SEG': 'E07000188',
    'SEL': 'E07000169',
    'SHF': 'E08000019',
    'SHE': 'E07000112',
    'SHR': 'E06000051',
    'SLG': 'E06000039',
    'SOL': 'E08000029',
    'SCA': 'E07000012',
    'SDE': 'E07000039',
    'SHO': 'E07000140',
    'SKE': 'E07000141',
    'SLA': 'E07000031',
    'STY': 'E08000023',
    'STH': 'E06000045',
    'SOS': 'E06000033',
    'SWK': 'E09000028',
    'SAL': 'E07000100',
    'STV': 'E07000101',
    'SKP': 'E08000007',
    'STT': 'E06000004',
    'STE': 'E06000021',
    'STO': 'E07000082',
    'SUF': 'E07000205',
    'SWD': 'E06000030',
    'TAW': 'E07000199',
    'TAN': 'E07000215',
    'TAU': 'E07000190',
    'TEI': 'E07000045',
    'TEN': 'E07000076',
    'THA': 'E07000114',
    'THR': 'E06000034',
    'TON': 'E07000115',
    'UTT': 'E07000077',
    'WRT': 'E06000007',
    'WAW': 'E07000222',
    'WAT': 'E07000103',
    'WAV': 'E07000206',
    'WAE': 'E07000216',
    'WEA': 'E07000065',
    'WEW': 'E07000104',
    'WBK': 'E06000037',
    'WLA': 'E07000127',
    'WGN': 'E08000010',
    'WIL': 'E06000054',
    'WIN': 'E07000094',
    'WRL': 'E08000015',
    'WOI': 'E07000217',
    'WOK': 'E06000041',
    'WLV': 'E08000031',
    'WYO': 'E07000007',
}
