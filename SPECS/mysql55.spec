%global basever 5.5

Name: mysql55
Version: 5.5.48
Release: 1.ius%{?dist}
Summary: MySQL client programs and shared libraries
Group: Applications/Databases
URL: http://www.mysql.com
# exceptions allow client libraries to be linked with most open source SW,
# not only GPL code.  See README.mysql-license
License: GPLv2 with exceptions

# Regression tests take a long time, you can skip 'em with this
%{!?runselftest:%global runselftest 1}

Source0: http://dev.mysql.com/get/Downloads/MySQL-5.5/mysql-%{version}.tar.gz
Source1: generate-tarball.sh
Source2: mysql.init
Source3: my.cnf
Source4: scriptstub.c
Source5: my_config.h
Source6: README.mysql-docs
Source7: README.mysql-license
Source8: libmysql.version
Source9: mysql-embedded-check.c
Source11: mysqld.sysconfig
# Working around perl dependency checking bug in rpm FTTB. Remove later.
Source999: filter-requires-mysql.sh

# IUS Sources
Source100: my-55-terse.cnf
Source101: my-55-verbose.cnf
Source102: mysql.logrotate
Patch1: mysql-errno.patch
Patch2: mysql-strmov.patch
Patch3: mysql-install-test.patch
Patch5: mysql-stack-guard.patch
Patch6: mysql-5.5.28-chain-certs.patch
Patch7: mysql-versioning.patch
Patch8: mysql-dubious-exports.patch
Patch9: mysql-disable-test.patch
Patch22: mysql-innodbwarn.patch

#Disable SSL_OP_NO_COMPRESSION as it is not available in openssl for RHEL 5
# Fixed upstream in 5.5.44
# Patch318: mysql-5.5.31-disable_SSL_OP_NO_COMPRESSION.patch

# Fixed upstream in 5.5.45
#Patch319: community-mysql-dh1024.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: gperf, perl, readline-devel, openssl-devel
BuildRequires: gcc-c++, cmake, ncurses-devel, zlib-devel, libaio-devel
BuildRequires: systemtap-sdt-devel
# make test requires time and ps
BuildRequires: time procps
# Socket is needed to run regression tests
BuildRequires: perl(Socket)

Requires: grep, fileutils
Requires: %{name}-libs%{?_isa} = %{version}-%{release}
Requires: bash

# MySQL (with caps) is upstream's spelling of their own RPMs for mysql
Conflicts: MySQL
# mysql-cluster used to be built from this SRPM, but no more
Obsoletes: mysql-cluster < 5.1.44

# IUS-isms
Conflicts: mysql < %{basever}
Provides: mysql = %{version}-%{release}
Provides: mysql%{?_isa} = %{version}-%{release}

# Added as a convenience, mysql51 doesn't require mysqlclient15
# but all the packages built against mysql 5.0/5.1 do
%if 0%{?el5}
Requires: mysqlclient15
%endif

%if 0%{?el6}
BuildRequires: perl-Time-HiRes
Requires: mysqlclient16
%endif

# Working around perl dependency checking bug in rpm FTTB. Remove later.
%global __perl_requires %{SOURCE999}


%description
MySQL is a multi-user, multi-threaded SQL database server. MySQL is a
client/server implementation consisting of a server daemon (mysqld)
and many different client programs and libraries. The base package
contains the standard MySQL client programs and generic MySQL files.


%package libs

Summary: The shared libraries required for MySQL clients
Group: Applications/Databases
Requires: /sbin/ldconfig

# IUS-isms
Conflicts: mysql-libs < %{basever}
Provides: mysql-libs = %{version}-%{release}
Provides: mysql-libs%{?_isa} = %{version}-%{release}
Provides: config(mysql-libs) = %{version}-%{release}


%description libs
The mysql-libs package provides the essential shared libraries for any 
MySQL client program or interface. You will need to install this package
to use any other MySQL package or any clients that need to connect to a
MySQL server.


%package server

Summary: The MySQL server and related files
Group: Applications/Databases
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: %{name}-libs%{?_isa} = %{version}-%{release}
Requires: sh-utils
Requires(pre): /usr/sbin/useradd
Requires(post): chkconfig
Requires(preun): chkconfig
# This is for /sbin/service
Requires(preun): initscripts
Requires(postun): initscripts
# mysqlhotcopy needs DBI/DBD support
Requires: perl-DBI, perl-DBD-MySQL
Conflicts: MySQL-server

# IUS-isms
Conflicts: mysql-server < %{basever}
Provides: mysql-server = %{version}-%{release}
Provides: mysql-server%{?_isa} = %{version}-%{release}
Provides: config(mysql-server) = %{version}-%{release}


%description server
MySQL is a multi-user, multi-threaded SQL database server. MySQL is a
client/server implementation consisting of a server daemon (mysqld)
and many different client programs and libraries. This package contains
the MySQL server and some accompanying files and directories.


%package devel

Summary: Files for development of MySQL applications
Group: Applications/Databases
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: %{name}-libs%{?_isa} = %{version}-%{release}
Requires: openssl-devel
Conflicts: MySQL-devel

# IUS-isms
Conflicts: mysql-devel < %{basever}
Provides: mysql-devel = %{version}-%{release}
Provides: mysql-devel%{?_isa} = %{version}-%{release}


%description devel
MySQL is a multi-user, multi-threaded SQL database server. This
package contains the libraries and header files that are needed for
developing MySQL client applications.


%package embedded

Summary: MySQL as an embeddable library
Group: Applications/Databases

# IUS-isms
Conflicts: mysql-embedded < %{basever}
Provides: mysql-embedded = %{version}-%{release}
Provides: mysql-embedded%{?_isa} = %{version}-%{release}


%description embedded
MySQL is a multi-user, multi-threaded SQL database server. This
package contains a version of the MySQL server that can be embedded
into a client application instead of running as a separate process.


%package embedded-devel

Summary: Development files for MySQL as an embeddable library
Group: Applications/Databases
Requires: %{name}-embedded%{?_isa} = %{version}-%{release}
Requires: %{name}-devel%{?_isa} = %{version}-%{release}

# IUS-isms
Conflicts: mysql-embedded-devel < %{basever}
Provides: mysql-embedded-devel = %{version}-%{release}
Provides: mysql-embedded-devel%{?_isa} = %{version}-%{release}


%description embedded-devel
MySQL is a multi-user, multi-threaded SQL database server. This
package contains files needed for developing and testing with
the embedded version of the MySQL server.


%package bench

Summary: MySQL benchmark scripts and data
Group: Applications/Databases
Requires: %{name}%{?_isa} = %{version}-%{release}
Conflicts: MySQL-bench

# IUS-isms
Conflicts: mysql-bench < %{basever}
Provides: mysql-bench = %{version}-%{release}
Provides: mysql-bench%{?_isa} = %{version}-%{release}


%description bench
MySQL is a multi-user, multi-threaded SQL database server. This
package contains benchmark scripts and data for use when benchmarking
MySQL.


%package test

Summary: The test suite distributed with MySQL
Group: Applications/Databases
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: %{name}-libs%{?_isa} = %{version}-%{release}
Requires: %{name}-server%{?_isa} = %{version}-%{release}
Conflicts: MySQL-test

# IUS-isms
Conflicts: mysql-test < %{basever}
Provides: mysql-test = %{version}-%{release}
Provides: mysql-test%{?_isa} = %{version}-%{release}


%description test
MySQL is a multi-user, multi-threaded SQL database server. This
package contains the regression test suite distributed with
the MySQL sources.


%prep
%setup -q -n mysql-%{version}

# my-55-verbose.cnf
cp %{SOURCE101} .

%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch22 -p1

# workaround for upstream bug #56342
rm -f mysql-test/t/ssl_8k_key-master.opt

# upstream has fallen down badly on symbol versioning, do it ourselves
cp %{SOURCE8} libmysql/libmysql.version


%build

# fail quickly and obviously if user tries to build as root
%if %runselftest
	if [ x"`id -u`" = x0 ]; then
		echo "mysql's regression tests fail if run as root."
		echo "If you really need to build the RPM as root, use"
		echo "--define='runselftest 0' to skip the regression tests."
		exit 1
	fi
%endif

CFLAGS="%{optflags} -D_GNU_SOURCE -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE"
# MySQL 4.1.10 definitely doesn't work under strict aliasing; also,
# gcc 4.1 breaks MySQL 5.0.16 without -fwrapv
CFLAGS="$CFLAGS -fno-strict-aliasing -fwrapv"
# force PIC mode so that we can build libmysqld.so
CFLAGS="$CFLAGS -fPIC"
# gcc seems to have some bugs on sparc as of 4.4.1, back off optimization
# submitted as bz #529298
%ifarch sparc sparcv9 sparc64
CFLAGS=`echo $CFLAGS| sed -e "s|-O2|-O1|g" `
%endif
# extra C++ flags as per recommendations in mysql's INSTALL-SOURCE doc
CXXFLAGS="$CFLAGS -felide-constructors -fno-rtti -fno-exceptions"
export CFLAGS CXXFLAGS

# The INSTALL_xxx macros have to be specified relative to CMAKE_INSTALL_PREFIX
# so we can't use %%{_datadir} and so forth here.

cmake . -DBUILD_CONFIG=mysql_release \
	-DFEATURE_SET="community" \
    -DCOMPILATION_COMMENT="Distributed by The IUS Community Project" \
	-DINSTALL_LAYOUT=RPM \
	-DCMAKE_INSTALL_PREFIX="%{_prefix}" \
	-DINSTALL_INCLUDEDIR=include/mysql \
	-DINSTALL_INFODIR=share/info \
	-DINSTALL_LIBDIR="%{_lib}/mysql" \
	-DINSTALL_MANDIR=share/man \
	-DINSTALL_MYSQLSHAREDIR=share/mysql \
	-DINSTALL_MYSQLTESTDIR=share/mysql-test \
	-DINSTALL_PLUGINDIR="%{_lib}/mysql/plugin" \
	-DINSTALL_SBINDIR=libexec \
	-DINSTALL_SCRIPTDIR=bin \
	-DINSTALL_SQLBENCHDIR=share \
	-DINSTALL_SUPPORTFILESDIR=share/mysql \
	-DMYSQL_DATADIR="/var/lib/mysql" \
	-DMYSQL_UNIX_ADDR="/var/lib/mysql/mysql.sock" \
	-DENABLED_LOCAL_INFILE=ON \
	-DENABLE_DTRACE=ON \
	-DWITH_EMBEDDED_SERVER=ON \
	-DWITH_READLINE=ON \
	-DWITH_SSL=system \
	-DWITH_ZLIB=system

