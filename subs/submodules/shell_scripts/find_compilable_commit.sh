#!/bin/bash

FILE="main_thesis_aerotaxonomy.tex"
BRANCH="main"  # or another branch name
MAX_COMMITS=50 # Maximum number of commits to test

echo "Saving local changes..."
git stash push -m "Backup before testing commits"

echo "Searching for a commit that compiles successfully..."
for commit in $(git rev-list --max-count=$MAX_COMMITS $BRANCH); do
    echo -e "\n--- Testing commit $commit ---"
    git checkout -q "$commit"

    # Compile the main file
    pdflatex -interaction=nonstopmode "$FILE" > build.log 2>&1

    # Check if the PDF was successfully generated
    if [ -f "${FILE%.tex}.pdf" ]; then
        echo "✅ Successfully compiled at commit $commit"
        echo "You can stay on this commit or check it out later with:"
        echo "  git checkout $commit"
        break
    else
        echo "❌ Compilation failed at commit $commit"
    fi
done

# Return to the original branch
git checkout -q "$BRANCH"
git stash pop

echo -e "\n🔁 Returning to the original branch."
