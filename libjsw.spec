Summary:	UNIX Joystick Wrapper Library and calibrator
Summary(pl.UTF-8):	Biblioteka do obsługi joysticka pod Uniksem
Name:		libjsw
Version:	1.5.6
Release:	2
License:	GPL-like
Group:		Libraries
Source0:	ftp://wolfpack.twu.net/users/wolfpack/%{name}-%{version}.tar.bz2
# Source0-md5:	d75948b7ff464982cc6e1de4c94008be
Source1:	jscalibrator.desktop
Source2:	jscalibrator.png
Patch0:		%{name}-intbool.patch
Patch1:		%{name}-link.patch
URL:		http://wolfpack.twu.net/libjsw/
BuildRequires:	gtk+-devel
BuildRequires:	libstdc++-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The UNIX Joystick Driver Wrapper Library and Calibrator (aka libjsw)
provides the programmer with the assistance to easilly code
applications that need to use the joystick driver and a convience to
users by storing the calibration information in a .joystick
calibration file.

%description -l pl.UTF-8
UNIX Joystick Driver Wrapper Library and Calibrator (czyli libjsw)
daje programiście możliwość łatwego pisania programów korzystających z
joysticka oraz możliwość przechowywania informacji o kalibracji w
pliku .joystick w katalogu domowym użytkownika.

%package devel
Summary:	libjsw development package
Summary(pl.UTF-8):	Pliki dla programistów libjsw
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
libjsw development package.

%description devel -l pl.UTF-8
Pliki dla programistów używających libjsw.

%package -n jscalibrator
Summary:	Joystick calibrator
Summary(pl.UTF-8):	Kalibrator joysticka
Group:		X11/Applications/Games
Requires:	%{name} = %{version}-%{release}

%description -n jscalibrator
Joystick calibrator for use with libjsw.

%description -n jscalibrator -l pl.UTF-8
Kalibrator joysticka do używania z libjsw.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
cd libjsw
%{__make} \
	CFLAGS="%{rpmcflags} %{!?debug:-fomit-frame-pointer} -funroll-loops -ffast-math -fPIC"
ln -sf libjsw.so.*.* libjsw.so
cd ..

ln -sf include/jsw.h .
%{__make} -C jscalibrator \
	CFLAGS="`gtk-config --cflags` %{rpmcflags} %{!?debug:-fomit-frame-pointer} -funroll-loops -ffast-math" \
	INC_DIRS="-I.."

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%{__make} -C libjsw install \
	JSW_LIB_DIR="$RPM_BUILD_ROOT%{_libdir}" \
	JSW_INC_DIR="$RPM_BUILD_ROOT%{_includedir}" \
	JSW_MAN_DIR="$RPM_BUILD_ROOT%{_mandir}/man3"

%{__make} -C jscalibrator install \
	BIN_DIR="$RPM_BUILD_ROOT%{_bindir}" \
	ICONS_DIR="$RPM_BUILD_ROOT%{_pixmapsdir}" \
	MAN_DIR="$RPM_BUILD_ROOT%{_mandir}/man1" \
	DATA_DIR="$RPM_BUILD_ROOT%{_datadir}/libjsw"

install -d $RPM_BUILD_ROOT%{_desktopdir}
install %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}
install %{SOURCE2} $RPM_BUILD_ROOT%{_pixmapsdir}
install jswdemos/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README AUTHORS LICENSE
%attr(755,root,root) %{_libdir}/libjsw.so.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libjsw.so
%{_includedir}/*
%{_mandir}/man3/*
%{_examplesdir}/%{name}-%{version}

%files -n jscalibrator
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
%{_datadir}/libjsw
%{_mandir}/man1/*
%{_pixmapsdir}/*.png
%{_desktopdir}/*.desktop
