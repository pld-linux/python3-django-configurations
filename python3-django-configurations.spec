#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_with	tests	# unit tests (require some django db setup up?)
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

Summary:	Helper for organizing Django settings
Summary(pl.UTF-8):	Moduł pomocniczy do organizowania ustawień Django
Name:		python3-django-configurations
# 2.3.x is the last version for Django 2.2
Version:	2.3.2
Release:	2
License:	BSD
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/django-configurations/
Source0:	https://files.pythonhosted.org/packages/source/d/django-configurations/django-configurations-%{version}.tar.gz
# Source0-md5:	54b8f7ad39dcbac2387f3c56a81cb68f
Patch0:		django-configurations-email-tests.patch
URL:		https://pypi.org/project/django-configurations/
BuildRequires:	python3-modules >= 1:3.6
BuildRequires:	python3-setuptools
BuildRequires:	python3-setuptools_scm
%if %{with tests}
BuildRequires:	python3-dj_database_url
BuildRequires:	python3-dj_email_url >= 1.0.5
BuildRequires:	python3-dj_search_url
BuildRequires:	python3-django >= 2.2
BuildRequires:	python3-django_cache_url >= 1.0.0
%if "%{py3_ver}" == "3.6" || "%{py3_ver}" == "3.7"
BuildRequires:	python3-importlib_metadata
%endif
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	python3-django >= 2.2
BuildRequires:	sphinx-pdg-3 >= 4
%endif
Requires:	python3-modules >= 1:3.6
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
django-configurations eases Django project configuration by relying on
the composability of Python classes. It extends the notion of Django's
module based settings loading with well established
object oriented programming patterns.

%description -l pl.UTF-8
django-configurations ułatwia konfigurowanie projektów Django poprzez
poleganie na składaniu klas Pythona. Rozszerza sposób ładowania
ustawień oparty na modułach Django o dobrze ustalone wzorce
programowania obiektowego.

%package apidocs
Summary:	API documentation for Python django-configurations module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona django-configurations
Group:		Documentation

%description apidocs
API documentation for Python django-configurations module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona django-configurations.

%prep
%setup -q -n django-configurations-%{version}
%patch -P 0 -p1

%build
%py3_build

%if %{with tests}
#django-cadmin-3 test -v2 tests
DJANGO_CONFIGURATION=Test \
DJANGO_SETTINGS_MODULE=tests.settings.main \
PYTHONPATH=$(pwd) \
%{__python3} -c 'from configurations.management import execute_from_command_line ; execute_from_command_line(["django-cadmin", "test", "-v2"])'
%endif

%if %{with doc}
PYTHONPATH=$(pwd) \
sphinx-build-3 -b html docs docs/_build/html
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

%{__mv} $RPM_BUILD_ROOT%{_bindir}/django-cadmin{,-3}
ln -sf django-cadmin-3 $RPM_BUILD_ROOT%{_bindir}/django-cadmin

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS LICENSE README.rst
%attr(755,root,root) %{_bindir}/django-cadmin
%attr(755,root,root) %{_bindir}/django-cadmin-3
%{py3_sitescriptdir}/configurations
%{py3_sitescriptdir}/django_configurations-%{version}-py*.egg-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_modules,_static,*.html,*.js}
%endif
