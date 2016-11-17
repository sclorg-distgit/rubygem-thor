%{?scl:%scl_package rubygem-%{gem_name}}
%{!?scl:%global pkg_name %{name}}

# Generated from thor-0.12.0.gem by gem2rpm -*- rpm-spec -*-
%global gem_name thor

# There are not all test dependencies are available in RHEL.
%global enable_test 1

Summary: Thor is a toolkit for building powerful command-line interfaces
Name: %{?scl_prefix}rubygem-%{gem_name}
Version: 0.19.1
Release: 6%{?dist}
Group: Development/Languages
License: MIT
URL: http://whatisthor.com/
Source0: http://rubygems.org/downloads/%{gem_name}-%{version}.gem
# Update rspec dependency to >= 3
Patch0: rubygem-thor-0.19.1-update-rspec-dependency.patch

Requires:      %{?scl_prefix_ruby}ruby(release)
Requires:      %{?scl_prefix_ruby}ruby(rubygems) >= 1.3.5
BuildRequires: %{?scl_prefix_ruby}rubygems-devel
BuildRequires: %{?scl_prefix_ruby}ruby(release)
BuildRequires: %{?scl_prefix_ruby}ruby
%if %{enable_test} > 0
BuildRequires: %{?scl_prefix}rubygem(rspec) >= 3
# Not necessary - omitting 2 tests
#BuildRequires: %%{?scl_prefix}rubygem(fakeweb)
BuildRequires: git
%endif
BuildArch: noarch
Provides:      %{?scl_prefix}rubygem(%{gem_name}) = %{version}

# Explicitly require runtime subpackage, as long as older scl-utils do not generate it
Requires: %{?scl_prefix}runtime

%description
Thor is a toolkit for building powerful command-line interfaces.

%package doc
Summary: Documentation for %{pkg_name}
Group: Documentation
Requires: %{?scl_prefix}%{pkg_name} = %{version}-%{release}
BuildArch: noarch

%description doc
This package contains documentation for %{pkg_name}.

%prep
%setup -n %{pkg_name}-%{version} -q -c -T

%{?scl:scl enable %{scl} - << \EOF}
%gem_install -n %{SOURCE0}
%{?scl:EOF}

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* %{buildroot}%{gem_dir}/

mkdir -p %{buildroot}%{_bindir}
cp -pa .%{_bindir}/* \
        %{buildroot}%{_bindir}/

find %{buildroot}%{gem_instdir}/bin -type f | xargs chmod a+x

%{?scl:scl enable %{scl} - << \EOF}
find %{buildroot}%{gem_instdir}/bin -type f | \
  xargs -n 1 sed -i -e "s|^#\!/usr/bin/env ruby|#\!`which ruby`|"

find %{buildroot}%{_bindir} -type f | \
  xargs -n 1 sed -i -e "s|^#\!/usr/bin/ruby|#\!`which ruby`|"
%{?scl:EOF}

%check
%if %{enable_test} > 0

pushd .%{gem_instdir}

# Drop bundler dependency
sed -i '/require "bundler"/ s/^/#/' Thorfile

# kill simplecov dependency
sed -i '/simplecov/,/end/ s/^/#/' spec/helper.rb

# Drop fakeweb dependency
sed -i '/require "fakeweb"/ s/^/#/' spec/helper.rb

# Fix failing tests
# /components and .empty_directory are present in git under v0.18.1 tag,
# but missing in .gem so the tests are failing
mkdir spec/fixtures/doc/components
touch spec/fixtures/doc/components/.empty_directory

patch -F 0 -p1 < %{PATCH0}

# Allow 2 failures due to dropped fakeweb dependency
%{?scl:scl enable %{scl} - << \EOF}
rspec spec | grep " examples, 2 failures"
%{?scl:EOF}
popd
%endif

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
* Wed Mar 02 2016 Pavel Valena <pvalena@redhat.com> - 0.19.1-6
- Fix shebang replacement

* Mon Feb 29 2016 Pavel Valena <pvalena@redhat.com> - 0.19.1-5
- Add Requires and Provides

* Mon Feb 29 2016 Pavel Valena <pvalena@redhat.com> - 0.19.1-4
- Add scl macros
- Update rspec dependency to >= 3

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.19.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.19.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Dec 09 2014 Vít Ondruch <vondruch@redhat.com> - 0.19.1-1
- Update to thor 1.19.1.

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.18.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Jul 25 2013 Josef Stribny <jstribny@redhat.com> - 0.18.1-1
- Update to Thor 0.18.1.

* Mon Mar 04 2013 Josef Stribny <jstribny@redhat.com> - 0.17.0-1
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0
- Update to Thor 0.17.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.16.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Nov 22 2012 Vít Ondruch <vondruch@redhat.com> - 0.16.0-2
- Disable tests for EL builds.

* Tue Nov 13 2012 Vít Ondruch <vondruch@redhat.com> - 0.16.0-1
- Update to thor 0.16.0.
- Remove rubygem(diff-lcs) dependency, since it is just optional.
- Remove rubygem(ruby2ruby) dependnecy, since it is just optional, to allow
  conversion of Rakefiles to Thorfiles (but it doesnt work withou ParseTree anyway).

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14.6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

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