gcc $CFLAGS $LDFLAGS -o scriptstub "-DLIBDIR=\"%{_libdir}/mysql\"" %{SOURCE4}

make %{?_smp_mflags} VERBOSE=1

# regular build will make libmysqld.a but not libmysqld.so :-(
mkdir libmysqld/work
cd libmysqld/work
ar -x ../libmysqld.a
# these result in missing dependencies: (filed upstream as bug 59104)
rm -f sql_binlog.cc.o rpl_utility.cc.o
gcc $CFLAGS $LDFLAGS -shared -Wl,-soname,libmysqld.so.0 -o libmysqld.so.0.0.1 \
	*.o \
	-lpthread -laio -lcrypt -lssl -lcrypto -lz -lrt -lstdc++ -ldl -lm -lc
# this is to check that we built a complete library
cp %{SOURCE9} .
ln -s libmysqld.so.0.0.1 libmysqld.so.0
gcc -I../../include $CFLAGS mysql-embedded-check.c libmysqld.so.0
LD_LIBRARY_PATH=. ldd ./a.out
cd ../..

%if %runselftest
  # hack to let 32- and 64-bit tests run concurrently on same build machine
  case `uname -m` in
    ppc64 | s390x | x86_64 | sparc64 )
      MTR_BUILD_THREAD=7
      ;;
    *)
      MTR_BUILD_THREAD=11
      ;;
  esac
  export MTR_BUILD_THREAD

  make test

  # The cmake build scripts don't provide any simple way to control the
  # options for mysql-test-run, so ignore the make target and just call it
  # manually.  Nonstandard options chosen are:
  # --force to continue tests after a failure
  # no retries please
  # test SSL with --ssl
  # avoid redundant test runs with --binlog-format=mixed
  # increase timeouts to prevent unwanted failures during mass rebuilds
  (
    cd mysql-test
    perl ./mysql-test-run.pl --force --retry=0 --ssl --mysqld=--binlog-format=mixed --suite-timeout=720 --testcase-timeout=30
    # cmake build scripts will install the var cruft if left alone :-(
    rm -rf var
  )
%endif


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/var/log/mysql \
         %{buildroot}/var/lib/mysqllogs \
         %{buildroot}/var/lib/mysqltmp

make DESTDIR=%{buildroot} install

# List the installed tree for RPM package maintenance purposes.
find %{buildroot} -print | sed "s|^%{buildroot}||" | sort > ROOTFILES

# multilib header hacks
# we only apply this to known Red Hat multilib arches, per bug #181335
case `uname -i` in
  i386 | x86_64 | ppc | ppc64 | s390 | s390x | sparc | sparc64 )
    mv %{buildroot}/usr/include/mysql/my_config.h %{buildroot}/usr/include/mysql/my_config_`uname -i`.h
    install -m 644 %{SOURCE5} %{buildroot}/usr/include/mysql/
    ;;
  *)
    ;;
esac

# cmake generates some completely wacko references to -lprobes_mysql when
# building with dtrace support.  Haven't found where to shut that off,
# so resort to this blunt instrument.  While at it, let's not reference
# libmysqlclient_r anymore either.
sed -e 's/-lprobes_mysql//' -e 's/-lmysqlclient_r/-lmysqlclient/' \
	${RPM_BUILD_ROOT}%{_bindir}/mysql_config >mysql_config.tmp
cp -f mysql_config.tmp ${RPM_BUILD_ROOT}%{_bindir}/mysql_config
chmod 755 ${RPM_BUILD_ROOT}%{_bindir}/mysql_config

mkdir -p %{buildroot}/var/log
touch %{buildroot}/var/log/mysqld.log

mkdir -p %{buildroot}/etc/rc.d/init.d
mkdir -p %{buildroot}/var/run/mysqld
install -m 0755 -d %{buildroot}/var/lib/mysql
install -m 0755 %{SOURCE2} %{buildroot}/etc/rc.d/init.d/mysqld

# Fix funny permissions that cmake build scripts apply to config files
chmod 644 ${RPM_BUILD_ROOT}%{_datadir}/mysql/config.*.ini

# Fix scripts for multilib safety
mv ${RPM_BUILD_ROOT}%{_bindir}/mysqlbug ${RPM_BUILD_ROOT}%{_libdir}/mysql/mysqlbug
install -m 0755 scriptstub ${RPM_BUILD_ROOT}%{_bindir}/mysqlbug
mv ${RPM_BUILD_ROOT}%{_bindir}/mysql_config ${RPM_BUILD_ROOT}%{_libdir}/mysql/mysql_config
install -m 0755 scriptstub ${RPM_BUILD_ROOT}%{_bindir}/mysql_config

# install my-55-terse.cnf
install -m 0644 %{SOURCE100} ${RPM_BUILD_ROOT}%{_sysconfdir}/my.cnf

# logrotate
mkdir -p %{buildroot}/etc/logrotate.d/
install -m 0644 %{SOURCE102} %{buildroot}/etc/logrotate.d/mysqld

# Environment file
install -m 755 -d $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig
install -m 644 %{SOURCE11} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/mysqld

# Remove libmysqld.a, install libmysqld.so
rm -f ${RPM_BUILD_ROOT}%{_libdir}/mysql/libmysqld.a
install -m 0755 libmysqld/work/libmysqld.so.0.0.1 ${RPM_BUILD_ROOT}%{_libdir}/mysql/libmysqld.so.0.0.1
ln -s libmysqld.so.0.0.1 ${RPM_BUILD_ROOT}%{_libdir}/mysql/libmysqld.so.0
ln -s libmysqld.so.0 ${RPM_BUILD_ROOT}%{_libdir}/mysql/libmysqld.so

# libmysqlclient_r is no more.  Upstream tries to replace it with symlinks
# but that really doesn't work (wrong soname in particular).  We'll keep
# just the devel libmysqlclient_r.so link, so that rebuilding without any
# source change is enough to get rid of dependency on libmysqlclient_r.
rm -f ${RPM_BUILD_ROOT}%{_libdir}/mysql/libmysqlclient_r.so*
ln -s libmysqlclient.so ${RPM_BUILD_ROOT}%{_libdir}/mysql/libmysqlclient_r.so

# mysql-test includes one executable that doesn't belong under /usr/share,
# so move it and provide a symlink
mv ${RPM_BUILD_ROOT}%{_datadir}/mysql-test/lib/My/SafeProcess/my_safe_process ${RPM_BUILD_ROOT}%{_bindir}
ln -s ../../../../../bin/my_safe_process ${RPM_BUILD_ROOT}%{_datadir}/mysql-test/lib/My/SafeProcess/my_safe_process

# Remove files that %%doc will install in preferred location
rm -f ${RPM_BUILD_ROOT}/usr/COPYING
rm -f ${RPM_BUILD_ROOT}/usr/README

