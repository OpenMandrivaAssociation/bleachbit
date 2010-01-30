%define name bleachbit
%define version 0.7.2
%define release %mkrel 1

Summary: Clean junk to free disk space and to maintain privacy 
Name: %{name}
Version: %{version}
Release: %{release}
Source0: %{name}-%{version}.tar.bz2
License: GPLv3+
Group: File tools
Url:            http://bleachbit.sourceforge.net
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildArch: noarch
BuildRequires:  python-devel

Requires:       gnome-python
Requires:       gnome-python-gnomevfs
Requires:       pygtk2.0 >= 2.6


%description
Delete traces of your activities and other junk files to free disk
space and maintain privacy.  BleachBit identifies and erases
broken menu entries, cache, cookies, localizations, recent document
lists, and temporary files in Firefox, OpenOffice.org, Bash, and 50
other applications.

Shred files to prevent recovery, and wipe free disk space to
hide previously deleted files.

%prep
%setup -q

%build
%{__python} setup.py build

%install
rm -rf %{buildroot}

%makeinstall_std prefix=%{_prefix}
# make install DESTDIR=$RPM_BUILD_ROOT prefix=%{_prefix}
make -C po install DESTDIR=$RPM_BUILD_ROOT

%find_lang %{name}

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root)
%doc COPYING README
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/%{name}/
%{_datadir}/pixmaps/%{name}.png

