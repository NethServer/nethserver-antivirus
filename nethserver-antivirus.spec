Summary: Integration of Clam AntiVirus for email and filesystem checks.
Name: nethserver-antivirus
Version: 1.5.2
Release: 1%{?dist}
License: GPLv3
URL: %{url_prefix}/%{name} 
Source0: %{name}-%{version}.tar.gz
Source1: %{name}-cockpit.tar.gz
BuildArch: noarch

Requires: nethserver-base
Requires: clamd
Requires: clamav-unofficial-sigs
Obsoletes: clamav-data

BuildRequires: nethserver-devtools


%description
Basic Clam AntiVirus configuration templates.

%prep
%setup

%build
perl createlinks
sed -i 's/_RELEASE_/%{version}/' %{name}.json

%install
rm -rf %{buildroot}
(cd root; find . -depth -print | cpio -dump %{buildroot})

mkdir -p %{buildroot}/usr/share/cockpit/%{name}/
mkdir -p %{buildroot}/usr/share/cockpit/nethserver/applications/
mkdir -p %{buildroot}/usr/libexec/nethserver/api/%{name}/
tar xvf %{SOURCE1} -C %{buildroot}/usr/share/cockpit/%{name}/
cp -a %{name}.json %{buildroot}/usr/share/cockpit/nethserver/applications/
cp -a api/* %{buildroot}/usr/libexec/nethserver/api/%{name}/

%{genfilelist} %{buildroot} \
    --file /etc/sudoers.d/50_nsapi_nethserver_antivirus 'attr(0440,root,root)' \
 > %{name}-%{version}-filelist

%files -f %{name}-%{version}-filelist
%defattr(-,root,root)
%doc COPYING
%dir %{_nseventsdir}/%{name}-update


%changelog
* Mon Mar 14 2022 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.5.2-1
- Clamd@rspamd in failed state after mail application removal - Bug NethServer/dev#6647

* Thu Jul 02 2020 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.5.1-1
- Human readable numbers in Cockpit dashboards - NethServer/dev#6206

* Wed Apr 08 2020 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.5.0-1
- Clamav official signatures uploaded even if disabled on old installations - Bug NethServer/dev#6113

* Wed Jan 08 2020 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.4.2-1
- Cockpit: change package Dashboard page title - NethServer/dev#6004

* Mon Oct 28 2019 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.4.1-1
- Logs page in Cockpit - Bug NethServer/dev#5866

* Tue Oct 01 2019 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.4.0-1
- New NethServer 7.7.1908 defaults - NethServer/dev#5831
- Antivirus Cockpit UI - NethServer/dev#5836
- Sudoers based authorizations for Cockpit UI - NethServer/dev#5805

* Thu Sep 12 2019 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.3.1-1
- Increate start timeout to 8 minutes - NethServer/dev#5803

* Fri Aug 30 2019 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.3.0-1
- Antivirus: improve memory usage - NethServer/dev#5803

* Tue Mar 12 2019 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.2.2-1
- ClamAV database doesn't get updated behind manual proxy - NethServer/dev#5727
- Requires only clamd package

* Fri Mar 03 2017 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.2.1-1
- clamav-data-empty conflicts clamav-data - Bug NethServer/dev#5223

* Thu Jul 07 2016 Stefano Fancello <stefano.fancello@nethesis.it> - 1.2.0-1
- First NS7 release

* Thu Feb 18 2016 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.1.5-1
- Update to clamav-0.99 + extra sigs - Enhancement #3349 [NethServer]
- Dashboard antivirus update status - Enhancement #3340 [NethServer]

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