# Remove files we don't want installed at all
rm -f ${RPM_BUILD_ROOT}/usr/INSTALL-BINARY
rm -f ${RPM_BUILD_ROOT}/usr/docs/ChangeLog
rm -f ${RPM_BUILD_ROOT}/usr/data/mysql/.empty
rm -f ${RPM_BUILD_ROOT}/usr/data/test/.empty
rm -rf ${RPM_BUILD_ROOT}/usr/share/mysql/solaris/
# should move this to /etc/ ?
rm -f ${RPM_BUILD_ROOT}%{_bindir}/mysqlaccess.conf
rm -f ${RPM_BUILD_ROOT}%{_libdir}/mysql/*.a
rm -f ${RPM_BUILD_ROOT}%{_datadir}/mysql/binary-configure
rm -f ${RPM_BUILD_ROOT}%{_datadir}/mysql/magic
rm -f ${RPM_BUILD_ROOT}%{_datadir}/mysql/ndb-config-2-node.ini
rm -f ${RPM_BUILD_ROOT}%{_datadir}/mysql/mysql.server
rm -f ${RPM_BUILD_ROOT}%{_datadir}/mysql/mysqld_multi.server
rm -f ${RPM_BUILD_ROOT}%{_datadir}/mysql/mysql-log-rotate
rm -f ${RPM_BUILD_ROOT}%{_mandir}/man1/comp_err.1*
rm -f ${RPM_BUILD_ROOT}%{_mandir}/man1/mysql-stress-test.pl.1*
rm -f ${RPM_BUILD_ROOT}%{_mandir}/man1/mysql-test-run.pl.1*

mkdir -p %{buildroot}/etc/ld.so.conf.d
echo "%{_libdir}/mysql" > %{buildroot}/etc/ld.so.conf.d/%{name}-%{_arch}.conf

# copy additional docs into build tree so %%doc will find them
cp %{SOURCE6} README.mysql-docs
cp %{SOURCE7} README.mysql-license


%clean
rm -rf %{buildroot}


%pre server
/usr/sbin/groupadd -g 27 mysql >/dev/null 2>&1 || :
/usr/sbin/useradd -M -o -r -d /var/lib/mysql -s /bin/bash \
    -c "MySQL Server" -u 27 mysql -g mysql > /dev/null 2>&1 || :


%post libs
/sbin/ldconfig


%post server
if [ $1 = 1 ]; then
    /sbin/chkconfig --add mysqld
fi
/bin/chmod 0755 /var/lib/mysql
/bin/touch /var/log/mysqld.log


%preun server
if [ $1 = 0 ]; then
    /sbin/service mysqld stop >/dev/null 2>&1
    /sbin/chkconfig --del mysqld
fi


%postun libs
if [ $1 = 0 ] ; then
    /sbin/ldconfig
fi


%postun server
if [ $1 -ge 1 ]; then
    /sbin/service mysqld condrestart >/dev/null 2>&1 || :
fi


%files
%defattr(-,root,root)
%doc README COPYING README.mysql-license
%doc README.mysql-docs

%{_bindir}/msql2mysql
%{_bindir}/mysql
%{_bindir}/mysql_config
%{_bindir}/mysql_find_rows
%{_bindir}/mysql_waitpid
%{_bindir}/mysqlaccess
%{_bindir}/mysqladmin
%{_bindir}/mysqlbinlog
%{_bindir}/mysqlcheck
%{_bindir}/mysqldump
%{_bindir}/mysqlimport
%{_bindir}/mysqlshow
%{_bindir}/mysqlslap
%{_bindir}/my_print_defaults
%{_bindir}/mysql_embedded
%{_bindir}/mysql_plugin

%{_mandir}/man1/mysql.1*
%{_mandir}/man1/mysql_config.1*
%{_mandir}/man1/mysql_find_rows.1*
%{_mandir}/man1/mysql_waitpid.1*
%{_mandir}/man1/mysqlaccess.1*
%{_mandir}/man1/mysqladmin.1*
%{_mandir}/man1/mysqldump.1*
%{_mandir}/man1/mysqlshow.1*
%{_mandir}/man1/mysqlslap.1*
%{_mandir}/man1/my_print_defaults.1*
%{_mandir}/man1/mysql_plugin.1.gz

%{_libdir}/mysql/mysql_config


%files libs
%defattr(-,root,root)
%doc README COPYING README.mysql-license
# although the default my.cnf contains only server settings, we put it in the
# libs package because it can be used for client settings too.
%config(noreplace) /etc/my.cnf
%dir %{_libdir}/mysql
%{_libdir}/mysql/libmysqlclient.so.*
/etc/ld.so.conf.d/*

%dir %{_datadir}/mysql
%{_datadir}/mysql/english
%lang(cs) %{_datadir}/mysql/czech
%lang(da) %{_datadir}/mysql/danish
%lang(nl) %{_datadir}/mysql/dutch
%lang(et) %{_datadir}/mysql/estonian
%lang(fr) %{_datadir}/mysql/french
%lang(de) %{_datadir}/mysql/german
%lang(el) %{_datadir}/mysql/greek
%lang(hu) %{_datadir}/mysql/hungarian
%lang(it) %{_datadir}/mysql/italian
%lang(ja) %{_datadir}/mysql/japanese
%lang(ko) %{_datadir}/mysql/korean
%lang(no) %{_datadir}/mysql/norwegian
%lang(no) %{_datadir}/mysql/norwegian-ny
%lang(pl) %{_datadir}/mysql/polish
%lang(pt) %{_datadir}/mysql/portuguese
%lang(ro) %{_datadir}/mysql/romanian
%lang(ru) %{_datadir}/mysql/russian
%lang(sr) %{_datadir}/mysql/serbian
%lang(sk) %{_datadir}/mysql/slovak
%lang(es) %{_datadir}/mysql/spanish
%lang(sv) %{_datadir}/mysql/swedish
%lang(uk) %{_datadir}/mysql/ukrainian
%{_datadir}/mysql/charsets


%files server
%defattr(-,root,root)
%doc support-files/*.cnf my-55-verbose.cnf
%config(noreplace) %{_sysconfdir}/logrotate.d/mysqld

%{_bindir}/myisamchk
%{_bindir}/myisam_ftdump
%{_bindir}/myisamlog
%{_bindir}/myisampack
%{_bindir}/mysql_convert_table_format
%{_bindir}/mysql_fix_extensions
%{_bindir}/mysql_install_db
%{_bindir}/mysql_secure_installation
%{_bindir}/mysql_setpermission
%{_bindir}/mysql_tzinfo_to_sql
%{_bindir}/mysql_upgrade
%{_bindir}/mysql_zap
%{_bindir}/mysqlbug
%{_bindir}/mysqldumpslow
%{_bindir}/mysqld_multi
%{_bindir}/mysqld_safe
%{_bindir}/mysqlhotcopy
%{_bindir}/mysqltest
%{_bindir}/innochecksum
%{_bindir}/perror
%{_bindir}/replace
%{_bindir}/resolve_stack_dump
%{_bindir}/resolveip

%{_libexecdir}/mysqld

%{_libdir}/mysql/mysqlbug

%{_libdir}/mysql/plugin

%{_mandir}/man1/msql2mysql.1*
%{_mandir}/man1/myisamchk.1*
%{_mandir}/man1/myisamlog.1*
%{_mandir}/man1/myisampack.1*
%{_mandir}/man1/mysql_convert_table_format.1*
%{_mandir}/man1/myisam_ftdump.1*
%{_mandir}/man1/mysql.server.1*
%{_mandir}/man1/mysql_fix_extensions.1*
%{_mandir}/man1/mysql_install_db.1*
%{_mandir}/man1/mysql_secure_installation.1*
%{_mandir}/man1/mysql_upgrade.1*
%{_mandir}/man1/mysql_zap.1*
%{_mandir}/man1/mysqlbug.1*
%{_mandir}/man1/mysqldumpslow.1*
%{_mandir}/man1/mysqlbinlog.1*
%{_mandir}/man1/mysqlcheck.1*
%{_mandir}/man1/mysqld_multi.1*
%{_mandir}/man1/mysqld_safe.1*
%{_mandir}/man1/mysqlhotcopy.1*
%{_mandir}/man1/mysqlimport.1*
%{_mandir}/man1/mysqlman.1*
%{_mandir}/man1/mysql_setpermission.1*
%{_mandir}/man1/mysqltest.1*
%{_mandir}/man1/innochecksum.1*
%{_mandir}/man1/perror.1*
%{_mandir}/man1/replace.1*
%{_mandir}/man1/resolve_stack_dump.1*
%{_mandir}/man1/resolveip.1*
%{_mandir}/man1/mysql_tzinfo_to_sql.1*
%{_mandir}/man8/mysqld.8*

%{_datadir}/mysql/errmsg-utf8.txt
%{_datadir}/mysql/fill_help_tables.sql
%{_datadir}/mysql/mysql_system_tables.sql
%{_datadir}/mysql/mysql_system_tables_data.sql
%{_datadir}/mysql/mysql_test_data_timezone.sql
%{_datadir}/mysql/my-*.cnf
%{_datadir}/mysql/config.*.ini

/etc/rc.d/init.d/mysqld
%config(noreplace) %{_sysconfdir}/sysconfig/mysqld
%attr(0755,mysql,mysql) %dir /var/run/mysqld
%attr(0755,mysql,mysql) %dir /var/lib/mysql
%attr(0640,mysql,mysql) %config(noreplace) %verify(not md5 size mtime) /var/log/mysqld.log
%attr(0755,mysql,mysql) %dir %{_localstatedir}/lib/mysqltmp/
%attr(0755,mysql,mysql) %dir /var/lib/mysqllogs
%attr(0755,mysql,mysql) %dir /var/log/mysql/


%files devel
%defattr(-,root,root)
%{_includedir}/mysql
%{_datadir}/aclocal/mysql.m4
%{_libdir}/mysql/libmysqlclient.so
%{_libdir}/mysql/libmysqlclient_r.so


%files embedded
%defattr(-,root,root)
%doc README COPYING README.mysql-license
%{_libdir}/mysql/libmysqld.so.*


%files embedded-devel
%defattr(-,root,root)
%{_libdir}/mysql/libmysqld.so
%{_bindir}/mysql_client_test_embedded
%{_bindir}/mysqltest_embedded
%{_mandir}/man1/mysql_client_test_embedded.1*
%{_mandir}/man1/mysqltest_embedded.1*


%files bench
%defattr(-,root,root)
%{_datadir}/sql-bench


%files test
%defattr(-,root,root)
%{_bindir}/mysql_client_test
%{_bindir}/my_safe_process
%attr(-,mysql,mysql) %{_datadir}/mysql-test

%{_mandir}/man1/mysql_client_test.1*


%changelog
* Fri Feb 05 2016 Ben Harper <ben.harper@rackspace.com> - 5.5.48-1.ius
- Latest upstream

* Mon Dec 07 2015 Ben Harper <ben.harper@rackspace.com> - 5.5.47-1.ius
- Latest upstream

* Fri Nov 13 2015 Carl George <carl.george@rackspace.com> - 5.5.46-2.ius
- Add _isa macro to provides/requires to assist with dependency resolution

* Thu Oct 01 2015 Carl George <carl.george@rackspace.com> - 5.5.46-1.ius
- Latest upstream

* Fri Jul 24 2015 Ben Harper <ben.harper@rackspace.com> - 5.5.45-1.ius
- Latest upstream
- Patch319 fixed upstream

* Wed Jun 17 2015 Ben Harper <ben.harper@rackspace.com> - 5.5.44-2.ius
- add Patch319 from http://pkgs.fedoraproject.org/cgit/community-mysql.git/tree/community-mysql-dh1024.patch
  see https://github.com/iuscommunity-pkg/mysql55/issues/4

* Fri May 29 2015 Carl George <carl.george@rackspace.com> - 5.5.44-1.ius
- Latest upstream
- Patch318 fixed upstream

* Tue Apr 07 2015 Carl George <carl.george@rackspace.com> - 5.5.43-1.ius
- Latest upstream

* Tue Feb 03 2015 Carl George <carl.george@rackspace.com> - 5.5.42-1.ius
- Latest upstream
- Patch4 and Patch200 resolved upstream

* Thu Dec 18 2014 Ben Harper <ben.harper@rackspace.com> - 5.5.41-2.ius
- Add Patch200

* Fri Nov 28 2014 Carl George <carl.george@rackspace.com> - 5.5.41-1.ius
- Latest upstream

* Mon Nov 10 2014 Ben Harper <ben.harper@rackspace.com> - 5.5-40-2.ius
- update mysql.init, see LP bug 1390900

* Wed Sep 24 2014 Carl George <carl.george@rackspace.com> - 5.5.40-1.ius
- Latest upstream

* Thu Jul 31 2014 Carl George <carl.george@rackspace.com> - 5.5.39-1.ius
- Latest sources from upstream
- While compiling libmysqld.so, disable explicit inclusion of probes_mysql.o
  since it is now underneath libmysqld/work and thus pulled in via wildcard.

* Tue Jun 03 2014 Ben Harper <ben.harper@rackspace.com> - 5.5.38-1.ius
- Latest sources from upstream

* Thu Mar 27 2014 Carl George <carl.george@rackspace.com> - 5.5.37-1.ius
- Latest sources from upstream

* Fri Jan 31 2014 Ben Harper <ben.harper@rackspace.com> - 5.5.36-1.ius
- Latest sources from upstream

* Wed Dec 04 2013 Ben Harper <ben.harper@rackspace.com> - 5.5.35-1.ius
- Latest sources from upstream
- remove conflicts added in 5.5.34-2.ius
- changed Source0 to URL to tarball since Oracle has removed non-free
  documentation and tarball is straightforward to download

* Thu Oct 24 2013 Ben Harper <ben.harper@rackspace.com> - 5.5.34-2.ius
- add conflicts for new mysql55 packages in base for EL 5.10

* Fri Sep 20 2013 Ben Harper <ben.harper@rackspace.com> - 5.5.34-1.ius
- Latest sources from upstream

* Mon Sep 16 2013 Ben Harper <ben.harper@rackspace.com> - 5.5.33-2.ius
- add mysqld.sysconfig to mysql55-server
- increase timeouts in mysql.init

* Fri Aug 16 2013 Ben Harper <ben.harper@rackspace.com> - 5.5.33-1.ius
- Latest sources from upstream
- Added Patch22 from mysql-5.5.32-1.fc17.src.rpm

* Thu Apr 18 2013 Ben Harper <ben.harper@rackspace.com> - 5.5.31-1.ius
- Latest sources from upstream
- Patch318 add as SSL_OP_NO_COMPRESSION is not available for RHEL 5 openssl

* Mon Feb 04 2013 Ben Harper <ben.harper@rackspace.com> - 5.5.30-1.ius
- Latest sources from upstream

* Fri Dec 21 2012 Ben Harper <ben.harper@rackspace.com> - 5.5.29-1.ius
- Latest sources from upstream

* Thu Nov 01 2012 Jeffrey Ness <jeffrey.ness@rackspace.com> - 5.5.28-2.ius
- Rebuilding against internal 6.3.z

* Mon Oct 1 2012 Ben Harper <ben.harper@rackspace.com> 5.5.28-1.ius
- Latest sources from upstream
- updated patch6 as format changed

* Thu Aug 16 2012 Jeffrey Ness <jeffrey.ness@rackspace.com> 5.5.27-2.ius
- Internal users of mysql55 symlink mysqllogs which breaks on update,
  adding mysqllogs for historic purposes.
- Adding commented logrotate

* Mon Aug 06 2012 Jeffrey Ness <jeffrey.ness@rackspace.com> 5.5.27-1.ius
- Latest sources from upstream

* Tue Jul 31 2012 Jeffrey Ness <jeffrey.ness@rackspace.com> 5.5.25-3.a.ius
- Disable slow-log by default.
- Change path of mysqllogs to /var/log/mysql per LP#1026008
- Removing logrotate for slow-log

* Thu Jun 04 2012 Jeffrey Ness <jeffrey.ness@rackspace.com> 5.5.25-2.a.ius
- Latest sources from upstream, full changelog found at:
  http://dev.mysql.com/doc/refman/5.5/en/news-5-5-25a.html
- A regression bug in the optimizer could cause excessive disk usage for 
  UPDATE statements. (Bug #65745, Bug #14248833)
- Append 'a' to prep line

* Thu May 31 2012 Jeffrey Ness <jeffrey.ness@rackspace.com> 5.5.25-1.ius
- Latest sources from upstream, full changelog found at:
  http://dev.mysql.com/doc/refman/5.5/en/news-5-5-25.html

* Tue May 08 2012 Jeffrey Ness <jeffrey.ness@rackspace.com> 5.5.24-1.ius
- Latest sources from upstream, full changelog found at:
  http://dev.mysql.com/doc/refman/5.5/en/news-5-5-24.html

* Mon Apr 16 2012 Jeffrey Ness <jeffrey.ness@rackspace.com> 5.5.23-1.ius
- Latest sources from upstream, full changelog found at:
  http://dev.mysql.com/doc/refman/5.5/en/news-5-5-23.html

* Mon Feb 21 2012 BJ Dierkes <wdierkes@rackspace.com> 5.5.22-1.ius
- Latest sources from upstream, full changelog found at:
  http://dev.mysql.com/doc/refman/5.5/en/news-5-5-22.html

* Mon Feb 21 2012 Jeffrey Ness <jeffrey.ness@rackspace.com> 5.5.21-1.ius
- Latest sources from upstream, full changelog found at:
  http://dev.mysql.com/doc/refman/5.5/en/news-5-5-21.html

* Thu Jan 12 2012 Jeffrey Ness <jeffrey.ness@rackspace.com> 5.5.20-1.ius
- Latest sources from upstream, full changelog found at:
  http://dev.mysql.com/doc/refman/5.5/en/news-5-5-20.html

* Mon Dec 12 2011 Jeffrey Ness <jeffrey.ness@rackspace.com> 5.5.19-1.ius
- Latest sources from upstream, full changelog found at:
  http://dev.mysql.com/doc/refman/5.5/en/news-5-5-19.html

* Tue Nov 22 2011 Jeffrey Ness <jeffrey.ness@rackspace.com> 5.5.18-1.ius
- Latest sources from upstream, full changelog found at:
  http://dev.mysql.com/doc/refman/5.5/en/news-5-5-18.html

* Mon Oct 24 2011 Jeffrey Ness <jeffrey.ness@rackspace.com> 5.5.17-1.ius
- Latest sources from upstream, full changelog found at:
  http://dev.mysql.com/doc/refman/5.5/en/news-5-5-17.html

* Mon Sep 19 2011 Jeffrey Ness <jeffrey.ness@rackspace.com> 5.5.16-1.ius
- Latest sources from upstream, full changelog found at:
  http://dev.mysql.com/doc/refman/5.5/en/news-5-5-16.html
- New files added to source:
 /usr/bin/mysql_embedded
 /usr/bin/mysql_plugin
 /usr/share/man/man1/mysql_plugin.1.gz

* Thu Aug 04 2011 Jeffrey Ness <jeffrey.ness@rackspace.com> 5.5.15-3.ius
- Sub package lib and server now provide config(mysql-*) per Launchpad 
  https://bugs.launchpad.net/ius/+bug/746115

* Thu Jul 28 2011 Jeffrey Ness <jeffrey.ness@rackspace.com> 5.5.15-2.ius
- Updating disabled patch #9

* Thu Jul 28 2011 Jeffrey Ness <jeffrey.ness@rackspace.com> 5.5.15-1.ius
- Latest sources from upstream, full changelog found at:
  http://dev.mysql.com/doc/refman/5.5/en/news-5-5-15.html

* Wed Jul 13 2011 BJ Dierkes <wdierkes@rackspace.com> 5.5.14-2.ius
- Requires: mysqlclient15 (only el5) and mysqlclient16 (only el6)

* Wed Jul 06 2011 Jeffrey Ness <jeffrey.ness@rackspace.com> 5.5.14-1.ius
- Latest sources from upstream, full changelog found at:
  http://dev.mysql.com/doc/refman/5.5/en/news-5-5-14.html

* Wed Jun 01 2011 Jeffrey Ness <jeffrey.ness@rackspace.com> 5.5.13-1.ius
- Latest sources from upstream, full changelog found at:
  http://dev.mysql.com/doc/refman/5.5/en/news-5-5-13.html

* Tue May 09 2011 Jeffrey Ness <jeffrey.ness@rackspace.com> 5.5.12-1.ius
- Latest sources from upstream, full changelog found at:
  http://dev.mysql.com/doc/refman/5.5/en/news-5-5-12.html

* Tue Apr 05 2011 Jeffrey Ness <jeffrey.ness@rackspace.com> 5.5.11-1.ius
- Latest sources from upstream, full changelog found at:
  http://dev.mysql.com/doc/refman/5.5/en/news-5-5-11.html

* Wed Mar 16 2011 Jeffrey Ness <jeffrey.ness@rackspace.com> 5.5.10-1.ius
- Latest sources from upstream, full changelog found at:
  http://dev.mysql.com/doc/refman/5.5/en/news-5-5-10.html

* Wed Feb 09 2011 BJ Dierkes <wdierkes@rackspace.com> 5.5.9-1.ius
- Added COMPLATION_COMMENT to build

* Wed Feb 09 2011 Jeffrey Ness <jeffrey.ness@rackspace.com> 5.5.9-1.ius
- Latest sources from upstream, full changelog found at:
  http://dev.mysql.com/doc/refman/5.5/en/news-5-5-9.html
- Removed: Patch300: mysql-5.5.8-bug58350.patch

* Tue Feb 01 2011 BJ Dierkes <wdierkes@rackspace.com> 5.5.8-7.ius
- Adding mysqltmp/mysqllogs directories
- Added Source100: my-55-terse.cnf (default), and 
  Source101: my-55-verbose.cnf which resolves LP#711271
- Added Source103: mysql.logrotate (for mysqllogs, not mysqld.log)
- BuildRequires: perl-Time-HiRes on el6

* Mon Jan 24 2011 Jeffrey Ness <jeffrey.ness@rackspace.com> 5.5.8-6.ius
- Added Requires: mysqlclient15 to resolve perl-DBD-MySQL resolution
  issues

* Fri Jan 21 2011 BJ Dierkes <wdierkes@rackspace.com> 5.5.8-5.ius
- Fix -server %%post script to properly add mysql user if missing.

* Thu Jan 06 2011 BJ Dierkes <wdierkes@rackspace.com> 5.5.8-4.ius
- Porting from Fedora Rawhide to IUS
- Package renamed as mysql55
- Adding Patch300: mysql-5.5.8-bug58350.patch which resolves MySQL Bug
  58350

* Mon Jan  3 2011 Tom Lane <tgl@redhat.com> 5.5.8-3
- my_print_help, load_defaults, free_defaults, and handle_options all turn
  out to be documented/recommended in Paul DuBois' MySQL book, so we'd better
  consider them part of the de-facto API.
Resolves: #666728

* Mon Dec 27 2010 Tom Lane <tgl@redhat.com> 5.5.8-2
- Add mysql_client_errors[] to the set of exported libmysqlclient symbols;
  needed by PHP.

* Thu Dec 23 2010 Tom Lane <tgl@redhat.com> 5.5.8-1
- Update to MySQL 5.5.8 (major version bump).  Note this includes removal
  of libmysqlclient_r.so.
- Add a linker version script to hide libmysqlclient functions that aren't
  part of the documented API.

* Mon Nov  1 2010 Tom Lane <tgl@redhat.com> 5.1.52-1
- Update to MySQL 5.1.52, for various fixes described at
  http://dev.mysql.com/doc/refman/5.1/en/news-5-1-52.html
Resolves: #646569

* Thu Oct  7 2010 Tom Lane <tgl@redhat.com> 5.1.51-2
- Re-disable the outfile_loaddata test, per report from Dan Horak.

* Wed Oct  6 2010 Tom Lane <tgl@redhat.com> 5.1.51-1
- Update to MySQL 5.1.51, for various fixes described at
  http://dev.mysql.com/doc/refman/5.1/en/news-5-1-51.html

* Sat Aug 28 2010 Tom Lane <tgl@redhat.com> 5.1.50-2
- Include my_compiler.h in distribution, per upstream bug #55846.
  Otherwise PHP, for example, won't build.

* Sat Aug 28 2010 Tom Lane <tgl@redhat.com> 5.1.50-1
- Update to MySQL 5.1.50, for various fixes described at
  http://dev.mysql.com/doc/refman/5.1/en/news-5-1-50.html
  http://dev.mysql.com/doc/refman/5.1/en/news-5-1-49.html

* Wed Jul 14 2010 Tom Lane <tgl@redhat.com> 5.1.48-3
- Fix FTBFS with gcc 4.5.
Related: #614293

* Tue Jul 13 2010 Tom Lane <tgl@redhat.com> 5.1.48-2
- Duplicate COPYING and EXCEPTIONS-CLIENT in -libs and -embedded subpackages,
  to ensure they are available when any subset of mysql RPMs are installed,
  per revised packaging guidelines
- Allow init script's STARTTIMEOUT/STOPTIMEOUT to be overridden from sysconfig
Related: #609734

* Mon Jun 21 2010 Tom Lane <tgl@redhat.com> 5.1.48-1
- Update to MySQL 5.1.48, for various fixes described at
  http://dev.mysql.com/doc/refman/5.1/en/news-5-1-48.html
  including a fix for CVE-2010-2008
Related: #614214

* Fri Jun  4 2010 Tom Lane <tgl@redhat.com> 5.1.47-2
- Add back "partition" storage engine
Resolves: #597390
- Fix broken "federated" storage engine plugin
Related: #587170
- Read all certificates in SSL certificate files, to support chained certs
Related: #598656

* Mon May 24 2010 Tom Lane <tgl@redhat.com> 5.1.47-1
- Update to MySQL 5.1.47, for various fixes described at
  http://dev.mysql.com/doc/refman/5.1/en/news-5-1-47.html
  including fixes for CVE-2010-1848, CVE-2010-1849, CVE-2010-1850
Resolves: #592862
Resolves: #583717
- Create mysql group explicitly in pre-server script, to ensure correct GID
Related: #594155

* Sat Apr 24 2010 Tom Lane <tgl@redhat.com> 5.1.46-1
- Update to MySQL 5.1.46, for various fixes described at
  http://dev.mysql.com/doc/refman/5.1/en/news-5-1-46.html

* Thu Mar 25 2010 Tom Lane <tgl@redhat.com> 5.1.45-2
- Fix multiple problems described in upstream bug 52019, because regression
  tests fail on PPC if we don't.

* Wed Mar 24 2010 Tom Lane <tgl@redhat.com> 5.1.45-1
- Update to MySQL 5.1.45, for various fixes described at
  http://dev.mysql.com/doc/refman/5.1/en/news-5-1-45.html

* Sun Feb 21 2010 Tom Lane <tgl@redhat.com> 5.1.44-2
- Add "Obsoletes: mysql-cluster" to fix upgrade-in-place from F-12
- Bring init script into some modicum of compliance with Fedora/LSB standards
Related: #557711
Related: #562749

* Sat Feb 20 2010 Tom Lane <tgl@redhat.com> 5.1.44-1
- Update to MySQL 5.1.44, for various fixes described at
  http://dev.mysql.com/doc/refman/5.1/en/news-5-1-44.html
- Remove mysql.info, which is not freely redistributable
Resolves: #560181
- Revert broken upstream fix for their bug 45058
Resolves: #566547

* Sat Feb 13 2010 Tom Lane <tgl@redhat.com> 5.1.43-2
- Remove mysql-cluster, which is no longer supported by upstream in this
  source distribution.  If we want it we'll need a separate SRPM for it.

* Fri Feb 12 2010 Tom Lane <tgl@redhat.com> 5.1.43-1
- Update to MySQL 5.1.43, for various fixes described at
  http://dev.mysql.com/doc/refman/5.1/en/news-5-1-43.html

* Fri Jan 29 2010 Tom Lane <tgl@redhat.com> 5.1.42-7
- Add backported patch for CVE-2008-7247 (upstream bug 39277)
Related: #543619
- Use non-expired certificates for SSL testing (upstream bug 50702)

* Tue Jan 26 2010 Tom Lane <tgl@redhat.com> 5.1.42-6
- Emit explicit error message if user tries to build RPM as root
Related: #558915

* Wed Jan 20 2010 Tom Lane <tgl@redhat.com> 5.1.42-5
- Correct Source0: tag and comment to reflect how to get the tarball

* Fri Jan  8 2010 Tom Lane <tgl@redhat.com> 5.1.42-4
- Disable symbolic links by default in /etc/my.cnf
Resolves: #553652

* Tue Jan  5 2010 Tom Lane <tgl@redhat.com> 5.1.42-3
- Remove static libraries (.a files) from package, per packaging guidelines
- Change %%define to %%global, per packaging guidelines

* Sat Jan  2 2010 Tom Lane <tgl@redhat.com> 5.1.42-2
- Disable building the innodb plugin; it tickles assorted gcc bugs and
  doesn't seem entirely ready for prime time anyway.

* Fri Jan  1 2010 Tom Lane <tgl@redhat.com> 5.1.42-1
- Update to MySQL 5.1.42, for various fixes described at
  http://dev.mysql.com/doc/refman/5.1/en/news-5-1-42.html
- Start mysqld_safe with --basedir=/usr, to avoid unwanted SELinux messages
Resolves: #547485

* Thu Dec 17 2009 Tom Lane <tgl@redhat.com> 5.1.41-2
- Stop waiting during "service mysqld start" if mysqld_safe exits
Resolves: #544095

* Mon Nov 23 2009 Tom Lane <tgl@redhat.com> 5.1.41-1
- Update to MySQL 5.1.41, for various fixes described at
  http://dev.mysql.com/doc/refman/5.1/en/news-5-1-41.html
  including fixes for CVE-2009-4019
Related: #540906
- Don't set old_passwords=1; we aren't being bug-compatible with 3.23 anymore
Resolves: #540735

* Tue Nov 10 2009 Tom Lane <tgl@redhat.com> 5.1.40-1
- Update to MySQL 5.1.40, for various fixes described at
  http://dev.mysql.com/doc/refman/5.1/en/news-5-1-40.html
- Do not force the --log-error setting in mysqld init script
Resolves: #533736

* Sat Oct 17 2009 Tom Lane <tgl@redhat.com> 5.1.39-4
- Replace kluge fix for ndbd sparc crash with a real fix (mysql bug 48132)

* Thu Oct 15 2009 Tom Lane <tgl@redhat.com> 5.1.39-3
- Work around two different compiler bugs on sparc, one by backing off
  optimization from -O2 to -O1, and the other with a klugy patch
Related: #529298, #529299
- Clean up bogosity in multilib stub header support: ia64 should not be
  listed (it's not multilib), sparc and sparc64 should be

* Wed Sep 23 2009 Tom Lane <tgl@redhat.com> 5.1.39-2
- Work around upstream bug 46895 by disabling outfile_loaddata test

* Tue Sep 22 2009 Tom Lane <tgl@redhat.com> 5.1.39-1
- Update to MySQL 5.1.39, for various fixes described at
  http://dev.mysql.com/doc/refman/5.1/en/news-5-1-39.html

* Mon Aug 31 2009 Tom Lane <tgl@redhat.com> 5.1.37-5
- Work around unportable assumptions about stpcpy(); re-enable main.mysql test
- Clean up some obsolete parameters to the configure script

* Sat Aug 29 2009 Tom Lane <tgl@redhat.com> 5.1.37-4
- Remove one misguided patch; turns out I was chasing a glibc bug
- Temporarily disable "main.mysql" test; there's something broken there too,
  but we need to get mysql built in rawhide for dependency reasons

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 5.1.37-3
- rebuilt with new openssl

* Fri Aug 14 2009 Tom Lane <tgl@redhat.com> 5.1.37-2
- Add a couple of patches to improve the probability of the regression tests
  completing in koji builds

* Sun Aug  2 2009 Tom Lane <tgl@redhat.com> 5.1.37-1
- Update to MySQL 5.1.37, for various fixes described at
  http://dev.mysql.com/doc/refman/5.1/en/news-5-1-37.html

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.1.36-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jul 10 2009 Tom Lane <tgl@redhat.com> 5.1.36-1
- Update to MySQL 5.1.36, for various fixes described at
  http://dev.mysql.com/doc/refman/5.1/en/news-5-1-36.html

* Sat Jun  6 2009 Tom Lane <tgl@redhat.com> 5.1.35-1
- Update to MySQL 5.1.35, for various fixes described at
  http://dev.mysql.com/doc/refman/5.1/en/news-5-1-35.html
- Ensure that /var/lib/mysql is created with the right SELinux context
Resolves: #502966

* Fri May 15 2009 Tom Lane <tgl@redhat.com> 5.1.34-1
- Update to MySQL 5.1.34, for various fixes described at
  http://dev.mysql.com/doc/refman/5.1/en/news-5-1-34.html
- Increase startup timeout per bug #472222

* Wed Apr 15 2009 Tom Lane <tgl@redhat.com> 5.1.33-2
- Increase stack size of ndbd threads for safety's sake.
Related: #494631

* Tue Apr  7 2009 Tom Lane <tgl@redhat.com> 5.1.33-1
- Update to MySQL 5.1.33.
- Disable use of pthread_setschedparam; doesn't work the way code expects.
Related: #477624

* Wed Mar  4 2009 Tom Lane <tgl@redhat.com> 5.1.32-1
- Update to MySQL 5.1.32.

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.1.31-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb 13 2009 Tom Lane <tgl@redhat.com> 5.1.31-1
- Update to MySQL 5.1.31.

* Thu Jan 22 2009 Tom Lane <tgl@redhat.com> 5.1.30-2
- hm, apparently --with-innodb and --with-ndbcluster are still needed
  even though no longer documented ...

* Thu Jan 22 2009 Tom Lane <tgl@redhat.com> 5.1.30-1
- Update to MySQL 5.1.30.  Note that this includes an ABI break for
  libmysqlclient (it's now got .so major version 16).
- This also updates mysql for new openssl build

* Wed Oct  1 2008 Tom Lane <tgl@redhat.com> 5.0.67-2
- Build the "embedded server" library, and package it in a new sub-RPM
  mysql-embedded, along with mysql-embedded-devel for devel support files.
Resolves: #149829

* Sat Aug 23 2008 Tom Lane <tgl@redhat.com> 5.0.67-1
- Update to mysql version 5.0.67
- Move mysql_config's man page to base package, again (apparently I synced
  that change the wrong way while importing specfile changes for ndbcluster)

* Sun Jul 27 2008 Tom Lane <tgl@redhat.com> 5.0.51a-2
- Enable ndbcluster support
Resolves: #163758
- Suppress odd crash messages during package build, caused by trying to
  build dbug manual (which we don't install anyway) with dbug disabled
Resolves: #437053
- Improve mysql.init to pass configured datadir to mysql_install_db,
  and to force user=mysql for both mysql_install_db and mysqld_safe.
Related: #450178

* Mon Mar  3 2008 Tom Lane <tgl@redhat.com> 5.0.51a-1
- Update to mysql version 5.0.51a

* Mon Mar  3 2008 Tom Lane <tgl@redhat.com> 5.0.45-11
- Fix mysql-stack-guard patch to work correctly on IA64
- Fix mysql.init to wait correctly when socket is not in default place
Related: #435494

* Mon Mar 03 2008 Dennis Gilmore <dennis@ausil.us> 5.0.45-10
- add sparc64 to 64 bit arches for test suite checking
- add sparc, sparcv9 and sparc64 to multilib handling

* Thu Feb 28 2008 Tom Lane <tgl@redhat.com> 5.0.45-9
- Fix the stack overflow problem encountered in January.  It seems the real
issue is that the buildfarm machines were moved to RHEL5, which uses 64K not
4K pages on PPC, and because RHEL5 takes the guard area out of the requested
thread stack size we no longer had enough headroom.
Related: #435337

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 5.0.45-8
- Autorebuild for GCC 4.3

* Tue Jan  8 2008 Tom Lane <tgl@redhat.com> 5.0.45-7
- Unbelievable ... upstream still thinks that it's a good idea to have a
  regression test that is guaranteed to begin failing come January 1.
- ... and it seems we need to raise STACK_MIN_SIZE again too.

* Thu Dec 13 2007 Tom Lane <tgl@redhat.com> 5.0.45-6
- Back-port upstream fixes for CVE-2007-5925, CVE-2007-5969, CVE-2007-6303.
Related: #422211

* Wed Dec  5 2007 Tom Lane <tgl@redhat.com> 5.0.45-5
- Rebuild for new openssl

* Sat Aug 25 2007 Tom Lane <tgl@redhat.com> 5.0.45-4
- Seems we need explicit BuildRequires on gawk and procps now
- Rebuild to fix Fedora toolchain issues

* Sun Aug 12 2007 Tom Lane <tgl@redhat.com> 5.0.45-3
- Recent perl changes in rawhide mean we need a more specific BuildRequires

* Thu Aug  2 2007 Tom Lane <tgl@redhat.com> 5.0.45-2
- Update License tag to match code.
- Work around recent Fedora change that makes "open" a macro name.

* Sun Jul 22 2007 Tom Lane <tgl@redhat.com> 5.0.45-1
- Update to MySQL 5.0.45
Resolves: #246535
- Move mysql_config's man page to base package
Resolves: #245770
- move my_print_defaults to base RPM, for consistency with Stacks packaging
- mysql user is no longer deleted at RPM uninstall
Resolves: #241912

* Thu Mar 29 2007 Tom Lane <tgl@redhat.com> 5.0.37-2
- Use a less hacky method of getting default values in initscript
Related: #233771, #194596
- Improve packaging of mysql-libs per suggestions from Remi Collet
Resolves: #233731
- Update default /etc/my.cnf ([mysql.server] has been bogus for a long time)

* Mon Mar 12 2007 Tom Lane <tgl@redhat.com> 5.0.37-1
- Update to MySQL 5.0.37
Resolves: #231838
- Put client library into a separate mysql-libs RPM to reduce dependencies
Resolves: #205630

* Fri Feb  9 2007 Tom Lane <tgl@redhat.com> 5.0.33-1
- Update to MySQL 5.0.33
- Install band-aid fix for "view" regression test designed to fail after 2006
- Don't chmod -R the entire database directory tree on every startup
Related: #221085
- Fix unsafe use of install-info
Resolves: #223713
- Cope with new automake in F7
Resolves: #224171

* Thu Nov  9 2006 Tom Lane <tgl@redhat.com> 5.0.27-1
- Update to MySQL 5.0.27 (see CVE-2006-4031, CVE-2006-4226, CVE-2006-4227)
Resolves: #202247, #202675, #203427, #203428, #203432, #203434, #208641
- Fix init script to return status 1 on server start timeout
Resolves: #203910
- Move mysqldumpslow from base package to mysql-server
Resolves: #193559
- Adjust link options for BDB module
Resolves: #199368

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 5.0.22-2.1
- rebuild

* Sat Jun 10 2006 Tom Lane <tgl@redhat.com> 5.0.22-2
- Work around brew's tendency not to clean up failed builds completely,
  by adding code in mysql-testing.patch to kill leftover mysql daemons.

* Thu Jun  8 2006 Tom Lane <tgl@redhat.com> 5.0.22-1
- Update to MySQL 5.0.22 (fixes CVE-2006-2753)
- Install temporary workaround for gcc bug on s390x (bz #193912)

* Tue May  2 2006 Tom Lane <tgl@redhat.com> 5.0.21-2
- Fix bogus perl Requires for mysql-test

* Mon May  1 2006 Tom Lane <tgl@redhat.com> 5.0.21-1
- Update to MySQL 5.0.21

* Mon Mar 27 2006 Tom Lane <tgl@redhat.com> 5.0.18-4
- Modify multilib header hack to not break non-RH arches, per bug #181335
- Remove logrotate script, per bug #180639.
- Add a new mysql-test RPM to carry the regression test files;
  hack up test scripts as needed to make them run in /usr/share/mysql-test.

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 5.0.18-2.1
- bump again for double-long bug on ppc(64)

* Thu Feb  9 2006 Tom Lane <tgl@redhat.com> 5.0.18-2
- err-log option has been renamed to log-error, fix my.cnf and initscript

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 5.0.18-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Thu Jan  5 2006 Tom Lane <tgl@redhat.com> 5.0.18-1
- Update to MySQL 5.0.18

* Thu Dec 15 2005 Tom Lane <tgl@redhat.com> 5.0.16-4
- fix my_config.h for ppc platforms

* Thu Dec 15 2005 Tom Lane <tgl@redhat.com> 5.0.16-3
- my_config.h needs to guard against 64-bit platforms that also define the
  32-bit symbol

* Wed Dec 14 2005 Tom Lane <tgl@redhat.com> 5.0.16-2
- oops, looks like we want uname -i not uname -m

* Mon Dec 12 2005 Tom Lane <tgl@redhat.com> 5.0.16-1
- Update to MySQL 5.0.16
- Add EXCEPTIONS-CLIENT license info to the shipped documentation
- Make my_config.h architecture-independent for multilib installs;
  put the original my_config.h into my_config_$ARCH.h
- Add -fwrapv to CFLAGS so that gcc 4.1 doesn't break it

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Mon Nov 14 2005 Tom Lane <tgl@redhat.com> 5.0.15-3
- Make stop script wait for daemon process to disappear (bz#172426)

* Wed Nov  9 2005 Tom Lane <tgl@redhat.com> 5.0.15-2
- Rebuild due to openssl library update.

* Thu Nov  3 2005 Tom Lane <tgl@redhat.com> 5.0.15-1
- Update to MySQL 5.0.15 (scratch build for now)

* Wed Oct  5 2005 Tom Lane <tgl@redhat.com> 4.1.14-1
- Update to MySQL 4.1.14

* Tue Aug 23 2005 Tom Lane <tgl@redhat.com> 4.1.12-3
- Use politically correct patch name.

* Tue Jul 12 2005 Tom Lane <tgl@redhat.com> 4.1.12-2
- Fix buffer overflow newly exposed in isam code; it's the same issue
  previously found in myisam, and not very exciting, but I'm tired of
  seeing build warnings.

* Mon Jul 11 2005 Tom Lane <tgl@redhat.com> 4.1.12-1
- Update to MySQL 4.1.12 (includes a fix for bz#158688, bz#158689)
- Extend mysql-test-ssl.patch to solve rpl_openssl test failure (bz#155850)
- Update mysql-lock-ssl.patch to match the upstream committed version
- Add --with-isam to re-enable the old ISAM table type, per bz#159262
- Add dependency on openssl-devel per bz#159569
- Remove manual.txt, as upstream decided not to ship it anymore;
  it was redundant with the mysql.info file anyway.

* Mon May  9 2005 Tom Lane <tgl@redhat.com> 4.1.11-4
- Include proper locking for OpenSSL in the server, per bz#155850

* Mon Apr 25 2005 Tom Lane <tgl@redhat.com> 4.1.11-3
- Enable openssl tests during build, per bz#155850
- Might as well turn on --disable-dependency-tracking

* Fri Apr  8 2005 Tom Lane <tgl@redhat.com> 4.1.11-2
- Avoid dependency on <asm/atomic.h>, cause it won't build anymore on ia64.
  This is probably a cleaner solution for bz#143537, too.

* Thu Apr  7 2005 Tom Lane <tgl@redhat.com> 4.1.11-1
- Update to MySQL 4.1.11 to fix bz#152911 as well as other issues
- Move perl-DBI, perl-DBD-MySQL dependencies to server package (bz#154123)
- Override configure thread library test to suppress HAVE_LINUXTHREADS check
- Fix BDB failure on s390x (bz#143537)
- At last we can enable "make test" on all arches

* Fri Mar 11 2005 Tom Lane <tgl@redhat.com> 4.1.10a-1
- Update to MySQL 4.1.10a to fix security vulnerabilities (bz#150868,
  for CAN-2005-0711, and bz#150871 for CAN-2005-0709, CAN-2005-0710).

* Sun Mar  6 2005 Tom Lane <tgl@redhat.com> 4.1.10-3
- Fix package Requires: interdependencies.

* Sat Mar  5 2005 Tom Lane <tgl@redhat.com> 4.1.10-2
- Need -fno-strict-aliasing in at least one place, probably more.
- Work around some C spec violations in mysql.

* Fri Feb 18 2005 Tom Lane <tgl@redhat.com> 4.1.10-1
- Update to MySQL 4.1.10.

* Sat Jan 15 2005 Tom Lane <tgl@redhat.com> 4.1.9-1
- Update to MySQL 4.1.9.

* Wed Jan 12 2005 Tom Lane <tgl@redhat.com> 4.1.7-10
- Don't assume /etc/my.cnf will specify pid-file (bz#143724)

* Wed Jan 12 2005 Tim Waugh <twaugh@redhat.com> 4.1.7-9
- Rebuilt for new readline.

* Tue Dec 21 2004 Tom Lane <tgl@redhat.com> 4.1.7-8
- Run make test on all archs except s390x (which seems to have a bdb issue)

* Mon Dec 13 2004 Tom Lane <tgl@redhat.com> 4.1.7-7
- Suppress someone's silly idea that libtool overhead can be skipped

* Sun Dec 12 2004 Tom Lane <tgl@redhat.com> 4.1.7-6
- Fix init script to not need a valid username for startup check (bz#142328)
- Fix init script to honor settings appearing in /etc/my.cnf (bz#76051)
- Enable SSL (bz#142032)

* Thu Dec  2 2004 Tom Lane <tgl@redhat.com> 4.1.7-5
- Add a restorecon to keep the mysql.log file in the right context (bz#143887)

* Tue Nov 23 2004 Tom Lane <tgl@redhat.com> 4.1.7-4
- Turn off old_passwords in default /etc/my.cnf file, for better compatibility
  with mysql 3.x clients (per suggestion from Joe Orton).

* Fri Oct 29 2004 Tom Lane <tgl@redhat.com> 4.1.7-3
- Handle ldconfig more cleanly (put a file in /etc/ld.so.conf.d/).

* Thu Oct 28 2004 Tom Lane <tgl@redhat.com> 4.1.7-2
- rebuild in devel branch

* Wed Oct 27 2004 Tom Lane <tgl@redhat.com> 4.1.7-1
- Update to MySQL 4.1.x.

* Tue Oct 12 2004 Tom Lane <tgl@redhat.com> 3.23.58-13
- fix security issues CAN-2004-0835, CAN-2004-0836, CAN-2004-0837
  (bugs #135372, 135375, 135387)
- fix privilege escalation on GRANT ALL ON `Foo\_Bar` (CAN-2004-0957)

* Wed Oct 06 2004 Tom Lane <tgl@redhat.com> 3.23.58-12
- fix multilib problem with mysqlbug and mysql_config
- adjust chkconfig priority per bug #128852
- remove bogus quoting per bug #129409 (MySQL 4.0 has done likewise)
- add sleep to mysql.init restart(); may or may not fix bug #133993

* Tue Oct 05 2004 Tom Lane <tgl@redhat.com> 3.23.58-11
- fix low-priority security issues CAN-2004-0388, CAN-2004-0381, CAN-2004-0457
  (bugs #119442, 125991, 130347, 130348)
- fix bug with dropping databases under recent kernels (bug #124352)

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com> 3.23.58-10
- rebuilt

* Sat Apr 17 2004 Warren Togami <wtogami@redhat.com> 3.23.58-9
- remove redundant INSTALL-SOURCE, manual.*
- compress manual.txt.bz2
- BR time

* Tue Mar 16 2004 Tom Lane <tgl@redhat.com> 3.23.58-8
- repair logfile attributes in %%files, per bug #102190
- repair quoting problem in mysqlhotcopy, per bug #112693
- repair missing flush in mysql_setpermission, per bug #113960
- repair broken error message printf, per bug #115165
- delete mysql user during uninstall, per bug #117017
- rebuilt

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Feb 24 2004 Tom Lane <tgl@redhat.com>
- fix chown syntax in mysql.init
- rebuild

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Nov 18 2003 Kim Ho <kho@redhat.com> 3.23.58-5
- update mysql.init to use anonymous user (UNKNOWN_MYSQL_USER) for
  pinging mysql server (#108779)

* Mon Oct 27 2003 Kim Ho <kho@redhat.com> 3.23.58-4
- update mysql.init to wait (max 10 seconds) for mysql server to 
  start (#58732)

* Mon Oct 27 2003 Patrick Macdonald <patrickm@redhat.com> 3.23.58-3
- re-enable Berkeley DB support (#106832)
- re-enable ia64 testing

* Fri Sep 19 2003 Patrick Macdonald <patrickm@redhat.com> 3.23.58-2
- rebuilt

* Mon Sep 15 2003 Patrick Macdonald <patrickm@redhat.com> 3.23.58-1
- upgrade to 3.23.58 for security fix

* Tue Aug 26 2003 Patrick Macdonald <patrickm@redhat.com> 3.23.57-2
- rebuilt

* Wed Jul 02 2003 Patrick Macdonald <patrickm@redhat.com> 3.23.57-1
- revert to prior version of MySQL due to license incompatibilities 
  with packages that link against the client.  The MySQL folks are
  looking into the issue.

* Wed Jun 18 2003 Patrick Macdonald <patrickm@redhat.com> 4.0.13-4
- restrict test on ia64 (temporary)

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com> 4.0.13-3
- rebuilt

* Thu May 29 2003 Patrick Macdonald <patrickm@redhat.com> 4.0.13-2
- fix filter-requires-mysql.sh with less restrictive for mysql-bench 

* Wed May 28 2003 Patrick Macdonald <patrickm@redhat.com> 4.0.13-1
- update for MySQL 4.0
- back-level shared libraries available in mysqlclient10 package

* Fri May 09 2003 Patrick Macdonald <patrickm@redhat.com> 3.23.56-2
- add sql-bench package (#90110) 

* Wed Mar 19 2003 Patrick Macdonald <patrickm@redhat.com> 3.23.56-1
- upgrade to 3.23.56 for security fixes
- remove patch for double-free (included in 3.23.56) 

* Tue Feb 18 2003 Patrick Macdonald <patrickm@redhat.com> 3.23.54a-11
- enable thread safe client
- add patch for double free fix

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Mon Jan 13 2003 Karsten Hopp <karsten@redhat.de> 3.23.54a-9
- disable checks on s390x

* Sat Jan  4 2003 Jeff Johnson <jbj@redhat.com> 3.23.54a-8
- use internal dep generator.

* Wed Jan  1 2003 Bill Nottingham <notting@redhat.com> 3.23.54a-7
- fix mysql_config on hammer

* Sun Dec 22 2002 Tim Powers <timp@redhat.com> 3.23.54a-6
- don't use rpms internal dep generator

* Tue Dec 17 2002 Elliot Lee <sopwith@redhat.com> 3.23.54a-5
- Push it into the build system

* Mon Dec 16 2002 Joe Orton <jorton@redhat.com> 3.23.54a-4
- upgrade to 3.23.54a for safe_mysqld fix

* Thu Dec 12 2002 Joe Orton <jorton@redhat.com> 3.23.54-3
- upgrade to 3.23.54 for latest security fixes

* Tue Nov 19 2002 Jakub Jelinek <jakub@redhat.com> 3.23.52-5
- Always include <errno.h> for errno
- Remove unpackaged files

* Tue Nov 12 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- do not prereq userdel, not used at all

* Mon Sep  9 2002 Trond Eivind Glomsrd <teg@redhat.com> 3.23.52-4
- Use %%{_libdir}
- Add patch for x86-64

* Wed Sep  4 2002 Jakub Jelinek <jakub@redhat.com> 3.23.52-3
- rebuilt with gcc-3.2-7

* Thu Aug 29 2002 Trond Eivind Glomsrd <teg@redhat.com> 3.23.52-2
- Add --enable-local-infile to configure - a new option
  which doesn't default to the old behaviour (#72885)

* Fri Aug 23 2002 Trond Eivind Glomsrd <teg@redhat.com> 3.23.52-1
- 3.23.52. Fixes a minor security problem, various bugfixes.

* Sat Aug 10 2002 Elliot Lee <sopwith@redhat.com> 3.23.51-5
- rebuilt with gcc-3.2 (we hope)

* Mon Jul 22 2002 Trond Eivind Glomsrd <teg@redhat.com> 3.23.51-4
- rebuild

* Thu Jul 18 2002 Trond Eivind Glomsrd <teg@redhat.com> 3.23.51-3
- Fix #63543 and #63542 

* Thu Jul 11 2002 Trond Eivind Glomsrd <teg@redhat.com> 3.23.51-2
- Turn off bdb on PPC(#68591)
- Turn off the assembly optimizations, for safety. 

* Wed Jun 26 2002 Trond Eivind Glomsrd <teg@redhat.com> 3.23.51-1
- Work around annoying auto* thinking this is a crosscompile
- 3.23.51

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Mon Jun 10 2002 Trond Eivind Glomsrd <teg@redhat.com> 3.23.50-2
- Add dependency on perl-DBI and perl-DBD-MySQL (#66349)

* Thu May 30 2002 Trond Eivind Glomsrd <teg@redhat.com> 3.23.50-1
- 3.23.50

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Mon May 13 2002 Trond Eivind Glomsrd <teg@redhat.com> 3.23.49-4
- Rebuild
- Don't set CXX to gcc, it doesn't work anymore
- Exclude Alpha

* Mon Apr  8 2002 Trond Eivind Glomsrd <teg@redhat.com> 3.23.49-3
- Add the various .cnf examples as doc files to mysql-server (#60349)
- Don't include manual.ps, it's just 200 bytes with a URL inside (#60349)
- Don't include random files in /usr/share/mysql (#60349)
- langify (#60349)

* Thu Feb 21 2002 Trond Eivind Glomsrd <teg@redhat.com> 3.23.49-2
- Rebuild

* Sun Feb 17 2002 Trond Eivind Glomsrd <teg@redhat.com> 3.23.49-1
- 3.23.49

* Thu Feb 14 2002 Trond Eivind Glomsrd <teg@redhat.com> 3.23.48-2
- work around perl dependency bug.

* Mon Feb 11 2002 Trond Eivind Glomsrd <teg@redhat.com> 3.23.48-1
- 3.23.48

* Thu Jan 17 2002 Trond Eivind Glomsrd <teg@redhat.com> 3.23.47-4
- Use kill, not mysqladmin, to flush logs and shut down. Thus, 
  an admin password can be set with no problems.
- Remove reload from init script

* Wed Jan 16 2002 Trond Eivind Glomsrd <teg@redhat.com> 3.23.47-3
- remove db3-devel from buildrequires, 
  MySQL has had its own bundled copy since the mid thirties

* Sun Jan  6 2002 Trond Eivind Glomsrd <teg@redhat.com> 3.23.47-1
- 3.23.47
- Don't build for alpha, toolchain immature.

* Mon Dec  3 2001 Trond Eivind Glomsrd <teg@redhat.com> 3.23.46-1
- 3.23.46
- use -fno-rtti and -fno-exceptions, and set CXX to increase stability. 
  Recommended by mysql developers.

* Sun Nov 25 2001 Trond Eivind Glomsrd <teg@redhat.com> 3.23.45-1
- 3.23.45

* Wed Nov 14 2001 Trond Eivind Glomsrd <teg@redhat.com> 3.23.44-2
- centralize definition of datadir in the initscript (#55873)

* Fri Nov  2 2001 Trond Eivind Glomsrd <teg@redhat.com> 3.23.44-1
- 3.23.44

* Thu Oct  4 2001 Trond Eivind Glomsrd <teg@redhat.com> 3.23.43-1
- 3.23.43

* Mon Sep 10 2001 Trond Eivind Glomsrd <teg@redhat.com> 3.23.42-1
- 3.23.42
- reenable innodb

* Tue Aug 14 2001 Trond Eivind Glomsrd <teg@redhat.com> 3.23.41-1
- 3.23.41 bugfix release
- disable innodb, to avoid the broken updates
- Use "mysqladmin flush_logs" instead of kill -HUP in logrotate 
  script (#51711)

* Sat Jul 21 2001 Trond Eivind Glomsrd <teg@redhat.com>
- 3.23.40, bugfix release
- Add zlib-devel to buildrequires:

* Fri Jul 20 2001 Trond Eivind Glomsrd <teg@redhat.com>
- BuildRequires-tweaking

* Thu Jun 28 2001 Trond Eivind Glomsrd <teg@redhat.com>
- Reenable test, but don't run them for s390, s390x or ia64
- Make /etc/my.cnf config(noplace). Same for /etc/logrotate.d/mysqld

* Thu Jun 14 2001 Trond Eivind Glomsrd <teg@redhat.com>
- 3.23.29
- enable innodb
- enable assembly again
- disable tests for now...

* Tue May 15 2001 Trond Eivind Glomsrd <teg@redhat.com>
- 3.23.38
- Don't use BDB on Alpha - no fast mutexes

* Tue Apr 24 2001 Trond Eivind Glomsrd <teg@redhat.com>
- 3.23.37
- Add _GNU_SOURCE to the compile flags

* Wed Mar 28 2001 Trond Eivind Glomsrd <teg@redhat.com>
- Make it obsolete our 6.2 PowerTools packages
- 3.23.36 bugfix release - fixes some security issues
  which didn't apply to our standard configuration
- Make "make test" part of the build process, except on IA64
  (it fails there)

* Tue Mar 20 2001 Trond Eivind Glomsrd <teg@redhat.com>
- 3.23.35 bugfix release
- Don't delete the mysql user on uninstall

* Tue Mar 13 2001 Trond Eivind Glomsrd <teg@redhat.com>
- 3.23.34a bugfix release

* Wed Feb  7 2001 Trond Eivind Glomsrd <teg@redhat.com>
- added readline-devel to BuildRequires:

* Tue Feb  6 2001 Trond Eivind Glomsrd <teg@redhat.com>
- small i18n-fixes to initscript (action needs $)

* Tue Jan 30 2001 Trond Eivind Glomsrd <teg@redhat.com>
- make it shut down and rotate logs without using mysqladmin 
  (from #24909)

* Mon Jan 29 2001 Trond Eivind Glomsrd <teg@redhat.com>
- conflict with "MySQL"

* Tue Jan 23 2001 Trond Eivind Glomsrd <teg@redhat.com>
- improve gettextizing

* Mon Jan 22 2001 Trond Eivind Glomsrd <teg@redhat.com>
- 3.23.32
- fix logrotate script (#24589)

* Wed Jan 17 2001 Trond Eivind Glomsrd <teg@redhat.com>
- gettextize
- move the items in Requires(post): to Requires: in preparation
  for an errata for 7.0 when 3.23.31 is released
- 3.23.31

* Tue Jan 16 2001 Trond Eivind Glomsrd <teg@redhat.com>
- add the log file to the rpm database, and make it 0640
  (#24116)
- as above in logrotate script
- changes to the init sequence - put most of the data
  in /etc/my.cnf instead of hardcoding in the init script
- use /var/run/mysqld/mysqld.pid instead of 
  /var/run/mysqld/pid
- use standard safe_mysqld
- shut down cleaner

* Mon Jan 08 2001 Trond Eivind Glomsrd <teg@redhat.com>
- 3.23.30
- do an explicit chmod on /var/lib/mysql in post, to avoid 
  any problems with broken permissons. There is a report
  of rm not changing this on its own (#22989)

* Mon Jan 01 2001 Trond Eivind Glomsrd <teg@redhat.com>
- bzipped source
- changed from 85 to 78 in startup, so it starts before
  apache (which can use modules requiring mysql)

* Wed Dec 27 2000 Trond Eivind Glomsrd <teg@redhat.com>
- 3.23.29a

* Tue Dec 19 2000 Trond Eivind Glomsrd <teg@redhat.com>
- add requirement for new libstdc++, build for errata

* Mon Dec 18 2000 Trond Eivind Glomsrd <teg@redhat.com>
- 3.23.29

* Mon Nov 27 2000 Trond Eivind Glomsrd <teg@redhat.com>
- 3.23.28 (gamma)
- remove old patches, as they are now upstreamed

* Thu Nov 14 2000 Trond Eivind Glomsrd <teg@redhat.com>
- Add a requirement for a new glibc (#20735)
- build on IA64

* Wed Nov  1 2000 Trond Eivind Glomsrd <teg@redhat.com>
- disable more assembly

* Wed Nov  1 2000 Jakub Jelinek <jakub@redhat.com>
- fix mysql on SPARC (#20124)

* Tue Oct 31 2000 Trond Eivind Glomsrd <teg@redhat.com>
- 3.23.27

* Wed Oct 25 2000 Trond Eivind Glomsrd <teg@redhat.com>
- add patch for fixing bogus aliasing in mysql from Jakub,
  which should fix #18905 and #18620

* Mon Oct 23 2000 Trond Eivind Glomsrd <teg@redhat.com>
- check for negative niceness values, and negate it
  if present (#17899)
- redefine optflags on IA32 FTTB

* Wed Oct 18 2000 Trond Eivind Glomsrd <teg@redhat.com>
- 3.23.26, which among other fixes now uses mkstemp()
  instead of tempnam().
- revert changes made yesterday, the problem is now
  isolated
 
* Tue Oct 17 2000 Trond Eivind Glomsrd <teg@redhat.com>
- use the compat C++ compiler FTTB. Argh.
- add requirement of ncurses4 (see above)

* Sun Oct 01 2000 Trond Eivind Glomsrd <teg@redhat.com>
- 3.23.25
- fix shutdown problem (#17956)

* Tue Sep 26 2000 Trond Eivind Glomsrd <teg@redhat.com>
- Don't try to include no-longer-existing PUBLIC file
  as doc (#17532)

* Thu Sep 12 2000 Trond Eivind Glomsrd <teg@redhat.com>
- rename config file to /etc/my.cnf, which is what
  mysqld wants... doh. (#17432)
- include a changed safe_mysqld, so the pid file option
  works. 
- make mysql dir world readable to they can access the 
  mysql socket. (#17432)
- 3.23.24

* Wed Sep 06 2000 Trond Eivind Glomsrd <teg@redhat.com>
- 3.23.23

* Sun Aug 27 2000 Trond Eivind Glomsrd <teg@redhat.com>
- Add "|| :" to condrestart to avoid non-zero exit code

* Thu Aug 24 2000 Trond Eivind Glomsrd <teg@redhat.com>
- it's mysql.com, not mysql.org and use correct path to 
  source (#16830)

* Wed Aug 16 2000 Trond Eivind Glomsrd <teg@redhat.com>
- source file from /etc/rc.d, not /etc/rd.d. Doh.

* Sun Aug 13 2000 Trond Eivind Glomsrd <teg@redhat.com>
- don't run ldconfig -n, it doesn't update ld.so.cache
  (#16034)
- include some missing binaries
- use safe_mysqld to start the server (request from
  mysql developers)

* Sat Aug 05 2000 Bill Nottingham <notting@redhat.com>
- condrestart fixes

* Mon Aug 01 2000 Trond Eivind Glomsrd <teg@redhat.com>
- 3.23.22. Disable the old patches, they're now in.

* Thu Jul 27 2000 Trond Eivind Glomsrd <teg@redhat.com>
- bugfixes in the initscript
- move the .so link to the devel package

* Wed Jul 19 2000 Trond Eivind Glomsrd <teg@redhat.com>
- rebuild due to glibc changes

* Tue Jul 18 2000 Trond Eivind Glomsrd <teg@redhat.com>
- disable compiler patch
- don't include info directory file

* Mon Jul 17 2000 Trond Eivind Glomsrd <teg@redhat.com>
- move back to /etc/rc.d/init.d

* Fri Jul 14 2000 Trond Eivind Glomsrd <teg@redhat.com>
- more cleanups in initscript

* Thu Jul 13 2000 Trond Eivind Glomsrd <teg@redhat.com>
- add a patch to work around compiler bug 
  (from monty@mysql.com) 

* Wed Jul 12 2000 Trond Eivind Glomsrd <teg@redhat.com>
- don't build the SQL daemon statically (glibc problems)
- fix the logrotate script - only flush log if mysql
  is running
- change the reloading procedure 
- remove icon - glint is obsolete a long time ago

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Mon Jul 10 2000 Trond Eivind Glomsrd <teg@redhat.com>
- try the new compiler again
- build the SQL daemon statically
- add compile time support for complex charsets
- enable assembler
- more cleanups in initscript

* Sun Jul 09 2000 Trond Eivind Glomsrd <teg@redhat.com>
- use old C++ compiler
- Exclusivearch x86

* Sat Jul 08 2000 Trond Eivind Glomsrd <teg@redhat.com>
- move .so files to devel package
- more cleanups
- exclude sparc for now

* Wed Jul 05 2000 Trond Eivind Glomsrd <teg@redhat.com>
- 3.23.21
- remove file from /etc/sysconfig
- Fix initscript a bit - initialization of databases doesn't
  work yet
- specify the correct licenses
- include a /etc/my.conf (empty, FTTB)
- add conditional restart to spec file

* Tue Jul  2 2000 Jakub Jelinek <jakub@redhat.com>
- Rebuild with new C++

* Fri Jun 30 2000 Trond Eivind Glomsrd <teg@redhat.com>
- update to 3.23.20
- use %%configure, %%makeinstall, %%{_tmppath}, %%{_mandir},
  %%{_infodir}, /etc/init.d
- remove the bench package
- change some of the descriptions a little bit
- fix the init script
- some compile fixes
- specify mysql user
- use mysql uid 27 (postgresql is 26)
- don't build on ia64

* Sat Feb 26 2000 Jos Vos <jos@xos.nl>
- Version 3.22.32 release XOS.1 for LinuX/OS 1.8.0
- Upgrade from version 3.22.27 to 3.22.32.
- Do "make install" instead of "make install-strip", because "install -s"
  now appears to fail on various scripts.  Afterwards, strip manually.
- Reorganize subpackages, according to common Red Hat packages: the client
  program and shared library become the base package and the server and
  some accompanying files are now in a separate server package.  The
  server package implicitly requires the base package (shared library),
  but we have added a manual require tag anyway (because of the shared
  config file, and more).
- Rename the mysql-benchmark subpackage to mysql-bench.

* Mon Jan 31 2000 Jos Vos <jos@xos.nl>
- Version 3.22.27 release XOS.2 for LinuX/OS 1.7.1
- Add post(un)install scripts for updating ld.so.conf (client subpackage).

* Sun Nov 21 1999 Jos Vos <jos@xos.nl>
- Version 3.22.27 release XOS.1 for LinuX/OS 1.7.0
- Initial version.
- Some ideas borrowed from Red Hat Powertools 6.1, although this spec
  file is a full rewrite from scratch.
