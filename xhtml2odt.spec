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
%if 0%{?mandriva_version}
BuildRequires:  python-uTidylib
%else
%if 0%{?suse_version}
BuildRequires:  python-utidy
%else
BuildRequires:  python-tidy
%endif
%endif
## Documentation
BuildRequires:  python-sphinx
%if 0%{?mandriva_version}
%else
# No phpdoc on Mandriva
BuildRequires:  phpdoc
%endif
BuildRequires:  dos2unix

## Python script
%if 0%{?mandriva_version}
BuildRequires:  python-uTidylib
%else
%if 0%{?suse_version}
BuildRequires:  python-utidy
%else
Requires:       python-tidy
%endif
%endif
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
# No phpdoc on Mandriva
%if 0%{?mandriva_version}
make doc-py
%else
make doc
%endif
rm -rf doc-python
mv doc-py/_build/html doc-python
rm -f doc-python/.buildinfo


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
%doc *.txt doc-python example-scripts
# No phpdoc on Mandriva
%if 0%{?mandriva_version}
%else
%doc doc-php
%endif
%{_bindir}/*
%{_datadir}/%{name}
%{_mandir}/man1/*


%changelog
* Thu Jul 14 2011 Aurelien Bompard <aurelien@bompard.org> -  1.3-1
- version 1.3

* Tue Sep 28 2010 Aurelien Bompard <aurelien@bompard.org> -  1.2-1
- initial package
