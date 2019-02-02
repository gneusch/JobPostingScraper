JobPostingScraper

Create a crontab entry to run the script periodically, modify as needed.
55	23	*	*	*	startScraping.sh >>startScraping.log 2>&1
