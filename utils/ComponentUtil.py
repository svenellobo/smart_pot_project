class ComponentUtil:

    @staticmethod
    def place_component(component, row, column, sticky=None):
        if sticky is None:
            component.grid(row=row, column=column, padx=5, pady=5)
        else:
            component.grid(row=row, column=column, padx=5, pady=5, sticky=sticky)