%if 0%{?fedora} >= 20 || 0%{?rhel} > 7
%define luaver 5.2
%else
%define luaver 5.1
%endif

%define luacompatver 5.1
%define luacompatlibdir %{_libdir}/lua/%{luacompatver}
%define luacompatpkgdir %{_datadir}/lua/%{luacompatver}
%define lua51dir %{_builddir}/lua51-%{name}-%{version}-%{release}

%global lualibdir %{_libdir}/lua/%{luaver}
%global luapkgdir %{_datadir}/lua/%{luaver}

%global real_name luasec

Name:           lua-sec
Version:        0.5
Release:        3%{?dist}
Summary:        Lua binding for OpenSSL library

Group:          Development/Libraries
License:        MIT
URL:            https://github.com/brunoos/luasec
Source0:        https://github.com/brunoos/luasec/archive/%{real_name}-%{version}.tar.gz
Patch0:         lua-sec-0.4.1-fix-Makefile.patch

BuildRequires:  lua-devel
BuildRequires:  openssl-devel
Requires:       lua-socket
%if 0%{?fedora} >= 16 || 0%{?rhel} >= 7
Requires: lua(abi) = %{luaver}
%else
Requires: lua >= %{luaver}
%endif

%if 0%{?fedora} >= 20
BuildRequires:  compat-lua >= %{luacompatver}, compat-lua-devel >= %{luacompatver}
%endif

%description
Lua binding for OpenSSL library to provide TLS/SSL communication.
It takes an already established TCP connection and creates a secure
session between the peers.

%if 0%{?fedora} >= 20
%package compat
Summary:        Lua 5.1 binding for OpenSSL library
Group:          Development/Libraries

%description compat
Lua 5.1 binding for OpenSSL library to provide TLS/SSL communication.
It takes an already established TCP connection and creates a secure
session between the peers.
%endif

%prep
%setup -q -n %{real_name}-%{real_name}-%{version}
%patch0 -p1 -b .fixMakefile

for file in CHANGELOG LICENSE; do
    iconv -f ISO-8859-1 -t UTF-8 -o $file.new $file && \
    touch -r $file $file.new && \
    mv $file.new $file
done

%if 0%{?fedora} >= 20
rm -rf %{lua51dir}
cp -a . %{lua51dir}
%endif

%build
make %{?_smp_mflags} CFLAGS="$RPM_OPT_FLAGS -fPIC -I. -I%{_includedir} -DWITH_LUASOCKET -DLUASOCKET_DEBUG" \
    LD="gcc -shared" LDFLAGS="-O -fPIC -shared -L./luasocket" \
    linux

%if 0%{?fedora} >= 20
pushd %{lua51dir}
make %{?_smp_mflags} CFLAGS="$RPM_OPT_FLAGS -fPIC -I. -I%{_includedir}/lua-%{luacompatver} -DWITH_LUASOCKET -DLUASOCKET_DEBUG" \
    LD="gcc -shared" LDFLAGS="-O -fPIC -shared -L./luasocket" \
    linux
popd
%endif

%install
mkdir -p $RPM_BUILD_ROOT%{luapkgdir}
mkdir -p $RPM_BUILD_ROOT%{lualibdir}
make install DESTDIR=$RPM_BUILD_ROOT \
    CFLAGS="$RPM_OPT_FLAGS -fPIC -I. -I%{_includedir}/lua-%{luaver} -DWITH_LUASOCKET -DLUASOCKET_DEBUG" \
    LUAPATH=%{luapkgdir} \
    LUACPATH=%{lualibdir}

%if 0%{?fedora} >= 20
pushd %{lua51dir}
mkdir -p $RPM_BUILD_ROOT%{luacompatpkgdir}
mkdir -p $RPM_BUILD_ROOT%{luacompatlibdir}
make install DESTDIR=$RPM_BUILD_ROOT \
    CFLAGS="$RPM_OPT_FLAGS -fPIC -I. -I%{_includedir}/lua-%{luacompatver} -DWITH_LUASOCKET -DLUASOCKET_DEBUG" \
    LUAPATH=%{luacompatpkgdir} \
    LUACPATH=%{luacompatlibdir}
popd
%endif


%files
%defattr(-,root,root,-)
%doc CHANGELOG LICENSE
%{lualibdir}/ssl.so
%{luapkgdir}/ssl.lua
%dir %{luapkgdir}/ssl
%{luapkgdir}/ssl/*

%if 0%{?fedora} >= 20
%files compat
%defattr(-,root,root,-)
%doc CHANGELOG LICENSE
%{luacompatlibdir}/ssl.so
%{luacompatpkgdir}/ssl.lua
%dir %{luacompatpkgdir}/ssl
%{luacompatpkgdir}/ssl/*
%endif

%changelog
* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 14 2014 Jan Kaluza <jkaluza@redhat.com> - 0.5-1
- update to luasec-0.5 (#1000622)
- build -compat subpackage against compat-lua

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun May 12 2013 Tom Callaway <spot@fedoraproject.org> - 0.4.1-5
- rebuild for lua 5.2

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Mar 06 2012 Johan Cwiklinski <johan AT x-tnd DOT be> 0.4.1-2
- Remove __mkdir macros

* Tue Mar 06 2012 Johan Cwiklinski <johan AT x-tnd DOT be> 0.4.1-1
- 0.4.1
- Add lua as a Requires (bz #551763)

* Fri Jan 01 2010 Johan Cwiklinski <johan AT x-tnd DOT be> 0.4-1
- Initial packaging
