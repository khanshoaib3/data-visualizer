pkgdatadir = get_option('prefix') / get_option('datadir') / meson.project_name()
moduledir = pkgdatadir / 'datavisualizer'
gnome = import('gnome')

gnome.compile_resources('datavisualizer',
  'datavisualizer.gresource.xml',
  gresource_bundle: true,
  install: true,
  install_dir: pkgdatadir,
)

python = import('python')
message(python.find_installation('python3').full_path())

conf = configuration_data()
conf.set('PYTHON', python.find_installation('python3').full_path())
conf.set('VERSION', meson.project_version())
conf.set('localedir', get_option('prefix') / get_option('localedir'))
conf.set('pkgdatadir', pkgdatadir)

configure_file(
  input: 'datavisualizer.in',
  output: 'datavisualizer',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir'),
  install_mode: 'r-xr-xr-x'
)

datavisualizer_sources = [
  '__init__.py',
  'main.py',
  'window.py',
]

install_data(datavisualizer_sources, install_dir: moduledir)