%define LANG en
Summary: English man (manual) pages from the Linux Documentation Project
Name: man-pages
Version: 3.32
Release: %mkrel 1
License: GPL-style
Group: System/Internationalization
Source: ftp://ftp.kernel.org/pub/linux/docs/man-pages/%name-%version.tar.bz2
Source1: rpcgen.1
Source3: ld.so.8
Source4: ldd.1
Source5: ldconfig.8
Source6: man-pages-extralocale.tar.bz2
Source8: man9-19971126.tar.bz2
Source9: man2.tar.bz2
Source10: strptime.3
Source11: man-network.tar.bz2
#Patch1: man-pages-1.31.iconv.patch.bz2
#Source2: netman-cvs.tar.bz2
URL:     http://www.kernel.org/doc/man-pages
# 	was ftp://ftp.win.tue.nl/pub/linux-local/manpages/
# Where to find it ????
# (fg) 20010627 Document that quad interpretation "feature" in socket API...
Buildroot: %_tmppath/%name-%version-root
BuildRequires: man => 1.5j-8mdk
# this prevent auto-install of man-pages for non en locales:
#Requires: locales-%LANG
Requires: man => 1.5j-8mdk
Autoreqprov: false
BuildArchitectures: noarch

%description
A large collection of man pages (reference material) from the Linux 
Documentation Project (LDP).  The man pages are organized into the
following sections:

        Section 1:  User commands (intro only)
        Section 2:  System calls
        Section 3:  Libc calls
        Section 4:  Devices (e.g., hd, sd)
        Section 5:  File formats and protocols (e.g., wtmp, /etc/passwd,
                nfs)
        Section 6:  Games (intro only)
        Section 7:  Conventions, macro packages, etc. (e.g., nroff, ascii)
        Section 8:  System administration (intro only)
        Section 9:  Kernel internal routines

%prep
%setup -q -a 9 -a 8 -a6

cp -a %SOURCE1 man1
cp -a %SOURCE3 man8
cp -a %SOURCE4 man1
cp -a %SOURCE5 man8
cp -a %SOURCE10 man3


%build
rm -fv man1/{diff,chgrp,chmod,chown,cp,dd,df,dircolors,du,install,dir,vdir}.1
rm -fv man1/{ln,ls,mkdir,mkfifo,mknod,mv,rm,rmdir,touch}.1
rm -fv man2/modules.2 man2/quotactl.2 man2/get_kernel_syms.2 
rm -fv man2/{create,delete,init,query}_module.2
rm -fv man4/{console,fd}.4 man5/{exports,nfs,fstab}.5

# those conflict with ld.so package
# this one conflicts with bind-utils
rm -rf man5/resolver.5

# this conflicts with ldconfig -- Geoff
rm -f man8/ldconfig.8

# those conflict with glibc{,-devel}
rm -f man1/{getent,iconv,ldd,locale,localedef,sprof}.1
rm -f man8/{ld.so,rpcinfo}.8
rm -f man1/rpcgen.1

# this conflict with glibc
rm -f man1/rpcgen.1.bz2
				
#mv man1/COPYING .

%install
rm -rf $RPM_BUILD_ROOT

set +x
mkdir -p $RPM_BUILD_ROOT/%_mandir
for n in 0p 1 1p 2 3 3p 4 5 6 7 8 9; do
	mkdir $RPM_BUILD_ROOT/%_mandir/man$n
done
for n in man*/*; do
	cp -a $n $RPM_BUILD_ROOT/%_mandir/$n
done

set -x

LANG='' DESTDIR=$RPM_BUILD_ROOT /usr/sbin/makewhatis $RPM_BUILD_ROOT/%_mandir/

mkdir -p $RPM_BUILD_ROOT/etc/cron.weekly
cat > $RPM_BUILD_ROOT/etc/cron.weekly/makewhatis-%LANG.cron << EOF
#!/bin/bash
LANG='' /usr/sbin/makewhatis %_mandir/%LANG
exit 0
EOF
chmod a+x $RPM_BUILD_ROOT/etc/cron.weekly/makewhatis-%LANG.cron

mkdir -p  $RPM_BUILD_ROOT/var/cache/man/%LANG
mkdir -p  $RPM_BUILD_ROOT{%_mandir/%LANG,/var/catman/}
tar xfj %SOURCE11 -C $RPM_BUILD_ROOT/%_mandir

 
%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(0644,root,man,755)
%doc README* *.Announce Changes
%dir %_mandir/%LANG
#%dir /var/cache/man/%LANG
%verify (not md5 mtime size) %{_mandir}/whatis
%dir %_mandir/man*p/
%_mandir/man*/*
#%attr(755,root,man)/var/catman/%LANG
%config(noreplace) %attr(755,root,root)/etc/cron.weekly/makewhatis-%LANG.cron
