Write-Host "Remote URLs:" -ForegroundColor Cyan
git remote -v
Write-Host "`nCurrent branch:" -ForegroundColor Cyan
git rev-parse --abbrev-ref HEAD
Write-Host "`nStatus (short):" -ForegroundColor Cyan
git status -sb
Write-Host "`nLast local commit:" -ForegroundColor Cyan
git log -1 --oneline
Write-Host "`nRemote HEAD on origin/main:" -ForegroundColor Cyan
git ls-remote origin refs/heads/main
