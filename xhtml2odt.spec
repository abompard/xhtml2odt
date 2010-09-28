Name:           xhtml2odt
Version:        1.2
Release:        1%{?dist}
Summary:        Convert XHTML to OpenDocument (ODT)

Group:          Applications/Publishing
License:        LGPLv2+
URL:            http://xhtml2odt.org
Source0:        http://xhtml2odt.org/dl/xhtml2odt-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

# Unit tests
BuildRequires:  python-nose
BuildRequires:  python-lxml
# Documentation
BuildRequires:  python-sphinx
BuildRequires:  phpdoc
BuildRequires:  help2man
BuildRequires:  dos2unix
# Python script
Requires:       python-tidy
Requires:       python-lxml
Requires:       python-imaging

%description
XHTML2ODT is a converting library from XHTML to ODT. It is based on XSL
style sheets for portability, and is designed to help web applications export
to the ODT document format.


%prep
%setup -q
dos2unix README.txt
chmod -x xhtml2odt.php xhtml2odt.sh


%build
make doc
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
%doc *.txt doc-php doc-python example-scripts
%{_bindir}/*
%{_datadir}/%{name}
%{_mandir}/man1/*


%changelog
* Tue Sep 28 2010 Aurelien Bompard <abompard@fedoraproject.org> -  1.2-1
- initial package
