cd ..
rm -Rf dist/* cannoli.egg-info
python3 -m build
python3 -m twine upload dist/* --verbose
