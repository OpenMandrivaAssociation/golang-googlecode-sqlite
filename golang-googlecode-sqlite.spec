%if 0%{?fedora} || 0%{?rhel} == 6
%global with_devel 1
%global with_bundled 0
%global with_debug 0
%global with_check 0
# No tests provided
%global with_unit_test 0
%else
%global with_devel 0
%global with_bundled 0
%global with_debug 0
%global with_check 0
%global with_unit_test 0
%endif

%if 0%{?with_debug}
%global _dwz_low_mem_die_limit 0
%else
%global debug_package   %{nil}
%endif

%define copying() \
%if 0%{?fedora} >= 21 || 0%{?rhel} >= 7 \
%license %{*} \
%else \
%doc %{*} \
%endif

%global provider        google
%global provider_sub    code
%global provider_tld    com
%global project         p
%global repo            gosqlite
%global rrepo           gosqlite
# https://code.google.com/p/gosqlite
%global provider_prefix %{provider_sub}.%{provider}.%{provider_tld}/%{project}/%{repo}
%global import_path     %{provider_prefix}
%global rev             74691fb6f83716190870cde1b658538dd4b18eb0
%global shortrev        %(c=%{rev}; echo ${c:0:12})

Name:           golang-%{provider}%{provider_sub}-sqlite
Version:        0
Release:        0.23.hg%{shortrev}%{?dist}
Summary:        Trivial sqlite3 binding for Go
License:        BSD
URL:            https://%{provider_prefix}
Source0:        https://%{rrepo}.%{provider}%{provider_sub}.%{provider_tld}/archive/%{rev}.zip
Source1:        LICENSE-BSD3-Go

# If go_arches not defined fall through to implicit golang archs
%if 0%{?go_arches:1}
ExclusiveArch:  %{go_arches}
%else
ExclusiveArch:   %{ix86} x86_64 %{arm}
%endif
# If gccgo_arches does not fit or is not defined fall through to golang
%ifarch 0%{?gccgo_arches}
BuildRequires:   gcc-go >= %{gccgo_min_vers}
%else
BuildRequires:   golang
%endif

%description
%{summary}

This package has no exported API. It registers a driver for the standard Go
database/SQL package.

%if 0%{?with_devel}
%package devel
Summary:       %{summary}
BuildArch:     noarch

%if 0%{?with_check}
%endif

Requires:       sqlite-devel

Provides:      golang(%{import_path}) = %{version}-%{release}
Provides:      golang(%{import_path}/sqlite) = %{version}-%{release}
Provides:      golang(%{import_path}/sqlite3) = %{version}-%{release}

%description devel
%{summary}

This package has no exported API. It registers a driver for the standard Go
database/SQL package.

This package contains library source intended for
building other packages which use import path with
%{import_path} prefix.
%endif

%if 0%{?with_unit_test}
%package unit-test
Summary:         Unit tests for %{name} package
# If go_arches not defined fall through to implicit golang archs
%if 0%{?go_arches:1}
ExclusiveArch:  %{go_arches}
%else
ExclusiveArch:   %{ix86} x86_64 %{arm}
%endif
# If gccgo_arches does not fit or is not defined fall through to golang
%ifarch 0%{?gccgo_arches}
BuildRequires:   gcc-go >= %{gccgo_min_vers}
%else
BuildRequires:   golang
%endif

%if 0%{?with_check}
#Here comes all BuildRequires: PACKAGE the unit tests
#in %%check section need for running
%endif

# test subpackage tests code from devel subpackage
Requires:        %{name}-devel = %{version}-%{release}

%description unit-test
%{summary}

This package contains unit tests for project
providing packages with %{import_path} prefix.
%endif

%prep
%setup -q -n %{rrepo}-%{shortrev}

%build
# Requested upstream to include LICENSE
# http://code.google.com/p/gosqlite/issues/detail?id=21
cp %{SOURCE1} ./LICENSE

%install
# source codes for building projects
%if 0%{?with_devel}
install -d -p %{buildroot}/%{gopath}/src/%{import_path}/
# find all *.go but no *_test.go files and generate devel.file-list
for file in $(find . -iname "*.go" \! -iname "*_test.go") ; do
    install -d -p %{buildroot}/%{gopath}/src/%{import_path}/$(dirname $file)
    cp -pav $file %{buildroot}/%{gopath}/src/%{import_path}/$file
    echo "%%{gopath}/src/%%{import_path}/$file" >> devel.file-list
