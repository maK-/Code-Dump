import argparse, socket, sys
from struct import *

#Return the formatted ethernet address
def eth_addr (a):
	b = "%.2x:%.2x:%.2x:%.2x:%.2x:%.2x" % (ord(a[0]) , ord(a[1]) , ord(a[2]), ord(a[3]), ord(a[4]) , ord(a[5]))
	return b

#Break down a packet
def disas_packet(packet):
	packet_info = {}
	packet_info['length'] = 14
	packet_info['header'] = packet[:packet_info['length']]
	packet_info['eth'] = unpack('!6s6sH', packet_info['header'])
	packet_info['protocol'] = socket.ntohs(packet_info['eth'][2])
	packet_info['dest_mac'] = eth_addr(packet[0:6])
	packet_info['src_mac'] = eth_addr(packet[6:12])
	return packet_info

#Break down an IP packet
def disas_ip(ip):
	ip_info = {}
	iph = unpack('!BBHHHBBH4s4s' , ip)
	ip_info['version_ihl'] = iph[0]
	ip_info['version'] = ip_info['version_ihl'] >> 4
	ip_info['ihl'] = ip_info['version_ihl'] & 0xF
	ip_info['length'] = ip_info['ihl'] * 4
	ip_info['ttl'] = iph[5]
	ip_info['protocol'] = iph[6]
	ip_info['src_addr'] = socket.inet_ntoa(iph[8]);
	ip_info['dest_addr'] = socket.inet_ntoa(iph[9]);
	return ip_info

#breaking down a tcp packet
def disas_tcp(tcp):
	tcp_info = {}
	tcph = unpack('!HHLLBBHHH' , tcp)
	tcp_info['src_port'] = tcph[0]
	tcp_info['dest_port'] = tcph[1]
	tcp_info['sequence'] = tcph[2]
	tcp_info['ack'] = tcph[3]
	tcp_info['doff_res'] = tcph[4]
	tcp_info['length'] = tcp_info['doff_res'] >> 4
	return tcp_info

def scan(dest_Address):
	#variable to decide which format the binary is displayed
	is_exe = False

	#create a AF_PACKET type raw socket
	#define ETH_P_ALL    0x0003  
	try:
		s = socket.socket( socket.AF_PACKET , socket.SOCK_RAW , socket.ntohs(0x0003))
	except socket.error , msg:
		print 'Socket could not be created. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
		sys.exit()

	# receive a packet
	while True:
		packet = s.recvfrom(65565)
		packet = packet[0]
		this_eth = disas_packet(packet)	
		
		#IP Protocol number = 8
		if this_eth['protocol'] == 8 :
			#Parse IP header.
			end_ip = this_eth['length']+20
			ip = packet[this_eth['length']:end_ip]
			this_ip = disas_ip(ip)
						
			#TCP protocol = 6
			if this_ip['protocol'] == 6:
				#print packet transfer information
				print '\n\033[37mVersion: '+str(this_ip['version'])+' IP Header Length: '+str(this_ip['ihl'])+' TTL: '+str(this_ip['ttl'])+' Protocol: '+str(this_ip['protocol'])+' Source Address: '+str(this_ip['src_addr'])+' Destination Address: '+str(this_ip['dest_addr'])+'\033[0m'
				t = this_ip['length'] + this_eth['length']
				tcp = packet[t:t+20]
				this_tcp = disas_tcp(tcp)
				
				print '\033[31mSource Port : ' + str(this_tcp['src_port']) + ' Dest Port : ' + str(this_tcp['dest_port']) + ' Sequence Number : ' + str(this_tcp['sequence']) + ' Acknowledgement : ' + str(this_tcp['ack']) + ' TCP header length : ' + str(this_tcp['length'])+'\033[0m'
			
				head_size = this_eth['length'] + this_ip['length'] + this_tcp['length'] * 4
				data_size = len(packet) - head_size
			
				#get data from the packet
				data = packet[head_size:]
				#print data+'\n\n'		
			
			#some other IP packet like IGMP
			else :
				continue

def main():
	arg = argparse.ArgumentParser(description='A simple tool for injecting shellcode into exe binaries on the network.')
	arg.add_argument('-sc', dest='SHELLCODE', type=str, help='Shellcode to be injected.')
	arg.add_argument('-s', dest='SOURCE', type=str, help='Source of exe in packet transfer.')
	arg.add_argument('-d', dest='DESTINATION', type=str, help='Destination of packet transer.')
	args = arg.parse_args()
	scan(args.DESTINATION)

if __name__ == '__main__':
	main()
