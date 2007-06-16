%define		apxs		/usr/sbin/apxs
Summary:	mod_nss - strong cryptography support for Apache using SSL/TLS library NSS
Summary(pl.UTF-8):	mod_nss - silna kryptografia dla Apache'a przy użyciu biblioteki SSL/TLS NSS
Name:		apache-mod_nss
Version:	1.0.7
Release:	0.1
License:	Apache 2.0
Group:		Networking/Daemons
Source0:	http://directory.fedoraproject.org/sources/mod_nss-%{version}.tar.gz
# Source0-md5:	71107cbc702bf07c6c79843aa92a0e09
URL:		http://directory.fedoraproject.org/wiki/Mod_nss
BuildRequires:	apache-apxs >= 2.0
BuildRequires:	apache-devel >= 2.0
BuildRequires:	apr-devel >= 1:1.0
BuildRequires:	apr-util-devel >= 1:1.0
BuildRequires:	nspr-devel >= 1:4.6.2
BuildRequires:	nss-devel >= 1:3.11.3
Requires:	apache(modules-api) = %{apache_modules_api}
Requires:	nspr >= 1:4.6.2
Requires:	nss >= 1:3.11.3
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR 2>/dev/null)
%define		_sysconfdir	%(%{apxs} -q SYSCONFDIR 2>/dev/null)

%description
An Apache 2.0 module for implementing crypto using the Mozilla NSS
crypto libraries. This supports SSL v3/TLS v1 including support for
client certificate authentication. NSS provides web applications with
a FIPS 140 certified crypto provider and support for a full range of
PKCS#11 devices.

mod_nss is based directly on the mod_ssl package from Apache 2.0.54.
It is a conversion from using OpenSSL calls to using NSS calls
instead.

%description -l pl.UTF-8
Moduł Apache'a 2.0 implementujący kryptografię przy użyciu bibliotek
kryptograficznych Mozilla NSS. Obsługuje SSL v3/TLS v1 wraz z
uwierzytelnianiem z użyciem certyfikatu klienta. NSS zapewnia
aplikacjom WWW dostarczanie kryptografii z certyfikacją FIPS 140 i
obsługę pełnego zakresu urządzeń PKCS#11.

mod_nss jest oparty bezpośrednio na pakiecie mod_ssl z Apache'a
2.0.54, jedynie został zmodyfikowany tak, aby używał wywołań NSS
zamiast OpenSSL.

%prep
%setup -q -n mod_nss-%{version}

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

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_pkglibdir}}

install .libs/libmodnss.so $RPM_BUILD_ROOT%{_pkglibdir}
install nss_pcache $RPM_BUILD_ROOT%{_sbindir}

# TODO: nss.conf -> %{_sysconfdir}/httpd.conf/XX_mod_nss.conf
# (NOTE: at least default config conflicts with mod_ssl)

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc NOTICE README TODO docs/mod_nss.html nss.conf
%attr(755,root,root) %{_pkglibdir}/libmodnss.so
%attr(755,root,root) %{_sbindir}/nss_pcache