done
%endif

# testing files for this project
%if 0%{?with_unit_test}
install -d -p %{buildroot}/%{gopath}/src/%{import_path}/
# find all *_test.go files and generate unit-test.file-list
for file in $(find . -iname "*_test.go"); do
    install -d -p %{buildroot}/%{gopath}/src/%{import_path}/$(dirname $file)
    cp -pav $file %{buildroot}/%{gopath}/src/%{import_path}/$file
    echo "%%{gopath}/src/%%{import_path}/$file" >> unit-test.file-list
done
%endif

%check
%if 0%{?with_check} && 0%{?with_unit_test} && 0%{?with_devel}
%ifarch 0%{?gccgo_arches}
function gotest { %{gcc_go_test} "$@"; }
%else
%if 0%{?golang_test:1}
function gotest { %{golang_test} "$@"; }
%else
function gotest { go test "$@"; }
%endif
%endif

export GOPATH=%{buildroot}/%{gopath}:%{gopath}
%endif

%if 0%{?with_devel}
%files devel -f devel.file-list
%copying LICENSE
%dir %{gopath}/src/%{import_path}
%endif

%if 0%{?with_unit_test}
%files unit-test -f unit-test.file-list
%copying LICENSE
%endif

%changelog
* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0-0.23.hg74691fb6f837
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0-0.22.hg74691fb6f837
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0-0.21.hg74691fb6f837
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0-0.20.hg74691fb6f837
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0-0.19.hg74691fb6f837
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jul 21 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0-0.18.hg74691fb6f837
- https://fedoraproject.org/wiki/Changes/golang1.7

* Mon Feb 22 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0-0.17.hg74691fb6f837
- https://fedoraproject.org/wiki/Changes/golang1.6

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0-0.16.hg74691fb6f837
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Aug 24 2015 jchaloup <jchaloup@redhat.com> - 0-0.15.hg74691fb6f837
- Fix package name
  related: #1254600

* Mon Aug 24 2015 jchaloup <jchaloup@redhat.com> - 0-0.14.hg74691fb6f837
- Add LICENSE
  related: #1254600

* Wed Aug 12 2015 Fridolin Pokorny <fpokorny@redhat.com> - 0-0.13.hg74691fb6f837
- Update spec file to spec-2.0
  resolves: #1254600

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0-0.12.hg74691fb6f837
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jul 31 2014 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0-0.11.hg74691fb6f837
- archfulness and defattr for el6 only
- do not own dirs owned by golang

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0-0.10.hg74691fb6f837
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Jan 19 2014 Lokesh Mandvekar <lsm5@redhat.com> 0-0.9.hg74691fb6f837
- exclusivearch for el6+

* Thu Oct 17 2013 Lokesh Mandvekar <lsm5@redhat.com> 0-0.8.hg74691fb6f837
- removed double quotes from provides

* Tue Oct 08 2013 Lokesh Mandvekar <lsm5@redhat.com> 0-0.7.hg74691fb6f837
- noarch for f19+ and rhel7+, exclusivearch otherwise
- requires sqlite-devel

* Tue Oct 08 2013 Lokesh Mandvekar <lsm5@redhat.com> 0-0.6.hg74691fb6f837
- sql -> SQL, rpmlint warning fixed

* Tue Oct 08 2013 Lokesh Mandvekar <lsm5@redhat.com> 0-0.5.hg74691fb6f837
- buildarch: noarch

* Tue Oct 08 2013 Lokesh Mandvekar <lsm5@redhat.com> 0-0.4.hg74691fb6f837
- description update
- added noarch to exclusivearch list

* Tue Oct 08 2013 Lokesh Mandvekar <lsm5@redhat.com> 0-0.3.hg74691fb6f837
- golang license for 2012 installed

* Tue Oct 08 2013 Lokesh Mandvekar <lsm5@redhat.com> 0-0.2.hg74691fb6f837
- exclusivearch as per golang
- debug_package nil

* Sun Oct 06 2013 Lokesh Mandvekar <lsm5@redhat.com> 0-0.1.hg74691fb6f837
- Initial fedora package
