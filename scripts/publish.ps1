Write-Host "Pushing changes to GitHub..." -ForegroundColor Cyan

# Check for uncommitted changes
$status = git status --porcelain
if ($status) {
    Write-Host "Committing changes..." -ForegroundColor Green
    git add -A
    git commit -m "chore: update publish script and trigger workflow"
} else {
    Write-Host "No changes to commit." -ForegroundColor Yellow
}

# Push to main
Write-Host "Pushing to remote..." -ForegroundColor Green
git push origin main
