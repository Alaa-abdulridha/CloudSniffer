# CloudSniffer

CloudSniffer is a powerful tool designed to assist in the discovery of the real IP address of a website protected by Cloudflare. By leveraging brute force techniques and analyzing server responses, CloudSniffer aims to uncover the actual IP address of the target website.

**Disclaimer: CloudSniffer should be used responsibly and with proper authorization and legal rights. It is intended for educational and research purposes only. Unauthorized use of this tool is strictly prohibited.**

## Features

- **Brute Force Testing:** CloudSniffer systematically tests a list of IP addresses to identify the real IP address of a website.
- **Status Code Analysis:** It analyzes the status codes returned by the server to determine potential matches for the real IP address.
- **HTTP and HTTPS Support:** CloudSniffer works with both HTTP and HTTPS protocols, enabling comprehensive testing across different security configurations.
- **Redirection Detection:** It identifies cases where the server responds with a redirect, indicating a possible match for the real IP address.
- **Aggressive Mode:** With the `--aggressive` option, CloudSniffer performs more intensive checks by testing additional paths like `/robots.txt`, `/license.txt`, and `/README.md`.
- **User Agent Rotation:** CloudSniffer supports using different user agents for each request, increasing the chances of bypassing certain protections.

## Requirements

- Python 3.6+
- Operating Systems:
  - Windows
  - macOS
  - Linux

CloudSniffer requires Python 3.6 or higher to run. It is compatible with major operating systems, including Windows, macOS, and Linux.

Please ensure that you have Python 3.6 or a later version installed on your system before using CloudSniffer.

Note: Some features or functionality of CloudSniffer may vary across different operating systems.


## Installation

1. Clone the CloudSniffer repository:

   ```shell
   git clone https://github.com/Alaa-abdulridha/CloudSniffer.git
   ```
   Navigate to the cloned directory:
   
   ```
   cd CloudSniffer
   ```
   Install the required dependencies:
   
   ```
   pip install -r requirements.txt
   ```
   
   ## Usage
   
   Run CloudSniffer with the desired options:
   
   ```
   python CloudSniffer.py domain ipfile [--trace] [--cleandns] [--useragents uafile] [--timeout seconds] [--aggressive]
   
   ```
   `domain`: The domain or subdomain to test.
   `ipfile`: The file containing the list of IP addresses to test against.
   `--trace`: Activate the trace file to record the results (optional).
   `--cleandns`: Clean the DNS cache after every hosts file change (optional).
   `--useragents uafile`: The file containing the list of user agents (optional).
   `--timeout seconds`: The timeout for each request in seconds (optional, default: 5).
   `--aggressive`: Perform more intensive checks (optional).
   
   Review the results displayed in the console. CloudSniffer will attempt to find the real IP address of the domain and provide potential matches based on the observed responses.
   
   ## Contribution
   
   Contributions to CloudSniffer are welcome! If you have any ideas, suggestions, or encounter any issues, please feel free to open an issue on the GitHub repository. You can also contribute by creating a pull request with your proposed changes.
   
   ## License
   
   CloudSniffer is licensed under the MIT License. See the LICENSE file for details.
   
   # Please note that CloudSniffer is intended for educational and research purposes only. Use it responsibly and ensure you have the necessary permissions and legal rights to perform such tests. Unauthorized use of this tool is strictly prohibited.
   
   
   
