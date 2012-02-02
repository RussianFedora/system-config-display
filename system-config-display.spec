%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Summary: A graphical interface for configuring the X Window System display
Name: system-config-display
Version: 2.2
Release: 3%{?dist}.R
URL: http://fedoraproject.org/wiki/SystemConfig/Tools
License: GPLv2+
ExclusiveOS: Linux
Group: System Environment/Base
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Provides: rhpxl = 1.12-4.fc12
Obsoletes: rhpxl < 1.12-4.fc12

Source0: http://fedorahosted.org/releases/s/y/%{name}/%{name}-%{version}.tar.bz2
Patch0: scd-2.2-preexec-fn.patch

ExcludeArch: s390 s390x
BuildRequires: desktop-file-utils
BuildRequires: intltool, gettext
BuildRequires: python-devel
BuildRequires: pkgconfig(xrandr)
Requires: pygtk2 >= 1.99.11
Requires: pygtk2-libglade
Requires: python2
Requires: usermode >= 1.36
Requires: usermode-gtk
Requires: hwdata >= 0.169
Requires: dbus-python
Requires: pyxf86config >= 0.3.16
Requires: /usr/bin/Xorg
Requires: metacity
Requires: gtk2 >= 2.6
Requires: hicolor-icon-theme

%description
system-config-display is a graphical application for configuring an
X Window System X server display.

%prep
%setup -q
%patch0 -p1 -b .py27

%build
make

%install
rm -rf $RPM_BUILD_ROOT
make INSTROOT=$RPM_BUILD_ROOT install
desktop-file-install --vendor system --delete-original 	\
  --dir $RPM_BUILD_ROOT%{_datadir}/applications 	\
  --remove-category Application 			\
  --remove-category SystemSetup 			\
  --add-category Settings 				\
  $RPM_BUILD_ROOT%{_datadir}/applications/system-config-display.desktop
