import sublime
import sublime_plugin
import urllib

DPASTE_API_URL = 'https://dpaste.de/api/'
SEP = """


# ------ 8< ------ 8< ------ 8< ------ 8< ------ 8< ------


"""

def paste_code(content):
    data = urllib.parse.urlencode({'content': content})
    data = data.encode('utf8')
    response = urllib.request.urlopen(DPASTE_API_URL, data)
    return response.read()[1:-1]


class DpasteCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        regions = [region for region in self.view.sel() if not region.empty()]
        regions = len(regions) == 0 and [sublime.Region(0, self.view.size())] \
                                     or regions
        region_data = [self.view.substr(region) for region in regions]
        content = SEP.join(region_data)

        paste_url = paste_code(content)
        paste_url = paste_url.decode('utf8')

        sublime.status_message('Pasted to %s and copied to your clipboard!' % paste_url)
        sublime.set_clipboard(paste_url)

        return None
