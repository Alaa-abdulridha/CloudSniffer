import unittest
from cloud_sniffer import CloudSniffer

# To be modified as seen fit
# This is not reliable unit test as the tool doesn't provide accurate results 100%
# This is for anyone want to take the tool to next level or to implement it into bigger framework.
class TestCloudSniffer(unittest.TestCase):

    def setUp(self):
        # Initialize CloudSniffer with example domain and IP file
        self.domain = 'example.com'
        self.ip_file = 'example_ips.txt'
        self.sniffer = CloudSniffer(self.domain, self.ip_file)

    def test_sniff_real_ip(self):
        # Test if CloudSniffer can detect the real IP address
        real_ip = '123.456.789.0'
        self.sniffer.sniff_ip(real_ip)
        self.assertEqual(self.sniffer.get_real_ip(), real_ip)

    def test_sniff_redirect(self):
        # Test if CloudSniffer can detect a redirect
        redirect_ip = '987.654.321.0'
        self.sniffer.sniff_ip(redirect_ip)
        self.assertIn(redirect_ip, self.sniffer.get_possible_ips())

    def test_no_ip_found(self):
        # Test if CloudSniffer handles the case when no IP is found
        self.assertEqual(self.sniffer.get_real_ip(), None)
        self.assertEqual(self.sniffer.get_possible_ips(), [])

if __name__ == '__main__':
    unittest.main()
