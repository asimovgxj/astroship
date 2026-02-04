param(
  [string]$User = "asimovgxj",
  [string]$Repo = "astroship"
)
$url = "git@github.com:$User/$Repo.git"
Write-Host "Setting origin to $url" -ForegroundColor Cyan
git remote set-url origin $url
Write-Host "New remotes:" -ForegroundColor Cyan
git remote -v
