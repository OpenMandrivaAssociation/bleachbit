%define name bleachbit
%define version 0.7.2
%define release %mkrel 1

%define python_compile_opt python -O -c "import compileall; compileall.compile_dir('.')"
%define python_compile     python -c "import compileall; compileall.compile_dir('.')"

Summary: Clean junk to free disk space and to maintain privacy 
Name: %{name}
Version: %{version}
Release: %{release}
Source0: %{name}-%{version}.tar.bz2
License: GPLv3
Group: File tools
Url:            http://bleachbit.sourceforge.net
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildArch: noarch
BuildRequires:  libpython2.6-devel

Requires:       gnome-python
Requires:       gnome-python-gnomevfs
Requires:       pygtk2.0 >= 2.6
Requires:       usermode-consoleonly


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

cp %{name}.desktop %{name}-root.desktop
sed -i -e 's/Name=BleachBit$/Name=BleachBit as Administrator/g' %{name}-root.desktop


# remove Windows-specific cleaners
grep -l os=.windows. cleaners/*xml | xargs rm -f
# remove Windows-specific modules
rm -f bleachbit/Windows.py


%install
rm -rf %{buildroot}

%makeinstall_std prefix=%{_prefix}
# make install DESTDIR=$RPM_BUILD_ROOT prefix=%{_prefix}
make -C po install DESTDIR=$RPM_BUILD_ROOT

%find_lang %{name}

%clean
rm -rf %{buildroot}

%post
%{update_menus}
%{update_desktop_database}

%postun
%{clean_menus}
%{clean_desktop_database}


%files -f %{name}.lang
%defattr(-,root,root)
%doc COPYING README
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/%{name}/
%{_datadir}/pixmaps/%{name}.png

