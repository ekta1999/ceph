%define pkg_version @VERSION@
# Build against the running kernel - this can be changed to whatever
kernel version you want to build against.
%define kernel %(uname -r)
%define mybuildroot
%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
%define optflags ""

Name:          ceph
Version:       %{pkg_version}
Release:       1%{?dist}
Packager:      Brock Erwin <brock.erwin@pnl.gov>
Summary:       ceph mon, mds, osd, fuse-client, and kernel-client
License:       LGPL
Group:         Utilities/System
URL:           http://ceph.newdream.net/
Source:        %{name}-%{pkg_version}.tar.gz
BuildRequires: gcc-c++, libtool, libtool-ltdl-devel, boost-devel, git,
perl, perl-devel, gdbm, kernel-devel == %{kernel}
BuildRoot:     %{mybuildroot}
Requires:      ceph-mon, ceph-mds, ceph-osd, kmod-ceph-%{kernel}

%description
Ceph is a distributed network file system designed to provide excellent
performance, reliability, and scalability.

%package    mon
Summary:    ceph monitor and admin binaries
Group:      Utilities/System
Requires:   libstdc++, glibc-devel, glibc, libgcc
%description mon
monitor and admin binaries

%package    mds
Summary:    ceph mds binaries
Group:      Utilities/System
Requires:   libstdc++, glibc-devel, glibc, libgcc
%description mds
mds binaries

%package     osd
Summary:     ceph osd binaries
Group:       Utilities/System
Requires:    libstdc++, glibc-devel, glibc, libgcc
%description osd
osd binaries

%package     fuse-client
Summary:     ceph fuse-based client
Group:       Utilities/System
Requires:    libstdc++, glibc-devel, glibc, libgcc, fuse-devel
%description fuse-client
fuse-based client

%package     -n kmod-ceph-%{kernel}
Summary:        kernel-client tools for mounting the ceph file system.
Group:          Utilities/System
Requires:       libstdc++, glibc-devel, glibc, libgcc
%description -n kmod-ceph-%{kernel}
kernel-client module

%package        testing
Summary:        kernel-client tools for mounting the ceph file system.
Group:          Utilities/System
Requires:       libstdc++, glibc-devel, glibc, libgcc
%description    testing
Used as a placeholder for binaries that are installed but unused by the
user (testing purposes only)

%prep
%setup -q -n %{name}-%{pkg_version}

%build
./autogen.sh
%{configure}
make %{_smp_mflags}
make -C src/kernel KERNELDIR=/lib/modules/%{kernel}/build # Build the
kernel module

%install
%{makeinstall}
mkdir -p $RPM_BUILD_ROOT/lib/modules/%{kernel}/extra
install src/kernel/ceph.ko $RPM_BUILD_ROOT/lib/modules/%{kernel}/extra
# Install the kernel module
mkdir -p $RPM_BUILD_ROOT/usr/share/ceph
install README $RPM_BUILD_ROOT/usr/share/ceph

%clean
rm -rf $RPM_BUILD_ROOT

%files
/usr/share/ceph/README

%files mon
%{_bindir}/cmon
%{_bindir}/cmonctl
%{_bindir}/crushtool
%{_bindir}/mkmonfs
%{_bindir}/monmaptool
%{_bindir}/osdmaptool
%{_bindir}/csyn

%files mds
%{_bindir}/cmds

%files osd
%{_bindir}/cosd
%{_bindir}/dupstore

%files fuse-client
%{_bindir}/cfuse

%files -n kmod-ceph-%{kernel}
/lib/modules/%{kernel}/extra/ceph.ko

%files testing
%{_bindir}/dumpjournal
%{_bindir}/streamtest

