import json

class Tree():
    def __init__(self, levels):
        self._levels = levels
        if isinstance(levels, str):
            self._levels = json.loads(levels)
        if len(self._levels) == 1:
            self.root = self._levels[0]
            self.children = None
            self.contents = self._levels
        else:
            self._levels = self.recompile_input_list(self._levels)
            if len(self._levels[1]) == 0:
                self.root = self._levels[0]
                self.children = None
                self.contents = [self.root]
            else:
                self.contents = self.flatten(self._levels)
                if len(set(self.contents)) != len(self.contents):
                    raise ValueError("Tree hierarchy contains duplicates")
                self.root = self._levels[0]
                self.children = []
                for child in range(len(self._levels[1])):
                    self.children.append(Tree(self._compile_child_list(child)))
        self.str = json.dumps(self._levels)

    def get_path(self, query):
        if query not in self.contents:
            return None
        else:
            path = [self.root]
            if query == self.root:
                return path
            for child in self.children:
                if query in child.contents:
                    path.extend(child.get_path(query))
        return path

    @staticmethod
    def flatten(object):
        gather = []
        for item in object:
            if isinstance(item, (list, tuple, set)):
                gather.extend(Tree.flatten(item))
            else:
                gather.append(item)
        return gather

    def _compile_child_list(self, child):
        chl = []
        for level, nodes in enumerate(self._levels):
            if level == 0:
                continue
            else:
                chl.append(nodes[child])
        return chl

    def print(self):
        print(self.root)
        if self.children is not None:
            print(self.contents)
            for child in self.children:
                child.print()

    @staticmethod
    def recompile_input_list(levels):
        assert isinstance(levels[0], str)
        if isinstance(levels[1], str):
            levels[1] = tuple([levels[1]])
        if len(levels) == 2:
            return levels
        for level, data in enumerate(levels):
            if level == 0 or level == 1:
                continue
            if isinstance(data, str):
                levels[level] = tuple([levels[level]])
        return levels


    @staticmethod
    def depth(t):
        if isinstance(t, str):
            return 0
        try:
            return 1 + max(Tree.depth(x) for x in t)
        except:
            return 0

    @staticmethod
    def get_string_locations(nested_tuple):
        found_strings = []
        for index, element in enumerate(nested_tuple):
            if isinstance(element, str):
                found_strings.append([index])
                continue
            elif isinstance(element, list) and len(element) == 0:
                continue
            strings_in_tuple = Tree.get_string_locations(element)
            strings_in_tuple = [[index]+ x for x in strings_in_tuple]
            found_strings.extend(strings_in_tuple)
        return found_strings