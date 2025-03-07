%define LANG en

Summary:	English man (manual) pages from the Linux Documentation Project
Name:		man-pages
Version:	6.13
Release:	1
License:	GPL-style
Group:		System/Internationalization
Url:		https://www.kernel.org/doc/man-pages
# 	was ftp://ftp.win.tue.nl/pub/linux-local/manpages/
# Where to find it ????
# (fg) 20010627 Document that quad interpretation "feature" in socket API...
Source0:	https://www.kernel.org/pub/linux/docs/man-pages/%{name}-%{version}.tar.xz
Source10:	strptime.3
BuildArch:	noarch
BuildRequires:	man
# this prevent auto-install of man-pages for non en locales:
#Requires: locales-%LANG
Requires:	man
Autoreq:	false

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
%autosetup -p1
cp -a %{SOURCE10} man3

%build
rm -fv man1/{diff,chgrp,chmod,chown,cp,dd,df,dircolors,du,install,dir,vdir}.1
rm -fv man1/{ln,ls,mkdir,mkfifo,mknod,mv,rm,rmdir,touch}.1
rm -fv man2/modules.2 man2/quotactl.2 man2/get_kernel_syms.2 
rm -fv man2/{create,delete,init,query}_module.2
rm -fv man4/{console,fd}.4 man5/{exports,nfs,fstab}.5

# those conflict with ld.so package
# this one conflicts with bind-utils
rm -rf man5/resolver.5

# those conflict with glibc{,-devel}
rm -f man1/{getent,iconv,locale,localedef,sprof}.1
rm -f man3/crypt{,_r}.3

# this conflict with glibc
rm -f man1/rpcgen.1.bz2

# (tpg) https://issues.openmandriva.org/show_bug.cgi?id=1221
rm -rf man5/attr.5

#mv man1/COPYING .

%install
mkdir -p %{buildroot}/%{_mandir}
for n in 0p 1 1p 2 2const 2type 3 3const 3head 3p 3type 4 5 6 7 8 9; do
	mkdir %{buildroot}/%{_mandir}/man$n
done
for n in man[0-9]*/*; do
	cp -a $n %{buildroot}/%{_mandir}/$n
done
for n in man/man*/*; do
	cp -a $n %{buildroot}/%{_mandir}/../$n
done

LANG='' DESTDIR=%{buildroot} %_bindir/mandb %{buildroot}/%{_mandir}/

mkdir -p  %{buildroot}/var/cache/man/%{LANG}
mkdir -p  %{buildroot}{%{_mandir}/%{LANG},/var/catman/}

# From libnuma-devel
rm %{buildroot}%{_mandir}/man2/move_pages.2*

%files
%doc README* Changes
%dir %{_mandir}/man*p/
%dir %_mandir/cat1
%dir %_mandir/cat2
%dir %_mandir/cat3
%dir %_mandir/cat4
%dir %_mandir/cat5
%dir %_mandir/cat6
%dir %_mandir/cat7
%dir %_mandir/cat8
%dir %_mandir/cat9
%verify (not md5 mtime size) %{_mandir}/index.db*
%{_mandir}/man*/*
