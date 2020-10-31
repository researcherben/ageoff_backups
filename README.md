
1) backups are generated daily
2) keep all backup files for this month and last month
3) for the months prior to last month, keep only N backup files (where `3<N<8`)

if a backup file is X MB, then the total space used in M months is `60*X + N*X*(M-2)`
