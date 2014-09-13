%define major	2
%define libname	%mklibname db %{major}

Summary:	The BSD database library for C (version 2)
Name:		db2
Version:	2.4.14
Release:	32
License:	BSD
Group:		System/Libraries
#Source: http://www.sleepycat.com/update/2.7.7/db-2.7.7.tar.gz
# Taken from glibc 2.1.3
Url:		http://www.sleepycat.com
Source0:	%{name}-glibc-2.1.3.tar.bz2
Source100:	db2.rpmlintrc
# Patch to make it standalone
Patch0:		db2-glibc-2.1.3.patch
Patch1:		db2-2.4.14-db2.patch
Patch2:		db2-2.4.14-db_fileid-64bit-fix.patch
Patch3:		db2-gcc34.patch
Patch4:		db2-64bit-fixes.patch
Patch5:		db2-sparc64-Makefile-fPIC.patch
Patch6:		db2-deps.patch
Patch7:		db2-LDFLAGS.diff

%description
The Berkeley Database (Berkeley DB) is a programmatic toolkit that provides
embedded database support for both traditional and client/server applications.
This library used to be part of the glibc package.

%package -n %{libname}
Summary:	The BSD database library for C (version 2)
Group:		System/Libraries
Provides:	%{name} = %{version}-%{release}

%description -n %{libname}
The Berkeley Database (Berkeley DB) is a programmatic toolkit that provides
embedded database support for both traditional and client/server applications.
This library used to be part of the glibc package.

%package -n %{libname}-devel
Summary:	Development libs/header files for Berkeley DB (version 2) library
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{libname}-devel
This package contains the header files, libraries, and documentation for
building programs which use Berkeley DB.

%prep
%setup -qn db2
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
CFLAGS="%{optflags}" %make LDFLAGS="%{ldflags}" CC=%{__cc}

%install
mkdir -p %{buildroot}%{_includedir}/db2
mkdir -p %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{_bindir}

# XXX this causes all symbols to be deleted from the shared library
#strip -R .comment libdb2.so.3
install -m644 libdb2.a			%{buildroot}/%{_libdir}/libdb2.a
install -m755 libdb2.so.3		%{buildroot}/%{_libdir}/libdb2.so.3
ln -sf libdb2.so.3 			%{buildroot}/%{_libdir}/libdb2.so
ln -sf libdb2.a				%{buildroot}/%{_libdir}/libndbm.a
ln -sf libdb2.so.3			%{buildroot}/%{_libdir}/libndbm.so

install -m644 db.h			%{buildroot}/%{_includedir}/db2
install -m644 db_185.h			%{buildroot}/%{_includedir}/db2
for p in db_archive db_checkpoint db_deadlock db_dump db_load \
	db_printlog db_recover db_stat; do
	q="`echo $p | sed -e 's,^db_,db2_,'`"
	install -s -m755 $p		%{buildroot}/%{_bindir}/$q
done

%files -n %{libname}
%doc README LICENSE
%{_libdir}/lib*.so.*

%files -n %{libname}-devel
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

