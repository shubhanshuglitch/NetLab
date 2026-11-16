from typing import Dict, Any, List, Optional
from pydantic import BaseModel
from backend.app.schemas.packets import ApplicationHeader


class DNSRecord(BaseModel):
    name: str
    record_type: str = "A"
    value: str
    ttl: int = 300


class DNSResolver:
    """
    Simulates recursive and iterative DNS resolution tree.
    """
    def __init__(self):
        # Local cache
        self.cache: Dict[str, DNSRecord] = {}
        
        # Simulated global authoritative zones
        self.zones: Dict[str, List[DNSRecord]] = {
            "google.com": [DNSRecord(name="google.com", record_type="A", value="142.250.190.46", ttl=300)],
            "youtube.com": [DNSRecord(name="youtube.com", record_type="A", value="142.250.190.78", ttl=300)],
            "whatsapp.com": [DNSRecord(name="whatsapp.com", record_type="A", value="157.240.22.53", ttl=300)],
            "github.com": [DNSRecord(name="github.com", record_type="A", value="140.82.112.4", ttl=300)],
            "cdn.youtube.com": [DNSRecord(name="cdn.youtube.com", record_type="CNAME", value="youtube.com", ttl=300)],
        }

    def resolve_domain(self, domain: str) -> Dict[str, Any]:
        """
        Executes resolution steps: Cache check -> Root -> TLD -> Authoritative.
        """
        steps = []
        domain = domain.lower().strip()

        # Step 1: Cache check
        if domain in self.cache:
            rec = self.cache[domain]
            steps.append({
                "step": 1,
                "server": "Local DNS Cache",
                "action": "CACHE_HIT",
                "query": domain,
                "response": rec.value,
                "explanation": f"Domain {domain} resolved instantly from local memory cache (TTL: {rec.ttl}s remaining)."
            })
            return {
                "domain": domain,
                "resolved_ip": rec.value,
                "from_cache": True,
                "steps": steps
            }

        steps.append({
            "step": 1,
            "server": "Local DNS Resolver",
            "action": "CACHE_MISS",
            "query": domain,
            "response": None,
            "explanation": f"Domain {domain} not in local cache. Initiating recursive query to Root DNS Server."
        })

        # Step 2: Root DNS Server
        tld = domain.split(".")[-1]
        steps.append({
            "step": 2,
            "server": "Root DNS Server (a.root-servers.net)",
            "action": "REFERRAL_TLD",
            "query": domain,
            "response": f"Referral to .{tld} TLD Nameservers",
            "explanation": f"Root server doesn't know the exact IP of {domain}, but directs resolver to the .{tld} Top-Level Domain (TLD) servers."
        })

        # Step 3: TLD Nameserver
        domain_sld = ".".join(domain.split(".")[-2:])
        steps.append({
            "step": 3,
            "server": f".{tld} TLD Server",
            "action": "REFERRAL_AUTH",
            "query": domain,
            "response": f"Referral to authoritative nameserver for {domain_sld}",
            "explanation": f".{tld} TLD nameserver directs resolver to authoritative nameservers for {domain_sld}."
        })

        # Step 4: Authoritative Nameserver
        matched_records = self.zones.get(domain, self.zones.get(domain_sld, []))
        if matched_records:
            target_ip = matched_records[0].value
            steps.append({
                "step": 4,
                "server": f"Authoritative DNS Server (ns1.{domain_sld})",
                "action": "ANSWER_A",
                "query": domain,
                "response": f"{domain} -> {target_ip}",
                "explanation": f"Authoritative nameserver contains the master DNS zone record for {domain} and returns IPv4 address {target_ip}."
            })
            # Cache the result
            self.cache[domain] = DNSRecord(name=domain, value=target_ip, ttl=300)
            return {
                "domain": domain,
                "resolved_ip": target_ip,
                "from_cache": False,
                "steps": steps
            }
        else:
            steps.append({
                "step": 4,
                "server": "Authoritative DNS Server",
                "action": "NXDOMAIN",
                "query": domain,
                "response": "NXDOMAIN",
                "explanation": f"Non-Existent Domain (NXDOMAIN): No DNS records found for {domain}."
            })
            return {
                "domain": domain,
                "resolved_ip": None,
                "from_cache": False,
                "steps": steps
            }


def create_dns_query_packet(domain: str, query_type: str = "A") -> ApplicationHeader:
    return ApplicationHeader(
        protocol="DNS",
        message_type="QUERY",
        dns_query_domain=domain,
        dns_record_type=query_type,
        payload=f"Standard DNS query {query_type} for {domain}"
    )


def create_dns_response_packet(domain: str, ip: str) -> ApplicationHeader:
    return ApplicationHeader(
        protocol="DNS",
        message_type="RESPONSE",
        dns_query_domain=domain,
        dns_record_type="A",
        dns_answers=[{"domain": domain, "type": "A", "ip": ip}],
        payload=f"DNS answer: {domain} -> {ip} (TTL 300)"
    )

