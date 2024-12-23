#
# Conditional build:
%bcond_without	tests		# unit tests

%define		qt_ver		5.3.0
%define		major_ver	5.3

Summary:	Grantlee - set of frameworks for use with Qt 5
Summary(pl.UTF-8):	Grantlee - zbiór szkieletów do wykorzystania z Qt 5
Name:		grantlee-qt5
Version:	5.3.1
Release:	3
License:	LGPL v2.1+
Group:		Libraries
Source0:	https://github.com/steveire/grantlee/releases/download/v%{version}/grantlee-%{version}.tar.gz
# Source0-md5:	4ef8eae5dd61e3c7603d76208eb4d922
Patch0:		x87fix.patch
URL:		http://www.grantlee.org/
BuildRequires:	Qt5Core-devel >= %{qt_ver}
BuildRequires:	Qt5Gui-devel >= %{qt_ver}
BuildRequires:	Qt5Network-devel >= %{qt_ver}
BuildRequires:	Qt5Script-devel >= %{qt_ver}
BuildRequires:	Qt5Sql-devel >= %{qt_ver}
BuildRequires:	Qt5Test-devel >= %{qt_ver}
BuildRequires:	Qt5WebKit-devel >= %{qt_ver}
BuildRequires:	Qt5Widgets-devel >= %{qt_ver}
BuildRequires:	Qt5XmlPatterns-devel >= %{qt_ver}
BuildRequires:	cmake >= 3.5
BuildRequires:	qt5-build >= %{qt_ver}
BuildRequires:	qt5-qmake >= %{qt_ver}
BuildRequires:	qt5-linguist >= %{qt_ver}
BuildRequires:	rpmbuild(macros) >= 1.605
Requires:	Qt5Core >= %{qt_ver}
Requires:	Qt5Gui >= %{qt_ver}
Requires:	Qt5Script >= %{qt_ver}
Conflicts:	grantlee-qt6 < 6
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# some combo of -fgcse and inlining triggers some miscompilation (two enum-compare tests fail) with gcc 14.2
%define		specflags_x86_64	-fno-gcse -fno-inline-functions -fno-partial-inlining

%description
Grantlee is a string template engine based on the Django template
system and written using Qt.

%description -l pl.UTF-8
Grantlee to silnik szablonów oparty na systemie szablonów Django i
napisany przy użyciu Qt.

%package devel
Summary:	Header files for grantlee libraries
Summary(pl.UTF-8):	Pliki nagłówkowe bibliotek grantlee
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	Qt5Core-devel >= %{qt_ver}
# only textdocument library
Requires:	Qt5Gui-devel >= %{qt_ver}
Conflicts:	grantlee-devel
Conflicts:	grantlee-qt6-devel < 6

%description devel
Header files for grantlee libraries.

%description devel -l pl.UTF-8
Pliki nagłówkowe bibliotek grantlee.

%prep
%setup -q -n grantlee-%{version}
%patch0 -p1

%build
install -d build
cd build
%cmake ..

%{__make}

%if %{with tests}
QT_QPA_PLATFORM=offscreen \
%{__make} test ARGS=-V
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS CHANGELOG README.md
%attr(755,root,root) %{_libdir}/libGrantlee_Templates.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libGrantlee_Templates.so.5
%attr(755,root,root) %{_libdir}/libGrantlee_TextDocument.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libGrantlee_TextDocument.so.5
%dir %{_libdir}/grantlee
%dir %{_libdir}/grantlee/%{major_ver}
%attr(755,root,root) %{_libdir}/grantlee/%{major_ver}/grantlee_defaultfilters.so
%attr(755,root,root) %{_libdir}/grantlee/%{major_ver}/grantlee_defaulttags.so
%attr(755,root,root) %{_libdir}/grantlee/%{major_ver}/grantlee_i18ntags.so
%attr(755,root,root) %{_libdir}/grantlee/%{major_ver}/grantlee_loadertags.so

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libGrantlee_Templates.so
%attr(755,root,root) %{_libdir}/libGrantlee_TextDocument.so
%{_includedir}/grantlee_templates.h
%{_includedir}/grantlee_textdocument.h
%{_includedir}/grantlee
%{_libdir}/cmake/Grantlee5
