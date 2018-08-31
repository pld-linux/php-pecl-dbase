%define		php_name	php%{?php_suffix}
%define		modname		dbase
%define		status		beta
%define		snap		beta1
%define		rel 		1
Summary:	%{modname} - dBase database file access functions
Summary(pl.UTF-8):	%{modname} - dostęp do plików baz danych dBase
Name:		%{php_name}-pecl-%{modname}
Version:	7.0.0
Release:	0.%{snap}.%{rel}
License:	PHP 3.01
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{modname}-%{version}%{snap}.tgz
# Source0-md5:	777fb23f829cb6e9590b11a1987866f6
URL:		http://pecl.php.net/package/dbase/
BuildRequires:	%{php_name}-devel >= 3:7.0.0
BuildRequires:	rpmbuild(macros) >= 1.650
%{?requires_php_extension}
Provides:	php(dbase) = %{version}
Obsoletes:	php-dbase
Obsoletes:	php-pecl-dbase < 5.1.0-5
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This module allows you to access records stored in dBase-format (dbf)
databases.

In PECL status of this extension is: %{status}.

%description -l pl.UTF-8
Ten moduł pozwala na dostęp do rekordów zapisanych w plikach baz
danych w formacie dBase (dbf).

To rozszerzenie ma w PECL status: %{status}.

%prep
%setup -qc
mv %{modname}-%{version}%{snap}/* .

%build
phpize
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	EXTENSION_DIR=%{php_extensiondir} \
	INSTALL_ROOT=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d
cat <<'EOF' > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{modname}.ini
; Enable %{modname} extension module
extension=%{modname}.so
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
%php_webserver_restart

%postun
if [ "$1" = 0 ]; then
	%php_webserver_restart
fi

%files
%defattr(644,root,root,755)
%doc CREDITS
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{modname}.so
