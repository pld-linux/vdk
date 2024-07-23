#
# Conditional build:
%bcond_without	static_libs	# static library
#
Summary:	VDK Visual Development Kit - C++ Wrapper over GTK+ 2.x library
Summary(pl.UTF-8):	VDK Visual Development Kit - obudowanie C++ dla GTK+ 2.x
Name:		vdk
Version:	2.5.1
Release:	1
License:	LGPL v2+
Group:		X11/Libraries
Source0:	https://downloads.sourceforge.net/vdklib/%{name}-%{version}.tar.gz
# Source0-md5:	559d9feab3ae8433620bd061f03e4fb4
Patch0:		%{name}-ac_FLAGS.patch
Patch1:		%{name}-format.patch
URL:		https://vdklib.sourceforkge.net/
BuildRequires:	autoconf >= 2.52
BuildRequires:	automake
BuildRequires:	doxygen
BuildRequires:	freetype-devel >= 2.0.0
BuildRequires:	gtk+2-devel >= 2:2.18.0
BuildRequires:	imlib-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:1.5
BuildRequires:	perl-devel >= 1:5.6
BuildRequires:	pkgconfig >= 1:0.8
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpm-perlprov >= 4.1-13
BuildRequires:	zlib-devel
Requires:	gtk+2 >= 2:2.18.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
C++ Wrapper over GTK+ 2.x library.

%description -l pl.UTF-8
Wrapper C++ dla GTK+ 2.x.

%package devel
Summary:	VDK header files, development documentation
Summary(pl.UTF-8):	Pliki nagłówkowe VDK, dokumentacja dla programistów
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	gtk+2-devel >= 2:2.18.0

%description devel
Header files and development documentation for VDK library.

%description devel -l pl.UTF-8
Pliki nagłówkowe i dokumentacja dla programistów do biblioteki VDK.

%package static
Summary:	VDK static libraries
Summary(pl.UTF-8):	Biblioteki statyczne VDK
Group:		X11/Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
VDK static libraries.

%description static -l pl.UTF-8
Biblioteki statyczne VDK.

%package apidocs
Summary:	API documentation for VDK library
Summary(pl.UTF-8):	Dokumentacja API biblioteki VDK
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for VDK library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki VDK.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{!?with_static_libs:--disable-static}
%{__make}

%{__make} docs

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	m4datadir=%{_aclocaldir}

cp -dpr example/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libvdk-2.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS BUGS ChangeLog NEWS README TODO
%attr(755,root,root) %{_libdir}/libvdk-2.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libvdk-2.so.2

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/vdk-config-2
%attr(755,root,root) %{_libdir}/libvdk-2.so
%{_includedir}/vdk-2
%{_pkgconfigdir}/vdk-2.x.pc
%{_aclocaldir}/vdk-2.m4
%{_mandir}/man1/vdk-config-2.1*
%{_examplesdir}/%{name}-%{version}

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libvdk-2.a
%endif

%files apidocs
%defattr(644,root,root,755)
%doc doc/doxy/html/*.{css,gif,html,js,png}
