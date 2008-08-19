# TODO, sometime: nvtvsimple

Summary:        Free multimedia player
Name:           xine
Version:        0.99.5
Release:        2%{?dist}.1
License:        GPL
Group:          Applications/Multimedia
URL:            http://xinehq.de/
Source0:        http://downloads.sourceforge.net/xine/xine-ui-%{version}.tar.gz
Patch0:         xine-ui-0.99.5-shared-lirc.patch
Patch1:         xine-ui-0.99.5-desktop.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Provides:       xine-ui = %{version}-%{release}
BuildRequires:  xine-lib-devel >= 1.1.0
BuildRequires:  aalib-devel >= 1.2.0
BuildRequires:  libpng-devel gettext ncurses-devel
BuildRequires:  libtermcap-devel desktop-file-utils readline-devel
BuildRequires:  curl-devel >= 7.10.2 lirc-libs lirc-devel libcaca-devel
BuildRequires:  libXxf86vm-devel libXv-devel libXinerama-devel libXtst-devel
BuildRequires:  libXt-devel libXft-devel
# libXext-devel and fontconfig-devel should be pulled in by other libX*-devel
BuildRequires:  libXext-devel fontconfig-devel
Conflicts:      xine-skins <= 1.0

Requires(post): coreutils
Requires(postun): coreutils

# --------------------------------------------------------------------

%description
xine is a free multimedia player.  It plays back CDs, DVDs, and VCDs.
It also decodes multimedia files like AVI, MOV, WMV, and MP3 from
local disk drives, and displays multimedia streamed over the Internet.

# --------------------------------------------------------------------

%prep
%setup -q -n %{name}-ui-%{version}
touch -r m4/_xine.m4 m4/_xine.m4.stamp
%patch0 -p1
touch -r m4/_xine.m4.stamp m4/_xine.m4
%patch1 -p1

# Fix unversioned dlopen("libX11.so") in aaxine
libx11so=$(ls -1 %{_libdir}/libX11.so.? | tail -n 1)
if [ -n "$libx11so" -a -f "$libx11so" ] ; then
    sed -i -e "s/\"libX11\\.so\"/\"$(basename $libx11so)\"/" src/aaui/main.c
fi

touch -r configure.ac configure.ac.stamp
sed -i -e 's/LINUX_KD_HB/LINUX_KD_H/' -e 's|linux/kd\.hb|linux/kd.h|' \
    config.h.in configure.ac configure
touch -r configure.ac.stamp configure.ac

