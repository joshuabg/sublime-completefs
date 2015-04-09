import sublime, sublime_plugin, os

class CompleteFSAutocomplete(sublime_plugin.EventListener):
	def on_query_completions(self,view,prefix,locations):
		region = view.line(locations[0]);
		cursor = locations[0] - region.a;
		line = view.substr(region);
		singleQoute = line[:cursor].rfind("'");
		doubleQoute = line[:cursor].rfind('"');
		qoute = singleQoute if singleQoute>doubleQoute else doubleQoute;
		if(qoute == -1):
			return [];
		path = line[qoute+1:cursor];
		firstDir = path.find('\');
		fileName = view.file_name();
		if(firstDir == -1 or (path[:firstDir] != '.' and path[:firstDir] != '..' and path[:firstDir] != '')):
			return [];
		dirName = os.path.join(os.path.dirname(fileName), path);
		if(os.path.isfile(dirName)):
			return [];

		dirContents = os.listdir(dirName);
		suggestions = [['../\tComplete FS','../']];
		for item in dirContents:
			if(os.path.isfile(os.path.join(dirName,item))):
				suggestions.append([item + '\tComplete FS',item])
			else:
				suggestions.append([item + '/\tComplete FS', item +'/'])
		return suggestions;
