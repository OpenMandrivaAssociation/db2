%define name  db2
%define version 2.4.14
%define release %mkrel 25

%define major		2
%define libname_orig	libdb%{major}
%define libname		%mklibname db %{major}

Summary: The BSD database library for C (version 2)
Name: %{name}
Version: %{version}
Release: %{release}
#Source: http://www.sleepycat.com/update/2.7.7/db-2.7.7.tar.gz
# Taken from glibc 2.1.3
Source0: %{name}-glibc-2.1.3.tar.bz2
# Patch to make it standalone
Patch0: db2-glibc-2.1.3.patch
Patch1: db2-2.4.14-db2.patch
Patch2: db2-2.4.14-db_fileid-64bit-fix.patch
Patch3: db2-gcc34.patch
Patch4: db2-64bit-fixes.patch
Patch5:	db2-sparc64-Makefile-fPIC.patch
Patch6: db2-deps.patch
Patch7: db2-LDFLAGS.diff
URL: http://www.sleepycat.com
License: BSD
Group: System/Libraries
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
%ifnarch ia64
Conflicts: glibc < 2.1.90
%endif

%description
The Berkeley Database (Berkeley DB) is a programmatic toolkit that provides
embedded database support for both traditional and client/server applications.
This library used to be part of the glibc package.

%package -n %{libname}
Summary: The BSD database library for C (version 2)
Group: System/Libraries
Obsoletes: %{name}
Provides: %{name} = %{version}-%{release}

%description -n %{libname}
The Berkeley Database (Berkeley DB) is a programmatic toolkit that provides
embedded database support for both traditional and client/server applications.
This library used to be part of the glibc package.

%package -n %{libname}-devel
Summary: Development libs/header files for Berkeley DB (version 2) library
Group: Development/C
Requires: %{libname} = %{version}-%{release}
Obsoletes: %{name}-devel
Provides: %{name}-devel = %{version}-%{release}
%ifnarch ia64
Conflicts: glibc-devel < 2.1.90
%endif

%description -n %{libname}-devel
The Berkeley Database (Berkeley DB) is a programmatic toolkit that provides
embedded database support for both traditional and client/server applications.
Berkeley DB includes B tree, Hashing, Fixed and Variable-length
record access methods.

This package contains the header files, libraries, and documentation for
building programs which use Berkeley DB.

%prep
%setup -q -n db2
%patch0 -p1
%patch1 -p1 -b .db2
%patch2 -p1 -b .db_fileid-64bit-fix
%patch3 -p1 -b .gcc34
%patch4 -p1 -b .64bit-fixes
%ifarch sparc64
%patch5 -p1 -b .sparc64
%endif
%patch6 -p1 -b .deps
%patch7 -p0 -b .LDFLAGS

%build
CFLAGS="%{optflags}" %make LDFLAGS="%{ldflags}"

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_includedir}/db2
mkdir -p $RPM_BUILD_ROOT%{_libdir}
mkdir -p $RPM_BUILD_ROOT%{_bindir}

# XXX this causes all symbols to be deleted from the shared library
#strip -R .comment libdb2.so.3
install -m644 libdb2.a			$RPM_BUILD_ROOT/%{_libdir}/libdb2.a
install -m755 libdb2.so.3		$RPM_BUILD_ROOT/%{_libdir}/libdb2.so.3
ln -sf libdb2.so.3 			$RPM_BUILD_ROOT/%{_libdir}/libdb2.so
ln -sf libdb2.a				$RPM_BUILD_ROOT/%{_libdir}/libndbm.a
ln -sf libdb2.so.3			$RPM_BUILD_ROOT/%{_libdir}/libndbm.so

install -m644 db.h			$RPM_BUILD_ROOT/%{_includedir}/db2
install -m644 db_185.h			$RPM_BUILD_ROOT/%{_includedir}/db2
for p in db_archive db_checkpoint db_deadlock db_dump db_load \
	 db_printlog db_recover db_stat; do
	q="`echo $p | sed -e 's,^db_,db2_,'`"
	install -s -m755 $p		$RPM_BUILD_ROOT/%{_bindir}/$q
done

%clean
rm -rf $RPM_BUILD_ROOT

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%files -n %{libname}
%defattr(-,root,root)
%doc README LICENSE
%{_libdir}/lib*.so.*

%files -n %{libname}-devel
%defattr(-,root,root)
%dir %{_includedir}/db2
%{_includedir}/db2/db.h
%{_includedir}/db2/db_185.h
%{_libdir}/libdb2.a
%{_libdir}/libdb2.so
%{_libdir}/libndbm.a
%{_libdir}/libndbm.so
%{_bindir}/db2_archive
%{_bindir}/db2_checkpoint
%{_bindir}/db2_deadlock
%{_bindir}/db2_dump
%{_bindir}/db2_load
%{_bindir}/db2_printlog
%{_bindir}/db2_recover
%{_bindir}/db2_stat

