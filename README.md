# gitbanner

This simple program will use the github dashboard contribution graph
to write a banner.

The file `banner.yaml` will contain the banner to write and the
starting date.

 - `start_date` should be formated as follow MM/DD/YYYY and should start
 a Sunday (first day of a week on github).

 - `message` should only contain `*` or `.` The **stars** are for a day
   were a commit should occurs the **dots** are for days without commit.


Run `gitbanner.py` at least once a day in cron and be patient. For
example it will take 30 weeks to print the world **HELLO**
