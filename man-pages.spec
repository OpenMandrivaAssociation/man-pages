%define LANG en

Summary:	English man (manual) pages from the Linux Documentation Project
Name:		man-pages
Version:	3.82
Release:	1
License:	GPL-style
Group:		System/Internationalization
Url:		http://www.kernel.org/doc/man-pages
# 	was ftp://ftp.win.tue.nl/pub/linux-local/manpages/
# Where to find it ????
# (fg) 20010627 Document that quad interpretation "feature" in socket API...
Source0:	http://www.kernel.org/pub/linux/docs/man-pages/%{name}-%{version}.tar.xz
Source1:	rpcgen.1
#Source2:	netman-cvs.tar.bz2
Source3:	ld.so.8
Source4:	ldd.1
Source5:	ldconfig.8
Source6:	man-pages-extralocale.tar.bz2
Source8:	man9-19971126.tar.bz2
Source9:	man2.tar.bz2
Source10:	strptime.3
Source11:	ifcfg.5
#Patch1:	man-pages-1.31.iconv.patch.bz2
BuildArch:	noarch
BuildRequires:	man
# this prevent auto-install of man-pages for non en locales:
#Requires: locales-%LANG
Requires:	man
Autoreqprov:	false

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

cp -a %{SOURCE1} man1
cp -a %{SOURCE3} man8
cp -a %{SOURCE4} man1
cp -a %{SOURCE5} man8
cp -a %{SOURCE10} man3
cp -a %{SOURCE11} man5

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
rm -f man3/crypt{,_r}.3

# this conflict with glibc
rm -f man1/rpcgen.1.bz2

#mv man1/COPYING .

%install
set +x
mkdir -p %{buildroot}/%{_mandir}
for n in 0p 1 1p 2 3 3p 4 5 6 7 8 9; do
	mkdir %{buildroot}/%{_mandir}/man$n
done
for n in man*/*; do
	cp -a $n %{buildroot}/%{_mandir}/$n
done

set -x

LANG='' DESTDIR=%{buildroot} %_bindir/mandb %{buildroot}/%{_mandir}/

mkdir -p %{buildroot}/etc/cron.weekly
cat > %{buildroot}/etc/cron.weekly/makewhatis-%{LANG}.cron << EOF
#!/bin/bash
LANG='' %_bindir/mandb %{_mandir}/%{LANG}
exit 0
EOF
chmod a+x %{buildroot}/etc/cron.weekly/makewhatis-%{LANG}.cron

mkdir -p  %{buildroot}/var/cache/man/%{LANG}
mkdir -p  %{buildroot}{%{_mandir}/%{LANG},/var/catman/}


%files
%defattr(0644,root,man,755)
%doc README* *.Announce Changes
%dir %{_mandir}/%{LANG}
%dir %{_mandir}/man*p/
%config(noreplace) %attr(755,root,root)/etc/cron.weekly/makewhatis-%{LANG}.cron

%verify (not md5 mtime size) %{_mandir}/CACHEDIR.TAG*
%dir %_mandir/cat1
%verify (not md5 mtime size) %{_mandir}/cat1/CACHEDIR.TAG*
%dir %_mandir/cat2
%verify (not md5 mtime size) %{_mandir}/cat2/CACHEDIR.TAG*
%dir %_mandir/cat3
%verify (not md5 mtime size) %{_mandir}/cat3/CACHEDIR.TAG*
%dir %_mandir/cat4
%verify (not md5 mtime size) %{_mandir}/cat4/CACHEDIR.TAG*
%dir %_mandir/cat5
%verify (not md5 mtime size) %{_mandir}/cat5/CACHEDIR.TAG*
%dir %_mandir/cat6
%verify (not md5 mtime size) %{_mandir}/cat6/CACHEDIR.TAG*
%dir %_mandir/cat7
%verify (not md5 mtime size) %{_mandir}/cat7/CACHEDIR.TAG*
%dir %_mandir/cat8
%verify (not md5 mtime size) %{_mandir}/cat8/CACHEDIR.TAG*
%dir %_mandir/cat9
%verify (not md5 mtime size) %{_mandir}/cat9/CACHEDIR.TAG*
%verify (not md5 mtime size) %{_mandir}/index.db*
%{_mandir}/man*/*

