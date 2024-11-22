import dns.immutable
import dns.rdtypes.dnskeybase
from dns.rdtypes.dnskeybase import REVOKE, SEP, ZONE

class CDNSKEY(dns.rdtypes.dnskeybase.DNSKEYBase):
    """CDNSKEY record"""