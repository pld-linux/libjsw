Summary:	UNIX Joystick Wrapper Library and calibrator
Name:		libjsw
Version:	1.4.0d
Release:	1
License:	extended GPL
Group:		Development/Libraries
Group(de):	Entwicklung/Libraries
Group(fr):	Development/Librairies
Group(pl):	Programowanie/Biblioteki
Source0:	ftp://fox.mit.edu/pub/xsw/%{name}%{version}.tgz
BuildRequires:	gtk+-devel
BuildRequires:	gcc-c++
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_prefix	/usr/X11R6

%description 
The UNIX Joystick Driver Wrapper Library and Calibrator (aka libjsw)
provides the programmer with the assistance to easilly code
applications that need to use the joystick driver and a convience to
users by storing the calibration information in a .joystick
calibration file.

%package devel
Summary:	libjsw development package
Group:		Development/Libraries
Group(de):	Entwicklung/Libraries
Group(fr):	Development/Librairies
Group(pl):	Programowanie/Biblioteki
Requires:	%{name} = %{version}

%description devel
libjsw development package

%package -n jscalibrator
Summary:	Joystick calibrator
Group:		Applications/Games
Group(de):	Applikationen/Spiele
Group(pl):	Aplikacje/Gry
Requires:	%{name} = %{version}

%description -n jscalibrator
Joystick calibrator for use with libjsw.

%prep
%setup -qn %{name}%{version}

%build
cd libjsw
%{__make} CFLAGS="-shared %{rpmcflags}"
ln -s libjsw.so.*.* libjsw.so
cd ..

cp include/jsw.h . 
cd jscalibrator
%{__make} CFLAGS="`gtk-config --cflags` %{rpmcflags}" INC="-I.." LIB_DIR="-L../libjsw"
cd ..

%install
rm -rf $RPM_BUILD_ROOT
cd libjsw
%{__make} install \
	JSW_LIB_DIR="$RPM_BUILD_ROOT/usr/lib" \
	JSW_INC_DIR="$RPM_BUILD_ROOT/usr/include" \
	JSW_MAN_DIR="$RPM_BUILD_ROOT/usr/man/man3" 
cd ..

cd jscalibrator
%{__make} install \
	BIN_DIR="$RPM_BUILD_ROOT%{_bindir}" \
	ICONS_DIR="$RPM_BUILD_ROOT%{_pixmapsdir}" \
	MAN_DIR="$RPM_BUILD_ROOT%{_mandir}/man1" 
cd ..

gzip -9nf README AUTHORS LICENSE

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc *.gz
%attr(755,root,root) /usr/lib/libjsw.so.*.*

%files devel
%defattr(644,root,root,755)
/usr/include/*
/usr/man/man*/*
%attr(755,root,root) /usr/lib/libjsw.so

%files -n jscalibrator
%defattr(644,root,root,755)
%doc LICENSE.gz
%attr(755,root,root) %{_bindir}/*
%{_mandir}/man*/*
%{_pixmapsdir}/*
