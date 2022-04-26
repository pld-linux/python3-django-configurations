#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_with	tests	# unit tests (require some django db setup up?)
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

Summary:	Helper for organizing Django settings
Summary(pl.UTF-8):	Moduł pomocniczy do organizowania ustawień Django
Name:		python-django-configurations
# keep 2.2 here for python2 support
Version:	2.2
Release:	1
License:	BSD
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/django-configurations/
Source0:	https://files.pythonhosted.org/packages/source/d/django-configurations/django-configurations-%{version}.tar.gz
# Source0-md5:	b66c70be1a6a6f1808c61cb984326d70
Patch0:		django-configurations-runner.patch
URL:		https://pypi.org/project/django-configurations/
%if %{with python2}
BuildRequires:	python-modules >= 1:2.7
BuildRequires:	python-setuptools
BuildRequires:	python-setuptools_scm
%if %{with tests}
BuildRequires:	python-Sphinx >= 1.4
BuildRequires:	python-dj_database_url
BuildRequires:	python-dj_email_url
BuildRequires:	python-dj_search_url
BuildRequires:	python-django >= 1.11
BuildRequires:	python-django < 2.0
BuildRequires:	python-django_cache_url >= 1.0.0
BuildRequires:	python-mock
BuildRequires:	python-six
%endif
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.5
BuildRequires:	python3-setuptools
BuildRequires:	python3-setuptools_scm
%if %{with tests}
BuildRequires:	python3-Sphinx >= 1.4
BuildRequires:	python3-dj_database_url
BuildRequires:	python3-dj_email_url
BuildRequires:	python3-dj_search_url
BuildRequires:	python3-django >= 1.11
BuildRequires:	python3-django_cache_url >= 1.0.0
BuildRequires:	python3-six
%endif
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	sphinx-pdg-2 >= 1.4
%endif
Requires:	python-modules >= 1:2.7
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

%package -n python3-django-configurations
Summary:	Helper for organizing Django settings
Summary(pl.UTF-8):	Moduł pomocniczy do organizowania ustawień Django
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.5

%description -n python3-django-configurations
django-configurations eases Django project configuration by relying on
the composability of Python classes. It extends the notion of Django's
module based settings loading with well established
object oriented programming patterns.

%description -n python3-django-configurations -l pl.UTF-8
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
%patch0 -p1

%build
%if %{with python2}
%py_build

%if %{with tests}
#django-cadmin-2 test -v2 tests
DJANGO_CONFIGURATION=Test \
DJANGO_SETTINGS_MODULE=tests.settings.main \
PYTHONPATH=$(pwd) \
%{__python} -c 'from configurations.management import execute_from_command_line ; execute_from_command_line(["django-cadmin", "test", "-v2"])'
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
#django-cadmin-3 test -v2 tests
DJANGO_CONFIGURATION=Test \
DJANGO_SETTINGS_MODULE=tests.settings.main \
PYTHONPATH=$(pwd) \
%{__python3} -c 'from configurations.management import execute_from_command_line ; execute_from_command_line(["django-cadmin", "test", "-v2"])'
%endif
%endif

%if %{with doc}
PYTHONPATH=$(pwd) \
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-2
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%{__mv} $RPM_BUILD_ROOT%{_bindir}/django-cadmin{,-2}

%py_postclean
%endif

%if %{with python3}
%py3_install

%{__mv} $RPM_BUILD_ROOT%{_bindir}/django-cadmin{,-3}
ln -sf django-cadmin-3 $RPM_BUILD_ROOT%{_bindir}/django-cadmin
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc AUTHORS LICENSE README.rst
%attr(755,root,root) %{_bindir}/django-cadmin-2
%{py_sitescriptdir}/configurations
%{py_sitescriptdir}/django_configurations-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-django-configurations
%defattr(644,root,root,755)
%doc AUTHORS LICENSE README.rst
%attr(755,root,root) %{_bindir}/django-cadmin
%attr(755,root,root) %{_bindir}/django-cadmin-3
%{py3_sitescriptdir}/configurations
%{py3_sitescriptdir}/django_configurations-%{version}-py*.egg-info
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_modules,_static,*.html,*.js}
%endif