for f in doc/man/{de,es,fr}/*.1* doc/README?{cs,de,es,fi,fr,it} ; do
    iconv -f iso-8859-1 -t utf-8 $f > $f.utf8 ; mv $f.utf8 $f
done
for f in doc/README_uk ; do
    iconv -f koi8-r -t utf-8 $f > $f.utf8 ; mv $f.utf8 $f
done
for f in doc/man/pl/*.1* doc/README?{cs,pl}* ; do
    iconv -f iso-8859-2 -t utf-8 $f > $f.utf8 ; mv $f.utf8 $f
done

# --------------------------------------------------------------------

%build
%configure --disable-dependency-tracking --enable-vdr-keys --with-aalib
make %{?_smp_mflags}

# --------------------------------------------------------------------

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT
%find_lang 'xi\(ne-ui\|tk\)'
rm -R $RPM_BUILD_ROOT%{_docdir} $RPM_BUILD_ROOT%{_datadir}/pixmaps

desktop-file-install --vendor livna --delete-original \
    --dir $RPM_BUILD_ROOT%{_datadir}/applications  \
    $RPM_BUILD_ROOT%{_datadir}/%{name}/desktop/xine.desktop

# --------------------------------------------------------------------

%clean
rm -rf $RPM_BUILD_ROOT

# --------------------------------------------------------------------

%post
touch --no-create %{_datadir}/icons/hicolor
if [ -x %{_bindir}/gtk-update-icon-cache ] ; then
    %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor
fi
if [ -x %{_bindir}/update-desktop-database ] ; then
    %{_bindir}/update-desktop-database --quiet
fi
:

%postun
touch --no-create %{_datadir}/icons/hicolor
if [ -x %{_bindir}/gtk-update-icon-cache ] ; then
    %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor
fi
if [ -x %{_bindir}/update-desktop-database ] ; then
    %{_bindir}/update-desktop-database --quiet
fi
:

%files -f 'xi\(ne-ui\|tk\)'.lang
%defattr(-,root,root,-)
%doc doc/README*
%{_bindir}/aaxine
%{_bindir}/cacaxine
%{_bindir}/fbxine
%{_bindir}/xine
%{_bindir}/xine-bugreport
%{_bindir}/xine-check
%{_bindir}/xine-remote
%{_datadir}/%{name}
%{_datadir}/applications/*xine.desktop
%{_datadir}/icons/hicolor/*x*/apps/xine.png
%{_mandir}/man1/*.1*
%lang(de) %{_mandir}/de/man1/*.1*
%lang(es) %{_mandir}/es/man1/*.1*
%lang(fr) %{_mandir}/fr/man1/*.1*
%lang(pl) %{_mandir}/pl/man1/*.1*

# --------------------------------------------------------------------

%changelog
* Tue Aug 19 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info - 0.99.5-2.1
- add lirc-libs as BR to hopefully circumvent a F8 buildsys issue

* Mon Aug 04 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info - 0.99.5-2
- rebuild

* Sat Jul 14 2007 Ville Skyttä <ville.skytta at iki.fi> - 0.99.5-1
- 0.99.5, lots of patches made obsolete.
- Update icon cache and desktop database.
- Patch {aa,caca}xine to dlopen libX11.so.* instead of libX11.so at runtime.
- Patch to look for linux/kd.h instead of linux/kd.hb during build.
- Don't run autotools during build.

* Thu Mar 01 2007 Thorsten Leemhuis <fedora at leemhuis.info> - 0.99.4-11
- rebuild for new curl

* Tue Nov  7 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.99.4-10
- Re-enable VDR keys and patch, patched xine-lib not required (#1241).

* Thu Nov  2 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.99.4-9
- Drop X-Livna and Application desktop entry categories.

* Thu Nov  2 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.99.4-8
- Make VDR support optional, disabled by default, fixes #1238.

* Thu Apr 20 2006 Dams <anvil[AT]livna.org> - 0.99.4-7
- Added patch8 to fix up buffer overflow describe in #926

* Thu Mar 09 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- switch to new release field

* Tue Feb 28 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- add dist

* Fri Jan 20 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.99.4-0.lvn.6
- %%langify non-English manpages, really convert all (and more docs) to UTF-8.
- Improve summary and description.

* Tue Jan  3 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.99.4-0.lvn.5
- Adapt to modular X.
- Drop pre-FC5 workarounds and rpmbuild conditionals.

* Thu Sep 29 2005 Ville Skyttä <ville.skytta at iki.fi> - 0.99.4-0.lvn.4
- Clean up obsolete pre-FC3 stuff (LIRC and CACA now unconditionally enabled).
- Drop zero Epochs.

* Thu Sep 15 2005 Ville Skyttä <ville.skytta at iki.fi> - 0:0.99.4-0.lvn.3
- Apply sprintf, uifixups and xftfontsize patches from Alex Stewart/freshrpms.
- Fix fbxine crash when the tty mode can't be set (upstreamed).
- Fix fbxine usage message and options (upstreamed).
- Make vdr support conditional (default enabled), require vdr-patched xine-lib
  if enabled, and build with it for FC4+.
- Build with gcc4 again on FC4+.

* Sun Aug 14 2005 Ville Skyttä <ville.skytta at iki.fi> - 0:0.99.4-0.lvn.2
- Sync VDR patch with vdr-xine-0.7.5 (just for tracking purposes, no changes).

* Tue Aug  2 2005 Dams <anvil[AT]livna.org> - 0:0.99.4-0.lvn.1
- Updated to 0.99.4
- Fixed files section
- Dropped patch5 
- Dropped patch3

* Sun Jul 10 2005 Ville Skyttä <ville.skytta at iki.fi> - 0:0.99.3-0.lvn.8
- Build with compat-gcc-32 for FC4 ("--with gcc32") as a temporary workaround
  for spurious directory creation attempts (#419) and possibly other issues.
- Use shared LIRC client libs, possibly enable LIRC support also on x86_64.
- Apply gcc4 menu crash fix, kudos for the patch to freshrpms.net and
  Alex Stewart, this'll be handy when we try with gcc4 again (#467).
- Clean up obsolete pre-FC2 stuff.

* Sat Jun  4 2005 Ville Skyttä <ville.skytta at iki.fi> - 0:0.99.3-0.lvn.7
- Apply VDR support update patch from vdr-xine-0.7.4.

* Sat May 28 2005 Thorsten Leemhuis <fedora at leemhuis.info> - 0:0.99.3-0.lvn.6
- Fix typo

* Mon May  9 2005 Ville Skyttä <ville.skytta at iki.fi> - 0:0.99.3-0.lvn.5
- Add support for CACA, rebuild with "--without caca" to disable (#380).

* Sat Apr 30 2005 Dams <anvil[AT]livna.org> - 0:0.99.3-0.lvn.4
- Fixed gcc4 build

* Wed Apr 13 2005 Dams <anvil[AT]livna.org> - 0:0.99.3-0.lvn.3
- Conditional lirc buildreq (default enabled)

* Sat Jan  1 2005 Ville Skyttä <ville.skytta at iki.fi> - 0:0.99.3-0.lvn.2
- Enable support for VDR interaction keys.
- Enable curl unconditionally.
- Build with dependency tracking disabled.

* Wed Dec 29 2004 Dams <anvil[AT]livna.org> - 0:0.99.3-0.lvn.1
- Updated to 0.99.3

* Tue Jul  6 2004 Dams <anvil[AT]livna.org> 0:0.99.2-0.lvn.2
- Updated no-march/mcpu patch
- Updated mkinstalldirs patch

* Mon Jul  5 2004 Dams <anvil[AT]livna.org> 0:0.99.2-0.lvn.1
- Updated to 0.99.2

* Sun Jun 13 2004 Dams <anvil[AT]livna.org> 0:0.99.1-0.lvn.3
- Updated desktop entry for HID compliance

* Fri May 21 2004 Dams <anvil[AT]livna.org> 0:0.99.1-0.lvn.2
- Updated URL in Source0

* Sat Apr 17 2004 Dams <anvil[AT]livna.org> 0:0.99.1-0.lvn.1
- Updated to 0.99.1

* Thu Feb 26 2004 Dams <anvil[AT]livna.org> 0:0.9.23-0.lvn.2
- Updated xine-lib version requirement in build dependancy
- Hopefully fixed build for RH9

* Thu Dec 25 2003 Dams <anvil[AT]livna.org> 0:0.9.23-0.lvn.1
- s/fedora/livna/

* Thu Dec 25 2003 Dams <anvil[AT]livna.org> 0:0.9.23-0.fdr.1
- Updated patch for no march/mcpu from configure

* Wed Dec 24 2003 Dams <anvil[AT]livna.org> 0:0.9.23-0.fdr.1
- Updated to 0.9.23

* Sun Sep 28 2003 Dams <anvil[AT]livna.org> 0:0.9.22-0.fdr.4
- Added patch to fix po/Makefile for servern2 build

* Sun Aug 31 2003 Dams <anvil[AT]livna.org> 0:0.9.22-0.fdr.3
- Translated manpages iconv'ed into utf-8 encoding

* Sat Aug 23 2003 Dams <anvil[AT]livna.org> 0:0.9.22-0.fdr.2
- Conflict with old xine-skins packages
- Removed lirc conditionnal build requirement
- Added conditionnal Build dependencies for curl
- Added missing libtool BuildRequires

* Wed Aug 20 2003 Dams <anvil[AT]livna.org> 0:0.9.22-0.fdr.2
- No more -skins package
- No more url in Source0

* Fri Aug  8 2003 Dams <anvil[AT]livna.org> 0:0.9.22-0.fdr.1
- Updated to 0.9.22

* Tue Jul 15 2003 Dams <anvil[AT]livna.org> 0:0.9.21-0.fdr.3
- exporting SED=__sed seems to fix build to rh80

* Sun Jul  6 2003 Dams <anvil[AT]livna.org> 0:0.9.21-0.fdr.2
- Trying to avoid unowned directories
- Patch for configure not to set march/mcpu.
- Removed BuildArch.

* Sat May 17 2003 Dams <anvil[AT]livna.org> 0:0.9.21-0.fdr.1
- Updated to 0.9.21
- buildroot -> RPM_BUILD_ROOT
- Updated URL in Source0
- Updated BuildRequires

* Sat Apr 12 2003 Dams <anvil[AT]livna.org> 0:0.9.20-0.fdr.5
- Arch stuff

* Wed Apr  9 2003 Dams <anvil[AT]livna.org> 0:0.9.20-0.fdr.4
- Fixed typo
- Rebuild, linked against xine-lib 1 beta10

* Mon Apr  7 2003 Dams <anvil[AT]livna.org> 0:0.9.20-0.fdr.3
- Only one find_lang

* Mon Apr  7 2003 Dams <anvil[AT]livna.org> 0:0.9.20-0.fdr.2
- Added BuildRequires.
- Added --with directives.
- Added use of desktop-file-install
- Added more Requires tag.

* Thu Apr  3 2003 Dams <anvil[AT]livna.org> 
- Initial build.
