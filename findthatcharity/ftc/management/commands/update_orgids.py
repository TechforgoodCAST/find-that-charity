import logging

from django.db import connection
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):

    update_sql = """
    update ftc_organisation o
    set "linked_orgs" = a.linked_orgs
    from (
        WITH RECURSIVE search_graph(org_id_a, org_id_b) AS (
                SELECT a.org_id_a, a.org_id_b
                FROM ftc_linkedorganisation a
            union
                SELECT sg.org_id_a, a.org_id_b
                FROM ftc_linkedorganisation a
                    inner JOIN search_graph sg
                        ON a.org_id_a = sg.org_id_b
        )
        SELECT org_id_a as "org_id",
            array_agg(org_id_b ORDER BY org_id_b ASC) as linked_orgs
        FROM search_graph
        group by org_id_a
    ) as a
    where a.org_id = o.org_id;
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = logging.getLogger(__name__)

    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            self.logger.info("Starting SQL to update orgIDs")
            cursor.execute(self.update_sql)
            self.logger.info("Finished SQL to update orgIDs")
