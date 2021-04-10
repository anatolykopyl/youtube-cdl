from rich.console import Console
#from rich import inspect
from pathlib import Path
import os
import json
from getch import getch
import keyboard
import youtube_dl
from get_channels import retrieve_youtube_subscriptions

output_dir = 'output'
c = Console()
ydl_opts = {
    'format': 'best',
    'outtmpl': '%(id)s.%(ext)s'
}

all_channels = retrieve_youtube_subscriptions()
curr_channel = 0
c.print(f'You will be prompted if you want to download \
a channel for each of your subscriptions. (total {len(all_channels)})')
for ch in all_channels:
	curr_channel += 1
	c.print(f'[dim][{curr_channel}/{len(all_channels)}]:[/dim] {ch["title"]} [cyan]\[y/n]')
	while True:
		key = getch()
		if key == "y":
			ch['download'] = True
			break
		elif key == "n":
			ch['download'] = False
			break
		else:
			c.print('Press "y" or "n"', style='orange')

c.print('All done! 🎉')
c.print('Saving to output.json...', style='italic')
f = open("output.json", "a", encoding='utf-8')
f.write(json.dumps(all_channels))
f.close()

for ch in all_channels:
	if ch['download']:
		ydl_opts['outtmpl'] = '{}/{}/%(id)s.%(ext)s'.format(output_dir, ch['title'])
		with youtube_dl.YoutubeDL(ydl_opts) as ydl:
			Path(os.path.join(output_dir, ch['title'])).mkdir(parents=True, exist_ok=True)
			ydl.download(['https://www.youtube.com/channel/{}'.format(ch["id"])])
