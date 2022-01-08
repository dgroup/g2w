#!/bin/bash

refname="$1"
oldrev="$2"
newrev="$3"

commit_regex='^#WS-\d+:$'

error_msg='
.git/hooks/update: Aborting commit due to absent Worksection task id in commit.

Commit message should follow pattern: "#WS-0000: The commmit message",
 where "0000" is Worksection task ID.

How to fix:
 * Option 1 (\033[0;32mfor HERO\033[0m): git amend
 	
    git commit --amend --only -m "#WS-???: your message"
    git push

    More:
     > https://github.com/k88hudson/git-flight-rules#i-wrote-the-wrong-thing-in-a-commit-message
     > https://git-scm.com/book/en/v2/Git-Tools-Rewriting-History
     > RUS https://bit.ly/3HDF4Iq
     > RUS https://www.youtube.com/watch?v=zitQtjMoHRI
     > https://docs.github.com/en/pull-requests/committing-changes-to-your-project/creating-and-editing-commits/changing-a-commit-message	

 * Option 2 (\033[0;31mfor loosers\033[0m): Fix some minor changes (for example - add space somewhere)
    
    git add <your recently modified file>
    git commit -m "#WS-???: your message"
    git push
'

if ! ${refname} | egrep -qi ${commit_regex} ; then
    echo -e "${error_msg}" >&2
    exit 1
fi


exit 0
