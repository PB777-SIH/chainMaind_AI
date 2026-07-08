# PowerShell script to fix PostgreSQL authentication
# Fix PostgreSQL authentication for remote connections

Start-Sleep -Seconds 5

# Update pg_hba.conf to use md5 for remote connections
$command = @"
echo 'host    all             all             0.0.0.0/0               md5' >> /var/lib/postgresql/data/pg_hba.conf
"@

docker exec chainmind_postgres bash -c $command

# Reload PostgreSQL configuration  
$env:PGPASSWORD='expert_password'
docker exec chainmind_postgres psql -U poshika -d chainmind_db -c "SELECT pg_reload_conf();"

Write-Host "✅ PostgreSQL authentication configured!"
