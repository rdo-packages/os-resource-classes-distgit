%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0x2426b928085a020d8a90d0d879ab7008d0896c8a
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
%global with_doc 1

%global sname os-resource-classes
%global pypi_name os_resource_classes
%global common_desc \
A list of standardized resource classes for OpenStack.\
\
A resource class is a distinct type of inventory that exists in a cloud\
environment, for example VCPU, DISK_GB. They are upper case with underscores.\
They often include a unit in their name.\
\
This package provides a collection of symbols representing those standard\
resource classes which are expected to be available in any OpenStack\
deployment.\
\
There also exists a concept of custom resource classes. These are countable\
types that are custom to a particular environment. The OpenStack placement API\
provides a way to create these. A custom resource class always begins with a\
CUSTOM_ prefix.

Name:           python-%{sname}
Version:        XXX
Release:        XXX
Summary:        A library containing standardized resource class names in the Placement service.

License:        ASL 2.0
URL:            https://docs.openstack.org/developer/os-resource-classes/
Source0:        http://tarballs.openstack.org/%{sname}/%{sname}-%{upstream_version}.tar.gz
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
Source101:        http://tarballs.openstack.org/%{sname}/%{sname}-%{upstream_version}.tar.gz.asc
Source102:        https://releases.openstack.org/_static/%{sources_gpg_sign}.txt
%endif
BuildArch:      noarch

# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
BuildRequires:  /usr/bin/gpgv2
%endif

BuildRequires:  git-core
BuildRequires:  openstack-macros

%description
%{common_desc}

%package -n     python3-%{sname}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{sname}}

Requires:       python3-pbr >= 2.0

BuildRequires:  python3-devel
BuildRequires:  python3-pbr
BuildRequires:  python3-setuptools

%description -n python3-%{sname}
%{common_desc}

%package -n     python3-%{sname}-tests
Summary:        %{summary}

# Required for the test suite
BuildRequires:  python3-coverage
BuildRequires:  python3-subunit
BuildRequires:  python3-oslotest
BuildRequires:  python3-testtools
BuildRequires:  python3-stestr

Requires:       python3-coverage >= 4.0
Requires:       python3-%{sname} = %{version}-%{release}
Requires:       python3-subunit
Requires:       python3-oslotest
Requires:       python3-testtools
Requires:       python3-stestr

%description -n python3-%{sname}-tests
This package contains tests for python os-resource-classes library.

%if 0%{?with_doc}
%package -n python-%{sname}-doc
Summary:        os-resource-classes documentation

BuildRequires:  python3-sphinx
BuildRequires:  python3-openstackdocstheme

%description -n python-%{sname}-doc
Documentation for os-resource-classes
%endif

%prep
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
%{gpgverify}  --keyring=%{SOURCE102} --signature=%{SOURCE101} --data=%{SOURCE0}
%endif
%autosetup -n %{sname}-%{upstream_version} -S git
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info
# remove requirements
%py_req_cleanup

%build
%{py3_build}

%if 0%{?with_doc}
# generate html docs
sphinx-build-3 -W -b html doc/source doc/build/html
# remove the sphinx build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%install
# Must do the subpackages' install first because the scripts in /usr/bin are
# overwritten with every setup.py install.
%{py3_install}

%check
%{__python3} setup.py test

%files -n python3-%{sname}
%license LICENSE
%doc README.rst
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}-%{upstream_version}-py%{python3_version}.egg-info
%exclude %{python3_sitelib}/%{pypi_name}/tests

%files -n python3-%{sname}-tests
%{python3_sitelib}/%{pypi_name}/tests

%if 0%{?with_doc}
%files -n python-%{sname}-doc
%license LICENSE
%doc doc/build/html
%endif

%changelog
