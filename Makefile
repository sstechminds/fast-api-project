create-pr:
	echo "Creating a PR"
	uv run ruff check --fix .
	uv run ruff format .
	git add .
	git commit -m "Created PR via automated script file" || true
	git branch -D makefilepr
	git checkout -b makefilepr
	git push origin HEAD
	gh pr create --title "Auto PR" --body "This PR created with Makefile"
