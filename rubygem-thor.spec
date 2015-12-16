%{!?scl:%global pkg_name %{name}}
%{?scl:%scl_package rubygem-%{gem_name}}

# Generated from thor-0.12.0.gem by gem2rpm -*- rpm-spec -*-
%global gem_name thor

Summary: Scripting framework that replaces rake, sake and rubigen
Name: %{?scl_prefix}rubygem-%{gem_name}
Version: 0.18.1
Release: 3%{?dist}
Group: Development/Languages
License: MIT
URL: http://github.com/wycats/thor
Source0: http://rubygems.org/downloads/%{gem_name}-%{version}.gem
Requires: %{?scl_prefix_ruby}ruby(rubygems)
Requires: %{?scl_prefix_ruby}ruby(release)
Requires: %{?scl_prefix_ruby}rubygem(rake)
Requires: %{?scl_prefix}rubygem(diff-lcs)
BuildRequires: %{?scl_prefix_ruby}rubygems-devel
BuildRequires: %{?scl_prefix_ruby}ruby(release)
BuildRequires: %{?scl_prefix}rubygem(rspec)
BuildRequires: %{?scl_prefix_ruby}rubygem(rake)
BuildRequires: %{?scl_prefix_ruby}rubygem(rdoc)
BuildRequires: %{?scl_prefix}rubygem(fakeweb)
#BuildRequires: %{?scl_prefix}rubygem(bundler)
BuildArch: noarch
Provides: %{?scl_prefix}rubygem(%{gem_name}) = %{version}

# Filter auto requires from /spec
%global __requires_exclude_from ^%{gem_instdir}/spec/.*$
%if ( 0%{?rhel} && 0%{?rhel} < 7 )
%filter_requires_in %{gem_instdir}/spec/.*$
%filter_setup
%endif


%description
Thor is a scripting framework that replaces rake, sake and rubigen.

%package doc
Summary: Documentation for %{pkg_name}
Group: Documentation

Requires: %{?scl_prefix}%{pkg_name} = %{version}-%{release}

%description doc
This package contains documentation for %{pkg_name}.

%prep
%setup -q -c -T
%{?scl:scl enable %{scl} - << \EOF}
%gem_install -n %{SOURCE0}
%{?scl:EOF}

%build

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a ./%{gem_dir}/* %{buildroot}%{gem_dir}/

# If there were programs installed:
mkdir -p %{buildroot}%{_bindir}
cp -a ./%{_bindir}/* %{buildroot}%{_bindir}

find %{buildroot}/%{_bindir} -type f | xargs chmod a+x

find %{buildroot}/%{_bindir} -type f | \
  xargs -n 1 sed -i -e 's"^#!/usr/bin/env ruby"#!%{?scl:%_scl_root}/usr/bin/ruby"'

%clean

%check
pushd %{buildroot}%{gem_instdir}

# Drop bundler dependency
sed -i "s/require 'bundler'//" Thorfile

# kill simplecov dependency
sed -i '3,10d' spec/helper.rb

# Fix failing tests
# /components and .empty_directory are present in git under v0.18.1 tag,
# but missing in .gem so the tests are failing
mkdir spec/fixtures/doc/components
touch spec/fixtures/doc/components/.empty_directory

%{?scl:scl enable %{scl} - << \EOF}
LANG=en_US.utf8 rspec spec
%{?scl:EOF}
popd

%files
%{_bindir}/thor
%doc %{gem_instdir}/LICENSE.md
%dir %{gem_instdir}
%{gem_instdir}/bin
%{gem_libdir}
%exclude %{gem_instdir}/.*
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/CHANGELOG.md
%doc %{gem_instdir}/README.md
%{gem_instdir}/Thorfile
%{gem_instdir}/spec
%{gem_instdir}/thor.gemspec

%changelog
* Thu Feb 13 2014 Josef Stribny <jstribny@redhat.com> - 0.18.1-3
- Filter auto-generated requires from example .sh script included in tests

* Mon Jan 27 2014 Josef Stribny <jstribny@redhat.com> - 0.18.1-2
- Fix upstream url

* Wed Jun 05 2013 Josef Stribny <jstribny@redhat.com> - 0.18.1-1
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0
- Update to Thor 0.18.1

* Thu Jul 26 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 0.15.4-1
- Update to Thor 0.15.4.
- Specfile cleanup

* Thu May 31 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 0.14.6-7
- Fix patches to apply cleanly.

* Tue Apr 03 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 0.14.6-6
- Rebuilt for scl.

* Wed Feb 01 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 0.14.6-5
- Enable tests.
- Add patches for the failing tests.
- Removed unnecessary ParseTree dependency.

* Mon Jan 30 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 0.14.6-4
- Rebuilt for Ruby 1.9.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 17 2011 Mohammed Morsi <mmorsi@redhat.com> - 0.14.6-1
- Updated to latest upstream version

* Wed May 5 2010 Matthew Kent <mkent@magoazul.com> - 0.13.6-1
- New upstream version.

* Fri Dec 18 2009 Matthew Kent <mkent@magoazul.com> - 0.12.0-2
- Add Requires for rubygem(rake) (#542559).
- Upstream replaced Source after the gemcutter migration, update to latest
  (#542559).
- Add Requires for rubygem(diff-lcs) as Thor can take advantage of it for
  colourized diff output (#542559).

* Mon Nov 16 2009 Matthew Kent <mkent@magoazul.com> - 0.12.0-1
- Initial package
