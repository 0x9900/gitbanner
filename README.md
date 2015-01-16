# gitbanner

This simple program will use the github dashboard contribution graph
to write a banner.

The file `banner.yaml` will contain the banner to write and the
starting date.

 - `start_date` should be formated as follow MM/DD/YYYY and should start
 a Sunday (first day of a week on github).

 - `message` should only contain `#` or `.` The **pound** is for a day
   were a commit should occurs the **dots** are for days without
   commit.

Run `gitbanner.py` at least once a day in cron and be patient, really
patient. It will take 329 days to print the world **0x9900** shown in
the example `banner.yaml`
