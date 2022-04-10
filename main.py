import mysql.connector
from scapy.all import *
from scapy.layers.dns import DNS, DNSQR, DNSRR

from scapy.layers.inet import TCP, IP


def InsertDetailsToDatabase(srcIp, srcPort, dstIp, dstPort, transId, Query):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        port=3307,
        database="dns_details"
    )
    my_cursor = mydb.cursor()
    query = 'CREATE TABLE IF NOT EXISTS pcapDnsdetails (src_ip varchar (50),src_port varchar (50), dst_ip varchar (50), dst_port varchar (50),trans_id varchar (50),query varchar (50))'
    my_cursor.execute(query)

    insertQuery = "INSERT INTO pcapDnsdetails(src_ip,src_port,dst_ip,dst_port,trans_id,query) values ( '" + srcIp + "', '" + srcPort + "', '" + dstIp + "', '" + dstPort + "', '" + transId + "', '" + Query + "' )"
    my_cursor.execute(insertQuery)
    mydb.commit()


def Fetch_DNS_Data():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        port=3307,
        database="dns_details"
    )
    my_cursor = mydb.cursor()
    my_cursor.execute('select * from pcapDnsdetails')
    data = my_cursor.fetchall()
    for row in data:
        print(row)


def Extract_DNS_Data(file):
    for packets in file:
        if packets.haslayer(DNS):
            src_port = packets.sport
            dst_port = packets.dport
            domain = packets[DNSQR].qname
            sourceIp = packets[IP].src
            # the domain we extracted from pcap file has its type with it so and we need only domain so we have to
            # cut type
            FullDomain = str(domain)
            final_domain = FullDomain[2:-2]

            # function call to insert valur into database
            InsertDetailsToDatabase(sourceIp, str(src_port), str(packets[IP].dst), str(dst_port), str(packets[IP].id),
                                    str(final_domain))
            Fetch_DNS_Data()


dns_packets = rdpcap('gmail.pcap')
Extract_DNS_Data(dns_packets)
