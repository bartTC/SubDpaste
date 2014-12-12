import sublime, sublime_plugin

import urllib
import urllib2
import sys

sep = """


# ------ 8< ------ 8< ------ 8< ------ 8< ------ 8< ------


"""

def paste_code(content):
    request = urllib2.Request(
        'https://dpaste.de/api/',
        urllib.urlencode([('content', content)]),
    )
    response = urllib2.urlopen(request)
    return response.read()[1:-1]


class DpasteCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        regions = [region for region in self.view.sel() if not region.empty()]
        regions = len(regions) == 0 and [sublime.Region(0, self.view.size())] \
                                     or regions
        region_data = [self.view.substr(region) for region in regions]
        content = sep.join(region_data)

        paste_url = paste_code(content)

        sublime.status_message('Pasted to %s and copied to your clipboard!' % paste_url)
        sublime.set_clipboard(paste_url)

        return None
