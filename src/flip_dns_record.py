class FlipDNSRecord:
    def __init__(self, client, live, green, blue, target_domain):
        self.client = client
        self.live = self.sanitize_domain(live)
        self.green = self.sanitize_domain(green)
        self.blue = self.sanitize_domain(blue)
        self.target_domain = self.sanitize_domain(target_domain)

    def sanitize_domain(self, domain):
        domain = domain.strip()
        if domain[-1] != '.':
            domain += '.'
        return domain

    def get_non_live_resource(self):
        if self.live == self.green:
            return self.blue
        elif self.live == self.blue:
            return self.green

    def get_resource_record_sets(self):
        zones = self.client.list_hosted_zones_by_name()
        zone_id = zones['HostedZones'][0]['Id']
        return self.client.list_resource_record_sets(HostedZoneId=zone_id)['ResourceRecordSets']


    def build_resource_struct(self):
        new_domain = self.get_non_live_resource()
        resource_records = self.get_resource_record_sets()

        resource = next(
            record for record in resource_records if record['Name'] == self.target_domain
        )

        resource['AliasTarget']['DNSName'] = new_domain

        return resource