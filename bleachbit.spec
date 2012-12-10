Name:		bleachbit
Version:	0.9.3
Release:	1
Summary:	A tool to remove unnecessary files, free disk space and maintain privacy
Group:		System/Configuration/Other
License:	GPLv3
URL:		http://bleachbit.sourceforge.net/
Source0:	%{name}-%{version}.tar.bz2
Source1:	%{name}.1
BuildArch:	noarch
BuildRequires:	python-devel
BuildRequires:	desktop-file-utils
Requires:	python
Requires:	gnome-python
Requires:	gnome-python-gnomevfs
Requires:	pygtk2.0 >= 2.6
Requires:	usermode-consoleonly

%description
BleachBit deletes unnecessary files to free valuable disk space
and maintain privacy. Rid your system of old junk including cache,
temporary files, and cookies. Designed for Linux systems, it
wipes clean Bash, Beagle, Epiphany, Firefox, Adobe Flash, Java,
KDE, OpenOffice.org, Opera, rpm-build, XChat and more.

%prep
%setup -q

%build
make -C po local
python setup.py build

sed -i -e 's|/usr/bin/env python|/usr/bin/python|g' bleachbit/GUI.py

%install
rm -rf %{buildroot}

%makeinstall_std prefix=%{_prefix}

# create root desktop-file
cp %{name}.desktop %{name}-root.desktop
sed -i -e 's/Name=BleachBit$/Name=BleachBit as Administrator/g' %{name}-root.desktop
sed -i -e 's/Exec=bleachbit$/Exec=bleachbit-root/g' %{name}-root.desktop

cat > bleachbit.pam <<EOF
#%PAM-1.0
auth            include         config-util
account         include         config-util
session         include         config-util
EOF

cat > bleachbit.console <<EOF
USER=root
PROGRAM=/usr/bin/bleachbit
SESSION=true
EOF


desktop-file-install \
	--add-category="Utility"\
        --dir=%{buildroot}%{_datadir}/applications/ \
        --vendor="" %{name}.desktop

desktop-file-install \
	--add-category="Utility"\
        --dir=%{buildroot}%{_datadir}/applications/ \
        --vendor="" %{name}-root.desktop

# consolehelper and userhelper
ln -s consolehelper %{buildroot}%{_bindir}/%{name}-root
mkdir -p %{buildroot}%{_sbindir}
ln -s ../..%{_bindir}/%{name} %{buildroot}%{_sbindir}/%{name}-root
mkdir -p %{buildroot}%{_sysconfdir}/pam.d
install -m 644 %{name}.pam %{buildroot}%{_sysconfdir}/pam.d/%{name}-root
mkdir -p %{buildroot}%{_sysconfdir}/security/console.apps
install -m 644 %{name}.console %{buildroot}%{_sysconfdir}/security/console.apps/%{name}-root
mkdir -p %{buildroot}%{_mandir}/man1
install -m 644 %{SOURCE1} %{buildroot}%{_mandir}/man1
install -m 644 %{SOURCE1} %{buildroot}%{_mandir}/man1/%{name}-root.1

chmod 644 %{buildroot}%{_datadir}/%{name}/Worker.py
chmod 755 %{buildroot}%{_datadir}/%{name}/CLI.py
chmod 755 %{buildroot}%{_datadir}/%{name}/GUI.py

%__rm %{buildroot}%{_datadir}/%{name}/*.pyo

%find_lang %{name}

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%doc COPYING README
%{_bindir}/%{name}
%{_bindir}/%{name}-root
%{_sbindir}/*
%config(noreplace) %{_sysconfdir}/pam.d/%{name}-root
%config(noreplace) %{_sysconfdir}/security/console.apps/%{name}-root
%{_datadir}/%{name}
%{_datadir}/pixmaps/*.png
%{_datadir}/applications/*.desktop
%{_mandir}/man1/%{name}.1.xz
%{_mandir}/man1/%{name}-root.1.xz



%changelog
* Tue Aug 28 2012 Andrey Bondrov <abondrov@mandriva.org> 0.9.3-1
+ Revision: 815884
- Push package update by Dago68 from MIB: New version 0.9.3, add manpage from Debian, add config(noreplace), add README

* Fri Jun 01 2012 Andrey Bondrov <abondrov@mandriva.org> 0.9.2-1
+ Revision: 801767
- imported package bleachbit

  + Peťoš Šafařík <petos@mandriva.org>
    - Fixed several problems is SPEC files (obsoleted scriplets, .desktop file etc.)
    -This line, and following ones, will be ignored--
      file SPECS/bleachbit.spec modified
    - New version of BleachBit
    - SPEC file cleaning
    - import bleachbit


* Fri Jun 01 2012 Andrey Bondrov <bondrov@math.dvgu.ru> 0.9.2-1mdv2010.2
- Update to 0.9.2

* Wed Nov 25 2009 Andrey Bondrov <bondrov@math.dvgu.ru> 0.7.1-69.1mib2009.1
- First build for MIB users
- Mandriva Italia Backports
