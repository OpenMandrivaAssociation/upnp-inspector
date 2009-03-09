%define tarball_name UPnP-Inspector

Name: upnp-inspector
Summary: An UPnP Device and Service analyzer
Version: 0.2.0
Release: %mkrel 1
Group: Networking/Other
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
URL: https://coherence.beebits.net/wiki/UPnP-Inspector
Source0: https://coherence.beebits.net/download/%{tarball_name}-%version.tar.bz2
License: MIT
Provides: UPnP-Inspector = %version
Requires: python-coherence >= 0.6.0
Requires: pygtk2

Requires(post):   rpm-helper
Requires(preun):  rpm-helper
BuildRequires: python-setuptools, imagemagick
%py_requires -d

%description
The Inspector is an UPnP Device and Service analyzer, and a debugging tool,
based on the Coherence DLNA/UPnP framework.
Modeled loosely after the Intel UPnP Device Spy and Device Validator.
It is a GUI to discover and explore UPnP devices on your network.
Detected devices are displayed in a tree-view, where actions can be called and
state-variables be queried.

%files
%defattr(-,root,root)
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%py_platsitedir/*

%prep
%setup -q -n %{tarball_name}-%version

%build
python setup.py build

%install
rm -rf %buildroot
mkdir -p %buildroot/%_initrddir
mkdir -p %buildroot/usr/share/icons/%name
mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications/

python setup.py install --root=%buildroot --install-lib=%py_platsitedir

# install icons
mkdir -p %{buildroot}%{_miconsdir}
mkdir -p %{buildroot}%{_iconsdir}
mkdir -p %{buildroot}%{_liconsdir}
install -m 644 upnp_inspector/icons/inspector-logo.png %{buildroot}%{_iconsdir}/%name.png
convert -scale 16x16 upnp_inspector/icons/inspector-logo.png $RPM_BUILD_ROOT%{_miconsdir}/%name.png
convert -scale 48x48 upnp_inspector/icons/inspector-logo.png $RPM_BUILD_ROOT%{_liconsdir}/%name.png

# menu
cat > $RPM_BUILD_ROOT%{_datadir}/applications/%{name}.desktop <<EOF
[Desktop Entry]
Encoding=UTF-8
Name=UPnP-Inspector
Comment=An UPnP Device and Service analyzer
Exec=upnp-inspector
Icon=upnp-inspector
StartupNotify=true
Terminal=false
Type=Application
Categories=X-MandrivaLinux-Internet;X-MandrivaLinux-CrossDesktop
EOF

%clean
rm -rf %buildroot

