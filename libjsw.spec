Summary:	UNIX Joystick Wrapper Library and calibrator
Summary(pl):	Biblioteka do obs³ugi joysticka pod UNIX-em
Name:		libjsw
Version:	1.4.0d
Release:	2
License:	Modyfied GPL
Group:		Libraries
Group(de):	Libraries
Group(es):	Bibliotecas
Group(fr):	Librairies
Group(pl):	Biblioteki
Source0:	ftp://fox.mit.edu/pub/xsw/%{name}%{version}.tgz
Source1:	jscalibrator.desktop
BuildRequires:	gtk+-devel
BuildRequires:	gcc-c++
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_xbindir	/usr/X11R6/bin
%define		_xmandir	/usr/X11R6/man

%description 
The UNIX Joystick Driver Wrapper Library and Calibrator (aka libjsw)
provides the programmer with the assistance to easilly code
applications that need to use the joystick driver and a convience to
users by storing the calibration information in a .joystick
calibration file.

%description -l pl
UNIX Joystick Driver Wrapper Library and Calibrator (czyli libjsw)
daje programi¶cie mo¿liwo¶æ ³atwego pisania programów korzystaj±cych z
joysticka oraz mo¿liwo¶æ przechowywania informacji o kalibracji w
pliku .joystick w katalogu domowym u¿ytkownika.

%package devel
Summary:	libjsw development package
Summary(pl):	Pliki dla programistów libjsw
Group:		Development/Libraries
Group(de):	Entwicklung/Libraries
Group(fr):	Development/Librairies
Group(pl):	Programowanie/Biblioteki
Requires:	%{name} = %{version}

%description devel
libjsw development package

%package -n jscalibrator
Summary:	Joystick calibrator
Summary(pl):	Kalibrator joysticka
Group:		Applications/Games
Group(de):	Applikationen/Spiele
Group(pl):	Aplikacje/Gry
Requires:	%{name} = %{version}

%description -n jscalibrator
Joystick calibrator for use with libjsw.

%description -n jscalibrator -l pl
Kalibrator joysticka do u¿ywania z libjsw.

%prep
%setup -qn %{name}%{version}

%build
cd libjsw
%{__make} CFLAGS="-shared %{rpmcflags}"
ln -sf libjsw.so.*.* libjsw.so
cd ..

cp -f include/jsw.h . 
cd jscalibrator
%{__make} CFLAGS="`gtk-config --cflags` %{rpmcflags}" INC="-I.." LIB_DIR="-L../libjsw"
cd ..

%install
rm -rf $RPM_BUILD_ROOT
cd libjsw
%{__make} install \
	JSW_LIB_DIR="$RPM_BUILD_ROOT%{_libdir}" \
	JSW_INC_DIR="$RPM_BUILD_ROOT%{_includedir}" \
	JSW_MAN_DIR="$RPM_BUILD_ROOT%{_mandir}/man3" 
cd ..

cd jscalibrator
%{__make} install \
	BIN_DIR="$RPM_BUILD_ROOT%{_xbindir}" \
	ICONS_DIR="$RPM_BUILD_ROOT%{_pixmapsdir}" \
	MAN_DIR="$RPM_BUILD_ROOT%{_xmandir}/man1" 
cd ..
install -d $RPM_BUILD_ROOT%{_applnkdir}/Settings
install %{SOURCE1} $RPM_BUILD_ROOT%{_applnkdir}/Settings

gzip -9nf README AUTHORS LICENSE

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc *.gz
%attr(755,root,root) %{_libdir}/libjsw.so.*.*
%attr(755,root,root) %{_libdir}/libjsw.so

%files devel
%defattr(644,root,root,755)
%{_includedir}/*
%{_mandir}/man*/*

%files -n jscalibrator
%defattr(644,root,root,755)
%doc LICENSE.gz
%attr(755,root,root) %{_xbindir}/*
%{_xmandir}/man*/*
%{_pixmapsdir}/*
%{_applnkdir}/Settings/*
