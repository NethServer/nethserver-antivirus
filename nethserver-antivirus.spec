Summary: Integration of Clam AntiVirus for email and filesystem checks.
Name: nethserver-antivirus
Version: 1.1.4
Release: 1%{?dist}
License: GPLv3
URL: %{url_prefix}/%{name} 
Source0: %{name}-%{version}.tar.gz
BuildArch: noarch

Requires: nethserver-base
Requires: clamav-server, clamav-server-systemd
Requires: clamav-unofficial-sigs

BuildRequires: nethserver-devtools


%description
Basic Clam AntiVirus configuration templates.

%prep
%setup

%build
perl createlinks

%installg
rm -rf %{buildroot}
(cd root; find . -depth -print | cpio -dump %{buildroot})
%{genfilelist} %{buildroot} > %{name}-%{version}-filelist

%files -f %{name}-%{version}-filelist
%defattr(-,root,root)
%doc COPYING
%dir %{_nseventsdir}/%{name}-update


%changelog
* Tue Sep 29 2015 Davide Principi <davide.principi@nethesis.it> - 1.1.4-1
- Make Italian language pack optional - Enhancement #3265 [NethServer]

* Tue May 19 2015 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.1.3-1
- Remove SecuriteInfo sigs - Enhancement #3142 [NethServer]
- Optimize clamd limits for performance - Enhancement #3141 [NethServer]

* Thu Mar 05 2015 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.1.2-1
- clamav unofficial sigs whitelist - Enhancement #3033 [NethServer]

* Tue Dec 09 2014 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.1.1-1.ns6
- Support  Sanesecurity Foxhole - Feature #2897 [NethServer]

* Wed Aug 20 2014 Davide Principi <davide.principi@nethesis.it> - 1.1.0-1.ns6
- Antivirus: add support for unofficial sigs - Enhancement #2831 [NethServer]

* Mon Mar 10 2014 Davide Principi <davide.principi@nethesis.it> - 1.0.7-1.ns6
- Antivirus dashboard widget - Enhancement #2686 [NethServer]
- Mail filter: remove clamav warning - Enhancement #2678 [NethServer]

* Wed Feb 05 2014 Davide Principi <davide.principi@nethesis.it> - 1.0.6-1.ns6
- freshclam should be run at least every hour - Bug #2504 [NethServer]

* Mon Sep 02 2013 Davide Principi <davide.principi@nethesis.it> - 1.0.5-1.ns6
- Antivirus: disable syslog messages - Enhancement #2109 [NethServer]
- Upgrade ClamAV to 0.97.8  - Enhancement #2062 [NethServer]

* Tue Jul 30 2013 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.0.4-1.ns6
- Do not save freshclam status on SME db #2035
- Web ui: move antivirus proxy configuration to nethserver-squidclamav package. #1959

* Tue Jun 25 2013 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.0.3-1.ns6
- Remove freshclam mirror checks #1907

* Tue Apr 30 2013 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.0.2-1.ns6
- Rebuild for automatic package handling. #1870

* Tue Mar 19 2013 Davide Principi <davide.principi@nethesis.it> - 1.0.1-1.ns6
- spec file adjustments: use url_prefix macro and fixed Release tag expansion. #1654
