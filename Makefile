create-pr:
	echo "Creating a PR"
	git add .
	git commit -m "Created PR via automated script file" || true
	git checkout -b makefilepr
	git push origin HEAD
	gh pr create --title "Auto PR" --body "This PR created with Makefile"
	git branch -D makefilepr