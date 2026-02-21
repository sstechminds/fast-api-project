create-pr:
	echo "Creating a PR"
	git add .
	git commit -m "Create a PR" || true
	git push origin HEAD
	gh pr create --title "Auto PR" --body "This PR created with Makefile"