chmod a-x $RPM_BUILD_ROOT%{_datadir}/system-config-display/pixmaps/*

%find_lang %name

%clean
rm -rf $RPM_BUILD_ROOT

%postun
touch --no-create %{_datadir}/icons/hicolor
if [ -x /usr/bin/gtk-update-icon-cache -a -e %{_datadir}/icons/hicolor ]; then
  gtk-update-icon-cache -q %{_datadir}/icons/hicolor
fi

%post
touch --no-create %{_datadir}/icons/hicolor
if [ -x /usr/bin/gtk-update-icon-cache -a -e %{_datadir}/icons/hicolor ]; then
  gtk-update-icon-cache -q %{_datadir}/icons/hicolor
fi


%files -f %{name}.lang
%defattr(-,root,root)
%{_bindir}/system-config-display
%{_datadir}/system-config-display
%{_datadir}/applications/*
%attr(0644,root,root) %config /etc/security/console.apps/system-config-display
%attr(0644,root,root) %config /etc/pam.d/system-config-display
%attr(0644,root,root) %{_datadir}/icons/hicolor/48x48/apps/system-config-display.png
%{python_sitearch}/_pyrandr*

%changelog
* Thu Feb  2 2012 Arkady L. Shane <ashejn@russianfedora.ru> 2.2-3.R
- rebuilt for EL

* Tue Jul 27 2010 Adam Jackson <ajax@redhat.com> 2.2-3
- scd-2.2-preexec-fn.patch: Remove bizarre chroot handling.

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Mon Sep 21 2009 Adam Jackson <ajax@redhat.com> 2.2-1
- s-c-d 2.2
- Prov/Obs: rhpxl

* Fri Sep 18 2009 Adam Jackson <ajax@redhat.com> 2.1-1
- s-c-d 2.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Feb 08 2009 Adam Jackson <ajax@redhat.com> 1.1.3-1
- s-c-d 1.1.3

* Mon Dec 01 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 1.1.1-2
- Rebuild for Python 2.6

* Wed Oct 22 2008 Adam Jackson <ajax@redhat.com> 1.1.1-1
- s-c-d 1.1.1

* Wed Oct 22 2008 Adam Jackson <ajax@redhat.com> 1.0.51-11
- Requires: usermode-gtk (#467923)

* Wed May 21 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.0.51-10
- fix license tag

* Sun Apr 06 2008 Adam Jackson <ajax@redhat.com> 1.0.51-9
- scd-1.0.51-backtick.patch: Fix unicode hilarity. (#441060)

* Thu Mar 27 2008 Bill Nottingham <notting@redhat.com> 1.0.51-8
- don't use rhpxl.mouse any more

* Mon Feb 25 2008 Adam Jackson <ajax@redhat.com> 1.0.51-7
- scd-1.0.51-unkudzify.patch: Replace kudzu dependency with dbus dependency.
- Fix the chmod fix from -6 to, you know, work.

* Tue Feb 12 2008 Adam Jackson <ajax@redhat.com> 1.0.51-6
- Clear executable bit from the icons. (#429875)

* Tue Jan 22 2008 Adam Jackson <ajax@redhat.com> 1.0.51-5
- scd-1.0.51-config-util.patch: Update for new usermode. (#428397)

* Mon Oct 01 2007 Adam Jackson <ajax@redhat.com> 1.0.51-4
- Un-Require: redhat-artwork, we don't actually require it. (#314001)

* Tue Jul 24 2007 Adam Jackson <ajax@redhat.com> 1.0.51-3
- Remove ppc64 from ExcludeArch.

* Wed Jun 27 2007 Matthias Clasen <mclasen@redhat.com> 1.0.51-2
- Fix up categories in desktop file

* Wed Apr 11 2007 Adam Jackson <ajax@redhat.com> 1.0.51-1
- Load the mouse and keyboard configs from the config file, so as not to
  clobber them. (#145316)

* Wed Mar 28 2007 Jeremy Katz <katzj@redhat.com> - 1.0.50-1
- start X server with a black background; we don't need xsri anymore

* Thu Mar 22 2007 Adam Jackson <ajax@redhat.com> 1.0.49-1
- Package review cleanups.

* Mon Jan 29 2007 Adam Jackson <ajax@redhat.com>
- Copy instead of rename when doing backup of xorg.conf, in case the user has
  it as a symlink. (#181965)

* Fri Dec 15 2006 Adam Jackson <ajax@redhat.com> 1.0.48-2
- Rebuild for translations.

* Fri Dec 8 2006 Adam Jackson <ajax@redhat.com>
- Add dist tag to Release.

* Thu Dec 7 2006 Adam Jackson <ajax@redhat.com> 1.0.48-1
- Import old driver list code from rhpxl. (#218241)

* Wed Dec 6 2006 Adam Jackson <ajax@redhat.com> 1.0.47-1
- Fail gracefully on machines with no video.

* Tue Nov 21 2006 Matthias Clasen <mclasen@redhat.com> - 1.0.46-1
- Fix mnemonic for the color depth combo on the last tab (#216391)

* Wed Sep 13 2006 Adam Jackson <ajackson@redhat.com> 1.0.45-1
- Refresh the mode state before first paint, to give rhpxl a chance to ask
  RANDR for the current mode.

* Mon Aug 28 2006 Adam Jackson <ajackson@redhat.com> 1.0.44-1
- Unpack properly when given a refresh rate instead of a refresh range.

* Fri Aug 25 2006 Adam Jackson <ajackson@redhat.com> 1.0.43-1
- Drop 8bpp support.
- Simplify monitor selection view.
- Fix initial window sizing to be large enough for all fields.

* Mon Aug 21 2006 Adam Jackson <ajackson@redhat.com> 1.0.42-1
- Align lists correctly in RTL locales.  (#202754)

* Thu Aug  3 2006 Bill Nottingham <notting@redhat.com> 1.0.41-1
- adjust to new rhpxl (<clumens@redhat.com>)
- work with newer, sparser, config files
- when dealing with autoprobed monitors, pull current resolution from randr

* Wed Jul 26 2006 Chris Lumens <clumens@redhat.com> 1.0.38-1
- Fix CHARSET in te and kn translations (#200203).
- Add gettext to buildrequires.

* Thu Mar 09 2006 Chris Lumens <clumens@redhat.com> 1.0.37-2
- Add back spec file parts that got lost on last rebuild.

* Tue Mar 07 2006 Chris Lumens <clumens@redhat.com> 1.0.37-1
- Initialize monitor name label to something other than unknown if we
  really know what it is.

* Fri Mar 03 2006 Martin Stransky <stransky@redhat.com> 1.0.36-3
- added pam fix (#170625)
- fix prereq (#182861, #182862)

* Wed Feb 22 2006 Chris Lumens <clumens@redhat.com> 1.0.36-2
- Add rhpxl to requires

* Fri Jan 27 2006 Paul Nasrat <pnasrat@redhat.com> - 1.0.36-1
- Rebuild for translations
- Fix reconfig mode

* Thu Jan 12 2006 Soren Sandmann <sandmann@redhat.com> - 1.0.35-1
- Rebuild

* Tue Jan 10 2006 Soren Sandmann <sandmann@redhat.com> - 1.0.34-1
- Some s/rhpl/rhpxl/ type changes

* Mon Nov 14 2005 Jeremy Katz <katzj@redhat.com> - 1.0.33-1
- minor changes needed for modular X

* Wed Sep 21 2005 Bill Nottingham <notting@redhat.com> 1.0.32-1
- Fix up some leftover code that still needed migration (#168932)

* Fri Sep  9 2005 Bill Nottingham <notting@redhat.com> 1.0.31-1
- Adapt to new kudzu video driver probing, and new rhpl

* Mon Jun 27 2005 Soren Sandmann <sandmann@redhat.com> 1.0.30-1
- Add ppc64 to ExcludeArchs

* Mon May 23 2005 Jeremy Katz <katzj@redhat.com> - 1.0.29-1
- put scriptlets from distcvs in this specfile

* Mon May 23 2005 Jeremy Katz <katzj@redhat.com> - 1.0.28-1
- fix typo in cleanup leading to traceback (#157423)

* Thu Apr 28 2005 Soren Sandmann <sandmann@redhat.com> 1.0.26-1
- Clean up deprecation warnings (#153937)

* Tue Jan 04 2005 Paul Nasrat <pnasrat@redhat.com> 1.0.25-1
- Only merge hardware_state if defined (#143944)
- Only print card if verbose (#143271)

* Mon Nov 15 2004 Paul Nasrat <pnasrat@redhat.com> 1.0.24-1
- Dual Head patch for testing thanks to Marc Andre Morissette (#136916)

* Tue Oct 19 2004 Paul Nasrat <pnasrat@redhat.com> 1.0.23-1
- Firstboot - re-read config so both kbd and display changes persist (#135361)

* Thu Oct 14 2004 Paul Nasrat <pnasrat@redhat.com> 1.0.22-1
- Depth callback patch from twaugh (#128650)

* Fri Oct 01 2004 Paul Nasrat <pnasrat@redhat.com> 1.0.21-1
- fix mouse traceback

* Tue Sep 07 2004 Paul Nasrat <pnasrat@redhat.com> - 1.0.20-1
- Refactor some stuff into rhpl
- Don't override driver changes unless in reconfig (#127779)
 
* Tue Sep 07 2004 Paul Nasrat <pnasrat@redhat.com> - 1.0.19-1
- Translatable desktop
- Layout changes for firstboot screen

* Thu Aug 19 2004 Paul Nasrat <pnasrat@redhat.com> - 1.0.18-2
- Ensure selection string translatable

* Thu Aug 19 2004 Paul Nasrat <pnasrat@redhat.com> - 1.0.18-1
- Monitor selection for first boot

* Fri Jun 25 2004 Brent Fox <bfox@redhat.com> - 1.0.17-1
- initialize self.probed_path in videocardDialog.py (bug #113695)

* Wed Jun 23 2004 Brent Fox <bfox@redhat.com> - 1.0.16-1
- reduce size of monitor-off.png and monitor-on.png to fit in 640x480 (bug #122142)

* Mon Jun 14 2004 Brent Fox <bfox@redhat.com> - 1.0.15-2
- set the text domain for xconf.py and xConfigDialog.py (bug #123494)

* Wed Jun  2 2004 Alex Larsson <alexl@redhat.com> 1.0.15-1
- fix --reconfig and catch some exceptions for readonly root

* Tue May 25 2004 Brent Fox <bfox@redhat.com> 1.0.14-2
- add BuildRequires for desktop-file-utils (bug# 124181)

* Fri Apr 30 2004 Brent Fox <bfox@redhat.com> 1.0.14-1
- do not write out extra XF86Config file during firstboot (bug #121729)

* Tue Apr 20 2004 Brent Fox <bfox@redhat.com> 1.0.13-3
- Do not write out XkbRules line to config file, as it is unnecessary to hard
  code the rules file, which has a built in default which should always
  work. (#120858)

* Wed Apr 14 2004 Brent Fox <bfox@redhat.com> 1.0.13-2
- update requires for new pyxf86config

* Tue Apr 13 2004 Brent Fox <bfox@redhat.com> 1.0.13-1
- make changes for XFree86 -> Xorg conversion

* Thu Apr  8 2004 Brent Fox <bfox@redhat.com> 1.0.12-2
- fix icon path (bug #120174)

* Tue Mar 23 2004 Brent Fox <bfox@redhat.com> 1.0.12-1
- filter out duplicate monitor entries (bug #118976)

* Wed Mar 17 2004 Mike A. Harris <mharris@redhat.com> 1.0.11-1
- Change Requires: XFree86 to Requires: /usr/X11R6/bin/XFree86, which is
  what it appears from the sources is being called.  That will need to change
  when the server gets renamed, so it should be implemented IMHO in a way
  that is not hard coded.  This should suffice for now however.
- Changed package description to remove "XFree86" name and replace it with
  generic "X Window System X server" term.
- Added the "via", and "voodoo" drivers that were missing to internal driver
  list in videocardDialog.py.  The list is still missing stuff though, but
  those sprung to mind.
- Added force-tag target to Makefile with tag -cF
- Added tag target without -F to Makefile
- Removed -F from archive target as that can potentially blow away an already
  tagged and released version from the repository if someone accidentally
  does a "make archive" without updating the spec file Version: field like
  I just about did.  ;o)

* Mon Mar  1 2004 Brent Fox <bfox@redhat.com> 1.0.10-1
- sanity check the monitor selection (bug #112314)

* Mon Mar  1 2004 Brent Fox <bfox@redhat.com> 1.0.9-3
- remove Requires on system-config-mouse

* Fri Feb 27 2004 Brent Fox <bfox@redhat.com> 1.0.9-2
- another stab at the dual-head code

* Thu Feb 26 2004 Brent Fox <bfox@redhat.com> 1.0.9-1
- write out "Screen" entry for dual-head cards

* Tue Feb 24 2004 Brent Fox <bfox@redhat.com> 1.0.8-1
- start up metacity to make the windows look nice (bug #108206)

* Thu Feb 19 2004 Brent Fox <bfox@redhat.com> 1.0.7-1
- don't import rhpl.mouse in xconf.py

* Tue Feb 17 2004 Brent Fox <bfox@redhat.com> 1.0.6-1
- write XF86Config to the correct path (bug #115501)

* Fri Jan 30 2004 Brent Fox <bfox@redhat.com> 1.0.5-1
- correct naming in the spec file description

* Thu Dec  4 2003 Brent Fox <bfox@redhat.com> 1.0.4-1
- add code to apply changes made in the firstboot display screen

* Tue Dec  2 2003 Brent Fox <bfox@redhat.com> 1.0.3-1
- add code to pull display notebook page into firstboot

* Thu Nov 20 2003 Brent Fox <bfox@redhat.com> 1.0.2-1
- fix path problem

* Wed Nov 19 2003 Brent Fox <bfox@redhat.com> 1.0.1-1
- rename from redhat-config-xfree86 to system-config-display
- add Obsoletes for redhat-config-xfree86
- make changes for Python2

* Thu Oct 23 2003 Brent Fox <bfox@redhat.com> 0.9.15-1
- work around cards with no driver entries (bug #106501)

* Thu Oct 23 2003 Brent Fox <bfox@redhat.com> 0.9.14-1
- check length of list before removing items (bug #107790)

* Thu Oct 16 2003 Brent Fox <bfox@redhat.com> 0.9.13-1
- allow dualhead to be disabled (bug #107261)

* Wed Oct 15 2003 Brent Fox <bfox@redhat.com> 0.9.12-1
- fix bug #106884 for real this time

* Tue Oct 14 2003 Brent Fox <bfox@redhat.com> 0.9.11-1
- package lightrays.png inside redhat-config-xfree86

* Mon Oct 13 2003 Brent Fox <bfox@redhat.com> 0.9.10-1
- make sure current is initialized (bug #106884)

* Mon Oct  6 2003 Brent Fox <bfox@redhat.com> 0.9.9-3
- add a Requires for XFree86 (bug #105992)

* Mon Oct  6 2003 Brent Fox <bfox@redhat.com> 0.9.9-2
- finish up the dual-head code
- catch case of having no layout options

* Thu Oct  2 2003 Brent Fox <bfox@redhat.com> 0.9.9-1
- first stab at multihead code
- commit some additional monitor icons

* Thu Aug 14 2003 Brent Fox <bfox@redhat.com> 0.9.8-1
- tag on every build

* Thu Jun  5 2003 Brent Fox <bfox@redhat.com> 0.9.7-1
- see if we have the name for an unprobed monitor

* Tue Jun  3 2003 Brent Fox <bfox@redhat.com> 0.9.6-1
- only offer the resolutions that we know to be reasonable for the selected monitor (bug #88269)

* Fri May 30 2003 Brent Fox <bfox@redhat.com> 0.9.5-1
- big UI changes
- make room in the UI for multihead stuff

* Wed May 28 2003 Brent Fox <bfox@redhat.com> 0.7.6-1
- add an ExcludeArch for s390 and s390x (bug #91811)

* Fri May 23 2003 Brent Fox <bfox@redhat.com> 0.7.5-1
- turn on horizontal scrolling in videocard window
- initialize dpi measurement option menu correctly (bug #90190)

* Wed May 21 2003 Michael Fulbright <msf@redhat.com> 0.7.4-1
- converted to use new way of representing Generic monitors in MonitorsDB

* Tue Feb  4 2003 Brent Fox <bfox@redhat.com> 0.7.3-2
- paint the background with lightrays.png

* Thu Jan 30 2003 Brent Fox <bfox@redhat.com> 0.7.3-1
- bump and build

* Tue Jan 21 2003 Brent Fox <bfox@redhat.com> 0.7.2-3
- add closing parenthesis (bug #80398)

* Mon Jan 20 2003 Brent Fox <bfox@redhat.com> 0.7.2-2
- iterate through available video cards until one works
- clean up the output

* Fri Jan 17 2003 Brent Fox <bfox@redhat.com> 0.7.1-6
- make monitor dialog a little larger and allow horz. scrolling (bug #82112)

* Tue Jan 14 2003 Brent Fox <bfox@redhat.com> 0.7.1-5
- fixed desktop file icon

* Thu Jan  9 2003 Jeremy Katz <katzj@redhat.com> 0.7.1-4
- import rhpl.monitor

* Mon Jan  6 2003 Brent Fox <bfox@redhat.com> 0.7.1-3
- try to read the XMOUSETYPE from /etc/sysconfig/mouse (bug #74992)

* Sun Jan  5 2003 Brent Fox <bfox@redhat.com> 0.7.1-2
- fix the dialog centering code
- connect the resolution menu to update_ui so the screenshot gets refreshed

* Sun Jan  5 2003 Brent Fox <bfox@redhat.com> 0.7.1-1
- change radio buttons to OptionMenus

* Fri Jan  3 2003 Brent Fox <bfox@redhat.com> 0.7.0-6
- default to us keyboard if /etc/sysconfig/keyboard contains a keyboard unknown to rhpl (bug #80993)

* Sun Dec 22 2002 Brent Fox <bfox@redhat.com> 0.7.0-5
- change xconfig.comment to reflect that redhat-config-xfree86 made the change

* Fri Dec 20 2002 Brent Fox <bfox@redhat.com> 0.7.0-4
- call mouse.read() if probing didn't return a valid DEVICE info (bug #80115)
- import string in videocardDialog.py
- pass hardware_state into VideocardDialog

* Thu Dec 19 2002 Brent Fox <bfox@redhat.com> 0.7.0-2
- made some ui cleanups that keeps the dialog from resizing while changing resolutions
- removed all the autoconf stuff and replaced it with simpler Makefile and spec file
- rebuild for completeness

* Fri Dec 13 2002 Brent Fox <bfox@redhat.com> 0.7.0-1
- pulled the classes out into their own files to make it more understandable

* Tue Nov 12 2002 Michael Fulbright <msf@redhat.com> 0.6.9-1
- migrated to new rhpl based backend

* Tue Nov  5 2002 Alexander Larsson <alexl@redhat.com>
- Fixed some small bugs

* Thu Sep  5 2002 Alexander Larsson <alexl@redhat.com>
- Require pygtk2-libglade

* Fri Aug 30 2002 Jeremy Katz <katzj@redhat.com> 0.6.6-1
- create /etc/X11/X symlink (#73108)

* Wed Aug 28 2002 Alexander Larsson <alexl@redhat.com> 0.6.5-1
- Fix DRI state changes. (#72255)

* Tue Aug 27 2002 Alexander Larsson <alexl@redhat.com> 0.6.4-1
- Fix XF86Option typo (#72243)

* Mon Aug 26 2002 Alexander Larsson <alexl@redhat.com> 0.6.3-1
- Fixes bug #72456

* Fri Aug 23 2002 Alexander Larsson <alexl@redhat.com> 0.6.2-1
- Fixed part of Bug #72275, the rest is in Gtk+.

* Wed Aug 21 2002 Preston Brown <pbrown@redhat.com> 0.6.1-1
- fixed starting tool when XF86Config is corrupt (#71461)

* Fri Aug  9 2002 Alexander Larsson <alexl@redhat.com> 0.6.0-1
- Add 640x480 to list of resolutions
- Kluge around treeview horizontal scroll bug in videocard dialog
- set textdomain everywhere it is needed to make i18n work
- Try --reconfig if starting an xserver with the current config file doesn't work.
- Tell gdm to restart server on logout after we write the config file.

* Tue Aug  6 2002 Preston Brown <pbrown@redhat.com> 0.5.2-1
- output to XF86Config (not XF86Config-4) when using --reconfig

* Fri Jul 19 2002 Alexander Larsson <alexl@redhat.com>
- Obsolete Xconfigurator

* Wed Jun 26 2002 Alexander Larsson <alexl@redhat.com> 0.3.1-1
- Updated to use configure

* Mon Jun 17 2002 Alexander Larsson <alexl@redhat.com>
- Bumped version to 0.3.0

* Thu May 30 2002 Alex Larsson <alexl@redhat.com>
- Bumped to 0.2.2

* Tue May 28 2002 Alex Larsson <alexl@redhat.com>
- Update to version 0.2.0

* Thu Apr 11 2002 Alex Larsson <alexl@redhat.com> 0.1.0-1
- Initial release

* Tue Apr  9 2002 Alex Larsson <alexl@redhat.com>
- Initial specfile


