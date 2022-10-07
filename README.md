# Selection of Security Solutions

This repository contains scripts that support selection of security monitoring solutions. The selection procedure relies on manual assessments of attack techniques, solutions, and organizations. These assessments are provided in the CSV files ``techniques.txt``, ``solutions.txt``, and ``organizations.txt`` respectively. The main idea of our approach is to (i) assess which assets are relevant to be protected in each organization, (ii) determine which attack techniques exist for these assets, (iii) obtain a list of security solutions that mitigate these attack techniques, (iv) assess the solutions with respect to requirements (e.g., cost, complexity) of the organizations, (v) identify which combinations of solutions provide added value, and (vi) aggregate all aformentioned properties to provide a ranking of security solutions for each organization. See the paper referenced in the bottom of this page for a more detailed description.

The example provided in this repository uses Office 365 as the main asset of three organizations: Organization A is a micro organization with a small budget and interest in finding an easy-to-deploy solution. Organization B is a medium-sized organization with little constraints regarding cost and complexity of solutions. Organization C has clear preferences regarding cost and complexity. We consider five commercial security solutions: Microsoft Defender for Office 365 (MDO) is a low-cost Microsoft product specifically designed to protect Office 365 against phishing, malware, spam, etc, Microsoft 365 Enterprise Mobility + Security E5 (MEMS) is a product for endpoint management and protection, Microsoft 365 E5 (ME) is a more advanced version of MEMS offering additional security applications, Azure Sentinel (AS) is yet another Microsoft product for Log Analytics, and Elastic Security Solution (ESS) is a cloud-based storage and analysis engine leveraging pre-defined rules for threat detection. 

Run the following script to obtain the top 6 solutions for each organization. The value next to the combination of solutions shows the normalized score, where higher values indicate that the solutions are more suitable to fulfill the needs of the respective organization.

```bash
user@ubuntu:~$ git clone https://github.com/d3tect/d3tect-solutions.git
user@ubuntu:~$ cd d3tect-solutions/
user@ubuntu:~/d3tect-solutions$ python3 assess_combos.py
Recommended solutions for organization A:
 * MDO: 0.216
 * MDO+AS: 0.089
 * MDO+MEMS: 0.078
 * AS: 0.069
 * MDO+AS+MEMS: 0.062
 * MDO+ESS: 0.049

Recommended solutions for organization B:
 * MDO+AS+MEMS: 0.667
 * MDO+ME+AS: 0.618
 * MDO+ESS+AS: 0.608
 * MDO+ESS+AS+MEMS: 0.604
 * MDO+AS: 0.588
 * MDO+ESS+MEMS: 0.582

Recommended solutions for organization C:
 * MDO+AS: 0.276
 * MDO+MEMS: 0.263
 * AS: 0.227
 * MDO: 0.216
 * MDO+ESS: 0.205
 * MDO+AS+MEMS: 0.169
```

If you use any of the scripts provided in this repository, please cite the following publication:
 * A logging maturity and decision model for the selection of detective cyber security solutions. Under review.
