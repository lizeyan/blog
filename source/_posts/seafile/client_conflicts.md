---
title: Fix 'there is a conflict with an existing library'
categories:
  - seafile
---
http://www.mnott.de/fix-seafile-error-there-is-a-conflict-with-an-existing-library/

>   # Fix SeaFile error “there is a conflict with an existing library”
>
>   Every now and then I get this error when working with Seafile: “there is a conflict with an existing library.” And just today I found out [that I had found a solution three years ago](https://github.com/haiwen/seafile-client/issues/117#issuecomment-98431071), and since then forgotten about it. So here’s again, for the record, what I did.
>
>
>   First of all, I’m working on OSX, and SeaFile client runs against a SQLite database stored in ~/Seafile/.seafile-data/repo.db. To edit that database, I use the sqlite3 command line tool that is available [here](https://www.sqlite.org/cli.html). Alternatively, you can also use any one SQLite graphical client like [SQLite Manager](https://www.sqlabs.com/sqlitemanager.php).
>
>   Anyway. So I cd into that directory:
>
>   ``` bash
>   cd ~/Seafile/.seafile-data
>   sqlite3 repo.db
>   sqlite> .tables
>   CommonAncestor       GarbageRepos         RepoPasswd         DeletedRepo          MergeInfo            RepoProperty       FileSyncError        Repo                 RepoTmpToken       FolderGroupPerms     RepoBranch           ServerProperty     FolderPermTimestamp  RepoKeys           FolderUserPerms      RepoLanToken
>   ```
>
>   The tables I am interested in is Repo, from which I want to delete an offending repository id. To find the repository ID that I am interested in, I need to use RepoProperty:
>
>   ``` sql
>   sqlite> SELECT * FROM RepoProperty where value like '%99 -%';07523e5e-5545-4bca-bf71-a971b106392e|worktree|/Users/mnott/Cloud/99 - Shared
>   ```
>
>   The repository that I wanted to re-sync and that gave the error was 99 – Shared, and with the above command I found its repository ID. I then deleted that repository from both the Repo as well as the RepoProperty tables:
>
>   ``` sql
>   sqlite> delete from repo where repo_id = '07523e5e-5545-4bca-bf71-a971b106392e';sqlite> delete from repoproperty where repo_id = '07523e5e-5545-4bca-bf71-a971b106392e';sqlite> ^D
>   ```
>
>   After that, I quit and restarted the SeaFile client, and I was able to re-sync the repository with its existing folder.

Then you should do the same thing in `clone.db`

