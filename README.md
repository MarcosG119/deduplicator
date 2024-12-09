# Deduplicator Submission

This is my attempt at creating a deduplicator to deduplicate leads by a given key. It also allows for deduplicating by multiple keys if so desired. The decision to deduplicate by one key at a time was so that we can loop through keys that we want to be unique. For the sake of the submission it defaults to `"email"` and `"_id"`. We loop through a list of unique identifiers deduplicating by each identifier. For each round of deduplication, I chose to use a hashmap to see if a certain unique identifier has been used already (in this case `"email"` or `"_id"`). If it hasn't been used yet, we go ahead and add it to the hashmap of leads, otherwise we compare the entry dates and the index of it's original position in the array. If the entry dates are the same, we go with the larger index, otherwise we go with the later date. At the end we return the list of deduplicated leads, using that same list to deduplicate again. At the end of the script, the updated leads will be stored in an updated file.

I built in in this way as well so if we wanted to customize how we make the decision of dealing with duplicates we can do that, similar to how Marketo allows for deduplicating leads. If we wanted unique names as well (I don't see why we would, but if there's some other key that must be unique), we can add them to the list of keys to deduplicate by.

The updated leads are stored in a file of a name by your choosing. The deduped leads will be in `"leads"`, and the change log will be in `"change_log"` of the output JSON file.  Instructions will be displayed below as to how to use the command line. 

## Python

I wrote this program initially in Python because that is my choice of language for data processing that is not time sensitive. To run this program with python you must have Python installed and this is how you would run the script on Mac. The command line takes three elements: the name of the script, the name of the input file, and the name of the output file.

`$ cd python`

`$ python deduplicator.py leads.json deduped_leads.json`

or if you have python 3

`$ python3 deduplicator.py leads.json deduped_leads.json`

The `deduped_leads.json` can be any name of your choosing and it will include the `"change_log"`.

## PHP

I rewrote this program in PHP in the spirit of learning how to use PHP. A couple things I noticed right off the bat working with PHP, it is dynamically typed like Python, but also allows for optional static typing like python3. A major difference between PHP and other languages is how it indexes arrays and the use of hashmaps. PHP doesn't have separate implementations for arrays and hashmaps. You can use a PHP array as a normal indexed array if you don't define keys. However, it seems as if at a lower level all PHP arrays are actually hashmaps, and you can define keys for the array to use it as an orthodox map. If you don't define keys then it is just a standard indexed array. I see how this can be powerful as a server-side language that PHP is often used as. 

To run the PHP code run the following commands:

`$ cd php`

`$ php deduplicator.php --input_file=leads.json --output_file=deduped_leads.json`

You can rename the files as you wish, just make sure to use the flags. The file `deduped_leads.json` will include the `"change_log"`