class DatabaseMeta(type):
    # new用于创建类对象
    def __new__(cls, class_name, class_parents, class_attr):
        # 给类添加一个instance属性
        class_attr['instance'] = None
        items = [item[0] for item in class_attr.items()]
        if ("databaseInit" not in items) or ("databaseClose" not in items):
            print("you must have databaseInit and databaseClose functions")
            return None

        # 返回类对象
        return super(DatabaseMeta, cls).__new__(cls, class_name, class_parents, class_attr)

    # 类对象实例化时将调用
    def __call__(self, *args, **kwargs):
        if self.instance is None:
            self.instance = super(DatabaseMeta, self).__call__(*args, **kwargs)
        return self.instance


