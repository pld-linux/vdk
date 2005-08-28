#
# Conditional build:
%bcond_without	static_libs # don't build static libraries
#
%include	/usr/lib/rpm/macros.perl
Summary:	C++ Wrapper over GTK+ 2.x library
Summary(pl):	Wrapper C++ dla GTK+ 2.x
Name:		vdk
Version:	2.4.1
Release:	0.1
License:	LGPL
Group:		X11/Libraries
Source0:	http://kent.dl.sourceforge.net/sourceforge/vdklib/%{name}-%{version}.tar.gz
# Source0-md5:	f388bf265a476880e98ddec7ac4e63f7
Patch0:		%{name}-ac_FLAGS.patch
URL:		http://www.mariomotta.it/vdklib/
BuildRequires:	autoconf >= 2.52
BuildRequires:	automake
BuildRequires:	doxygen
BuildRequires:	freetype-devel >= 2.0.0
BuildRequires:	gtk+2-devel >= 2:2.4.0
BuildRequires:	imlib-devel
# both???
BuildRequires:	libsigc++1-devel
BuildRequires:	libsigc++12-devel >= 1.0.0
BuildRequires:	libstdc++-devel
BuildRequires:	libtool
BuildRequires:	perl-devel >= 1:5.6
BuildRequires:	pkgconfig
BuildRequires:	rpm-perlprov >= 4.1-13
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
C++ Wrapper over GTK+ 2.x library.

%description -l pl
Wrapper C++ dla GTK+ 2.x.

%package devel
Summary:	VDK header files, development documentation
Summary(pl):	Pliki nag³ówkowe VDK, dokumentacja dla programistów
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	gtk+2-devel >= 2:2.4.0

%description devel
Header files and development documentation for VDK library.

%description devel -l pl
Pliki nag³ówkowe i dokumentacja dla programistów do biblioteki VDK.

%package static
Summary:	VDK static libraries
Summary(pl):	Biblioteki statyczne VDK
Group:		X11/Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
VDK static libraries.

%description static -l pl
Biblioteki statyczne VDK.

%prep
%setup -q
%patch0 -p1

%build
# exceptions and rtti are used in this package --misiek
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	%{?with_static_libs:--enable-static=yes} \
	%{!?with_static_libs:--enable-static=no}
%{__make}
%{__make} docs

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	m4datadir=%{_aclocaldir}

cp -dpr example/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so.*.*

%files devel
%defattr(644,root,root,755)
%doc README ChangeLog AUTHORS NEWS BUGS TODO doc/doxy/html
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_aclocaldir}/*.m4
%{_includedir}/vdk2
%{_mandir}/man1/*
%{_examplesdir}/%{name}-%{version}
%{_pkgconfigdir}/*

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
%endif
