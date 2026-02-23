pr:
	echo "Creating a PR"
	git branch -D makefilepr
	git checkout -b makefilepr
	uv run ruff check --select I --fix .
	uv run ruff format .
	git add .
	git commit -m "Created PR via automated script file" || true
	git push origin HEAD
	gh pr create --title "Auto PR" --body "This PR created with Makefile"
