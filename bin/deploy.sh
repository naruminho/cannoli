cd ..
git add --all
git commit -m "added MANIFEST.in"
git push 


rm -rf dist
rm -rf cannoli.egg-info
python3 -m build
#python3 setup.py sdist
python3 -m twine upload dist/* --verbose
