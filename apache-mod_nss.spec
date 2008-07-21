# TODO
# - certutil tries to open /dev/tty to get passphrase for nss db init
%define		mod_name	nss
%define		apxs		/usr/sbin/apxs
Summary:	mod_nss - strong cryptography support for Apache using SSL/TLS library NSS
Summary(pl.UTF-8):	mod_nss - silna kryptografia dla Apache'a przy użyciu biblioteki SSL/TLS NSS
Name:		apache-mod_nss
Version:	1.0.8
Release:	0.1
License:	Apache v2.0
Group:		Networking/Daemons
Source0:	http://directory.fedoraproject.org/sources/mod_nss-%{version}.tar.gz
# Source0-md5:	32458d91ce909260a6081cce58004e2f
Source1:	apache-server.crt
Source2:	apache-server.key
Patch0:		%{name}-config.patch
URL:		http://directory.fedoraproject.org/wiki/Mod_nss
BuildRequires:	%{apxs}
BuildRequires:	apache-devel >= 2.0
BuildRequires:	apr-devel >= 1:1.0
BuildRequires:	apr-util-devel >= 1:1.0
BuildRequires:	nspr-devel >= 1:4.6.2
BuildRequires:	nss-devel >= 1:3.11.3
#BuildRequires:	nss-tools
#BuildRequires:	openssl-tools
Requires:	apache(modules-api) = %{apache_modules_api}
Requires:	nspr >= 1:4.6.2
Requires:	nss >= 1:3.11.3
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR 2>/dev/null)
%define		_sysconfdir	%(%{apxs} -q SYSCONFDIR 2>/dev/null)

%description
An Apache 2.x module for implementing crypto using the Mozilla NSS
crypto libraries. This supports SSL v3/TLS v1 including support for
client certificate authentication. NSS provides web applications with
a FIPS 140 certified crypto provider and support for a full range of
PKCS#11 devices.

mod_nss is based directly on the mod_ssl package from Apache 2.0.54.
It is a conversion from using OpenSSL calls to using NSS calls
instead.

%description -l pl.UTF-8
Moduł Apache'a 2.x implementujący kryptografię przy użyciu bibliotek
kryptograficznych Mozilla NSS. Obsługuje SSL v3/TLS v1 wraz z
uwierzytelnianiem z użyciem certyfikatu klienta. NSS zapewnia
aplikacjom WWW dostarczanie kryptografii z certyfikacją FIPS 140 i
obsługę pełnego zakresu urządzeń PKCS#11.

mod_nss jest oparty bezpośrednio na pakiecie mod_ssl z Apache'a
2.0.54, jedynie został zmodyfikowany tak, aby używał wywołań NSS
zamiast OpenSSL.

%prep
%setup -q -n mod_nss-%{version}
%patch0 -p1
cp %{SOURCE1} server.crt
cp %{SOURCE2} server.key

%build
# apr-util is missing in configure check
CPPFLAGS="`apu-1-config --includes`"
%configure \
	--with-apxs=%{apxs} \
	--with-apr-config \
	--with-nspr-inc=/usr/include/nspr \
	--with-nspr-lib=%{_libdir} \
	--with-nss-inc=/usr/include/nss \
	--with-nss-lib=%{_libdir}

%{__make}

install -d nss
# XXX: this is interactive, cannot be done in rpm build process
#certutil -N -d nss
#openssl pkcs12 -export -in server.crt -inkey server.key -out server.p12 -name "Server-Cert" -passout pass:
#pk12util -i server.p12 -d nss -W ''

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_pkglibdir},%{_sysconfdir}/{conf.d,nss}}
install .libs/libmodnss.so $RPM_BUILD_ROOT%{_pkglibdir}
install nss_pcache $RPM_BUILD_ROOT%{_sbindir}

cp -a nss.conf $RPM_BUILD_ROOT%{_sysconfdir}/conf.d/40_mod_%{mod_name}.conf
#cp -a nss/* $RPM_BUILD_ROOT%{_sysconfdir}/nss

%clean
rm -rf $RPM_BUILD_ROOT

%post
%service -q httpd restart

%postun
if [ "$1" = "0" ]; then
	%service -q httpd restart
fi

%files
%defattr(644,root,root,755)
%doc NOTICE README TODO docs/mod_nss.html migrate.pl
%attr(750,root,root) %dir %{_sysconfdir}/nss
#%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/nss/cert8.db
#%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/nss/key3.db
#%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/nss/secmod.db
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/*_mod_%{mod_name}.conf
%attr(755,root,root) %{_pkglibdir}/libmodnss.so
%attr(755,root,root) %{_sbindir}/nss_pcache
