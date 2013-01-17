%define LANG en
Summary: English man (manual) pages from the Linux Documentation Project
Name: man-pages
Version: 3.34
Release: 1
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
Source11: ifcfg.5
#Patch1: man-pages-1.31.iconv.patch.bz2
#Source2: netman-cvs.tar.bz2
URL:     http://www.kernel.org/doc/man-pages
# 	was ftp://ftp.win.tue.nl/pub/linux-local/manpages/
# Where to find it ????
# (fg) 20010627 Document that quad interpretation "feature" in socket API...
BuildRequires: man => 1.5j-8mdk
# this prevent auto-install of man-pages for non en locales:
#Requires: locales-%LANG
Requires: man => 1.5j-8mdk
Autoreqprov: false
BuildArch: noarch

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
cp -a %SOURCE11 man5


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
mkdir -p %{buildroot}/%_mandir
for n in 0p 1 1p 2 3 3p 4 5 6 7 8 9; do
	mkdir %{buildroot}/%_mandir/man$n
done
for n in man*/*; do
	cp -a $n %{buildroot}/%_mandir/$n
done

set -x

LANG='' DESTDIR=%{buildroot} /usr/bin/mandb %{buildroot}/%_mandir/

mkdir -p %{buildroot}/etc/cron.weekly
cat > %{buildroot}/etc/cron.weekly/makewhatis-%LANG.cron << EOF
#!/bin/bash
LANG='' %{_bindir}/mandb %_mandir/%LANG
exit 0
EOF
chmod a+x %{buildroot}/etc/cron.weekly/makewhatis-%LANG.cron

mkdir -p  %{buildroot}/var/cache/man/%LANG
mkdir -p  %{buildroot}{%_mandir/%LANG,/var/catman/}

%files
%defattr(0644,root,man,755)
%doc README* *.Announce Changes
%dir %_mandir/%LANG
#%dir /var/cache/man/%LANG
#%verify (not md5 mtime size) %{_mandir}/whatis
%dir %_mandir/man*p/
%_mandir/man*/*
%_mandir/cat*/*
%_mandir/index.db*
%_mandir/CACHEDIR.TAG*
#%attr(755,root,man)/var/catman/%LANG
%config(noreplace) %attr(755,root,root)/etc/cron.weekly/makewhatis-%LANG.cron


%changelog
* Tue Feb 21 2012 abf
- The release updated by ABF

* Wed May 04 2011 Oden Eriksson <oeriksson@mandriva.com> 3.32-3mdv2011.0
+ Revision: 666364
- mass rebuild

* Mon Dec 27 2010 Per Øyvind Karlsen <peroyvind@mandriva.org> 3.32-2mdv2011.0
+ Revision: 625385
- fix conflicting man pages (#61997)

* Sun Dec 05 2010 Thierry Vignaud <tv@mandriva.org> 3.32-1mdv2011.0
+ Revision: 610590
- new release

* Sun Nov 14 2010 Funda Wang <fwang@mandriva.org> 3.31-1mdv2011.0
+ Revision: 597443
- update to new version 3.31

* Mon Nov 08 2010 Thierry Vignaud <tv@mandriva.org> 3.30-1mdv2011.0
+ Revision: 594901
- new release

* Wed Oct 20 2010 Thierry Vignaud <tv@mandriva.org> 3.29-1mdv2011.0
+ Revision: 586992
- new release

* Wed Oct 06 2010 Funda Wang <fwang@mandriva.org> 3.28-1mdv2011.0
+ Revision: 583367
- update to new version 3.28

* Wed Sep 22 2010 Thierry Vignaud <tv@mandriva.org> 3.27-1mdv2011.0
+ Revision: 580625
- new release

* Sat Feb 27 2010 Funda Wang <fwang@mandriva.org> 3.24-1mdv2010.1
+ Revision: 512179
- update file list
- new version 3.24

* Wed Sep 30 2009 Frederik Himpe <fhimpe@mandriva.org> 3.23-1mdv2010.0
+ Revision: 451842
- update to new version 3.23

* Sat Jul 25 2009 Frederik Himpe <fhimpe@mandriva.org> 3.22-1mdv2010.0
+ Revision: 399655
- update to new version 3.22

* Fri May 01 2009 Frederik Himpe <fhimpe@mandriva.org> 3.21-1mdv2010.0
+ Revision: 369680
- update to new version 3.21

* Fri Feb 20 2009 Frederik Himpe <fhimpe@mandriva.org> 3.19-1mdv2009.1
+ Revision: 343500
- update to new version 3.19

* Tue Feb 10 2009 Frederik Himpe <fhimpe@mandriva.org> 3.18-1mdv2009.1
+ Revision: 339241
- update to new version 3.18

* Thu Jan 22 2009 Frederik Himpe <fhimpe@mandriva.org> 3.17-1mdv2009.1
+ Revision: 332632
- Update to new version 3.17
- Remove patch describing ext3 in filesystems(5): it's already documented

  + Thierry Vignaud <tv@mandriva.org>
    - new release

* Sat Dec 06 2008 Frederik Himpe <fhimpe@mandriva.org> 3.15-1mdv2009.1
+ Revision: 311180
- update to new version 3.15

* Wed Nov 26 2008 Thierry Vignaud <tv@mandriva.org> 3.14-1mdv2009.1
+ Revision: 307026
- new release

* Wed Nov 12 2008 Funda Wang <fwang@mandriva.org> 3.13-1mdv2009.1
+ Revision: 302479
- New version 3.13

* Fri Oct 31 2008 Frederik Himpe <fhimpe@mandriva.org> 3.12-1mdv2009.1
+ Revision: 299007
- update to new version 3.12

* Fri Oct 10 2008 Frederik Himpe <fhimpe@mandriva.org> 3.11-1mdv2009.1
+ Revision: 291638
- update to new version 3.11

  + Funda Wang <fwang@mandriva.org>
    - New version 3.10

* Thu Sep 11 2008 Thierry Vignaud <tv@mandriva.org> 3.09-1mdv2009.0
+ Revision: 283797
- new release

* Wed Aug 27 2008 Thierry Vignaud <tv@mandriva.org> 3.08-1mdv2009.0
+ Revision: 276576
- new release

* Wed Aug 13 2008 Frederik Himpe <fhimpe@mandriva.org> 3.07-1mdv2009.0
+ Revision: 271512
- update to new version 3.07

* Thu Aug 07 2008 Funda Wang <fwang@mandriva.org> 3.06-1mdv2009.0
+ Revision: 265802
- New version 3.06

* Thu Jul 24 2008 Funda Wang <fwang@mandriva.org> 3.05-1mdv2009.0
+ Revision: 246150
- New version 3.05

* Fri Jul 18 2008 Funda Wang <fwang@mandriva.org> 3.04-1mdv2009.0
+ Revision: 238227
- New version 3.04

* Sun Jun 29 2008 Funda Wang <fwang@mandriva.org> 3.01-1mdv2009.0
+ Revision: 229934
- New version 3.01

* Fri Jun 20 2008 Funda Wang <fwang@mandriva.org> 3.00-1mdv2009.0
+ Revision: 227331
- fix file list
- New version 3.00

* Wed Jun 11 2008 Funda Wang <fwang@mandriva.org> 2.80-1mdv2009.0
+ Revision: 217915
- New version 2.80

* Fri Feb 22 2008 Thierry Vignaud <tv@mandriva.org> 2.78-1mdv2008.1
+ Revision: 173831
- new release

* Sat Feb 02 2008 Funda Wang <fwang@mandriva.org> 2.77-1mdv2008.1
+ Revision: 161479
- update to new version 2.77

* Mon Jan 28 2008 Thierry Vignaud <tv@mandriva.org> 2.76-1mdv2008.1
+ Revision: 159257
- new release

* Fri Jan 11 2008 Funda Wang <fwang@mandriva.org> 2.75-1mdv2008.1
+ Revision: 147847
- update to new version 2.75

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Sun Dec 30 2007 Funda Wang <fwang@mandriva.org> 2.74-1mdv2008.1
+ Revision: 139527
- update to new version 2.74

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Fri Dec 14 2007 Thierry Vignaud <tv@mandriva.org> 2.72-1mdv2008.1
+ Revision: 119859
- rediff patch 2
- new release

* Mon Dec 03 2007 Thierry Vignaud <tv@mandriva.org> 2.69-1mdv2008.1
+ Revision: 114625
- new release
- new download URL
- new URL

* Wed Oct 24 2007 Funda Wang <fwang@mandriva.org> 2.67-1mdv2008.1
+ Revision: 101828
- update to new version 2.67
- fix tarball URL

* Tue Oct 09 2007 Thierry Vignaud <tv@mandriva.org> 2.66-1mdv2008.0
+ Revision: 95785
- new release

* Fri Aug 10 2007 Thierry Vignaud <tv@mandriva.org> 2.64-1mdv2008.0
+ Revision: 61545
- new release

* Wed Jul 25 2007 Funda Wang <fwang@mandriva.org> 2.63-1mdv2008.0
+ Revision: 55165
- New version 2.63

* Sat Jul 14 2007 Funda Wang <fwang@mandriva.org> 2.62-1mdv2008.0
+ Revision: 51990
- New version

* Tue Jun 26 2007 Thierry Vignaud <tv@mandriva.org> 2.60-1mdv2008.0
+ Revision: 44432
- new release

* Mon Jun 18 2007 Funda Wang <fwang@mandriva.org> 2.57-1mdv2008.0
+ Revision: 40670
- New upstream version

* Thu Jun 14 2007 Thierry Vignaud <tv@mandriva.org> 2.56-1mdv2008.0
+ Revision: 39350
- new release

* Fri Jun 08 2007 Thierry Vignaud <tv@mandriva.org> 2.54-1mdv2008.0
+ Revision: 37568
- no more man vs gnu info README
- new release
- new release

* Thu May 31 2007 Funda Wang <fwang@mandriva.org> 2.50-1mdv2008.0
+ Revision: 33005
- New version

* Mon Apr 23 2007 Thierry Vignaud <tv@mandriva.org> 2.44-1mdv2008.0
+ Revision: 17402
- new release


* Thu Feb 08 2007 Thierry Vignaud <tvignaud@mandriva.com> 2.43-1mdv2007.0
+ Revision: 118082
- kill icon
- new release
- new release

* Wed Oct 25 2006 Thierry Vignaud <tvignaud@mandriva.com> 2.41-1mdv2007.1
+ Revision: 72348
- Import man-pages

* Wed Oct 25 2006 Thierry Vignaud <tvignaud@mandriva.com> 2.41-1mdv2007.1
- new release

* Sat Aug 12 2006 Thierry Vignaud <tvignaud@mandriva.com> 2.36-1mdv2007.0
- new release

* Fri Jul 28 2006 Thierry Vignaud <tvignaud@mandriva.com> 2.36-1mdv2007.0
- new release

* Thu Jun 22 2006 Thierry Vignaud <tvignaud@mandriva.com> 2.34-1mdv2007.0
- new release

* Thu Jun 01 2006 Thierry Vignaud <tvignaud@mandriva.com> 2.33-1mdv2007.0
- new release

* Thu May 18 2006 Thierry Vignaud <tvignaud@mandriva.com> 2.32-1mdk
- new release

* Fri May 05 2006 Thierry Vignaud <tvignaud@mandriva.com> 2.31-1mdk
- new release

* Wed May 03 2006 Thierry Vignaud <tvignaud@mandriva.com> 2.30-1mdk
- new release

* Sat Apr 15 2006 Thierry Vignaud <tvignaud@mandriva.com> 2.29-1mdk
- new release

* Tue Mar 21 2006 Thierry Vignaud <tvignaud@mandriva.com> 2.26-1mdk
- new release

* Fri Mar 10 2006 Thierry Vignaud <tvignaud@mandriva.com> 2.25-1mdk
- new release

* Wed Feb 22 2006 Thierry Vignaud <tvignaud@mandriva.com> 2.24-1mdk
- new release

* Mon Feb 13 2006 Thierry Vignaud <tvignaud@mandriva.com> 2.23-1mdk
- new release

* Mon Jan 30 2006 Thierry Vignaud <tvignaud@mandriva.com> 2.21-1mdk
- new release

* Fri Oct 07 2005 Thierry Vignaud <tvignaud@mandriva.com> 2.08-1mdk
- new release
- fix unowned directories (#17427)
- kill patches 4, 5 & 6 (merged)

* Fri Aug 19 2005 Thierry Vignaud <tvignaud@mandriva.com> 2.07-1mdk
- new release

* Fri Jul 08 2005 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.04-2mdk
- include POSIX man pages (#16167)

* Fri Jun 24 2005 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.04-1mdk
- new release

* Sat Jun 04 2005 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.03-1mdk
- new release

* Mon Apr 18 2005 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.02-1mdk
- new release

* Tue Jan 25 2005 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.01-2mdk
- remove the require on locales-en (otherwise man-pages are only installed
  for english installs)
- fix rpmlint warnings

* Mon Dec 20 2004 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.01-1mdk
- new release

* Fri Dec 17 2004 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.00-1mdk
- new release

* Fri Aug 27 2004 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.67-1mdk
- new release

* Wed Apr 07 2004 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.66-1mdk
- new release

