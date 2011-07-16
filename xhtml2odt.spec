%define python_tidy python-tidy
%define phpdoc phpdoc
%if 0%{?mandriva_version}
%define python_tidy python-uTidylib
%define phpdoc php-pear-PhpDocumentor
%endif
%if 0%{?suse_version}
%define python_tidy python-utidy
%define phpdoc php5-pear-phpdocumentor
%endif

Name:           xhtml2odt
Version:        1.3
Release:        1%{?dist}
Summary:        Convert XHTML to OpenDocument (ODT)

Group:          Applications/Publishing
License:        LGPLv2+
URL:            http://xhtml2odt.org
Source0:        http://xhtml2odt.org/dl/xhtml2odt-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

## Unit tests
BuildRequires:  python-nose
BuildRequires:  python-lxml
BuildRequires:  python-imaging
BuildRequires:  %{python_tidy}
## Documentation
BuildRequires:  python-sphinx
%if 0%{?mandriva_version}%{?suse_version}
# Can't make it work in OBS for now
%else
BuildRequires:  %{phpdoc}
%endif
BuildRequires:  dos2unix
BuildRequires:  help2man

## Python script
Requires:       %{python_tidy}
Requires:       python-lxml
Requires:       python-imaging


%description
XHTML2ODT is a converting library from XHTML to ODT. It is based on XSL
style sheets for portability, and is designed to help web applications export
to the ODT document format.


%prep
%setup -q
dos2unix README.txt NEWS.txt LICENSE.txt
chmod -x xhtml2odt.php xhtml2odt.sh


%build
make doc || :
rm -f doc/python/.buildinfo doc/python/.doctrees


%install
rm -rf $RPM_BUILD_ROOT
make install \
    PREFIX=%{_prefix} \
    DESTDIR=$RPM_BUILD_ROOT

rm -rf example-scripts
mkdir example-scripts
cp -a xhtml2odt.php xhtml2odt.sh example-scripts/


%check
make tests


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc *.txt doc/python example-scripts
%if 0%{?mandriva_version}%{?suse_version}
# Can't make it work in OBS for now
%else
%doc doc/php
%endif
%{_bindir}/*
%{_datadir}/%{name}
%{_mandir}/man1/*


%changelog
* Thu Jul 14 2011 Aurelien Bompard <aurelien@bompard.org> -  1.3-1
- version 1.3

* Tue Sep 28 2010 Aurelien Bompard <aurelien@bompard.org> -  1.2-1
- initial package
