from django.http import HttpResponse
from django.shortcuts import render
import dns.resolver
import ipaddress

# Create your views here.

# Lista przykładowych publicznych DNS-ów z różnych krajów (można dodać więcej)
DNS_SERVERS = {
    'Google (US)': '8.8.8.8',
    'Cloudflare (Global)': '1.1.1.1',
    'OpenDNS (US)': '208.67.222.222',
    'Quad9 (EU)': '9.9.9.9',
    'Level3 (US)': '4.2.2.1',
}

def ip(request):
    # Pobierz IP klienta
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    client_ip = x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')

    domain = ''
    dns_results = {}
    ip_calc = None

    if request.method == 'POST':
        domain = request.POST.get('domain', '').strip()
        cidr_input = request.POST.get('cidr', '').strip()

        if domain:
            for name, dns_server in DNS_SERVERS.items():
                resolver = dns.resolver.Resolver()
                resolver.nameservers = [dns_server]
                try:
                    result = resolver.resolve(domain, 'A', lifetime=3)
                    ip_list = [r.to_text() for r in result]
                    dns_results[name] = ip_list
                except Exception as e:
                    dns_results[name] = [f"Error: {str(e)}"]

        if cidr_input:
            try:
                network = ipaddress.IPv4Network(cidr_input, strict=False)
                ip_calc = {
                    'network': str(network.network_address),
                    'netmask': str(network.netmask),
                    'broadcast': str(network.broadcast_address),
                    'host_min': str(list(network.hosts())[0]),
                    'host_max': str(list(network.hosts())[-1]),
                    'hosts': network.num_addresses - 2 if network.num_addresses > 2 else 0,
                }
            except Exception as e:
                ip_calc = {'error': f"Error: {str(e)}"}

    return render(request, "ip.html", {
        'ip': client_ip,
        'domain': domain,
        'dns_results': dns_results,
        'ip_calc': ip_calc,
    })

def home(request ,*arg, **kwargs):
	print(arg, kwargs)
	print(request.user)
	return render(request ,"home.html", {})

    #return HttpResponse("home")

