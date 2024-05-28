chmod +x /usr/lib/generate_data/load_data.sql
cd /usr/lib/generate_data
psql -U b2b_user -d b2b_db -f /usr/lib/generate_data/load_data.sql
cd ~/
