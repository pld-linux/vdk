%include        /usr/lib/rpm/macros.perl
Summary:	C++ Wrapper over GTK+ 2.0.x library
Summary(pl):	Wrapper C++ dla GTK+ 2.0.x
Name:		vdk
Version:	2.0.1
Release:	2
License:	LGPL
Group:		X11/Libraries
Source0:	http://prdownloads.sourceforge.net/vdkbuilder/%{name}-%{version}.tar.gz
URL:		http://vdkbuilder.sourceforge.net/
BuildRequires:	atk-devel >= 1.0.0
BuildRequires:	autoconf
BuildRequires:	doxygen
BuildRequires:	freetype-devel
BuildRequires:	glib2-devel >= 2.0.0
BuildRequires:	gtk+2-devel >= 2.0.0
BuildRequires:	imlib-devel
BuildRequires:	libsigc++-devel >= 1.0.0
BuildRequires:	libstdc++-devel
BuildRequires:	pango-devel >= 1.0.0
BuildRequires:	perl
BuildRequires:	perl >= 5.6
BuildRequires:	pkgconfig
BuildRequires:	rpm-perlprov >= 3.0.3-16
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_prefix		/usr/X11R6
%define		_mandir		%{_prefix}/man

%description
C++ Wrapper over GTK+ 2.0.x library.

%description -l pl
Wrapper C++ dla GTK+ 2.0.x.

%package devel
Summary:	VDK header files, development documentation
Summary(pl):	Pliki nag³ówkowe VDK, dokumentacja dla programistów
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}
Requires:	gtk+2-devel >= 2.0.0

%description devel
Header files and development documentation for VDK library.

%description devel -l pl
Pliki nag³ówkowe i dokumentacja dla programistów do biblioteki VDK.

%package static
Summary:	VDK static libraries
Summary(pl):	Biblioteki statyczne VDK
Group:		X11/Development/Libraries
Requires:	%{name}-devel = %{version}

%description static
VDK static libraries.

%description static -l pl
Biblioteki statyczne VDK.

%prep
%setup -q

%build
# exceptions and rtti are used in this package --misiek
%configure \
	--enable-static=yes
%{__make}
%{__make} docs

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/usr/src/examples/%{name}-%{version}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	m4datadir=%{_aclocaldir}

cp -dpr example/* $RPM_BUILD_ROOT/usr/src/examples/%{name}-%{version}

gzip -9nf README ChangeLog AUTHORS NEWS BUGS TODO

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so.*.*

%files devel
%defattr(644,root,root,755)
%doc *.gz doc/doxy/html
%{_examplesdir}/%{name}-%{version}
%attr(755,root,root) %{_libdir}/lib*.so
%attr(755,root,root) %{_libdir}/lib*.la
%attr(755,root,root) %{_bindir}/*
%{_aclocaldir}/*.m4
%{_includedir}/vdk2
%{_mandir}/man1/*

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
