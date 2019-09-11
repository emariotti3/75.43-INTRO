import dns.resolver

def resolve(query):
	return dns.resolver.query(query)
