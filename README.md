# Pinboard to Movable Type

A Python script to take a day's worth of links from your [Pinboard](https://pinboard.in/) account and create a new [Movable Type](http://movabletype.org/) weblog Entry from them. 

It's a bit basic, might break, but so far seems to work for me.

Assumes Movable Type is using a MySQL database.


## Setup

Copy `pinboard_example.cfg` to `pinboard.cfg` and change the settings to your own.

Use [pip](https://pypi.python.org/pypi/pip) to install the required modules:

    pip install -r requirements.txt


## Usage

Run the script either like:

    $ python pinboard-to-mt.py 2014-03-25

which will fetch any Pinboard links for that date, or like:

    $ python pinboard-to-mt.py

which will fetch any Pinboard links for the current date.

The new Movable Type entry will have its Authored On time set to the chosen date (as specified, or the current date) with a time of whatever is set in your `pinboard.cfg`. Its status will be "Scheduled" so, if everything's running smoothly, Movable Type should publish the entry at the Authored On time.

NOTE: All dates and times assume everything is in UTC. If something isn't (Pinboard? Your server?) then things might get weird.


## Example output

The blog entries will have titles like "Links for Tuesday 17 December 2013" and a main body something like:

    <dl class="links">
    <dt><a href="http://www.lifeisaprayer.com/articles/photography/iphone-4-ipad-external-mic-audio-input">External Microphones for iPhone 5, 4S, iPad and iPod Touch Audio input | Life is a Prayer.com</a></dt>
    <dd>A good roundup of this stuff, although from 2011. I'd like to find a similar thing a bit more recent. Still, always nice to see something quite thorough. <span class="tags"><a href="https://pinboard.in/u:philgyford/t:iphone">iphone</a>, <a href="https://pinboard.in/u:philgyford/t:ipad">ipad</a>, <a href="https://pinboard.in/u:philgyford/t:ios">ios</a>, <a href="https://pinboard.in/u:philgyford/t:microphones">microphones</a>, <a href="https://pinboard.in/u:philgyford/t:jeffgeerling">jeffgeerling</a>, <a href="https://pinboard.in/u:philgyford/t:audio">audio</a></span></dd>
    <dt><a href="https://medium.com/@jennschiffer">Jenn $chiffer — Medium</a></dt>
    <dd>Really enjoying these posts. While Medium gives a weird fake authority to self-important blog posts from dotcom fools, it also gives a weird fake authority to these. Brilliant. <span class="tags"><a href="https://pinboard.in/u:philgyford/t:jennschiffer">jennschiffer</a></span></dd>
    </dl>

You can choose not to include the tags using the setting in your `pinboard.cfg`.

