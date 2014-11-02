#Livetab Sublime Text 2/3 Plugin

Sublime Text plugin that allow you to share tabs with other people, for realtime editing. Supports multiple sessions.

Not currently in Package Control

To use with ST2:

1. clone Repo
2. Run `git clone https://github.com/fosterdill/sublime-live-tab-plugin.git && cd sublime-live-tab-plugin/ && cp plugin/ST2/Livetab.py ~/Library/Application\ Support/Sublime\ Text\ 2/Packages/User/`
3. Reload Sublime Text
4. run `view.run_command('livetab', {'session_id': '[anything here]'})` in Sublime Text console
5. give the session_id you chose to anyone to start collaborating

To use with ST3:

Follow all steps, but use `git clone https://github.com/fosterdill/sublime-live-tab-plugin.git && cd sublime-live-tab-plugin/ && cp plugin/ST3/Livetab.py ~/Library/Application\ Support/Sublime\ Text\ 3/Packages/User/` instead for step 2.