from dnslib import DNSRecord, QTYPE, RR, A, DNSHeader
from config import HOST, DNS_PORT
import socket
import socketserver

hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)

DOMAIN_TO_IP = {
    'a.com.': local_ip,
    'b.com.': local_ip,
}

class DNSHanlder(socketserver.BaseRequestHandler):

    def handle(self):
        data = self.request[0].strip()
        socket = self.request[1]

        try:
            request = DNSRecord.parse(data)
            print(f"Received request for: {str(request.q.qname)}")

            reply = DNSRecord(DNSHeader(id=request.header.id, qr=1, aa=1, ra=1, q=request.q))

            qname = str(request.q.qname)
            qtype = QTYPE[request.q.qtype]

            if qname in DOMAIN_TO_IP:
                reply.add_answer(RR(qname, QTYPE.A, rdata=A(DOMAIN_TO_IP[qname])))
            else:
                print("Not Availbale")
            socket.sendto(reply.pack(), self.client_address)
        except Exception as e:
            print("Encountered with error", str(e))

if __name__ == '__main__':
    server = socketserver.UDPServer((HOST, DNS_PORT), DNSHanlder)
    print("dns server run!!!")
    server.serve_forever()