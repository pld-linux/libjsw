Summary:	UNIX Joystick Wrapper Library and calibrator
Summary(pl):	Biblioteka do obs³ugi joysticka pod UNIX-em
Name:		libjsw
Version:	1.5.0
Release:	3
License:	GPL-like
Group:		Libraries
Source0:	ftp://wolfpack.twu.net/users/wolfpack/libjsw-1.5.0.tar.bz2
Source1:	jscalibrator.desktop
Source2:	jscalibrator.png
Patch0:		%{name}-intbool.patch
URL:		http://wolfpack.twu.net/libjsw/
BuildRequires:	gtk+-devel
BuildRequires:	gcc-c++
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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
Requires:	%{name} = %{version}

%description devel
libjsw development package

%package -n jscalibrator
Summary:	Joystick calibrator
Summary(pl):	Kalibrator joysticka
Group:		Applications/Games
Requires:	%{name} = %{version}

%description -n jscalibrator
Joystick calibrator for use with libjsw.

%description -n jscalibrator -l pl
Kalibrator joysticka do u¿ywania z libjsw.

%prep
%setup -q
%patch0 -p0

%build
cd libjsw
%{__make} \
	CFLAGS="-shared %{rpmcflags} -fomit-frame-pointer -funroll-loops -ffast-math"
ln -sf libjsw.so.*.* libjsw.so
cd ..

cp -f include/jsw.h .
cd jscalibrator
%{__make} \
	CFLAGS="`gtk-config --cflags` %{rpmcflags} -fomit-frame-pointer -funroll-loops -ffast-math" \
	LIB_DIR="-L../libjsw" \
	INC="-I.."
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
	BIN_DIR="$RPM_BUILD_ROOT%{_bindir}" \
	ICONS_DIR="$RPM_BUILD_ROOT%{_pixmapsdir}" \
	MAN_DIR="$RPM_BUILD_ROOT%{_mandir}/man1" \
	DATA_DIR="$RPM_BUILD_ROOT%{_datadir}/libjsw"

cd ..

install -d $RPM_BUILD_ROOT%{_applnkdir}/Settings
install %{SOURCE1} $RPM_BUILD_ROOT%{_applnkdir}/Settings
install %{SOURCE2} $RPM_BUILD_ROOT%{_pixmapsdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README AUTHORS LICENSE
%attr(755,root,root) %{_libdir}/libjsw.so.*.*
%attr(755,root,root) %{_libdir}/libjsw.so

%files devel
%defattr(644,root,root,755)
%{_includedir}/*
%{_mandir}/man*/*

%files -n jscalibrator
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
%{_datadir}/libjsw
%{_mandir}/man*/*
%{_pixmapsdir}/*.png
%{_applnkdir}/Settings/*
