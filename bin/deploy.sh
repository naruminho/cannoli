cd ..
git add --all
git commit -m "updated"
git push origin --tags

rm -Rf cannoli.egg-info
rm -Rf dist/*
python3 -m build
python3 -m twine upload dist/* --verbose
