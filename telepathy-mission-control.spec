%define tp_glib_ver 0.17.5

Name:           telepathy-mission-control
Version:        5.16.3
Release:        2%{?dist}
Epoch:          1
Summary:        Central control for Telepathy connection manager

Group:          System Environment/Libraries
License:        LGPLv2
URL:            http://telepathy.freedesktop.org/wiki/Mission_Control
Source0:        http://telepathy.freedesktop.org/releases/%{name}/%{name}-%{version}.tar.gz

# Fails intermittently on the builder -- possibly broken test cases
Patch0:         %{name}-tests-disable-auto-connect.patch
Patch1:         %{name}-tests-disable-avatar.patch
Patch2:         %{name}-tests-disable-avatar-refresh.patch
Patch3:         %{name}-tests-disable-crash-recovery.patch
Patch4:         %{name}-tests-disable-create-at-startup.patch
Patch5:         %{name}-tests-disable-default-keyring-storage.patch
Patch6:         %{name}-tests-disable-make-valid.patch
Patch7:         %{name}-tests-disable-respawn-activatable-observers.patch
Patch8:         %{name}-tests-disable-vanishing-client.patch

## upstream patches
# fix failing avatar test, https://bugs.freedesktop.org/show_bug.cgi?id=71001
Patch0049: 0049-account-manager-avatar.py-fix-race-condition-by-comb.patch

BuildRequires:  chrpath
BuildRequires:  dbus-python
BuildRequires:  glib2-devel
BuildRequires:  libxslt-devel
BuildRequires:  NetworkManager-glib-devel
BuildRequires:  pygobject2
BuildRequires:  python-twisted-core
BuildRequires:  telepathy-glib-devel >= %{tp_glib_ver}
BuildRequires:  gtk-doc


%description
Mission Control, or MC, is a Telepathy component providing a way for
"end-user" applications to abstract some of the details of connection
managers, to provide a simple way to manipulate a bunch of connection
managers at once, and to remove the need to have in each program the
account definitions and credentials.


%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{epoch}:%{version}-%{release}
Requires:       dbus-devel
Requires:       dbus-glib-devel
Requires:       telepathy-glib-devel >= %{tp_glib_ver}


%description    devel
The %{name}-devel package contains libraries and header
files for developing applications that use %{name}.


%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch0049 -p1 -b .0049


%build
%configure --disable-static --enable-gtk-doc --enable-mcd-plugins --with-connectivity=nm --disable-upower

# Omit unused direct shared library dependencies.
sed --in-place --expression 's! -shared ! -Wl,--as-needed\0!g' libtool

make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}

# Remove lib64 rpaths
chrpath --delete %{buildroot}%{_libexecdir}/mission-control-5

# Remove .la files
find %{buildroot} -name '*.la' -delete


%check
make check


%post -p /sbin/ldconfig


%postun
/sbin/ldconfig
if [ $1 -eq 0 ] ; then
    /usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi

%posttrans
    /usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :


%files
%doc AUTHORS NEWS COPYING
%{_bindir}/*
%{_datadir}/dbus-1/services/*.service
%{_datadir}/glib-2.0/schemas/im.telepathy.MissionControl.FromEmpathy.gschema.xml
%{_libdir}/libmission-control-plugins.so.*
%{_libexecdir}/mission-control-5
%{_mandir}/man*/*.gz


%files devel
%doc %{_datadir}/gtk-doc/html/mission-control-plugins
%{_includedir}/*
%{_libdir}/pkgconfig/*.pc
%{_libdir}/libmission-control-plugins.so


%changelog
* Wed May 13 2015 Debarshi Ray <rishi@fedoraproject.org> - 1:5.16.3-2
- Rebuild for upower soname bump
- Resolves: #1174525

* Thu Mar 19 2015 Richard Hughes <rhughes@redhat.com> 1:5.16.3-1
- Update to 5.16.3
- Resolves: #1174525

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 1:5.14.1-8
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 1:5.14.1-7
- Mass rebuild 2013-12-27

* Wed Oct 16 2013 Debarshi Ray <rishi@fedoraproject.org> - 1:5.14.1-6
- Remove ancient %%changelog entries, some of which had broken dates (Red Hat
  #884191)

* Thu Sep 19 2013 Debarshi Ray <rishi@fedoraproject.org> - 1:5.14.1-5
- Add %%check to run the upstream test suite on each build (Red Hat #1000705)
- Resort to using chrpath for removing rpaths instead of hacking libtool

* Wed Jul 17 2013 Debarshi Ray <rishi@fedoraproject.org> - 1:5.14.1-4
- Remove rpath and omit some unused direct shared library dependencies.

* Mon Jul 15 2013 Matthias Clasen <mclasen@redhat.com> - 1:5.14.1-3
- Rebuild against newer gtk-doc to fix multilib issues

* Thu Jun 20 2013 Matthias Clasen <mclasen@redhat.com> - 1:5.14.1-2
- Install NEWS instead of ChangeLog

* Fri May  3 2013 Brian Pepple <bpepple@fedoraproject.org> - 1:5.14.1-1
- Update to 5.14.1.
- Drop defattr. No longer needed.
- Drop ignore gnome keyring patch. Fixed upstream.

* Thu Jan 24 2013 Peter Robinson <pbrobinson@fedoraproject.org> 1:5.14.0-2
- Add patch for upstream b.fd.o # 59468

* Wed Oct  3 2012 Brian Pepple <bpepple@fedoraproject.org> - 1:5.14.0-1
- Update to 5.14.0

* Thu Sep 20 2012 Brian Pepple <bpepple@fedoraproject.org> - 1:5.13.2-1
- Update to 5.13.2.

* Thu Sep  6 2012 Brian Pepple <bpepple@fedoraproject.org> - 1:5.13.1-1
- Update to 5.13.1.

* Mon Jul 23 2012 Brian Pepple <bpepple@fedoraproject.org> - 1:5.13.0-1
- Update to 5.13.0.

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:5.12.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jul 11 2012 Brian Pepple <bpepple@fedoraproject.org> - 1:5.12.1-1
- Update to 5.12.1.

* Mon Apr  2 2012 Brian Pepple <bpepple@fedoraproject.org> - 1:5.12.0-1
- Update to 5.12.0.

* Wed Feb 22 2012 Brian Pepple <bpepple@fedoraproject.org> - 1:5.11.0-1
- Update to 5.11.0
- Bump minimum version of tp-glib.
